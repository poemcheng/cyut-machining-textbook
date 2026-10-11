"""Build the Markdown, accessible HTML reader and typeset PDF from chapters.

Python 3.11+: pip install -r requirements.txt
Use CJK_FONT and CJK_BOLD_FONT to override the Windows Traditional Chinese fonts.
"""
from pathlib import Path
import os, re, html, json, copy
import markdown
from lxml import html as lh
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import String
from svglib.svglib import svg2rlg
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
TITLE = '車床與銑床：圖解操作教科書'
SUBTITLE = '朝陽工管製造程序實習 · 科普入門與受監督操作'
W, H = A4
MARGIN = 44
CONTENT = W - MARGIN * 2
NAVY = colors.HexColor('#163249')
TEAL = colors.HexColor('#087f8c')
GRAY = colors.HexColor('#536471')


def chapter_data():
    data = []
    for path in sorted((DOCS / 'chapters').glob('*.md')):
        raw = path.read_text(encoding='utf-8')
        # Chapter-level navigation is generated consistently in the reader.
        raw = re.sub(r'^\[上一章[^\n]*$', '', raw, flags=re.M)
        raw = raw.replace('../assets/', 'assets/')
        raw = re.sub(r'\]\((\d{2}[-a-z]+\.md)\)', r'](chapters/\1)', raw)
        title = re.search(r'^#\s+(.+)', raw, re.M).group(1)
        data.append({'path': path, 'id': path.stem, 'title': title, 'raw': raw})
    return data


def make_html(data):
    nav = '\n'.join(f'<a href="#{c["id"]}">{html.escape(c["title"])}</a>' for c in data)
    parts = []
    for c in data:
        body = markdown.markdown(c['raw'], extensions=['tables', 'fenced_code'])
        body = re.sub(r'href="chapters/(\d{2}[-a-z]+)\.md"', r'href="#\1"', body)
        body = re.sub(r'<p>(<img[^>]+>)</p>', r'<figure>\1</figure>', body)
        # Captions use the meaningful image alternative text.
        body = re.sub(r'(<img[^>]*alt="([^"]*)"[^>]*>)(</figure>)',
                      r'\1<figcaption>\2</figcaption>\3', body)
        body = body.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
        parts.append(f'<article id="{c["id"]}" class="chapter">{body}</article>')
    sources = DOCS / 'sources.md'
    source_text = sources.read_text(encoding='utf-8') if sources.exists() else ''
    if source_text:
        source_html = markdown.markdown(source_text, extensions=['tables'])
        source_html = source_html.replace('<table>', '<div class="table-wrap"><table>').replace('</table>', '</table></div>')
        parts.append('<section id="sources" class="chapter">' + source_html + '</section>')
    template = (ROOT / 'scripts' / 'reader-template.html').read_text(encoding='utf-8')
    final = template.replace('@@TITLE@@', TITLE).replace('@@SUBTITLE@@', SUBTITLE)
    final = final.replace('@@NAV@@', nav).replace('@@CHAPTERS@@', '\n'.join(parts))
    (DOCS / 'index.html').write_text(final, encoding='utf-8')
    merged = '# ' + TITLE + '\n\n' + SUBTITLE + '\n\n版本 1.0 · 2026-10-11\n\n' + '\n\n'.join(c['raw'] for c in data) + '\n\n' + source_text
    (DOCS / 'textbook.md').write_text(merged, encoding='utf-8')
    index = '# 教材目錄\n\n[HTML 閱讀器](index.html) · [完整 Markdown](textbook.md) · [PDF](textbook.pdf)\n\n'
    index += '\n'.join(f'- [{c["title"]}](chapters/{c["path"].name})' for c in data)
    (DOCS / 'index.md').write_text(index + '\n', encoding='utf-8')


def setup_styles():
    font = os.environ.get('CJK_FONT', 'C:/Windows/Fonts/msjh.ttc')
    bold = os.environ.get('CJK_BOLD_FONT', 'C:/Windows/Fonts/msjhbd.ttc')
    pdfmetrics.registerFont(TTFont('TC', font, subfontIndex=0))
    pdfmetrics.registerFont(TTFont('TC-Bold', bold, subfontIndex=0))
    pdfmetrics.registerFontFamily('TC', normal='TC', bold='TC-Bold', italic='TC', boldItalic='TC-Bold')
    base = dict(fontName='TC', fontSize=10.3, leading=17.3, textColor=NAVY,
                wordWrap='CJK', spaceAfter=8, allowWidows=0, allowOrphans=0)
    styles = {'body': ParagraphStyle('Body', **base)}
    styles['h1'] = ParagraphStyle('Chapter', parent=styles['body'], fontName='TC-Bold',
                                 fontSize=22, leading=30, spaceAfter=18, keepWithNext=True)
    styles['h2'] = ParagraphStyle('Section', parent=styles['body'], fontName='TC-Bold',
                                 fontSize=14, leading=21, textColor=TEAL,
                                 spaceBefore=15, spaceAfter=9, keepWithNext=True)
    styles['h3'] = ParagraphStyle('Subsection', parent=styles['h2'], fontSize=11.5, leading=18)
    styles['small'] = ParagraphStyle('Small', parent=styles['body'], fontSize=8, leading=12, textColor=GRAY)
    styles['caption'] = ParagraphStyle('Caption', parent=styles['small'], alignment=TA_CENTER, spaceAfter=14)
    styles['table'] = ParagraphStyle('Cell', parent=styles['body'], fontSize=8.7, leading=13.5, spaceAfter=0)
    styles['thead'] = ParagraphStyle('HeadCell', parent=styles['table'], fontName='TC-Bold', textColor=colors.white)
    styles['quote'] = ParagraphStyle('Callout', parent=styles['body'], leftIndent=12, rightIndent=12,
                                    backColor=colors.HexColor('#eef7f7'), borderPadding=10,
                                    spaceBefore=6, spaceAfter=12)
    styles['list'] = ParagraphStyle('List', parent=styles['body'], leftIndent=18, firstLineIndent=-16)
    styles['code'] = ParagraphStyle('Formula', parent=styles['quote'], fontSize=9.5, leading=16)
    return styles


def inline(node):
    pieces = [html.escape(node.text or '')]
    for child in node:
        tag = child.tag.lower()
        value = inline(child)
        if tag in ('strong', 'b'): value = '<b>' + value + '</b>'
        elif tag in ('em', 'i'): value = '<i>' + value + '</i>'
        elif tag == 'br': value = '<br/>'
        elif tag == 'a':
            url = child.get('href', '')
            if url.startswith('https://'):
                value = '<a href="' + html.escape(url, quote=True) + '" color="#087f8c">' + value + '</a>'
        pieces.append(value)
        pieces.append(html.escape(child.tail or ''))
    return ''.join(pieces)


def fix_svg_fonts(obj):
    if isinstance(obj, String):
        obj.fontName = 'TC-Bold' if 'bold' in str(obj.fontName).lower() else 'TC'
    for child in getattr(obj, 'contents', []): fix_svg_fonts(child)


def figure(path, alt, styles):
    if not path.exists(): raise FileNotFoundError(path)
    if path.suffix == '.svg':
        drawing = svg2rlg(str(path))
        fix_svg_fonts(drawing)
        scale = min(CONTENT / drawing.width, 340 / drawing.height)
        drawing.scale(scale, scale)
        drawing.width *= scale
        drawing.height *= scale
        drawing.hAlign = 'CENTER'
        fig = drawing
    else:
        with PILImage.open(path) as pic: pw, ph = pic.size
        scale = min(CONTENT / pw, 330 / ph)
        fig = Image(str(path), width=pw * scale, height=ph * scale)
        fig.hAlign = 'CENTER'
    return KeepTogether([Spacer(1, 8), fig, Spacer(1, 5), Paragraph(html.escape(alt), styles['caption'])])


def blocks(nodes, styles):
    flow = []
    for node in nodes:
        tag = node.tag.lower()
        if tag == 'h1':
            p = Paragraph(inline(node), styles['h1'])
            p.book_title = node.text_content()
            flow.append(p)
        elif tag in ('h2', 'h3'): flow.append(Paragraph(inline(node), styles[tag]))
        elif tag == 'p':
            imgs = node.findall('img')
            if imgs:
                for im in imgs: flow.append(figure(DOCS / im.get('src'), im.get('alt', ''), styles))
            else:
                value = inline(node)
                if value.strip(): flow.append(Paragraph(value, styles['small'] if node.text_content().startswith(('來源：', '来源：')) else styles['body']))
        elif tag == 'blockquote':
            for el in node:
                flow.append(Paragraph(inline(el), styles['quote']))
        elif tag in ('ul', 'ol'):
            for i, item in enumerate(node.findall('li'), 1):
                label = f'{i}. ' if tag == 'ol' else '• '
                # flatten nested blocks but retain emphasis and links
                flow.append(Paragraph(label + inline(item), styles['list']))
        elif tag == 'table':
            rows = node.xpath('.//tr')
            matrix = []
            for i, row in enumerate(rows):
                cells = row.xpath('./th|./td')
                matrix.append([Paragraph(inline(c), styles['thead'] if i == 0 else styles['table']) for c in cells])
            count = len(matrix[0])
            ratios = {2: [0.28,0.72], 3: [0.20,0.41,0.39], 4: [0.20,0.25,0.30,0.25]}.get(count, [1/count]*count)
            table = Table(matrix, colWidths=[CONTENT*r for r in ratios], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),NAVY), ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6f7')]),
                ('LINEBELOW',(0,0),(-1,0),0.5,TEAL),
                ('LINEBELOW',(0,1),(-1,-1),0.25,colors.HexColor('#d5e1e5')),
                ('LEFTPADDING',(0,0),(-1,-1),7), ('RIGHTPADDING',(0,0),(-1,-1),7),
                ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ]))
            flow.extend([Spacer(1,5),table,Spacer(1,12)])
        elif tag == 'pre':
            text = html.escape(node.text_content()).strip().replace('\n','<br/>')
            flow.append(Paragraph(text,styles['code']))
        elif tag == 'hr': flow.append(Spacer(1,10))
        else: flow.extend(blocks(list(node), styles))
    return flow


class BookDoc(BaseDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addPageTemplates(PageTemplate(id='book', frames=[Frame(MARGIN,48,CONTENT,H-95,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)], onPage=self.page))
    def page(self,c,doc):
        c.saveState()
        if doc.page > 1:
            c.setStrokeColor(TEAL); c.setLineWidth(0.7)
            c.line(MARGIN,H-31,W-MARGIN,H-31)
            c.setFont('TC',8); c.setFillColor(GRAY)
            c.drawString(MARGIN,H-24,'朝陽工管製造程序實習 · 車床與銑床')
            c.drawString(MARGIN,29,'v1.0 · 2026-10-11 · 實作前完成現場核對')
            c.drawRightString(W-MARGIN,29,str(doc.page))
        c.restoreState()
    def afterFlowable(self, flowable):
        if hasattr(flowable,'book_title'):
            title = flowable.book_title
            key = 'chapter-' + re.sub(r'[^0-9]','',title[:4])
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,0)
            self.notify('TOCEntry',(0,title,self.page,key))


def make_pdf(data):
    styles = setup_styles()
    output = ROOT/'output'/'pdf'/'cyut-lathe-milling-textbook.pdf'
    output.parent.mkdir(parents=True,exist_ok=True)
    story = [Spacer(1,38)]
    cover = ParagraphStyle('Cover',parent=styles['h1'],fontSize=33,leading=47,spaceAfter=16)
    story += [Paragraph('從旋轉看懂製造',styles['h2']), Paragraph('車床與銑床<br/>圖解操作教科書',cover),
              Paragraph(SUBTITLE,styles['body']),Spacer(1,12)]
    story.append(figure(DOCS/'assets'/'lathe-motion.svg','工件旋轉 × 刀具進給 · 原創示意',styles))
    story += [Spacer(1,14),Paragraph('實機照片導讀 / 逐步操作 / 兩個完整實作 / 量測與檢核',styles['body']),
              Paragraph('繁體中文 · 版本 1.0 · 2026-10-11',styles['body']),
              Paragraph('以使用者提供的 WINHO 威赫車床及立式膝式銑床照片為起點。品牌、部位與通用原理可對照；型號、面板程序與切削設定須由現場原廠手冊及教師確認。',styles['quote']),PageBreak()]
    story += [Paragraph('閱讀地圖',styles['h1']),Paragraph('先完成安全與現場確認，再進入受監督的切削練習。來源連結可在 PDF 中點擊；圖解可放大閱讀。',styles['body'])]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOC',parent=styles['body'],fontSize=11,leading=20,spaceBefore=8,leftIndent=0)]
    story += [toc,Spacer(1,22),Paragraph('實作前停點',styles['h2']),
              Paragraph('確認一：辨識控制與停止。<br/>確認二：裝夾、基準、刀具、間隙與參數。<br/>確認三：試刀、停機量測與下一刀。<br/>確認四：完工檢驗、清理與設備交回。',styles['quote'])]
    for chapter in data:
        story.append(PageBreak())
        fragment = lh.fragment_fromstring(markdown.markdown(chapter['raw'],extensions=['tables','fenced_code']),create_parent='div')
        story.extend(blocks(list(fragment),styles))
    # Include the source register in every durable edition.
    sources = DOCS/'sources.md'
    if sources.exists():
        story.append(PageBreak())
        fragment = lh.fragment_fromstring(markdown.markdown(sources.read_text(encoding='utf-8'),extensions=['tables']),create_parent='div')
        story.extend(blocks(list(fragment),styles))
    doc = BookDoc(str(output),pagesize=A4,title=TITLE,author='製造程序實習教材編製',subject=SUBTITLE)
    doc.multiBuild(story)
    import shutil
    shutil.copy2(output,DOCS/'textbook.pdf')
    print(json.dumps({'pdf':str(output),'chapters':len(data),'pages':doc.page,'bytes':output.stat().st_size},ensure_ascii=False))


if __name__ == '__main__':
    data = chapter_data()
    if len(data) != 10: raise RuntimeError(f'Expected 10 chapters, found {len(data)}')
    make_html(data)
    make_pdf(data)
