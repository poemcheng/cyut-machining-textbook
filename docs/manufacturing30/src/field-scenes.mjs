import * as THREE from 'three';
/** Authored representative layouts. No manufacturer CAD or surveyed facility claim. */
export function buildField(field){
 const root=new THREE.Group();root.name=field.name+' / authored representative layout';
 const materials=new Map(),geometries=new Set(),textures=new Set();
 const mat=(c,metal=.15)=>{const key=c+'|'+metal;if(!materials.has(key))materials.set(key,new THREE.MeshStandardMaterial({color:c,roughness:.67,metalness:metal}));return materials.get(key);};
 function mesh(g,m,x,y,z,name){const o=new THREE.Mesh(g,m);geometries.add(g);o.position.set(x,y,z);o.name=name;o.castShadow=true;o.receiveShadow=true;root.add(o);return o;}
 const box=(x,y,z,w,h,d,c,name='field fixture')=>mesh(new THREE.BoxGeometry(w,h,d),mat(c),x,y,z,name);
 const cylinder=(x,y,z,r,h,c,name='utility')=>mesh(new THREE.CylinderGeometry(r,r,h,24),mat(c,.35),x,y,z,name);
 function label(text,x,y,z,width=3.4,size=.42){const c=document.createElement('canvas');c.width=768;c.height=96;const ctx=c.getContext('2d');ctx.fillStyle='#f7fafb';ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle='#1c4052';ctx.font='600 37px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,384,49,730);const t=new THREE.CanvasTexture(c);textures.add(t);const m=new THREE.SpriteMaterial({map:t,depthTest:true});materials.set('sprite'+materials.size,m);const s=new THREE.Sprite(m);s.position.set(x,y,z);s.scale.set(width,size,1);root.add(s);return s;}
 function zone(x,z,w,d,text,color=0x9eb9ba){box(x,.015,z,w,.025,d,color,'floor zoning');for(const a of [-1,1]){box(x+a*w/2,.038,z,.05,.01,d,0xe4b83b,'zone boundary');box(x,.038,z+a*d/2,w,.01,.05,0xe4b83b,'zone boundary');}label(text,x,.45,z,widthFor(text),.3);}
 function widthFor(s){return Math.min(3.2,1+s.length*.08);}
 function table(x,z){box(x,.9,z,2.4,.13,1.2,0x677c84,'workbench');for(const dx of [-1,1])for(const dz of [-.45,.45])box(x+dx,.45,z+dz,.1,.9,.1,0x3b515f,'bench leg');}
 function pallet(x,z){for(let i=0;i<5;i++)box(x-1+i*.5,.12,z,.4,.17,1.4,0xb89e75,'pallet slat');for(const dz of [-.55,.55])box(x,.05,z+dz,2.4,.09,.17,0x987e59,'pallet stringer');for(let i=0;i<4;i++)box(x+(i%2-.5)*.78,.39,z+(Math.floor(i/2)-.5)*.58,.7,.37,.5,0x7f9faa,'work-in-process bin');}
 function rack(x,z){for(const dx of [-1.4,1.4])for(const dz of [-.6,.6])box(x+dx,1.4,z+dz,.12,2.8,.12,0x3c667d,'rack post');for(const y of [.3,1.25,2.2]){box(x,y,z,3,.12,1.4,0xc4a450,'shelf');for(let i=0;i<3;i++)box(x-.95+i*.95,y+.26,z,.72,.4,.95,0x7c919e,'stored stock');}}
 function cabinet(x,z){box(x,1.15,z,1.5,2.3,.75,0xc3ced3,'storage cabinet');for(const dx of [-.37,.37]){box(x+dx,1.2,z+.39,.7,2.05,.025,0xdfe6e9,'cabinet door');box(x+dx+Math.sign(dx)*-.16,1.2,z+.43,.045,.35,.05,0x3b5563,'handle');}}
 function exhaust(x,z){cylinder(x,2.4,z,.17,3.9,0x728a98,'extraction riser');box(x-.6,3.85,z,1.4,.32,.36,0x7c939e,'extraction duct');mesh(new THREE.ConeGeometry(.7,.45,4),mat(0x9dafb8),x-.95,3.48,z,'exhaust hood').rotation.y=Math.PI/4;}
 function fence(x,z,w){for(const dx of [-w/2,w/2])box(x+dx,1.05,z,.09,2.1,.09,0xd6ab43,'fence post');for(const yy of [.2,2])box(x,yy,z,w,.06,.06,0x4b5d69,'fence frame');for(let j=0;j<Math.round(w/.19);j++)box(x-w/2+j*.19,1.1,z,.018,1.8,.018,0x647b86,'mesh fence');for(let j=0;j<9;j++)box(x,.25+j*.2,z,w,.014,.018,0x647b86,'mesh fence');}
 // Open-front educational cutaway: no ceiling hiding the machinery.
 box(0,-.1,0,18,.18,15,0xe0e7e9,'shop floor');box(0,1.7,-7.2,18,3.4,.18,field.id==='cleanroom'?0xf3eee0:0xd2dce0,'rear partition');
 for(const x of [-8.2,0,8.2]){box(x,2.2,-7, .24,4.4,.24,0x7a909b,'building column');box(x,4.2,-6.3,2.5,.1,.55,0xf5f6ed,'overhead luminaire');}
 label(field.en,0,3.65,-7,8,.53);
 box(0,.025,6.05,17,.025,1.2,0xb5c8bf,'pedestrian reference aisle');for(const z of [5.4,6.7])box(0,.05,z,17,.015,.06,0xe4b83b,'walkway boundary');
 for(let i=0;i<12;i++)box(-8+i*1.4,.055,6.05,.6,.01,.045,0xf3f7f3,'walkway dash');
 zone(-5,3.7,3.6,2.5,'01 / INPUT');zone(0,0,8,6,'02 / PROCESS',0xd8e1e5);zone(5,3.7,3.6,2.5,'04 / OUTPUT');pallet(-5,3.7);pallet(5,3.7);
 const marker=new THREE.Mesh(new THREE.TorusGeometry(.55,.055,8,32),new THREE.MeshBasicMaterial({color:0x0a8f9a}));marker.rotation.x=-Math.PI/2;marker.position.set(-5,.12,3.7);root.add(marker);geometries.add(marker.geometry);materials.set('marker',marker.material);
 // Material-flow arrows are instructional, not certified transport routes.
 for(const [x,z,dx,dz] of [[-3.4,4,1,0],[3.3,4,1,0]]){const a=new THREE.ArrowHelper(new THREE.Vector3(dx,0,dz),new THREE.Vector3(x,.09,z),1.1,0x487a86,.3,.2);root.add(a);}
 const props=field.props;
 for(let index=0;index<props.length;index++){
  const type=props[index],x=index%2===0?-6:6,z=index<2?-3.8:.2;
  switch(type){
   case 'rack':rack(x,z);break;
   case 'cabinet':cabinet(x,z);break;
   case 'bench':table(x,z);break;
   case 'computer':table(x,z);box(x,1.4,z,1.05,.65,.11,0x243d4c,'inspection computer');box(x,1.1,z,.12,.25,.1,0x465c69,'monitor stand');break;
   case 'toolcart':case 'diecart':box(x,.58,z,1.7,1.05,1,0x5b8197,'tool / die cart');for(let j=0;j<4;j++){box(x,.23+j*.22,z+.52,1.55,.17,.025,0xa6b8c2,'drawer');box(x,.23+j*.22,z+.55,.55,.025,.03,0x3e5867,'drawer handle');}for(const xx of [-.6,.6])for(const zz of [-.34,.34])cylinder(x+xx,.12,z+zz,.12,.12,0x2c4351,'caster');break;
   case 'chipbin':box(x,.45,z,1.45,.85,1.1,0x497c8a,'chip bin');for(let j=0;j<18;j++)box(x+Math.sin(j*17)*.5,.9,z+Math.cos(j*7)*.4,.16,.06,.06,0x8b9ca5,'chip representation');break;
   case 'coolant':case 'chiller':case 'rectifier':box(x,.8,z,1.4,1.6,1.15,0xb0c0c8,type);for(let j=0;j<7;j++)box(x,.3+j*.14,z+.59,1,.05,.02,0x587481,'ventilation slot');box(x,1.3,z+.6,.5,.3,.02,0x2e555e,'utility controls');break;
   case 'exhaust':exhaust(x,z);break;
   case 'guard':fence(0,-4.2,7.8);break;
   case 'weldscreen':for(const xx of [-6,6]){box(xx,1.45,-2,2.6,2.5,.08,0x9e634f,'welding screen');for(const dx of [-1.2,1.2])box(xx+dx,1.4,-2,.06,2.8,.06,0x3f5360,'screen frame');}break;
   case 'gas':for(const dx of [-.42,.42]){cylinder(x+dx,1.2,z,.28,2.15,0x637e82,'secured shielding gas cylinder');cylinder(x+dx,2.35,z,.09,.16,0x997d49,'valve');box(x+dx,1.3,z+.28,.7,.05,.05,0x354d5b,'retaining bracket');}break;
   case 'dryer':cylinder(x,1.7,z,.55,1.3,0xd8dcdd,'hopper dryer');box(x,.5,z,1.35,1,1.1,0x718fa2,'dryer cabinet');break;
   case 'resin':case 'powder':for(const dx of [-.55,.55]){cylinder(x+dx,.6,z,.43,1.1,type==='powder'?0x8e9598:0x83a0ad,type+' container');cylinder(x+dx,1.18,z,.45,.08,0x425c6b,'sealed lid');}break;
   case 'tank':box(x,.6,z,2.6,1.2,1.4,0x577f89,'process / rinse tank');box(x,1.22,z,2.35,.02,1.15,0x90b6b8,'liquid surface schematic');break;
   case 'ladle':cylinder(x,.65,z,.65,1.2,0x7d7e75,'ladle schematic');box(x,1.1,z,1.8,.1,.1,0x494e52,'lifting yoke');break;
   case 'sandbin':box(x,.55,z,2.6,1.1,1.5,0x787b6f,'sand handling bin');box(x,1.12,z,2.4,.04,1.3,0xc3b496,'sand surface');break;
   case 'coil':case 'rolls':case 'spools':table(x,z);for(let i=0;i<3;i++){const o=cylinder(x-.75+i*.75,1.35,z,.33,.35,type==='coil'?0x8a969c:type==='rolls'?0x455765:0x577f91,type);o.rotation.x=Math.PI/2;}break;
   case 'conveyor':box(x,.8,z,2.7,.25,1,0x506975,'transfer conveyor');for(let i=0;i<9;i++){const a=cylinder(x-1.2+i*.3,.97,z,.09,.9,0xaebcc1,'conveyor roller');a.rotation.x=Math.PI/2;}break;
   case 'ffu':box(x,2.9,z,2.4,.3,1.6,0xdce5e9,'filter fan module schematic');for(let i=0;i<8;i++)box(x-1+i*.28,2.73,z,.05,.02,1.4,0x8da4b1,'filter grille');break;
   case 'wafer':table(x,z);for(let i=0;i<4;i++)cylinder(x-.75+i*.5,1.02,z,.2,.025,0x586c86,'wafer');break;
   default:table(x,z);for(let i=0;i<6;i++){if(type==='bottles')cylinder(x-1+(i%3)*.8,1.2,z+Math.floor(i/3)*.4-.2,.14,.4,0x9fb5ae,'glass container');else box(x-1+(i%3)*.8,1.06,z+Math.floor(i/3)*.4-.2,.55,.18,.3,0x849aa7,type+' fixture');}
  }
  label(type.toUpperCase(),x,3.15,z,2.3,.28);
 }
 const positions=[[-5,3.7],[0,2.5],[0,-2.5],[5,3.7]];
 return {root,field,stats:{field:field.id,props:[...props],layout:'authored / unscaled'},setStage(i){const p=positions[i]||positions[0];marker.position.set(p[0],.12,p[1]);},dispose(){root.removeFromParent();root.traverse(o=>{if(o.geometry)geometries.add(o.geometry);});for(const g of geometries)g.dispose();for(const m of materials.values())m.dispose();for(const t of textures)t.dispose();}};
}
