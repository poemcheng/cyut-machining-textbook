#!/usr/bin/env python3
"""Convert pinned manufacturer VISUAL meshes to indexed float32 buffers.
No simplification, no collision mesh substitution, no new OEM geometry.
Requires numpy, PyYAML. Sources are fetched separately by the CI workflow.
"""
from __future__ import annotations
import argparse, hashlib, json, math, shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import yaml
UR_REF='81f7c9fe003c2f0e02eec5a7253f1b262ad38b61'
TM_REF='377e2aacd95318903bc293bf694a044801e78128'
N={'c':'http://www.collada.org/2005/11/COLLADASchema'}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def numbers(s): return [float(x) for x in s.split()]
def local(t): return t.split('}')[-1]
def unit_norm(n): return n / np.maximum(np.linalg.norm(n,axis=1,keepdims=True),1e-20)
def normals(p):
    a=p.reshape(-1,3,3); v=np.cross(a[:,1]-a[:,0],a[:,2]-a[:,0]); return np.repeat(unit_norm(v),3,axis=0)

def dae(p):
    """Bake COLLADA scene transforms; preserve source Z-up (URDF convention)."""
    r=ET.parse(p).getroot(); out=[]
    effects={}
    for e in r.findall('c:library_effects/c:effect',N):
        x=e.find('.//c:diffuse/c:color',N); effects[e.get('id')]=numbers(x.text)[:3] if x is not None else [.65,.68,.7]
    materials={m.get('id'):effects[m.find('c:instance_effect',N).get('url')[1:]] for m in r.findall('c:library_materials/c:material',N)}
    geometries={}
    for geom in r.findall('c:library_geometries/c:geometry',N):
        m=geom.find('c:mesh',N); sources={}
        for s in m.findall('c:source',N):
            a=s.find('c:float_array',N); acc=s.find('c:technique_common/c:accessor',N)
            sources[s.get('id')]=np.fromstring(a.text,sep=' ').reshape(-1,int(acc.get('stride','1')))
        vertices={v.get('id'):v.find("c:input[@semantic='POSITION']",N).get('source')[1:] for v in m.findall('c:vertices',N)}
        groups=[]
        for prim in m:
            tag=local(prim.tag)
            if tag not in ['triangles','polylist']: continue
            inputs=prim.findall('c:input',N); stride=max(int(i.get('offset')) for i in inputs)+1
            raw=np.fromstring(prim.find('c:p',N).text,sep=' ',dtype=np.int64).reshape(-1,stride)
            if tag=='polylist':
                vc=np.fromstring(prim.find('c:vcount',N).text,sep=' ',dtype=np.int64)
                if not np.all(vc==3):
                    tri=[]; offset=0
                    for count in vc:
                        for k in range(1,count-1): tri.extend([offset,offset+k,offset+k+1])
                        offset+=count
                    raw=raw[tri]
            inp={i.get('semantic'):(i.get('source')[1:],int(i.get('offset'))) for i in inputs}
            vs,vi=inp['VERTEX']; pos=sources[vertices[vs]][raw[:,vi],:3]
            if 'NORMAL' in inp:
                ns,ni=inp['NORMAL']; norm=sources[ns][raw[:,ni],:3]
            else: norm=normals(pos)
            groups.append((prim.get('material'),pos,norm))
        geometries[geom.get('id')]=groups
    def visit(node,parent):
        mat=parent.copy()
        for tr in node:
            t=local(tr.tag); a=numbers(tr.text or '') if t in ['matrix','translate','rotate','scale'] else []
            T=np.eye(4)
            if t=='matrix': T=np.array(a).reshape(4,4)
            elif t=='translate': T[:3,3]=a
            elif t=='scale': T[:3,:3]=np.diag(a)
            elif t=='rotate':
                axis=np.array(a[:3]); axis/=np.linalg.norm(axis); ang=math.radians(a[3]); K=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
                T[:3,:3]=np.eye(3)+math.sin(ang)*K+(1-math.cos(ang))*(K@K)
            else: continue
            mat=mat@T
        for inst in node.findall('c:instance_geometry',N):
            binds={b.get('symbol'):b.get('target')[1:] for b in inst.findall('.//c:instance_material',N)}
            for sym,pos,norm in geometries[inst.get('url')[1:]]:
                points=pos@mat[:3,:3].T+mat[:3,3]
                norms=unit_norm(norm@np.linalg.inv(mat[:3,:3]))
                if np.linalg.det(mat[:3,:3])<0:
                    points=points.reshape(-1,3,3)[:,[0,2,1],:].reshape(-1,3); norms=norms.reshape(-1,3,3)[:,[0,2,1],:].reshape(-1,3)
                out.append((sym,points,norms,materials.get(binds.get(sym,sym),[.7,.7,.7])))
        for ch in node.findall('c:node',N): visit(ch,mat)
    vs=r.find('c:library_visual_scenes/c:visual_scene',N)
    assert r.find('c:asset/c:up_axis',N).text=='Z_UP', 'Review coordinate convention before conversion'
    for n in vs.findall('c:node',N): visit(n,np.eye(4))
    return out

def obj(p):
    colors={}; active=None
    for line in p.with_suffix('.mtl').read_text(encoding='utf-8-sig').splitlines():
        s=line.split()
        if s and s[0]=='newmtl': active=s[1]
        elif s and s[0]=='Kd': colors[active]=list(map(float,s[1:4]))
    verts=[]; norms=[]; buckets={}; material='DEFAULT_MTL'
    for line in p.read_text(encoding='utf-8-sig').splitlines():
        s=line.split()
        if not s: continue
        if s[0]=='v': verts.append(list(map(float,s[1:4])))
        elif s[0]=='vn': norms.append(list(map(float,s[1:4])))
        elif s[0]=='usemtl': material=s[1]
        elif s[0]=='f':
            corners=[]
            for ref in s[1:]:
                a=ref.split('/'); vi=int(a[0]); ni=int(a[2]) if len(a)>2 and a[2] else 0
                corners.append((vi-1 if vi>0 else len(verts)+vi,ni-1 if ni>0 else (len(norms)+ni if ni<0 else -1)))
            for k in range(1,len(corners)-1): buckets.setdefault(material,[]).extend([corners[0],corners[k],corners[k+1]])
    v=np.array(verts); n=np.array(norms); result=[]
    for name,idx in buckets.items():
        a=np.array(idx); pos=v[a[:,0]]; norm=n[a[:,1]] if np.all(a[:,1]>=0) else normals(pos)
        result.append((name,pos,unit_norm(norm),colors.get(name,[.65,.68,.7])))
    return result

def transform(xyz,rpy):
    a,b,c=rpy; ca,sa=math.cos(a),math.sin(a); cb,sb=math.cos(b),math.sin(b); cc,sc=math.cos(c),math.sin(c)
    R=np.array([[cc,-sc,0],[sc,cc,0],[0,0,1]])@np.array([[cb,0,sb],[0,1,0],[-sb,0,cb]])@np.array([[1,0,0],[0,ca,-sa],[0,sa,ca]])
    M=np.eye(4);M[:3,:3]=R;M[:3,3]=xyz;return M

def export_robot(key,name,spec,meshes,out,source_root,repo,ref,license_path):
    target=out/key;target.mkdir(parents=True,exist_ok=True)
    binary=bytearray();parts=[];total_tri=0
    for link,p,xyz,rpy in meshes:
        groups=[]
        for material,points,norm,color in (dae(p) if p.suffix=='.dae' else obj(p)):
            data=np.column_stack([points,norm]).astype('<f4'); assert np.all(np.isfinite(data))
            unique,index=np.unique(data,axis=0,return_inverse=True)
            vo=len(binary);binary.extend(unique.astype('<f4').tobytes()); io=len(binary);binary.extend(index.astype('<u4').tobytes())
            groups.append({'material':material,'color':color,'vertexOffset':vo,'vertexCount':len(unique),'indexOffset':io,'indexCount':len(index),'bounds':[points.min(axis=0).tolist(),points.max(axis=0).tolist()]})
            total_tri+=len(index)//3
        parts.append({'link':link,'source':str(p.relative_to(source_root)),'sha256':sha(p),'xyz':xyz,'rpy':rpy,'groups':groups})
    (target/'visuals.bin').write_bytes(binary)
    doc={'schema':'mfg30/oem-visual-v1','key':key,'name':name,'sourceRepository':repo,'sourceRevision':ref,'license':'BSD-3-Clause','coordinateSystem':'URDF right-handed Z-up, metre; display rotation/scaling excluded from FK','conversion':'Original VISUAL triangles, baked COLLADA node transforms, indexed float32 position+normal; no simplification. No collision meshes used.','binary':'visuals.bin','binarySha256':sha(target/'visuals.bin'),'triangles':total_tri,'parts':parts,**spec}
    samples=[]
    for q in [[0]*6,spec['homeDegrees'],[15,-35,65,-20,45,10]]:
        M=transform([0,0,0],spec.get('baseRPY',[0,0,0]))
        for j,deg in zip(spec['joints'],q): M=M@transform(j['xyz'],j['rpy'])@transform([0,0,0],[0,0,math.radians(deg)])
        M=M@transform(spec['tool']['xyz'],spec['tool']['rpy'])
        samples.append({'degrees':q,'matrixRowMajor':M.flatten().tolist(),'positionMetres':M[:3,3].tolist()})
    doc['fkFixtures']=samples
    (target/'model.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
    shutil.copyfile(license_path,target/'LICENSE.txt')
    print(key,'parts',len(parts),'triangles',total_tri,'MB',round(len(binary)/1e6,2))
    return {'key':key,'name':name,'triangles':total_tri,'bytes':len(binary),'revision':ref,'manifestSha256':sha(target/'model.json'),'visualSha256':doc['binarySha256']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--intake',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    src=args.intake;out=args.output;out.mkdir(parents=True,exist_ok=True)
    class Loader(yaml.SafeLoader): pass
    Loader.add_constructor('!degrees',lambda l,n:math.radians(float(l.construct_scalar(n))))
    ur=src/'ur';cfg=ur/'config/ur5e';k=yaml.load((cfg/'default_kinematics.yaml').read_text(),Loader)['kinematics'];v=yaml.load((cfg/'visual_parameters.yaml').read_text(),Loader)['mesh_files']
    ur_keys=['base','shoulder','upper_arm','forearm','wrist_1','wrist_2','wrist_3'];meshes=[]
    for key in ur_keys:
        a=v[key]['mesh_offset']; meshes.append((key,ur/v[key]['visual']['mesh']['path'],[a[x] for x in ['x','y','z']],[a[x] for x in ['roll','pitch','yaw']]))
    joints=[{'name':key,'parent':ur_keys[i],'child':key,'xyz':[k[key][x] for x in ['x','y','z']],'rpy':[k[key][x] for x in ['roll','pitch','yaw']],'axis':[0,0,1],'limitsDegrees':([-180,180] if key=='forearm' else [-360,360])} for i,key in enumerate(ur_keys[1:])]
    # Source wrist_3->flange and flange->tool0 are both fixed rotations.
    tool=transform([0,0,0],[0,-math.pi/2,-math.pi/2])@transform([0,0,0],[math.pi/2,0,math.pi/2])
    # These two fixed transforms compose to the identity at tool0.
    assert np.allclose(tool,np.eye(4),atol=1e-12)
    index=[]
    index.append(export_robot('ur5e','Universal Robots UR5e',{'baseRPY':[0,0,math.pi],'baseLink':'base','joints':joints,'tool':{'xyz':[0,0,0],'rpy':[0,0,0]},'homeDegrees':[0,-65,90,-115,-90,0],'calibration':'Nominal UR5e parameters, not calibrated against an individual serial-numbered robot.'},meshes,out,ur,'UniversalRobots/Universal_Robots_ROS2_Description',UR_REF,ur/'LICENSE'))
    shutil.copy(cfg/'joint_limits.yaml',out/'ur5e/joint_limits.yaml');shutil.copy(cfg/'default_kinematics.yaml',out/'ur5e/default_kinematics.yaml');shutil.copy(cfg/'visual_parameters.yaml',out/'ur5e/visual_parameters.yaml');shutil.copy(ur/'README.md',out/'ur5e/UPSTREAM_README.md')
    tm=src/'tm';base=tm/'tm_description/cobot/tm5_900_description';macro=base/'xacro/macro.tm5-900-nominal.urdf.xacro';root=ET.parse(macro).getroot().find('{http://www.ros.org/wiki/xacro}macro')
    clean=lambda s:s.replace('${prefix}','')
    meshes=[]
    for link in root.findall('link'):
        visual=link.find('visual')
        if visual is None: continue
        f=visual.find('geometry/mesh').get('filename').split(')/')[1].replace('${format}','obj');orig=visual.find('origin')
        meshes.append((clean(link.get('name')),base/f,numbers(orig.get('xyz','0 0 0')) if orig is not None else [0,0,0],numbers(orig.get('rpy','0 0 0')) if orig is not None else [0,0,0]))
    limits=[270,180,155,180,180,270];joints=[]
    for joint in root.findall('joint'):
        if joint.get('type')!='revolute': continue
        orig=joint.find('origin');i=len(joints)
        joints.append({'name':clean(joint.get('name')),'parent':clean(joint.find('parent').get('link')),'child':clean(joint.find('child').get('link')),'xyz':numbers(orig.get('xyz')),'rpy':numbers(orig.get('rpy')),'axis':numbers(joint.find('axis').get('xyz')),'limitsDegrees':[-limits[i],limits[i]]})
    index.append(export_robot('tm5-900','Techman Robot TM5-900',{'baseRPY':[0,0,0],'baseLink':'base_link','joints':joints,'tool':{'xyz':[0,0,0],'rpy':[0,0,0]},'homeDegrees':[0,-20,70,30,90,0],'calibration':'Nominal TM5-900 URDF, not a measured laboratory robot.'},meshes,out,tm,'TechmanRobotInc/TM_Cobots_ROS2_Description',TM_REF,tm/'LICENSE'))
    shutil.copy(macro,out/'tm5-900/UPSTREAM.urdf.xacro');shutil.copy(tm/'README.md',out/'tm5-900/UPSTREAM_README.md')
    (out/'index.json').write_text(json.dumps({'generatedBy':'scripts/prepare-manufacturer-assets.py','models':index},indent=2))
if __name__=='__main__':main()
