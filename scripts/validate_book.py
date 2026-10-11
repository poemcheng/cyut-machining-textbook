"""Artifact checks: local references, diagrams, UTF-8, PDF text and page bounds."""
from pathlib import Path
import re, json, xml.etree.ElementTree as ET
from urllib.parse import unquote
from pypdf import PdfReader
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
errors = []
files = list((ROOT/'docs').rglob('*.md')) + [ROOT/'README.md',ROOT/'LICENSE-CONTENT.md']
for path in files:
    content = path.read_text(encoding='utf-8')
    if '\ufffd' in content: errors.append(f'Encoding error: {path}')
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',content):
        if target.startswith(('https://','http://','#')): continue
        local = unquote(target.split('#')[0])
        if local and not (path.parent/local).is_file(): errors.append(f'Broken reference: {path.name}: {local}')

svgs = list((ROOT/'docs'/'assets').glob('*.svg'))
if len(svgs) != 19: errors.append(f'Expected 19 SVGs, found {len(svgs)}')
for path in svgs:
    tree = ET.parse(path)
    root = tree.getroot()
    if not root.get('viewBox'): errors.append(f'Missing viewBox: {path.name}')
    for element in root.iter():
        for key in ('marker-start','marker-end'):
            if key in element.attrib: errors.append(f'PDF unsupported marker: {path.name}')
        if element.tag.endswith('image'):
            source = element.get('href') or element.get('{http://www.w3.org/1999/xlink}href')
            if source and not source.startswith('data:') and not (path.parent/source).is_file():
                errors.append(f'Missing SVG photo: {path.name}: {source}')

pdf = ROOT/'docs'/'textbook.pdf'
reader = PdfReader(pdf)
all_text = '\n'.join(page.extract_text() or '' for page in reader.pages)
for term in ('WINHO','尾座','能源隔離','逆銑','22 mm','16.80','20.10','現場核對','來源'):
    if term not in all_text: errors.append(f'Missing PDF content: {term}')
for number,page in enumerate(reader.pages,1):
    if len((page.extract_text() or '').strip()) < 30: errors.append(f'Near-empty PDF page: {number}')
with pdfplumber.open(pdf) as document:
    for number,page in enumerate(document.pages,1):
        for char in page.chars:
            if char['x0'] < 12 or char['x1'] > page.width-12 or char['top'] < 5 or char['bottom'] > page.height-8:
                errors.append(f'PDF text outside page: {number}: {char["text"]}')
                break

print(json.dumps({'chapters':len(list((ROOT/'docs'/'chapters').glob('*.md'))),'svg_diagrams':len(svgs),
                  'pdf_pages':len(reader.pages),'pdf_bytes':pdf.stat().st_size,'errors':errors},ensure_ascii=False,indent=2))
if errors: raise SystemExit(1)
