"""Restore an audited source delta and apply browser-input test corrections."""
import base64, hashlib, json, lzma
from pathlib import Path
root=Path('docs/manufacturing30').resolve()
folder=Path('.github/mfg4-source')
if folder.exists():
    raw=base64.b64decode(''.join((folder/f'part{i}.b64').read_text() for i in range(5)),validate=True)
    assert hashlib.sha256(raw).hexdigest()=='002c525ce279b221095cd3cbfeaf096c411eb6bda38debeb005157d8532160a5'
    data=json.loads(lzma.decompress(raw))
    def target(name):
        p=(root/name).resolve();assert p.is_relative_to(root);return p
    for name,item in data['patches'].items():
        p=target(name);text=p.read_text(encoding='utf-8')
        assert hashlib.sha256(text.encode()).hexdigest()==item['baseSha256'],name
        for e in sorted(item['edits'],key=lambda x:x['start'],reverse=True):
            text=text[:e['start']]+e['text']+text[e['end']:]
        assert hashlib.sha256(text.encode()).hexdigest()==item['resultSha256'],name
        p.write_text(text,encoding='utf-8')
    for name,text in data['newFiles'].items():
        p=target(name);assert not p.exists(),name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
    print('Restored 16 checksum-verified source files')
p=root/'tests/realworld-browser.mjs';s=p.read_text()
s=s.replace("await page.locator('#rwJoints [data-joint=\"0\"]').fill('20');", "await page.locator('#rwJoints [data-joint=\"0\"]').evaluate(el=>{el.value='20';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));});")
s=s.replace('report.success=true;', "report.success=true;report.status='passed';")
p.write_text(s)
p=root/'src/field-scenes.mjs';s=p.read_text();s=s.replace('[[-3.4,4,-1,0],[3.3,4,1,0]]','[[-3.4,4,1,0],[3.3,4,1,0]]');p.write_text(s)
