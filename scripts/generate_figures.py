"""Rebuild original, editable teaching diagrams (standard library only).

Run: python scripts/generate_figures.py
Photo callouts reference site-mill.jpg and site-lathe.jpg in docs/assets.
"""
from pathlib import Path
from html import escape
import math

OUT = Path(__file__).resolve().parents[1] / 'docs' / 'assets'
NAVY = '#163249'
TEAL = '#087f8c'
ORANGE = '#ed8b3a'
PALE = '#e9f4f5'
GRAY = '#dbe3e9'
MUTED = '#61788a'


class SVG:
    def __init__(self, title, subtitle='', height=700):
        self.p = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc">',
                  f'<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>',
                  f'<rect width="1200" height="{height}" fill="white"/>',
                  '<style>text{font-family:"Microsoft JhengHei","Noto Sans TC",sans-serif}</style>']
        self.text(40, 49, title, size=34, weight='bold')
        if subtitle:
            self.text(40, 86, subtitle, size=24, color=MUTED)
        self.line(40, 108, 1160, 108, color=GRAY, width=2)

    def raw(self, s): self.p.append(s)
    def text(self, x, y, s, size=26, color=NAVY, anchor='start', weight='normal'):
        self.p.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>')
    def lines(self, x, y, lines, size=26, step=35, **kwargs):
        for i, t in enumerate(lines): self.text(x, y + i * step, t, size=size, **kwargs)
    def rect(self, x, y, w, h, fill=PALE, stroke=NAVY, width=3, radius=0):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def circle(self, x, y, r, fill=PALE, stroke=NAVY, width=3):
        self.p.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def ellipse(self, x, y, rx, ry, fill=PALE, stroke=NAVY, width=3):
        self.p.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def _head(self, x, y, dx, dy, color, width, max_length=None):
        """Explicit triangles survive browser, svglib and ReportLab rendering."""
        norm = math.hypot(dx, dy)
        if norm == 0: raise ValueError('An arrow requires a non-zero direction')
        ux, uy = dx / norm, dy / norm
        length = 9 * width
        if max_length is not None: length = min(length, max_length)
        half = length / 2
        bx, by = x - length * ux, y - length * uy
        points = [(x,y), (bx-half*uy,by+half*ux), (bx+half*uy,by-half*ux)]
        attrs = ' '.join(f'{a:.3f},{b:.3f}' for a,b in points)
        self.p.append(f'<polygon data-role="arrowhead" points="{attrs}" fill="{color}" stroke="none"/>')
    def path(self, d, fill='none', color=NAVY, width=3, arrow=False, dash=None,
             arrow_tip=None, arrow_dir=None):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        self.p.append(f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"{extra}/>')
        if arrow:
            if arrow_tip is None or arrow_dir is None:
                raise ValueError('Curved arrow paths require an endpoint and tangent')
            self._head(*arrow_tip, *arrow_dir, color, width)
    def line(self, x1, y1, x2, y2, color=NAVY, width=3, arrow=False, both=False, dash=None):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        self.p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{extra}/>')
        if arrow or both:
            segment = math.hypot(x2-x1,y2-y1)
            cap = segment * (0.45 if both else 0.85)
            self._head(x2,y2,x2-x1,y2-y1,color,width,cap)
            if both: self._head(x1,y1,x1-x2,y1-y2,color,width,cap)
    def poly(self, pts, fill=GRAY, stroke=NAVY, width=3):
        self.p.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>')
    def leader(self, x1, y1, x2, y2): self.line(x1,y1,x2,y2,color=MUTED,width=2)
    def dim(self, x1, x2, y, t, ext=None):
        self.line(x1,y,x2,y,color=MUTED,width=2,both=True)
        self.text((x1+x2)/2,y-12,t,size=24,anchor='middle')
        if ext is not None:
            self.line(x1,y+6,x1,ext,color=MUTED,width=1.5)
            self.line(x2,y+6,x2,ext,color=MUTED,width=1.5)
    def vdim(self, y1,y2,x,t,ext=None):
        self.line(x,y1,x,y2,color=MUTED,width=2,both=True)
        self.text(x-12,(y1+y2)/2,t,size=24,anchor='end')
        if ext is not None:
            self.line(x+6,y1,ext,y1,color=MUTED,width=1.5)
            self.line(x+6,y2,ext,y2,color=MUTED,width=1.5)
    def note(self, lines, y=622):
        self.rect(40,y-27,1120,68,fill=PALE,stroke='none',radius=12)
        self.lines(60,y,lines,size=24,step=31)
    def save(self,name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT/name).write_text('\n'.join(self.p)+ '\n</svg>\n',encoding='utf-8')


def chuck(s, x, y, w=75, h=160):
    s.rect(x,y-h/2,w,h,fill=GRAY,radius=8)
    s.rect(x+w-8,y-h/2+10,20,37,fill=MUTED)
    s.rect(x+w-8,y+h/2-47,20,37,fill=MUTED)
    s.line(x-25,y,x+w+380,y,color=MUTED,width=2,dash='10 8')


def tool(s,x,y, orientation='upper'):
    if orientation == 'upper':
        s.poly([(x,y),(x+30,y-43),(x+120,y-43),(x+120,y-18)],fill=ORANGE)
    else:
        s.poly([(x,y),(x+30,y+43),(x+120,y+43),(x+120,y+18)],fill=ORANGE)


def lathe_anatomy():
    s=SVG('車床構造：工件旋轉，刀具移動','一般臥式車床示意；名稱位置須與現場機台核對。')
    s.rect(160,270,190,200,fill=GRAY,radius=10)
    s.rect(170,305,65,100,fill=PALE)
    s.circle(198,430,17,fill=ORANGE)
    chuck(s,350,350,65,140)
    s.rect(415,317,255,66)
    s.rect(630,390,190,80,fill=GRAY)
    s.rect(665,333,90,60,fill=GRAY)
    s.rect(682,300,52,32,fill=TEAL)
    tool(s,653,317)
    s.rect(872,305,150,108,fill=GRAY,radius=10)
    s.rect(818,337,55,25,fill=MUTED)
    s.poly([(818,337),(792,350),(818,362)],fill=GRAY)
    s.circle(1047,351,28,fill='none')
    s.line(1022,351,1072,351)
    s.rect(140,470,955,45,fill=GRAY)
    s.line(170,535,1060,535,color=MUTED,width=10)
    for x in range(200,1050,24): s.line(x,526,x+10,544,color=NAVY,width=2)
    s.rect(170,550,140,44,fill=GRAY); s.rect(900,550,140,44,fill=GRAY)
    s.text(110,190,'主軸箱',weight='bold'); s.leader(200,205,255,275)
    s.text(380,178,'夾頭與工件',weight='bold'); s.leader(475,195,415,310)
    s.text(620,176,'刀架與車刀',weight='bold'); s.leader(700,191,705,299)
    s.text(932,210,'尾座／套筒',weight='bold',anchor='middle'); s.leader(930,222,920,305)
    s.text(810,449,'溜座',weight='bold'); s.leader(809,440,777,417)
    s.text(65,570,'床身導軌',weight='bold'); s.leader(184,555,192,490)
    s.text(483,583,'絲桿／進給軸',weight='bold'); s.leader(610,566,610,535)
    s.text(45,445,'控制／停機',weight='bold'); s.leader(159,437,180,430)
    s.note(['圖為功能導覽，不能用它辨認未知手柄；變速、進給與急停須由教師逐一確認。'])
    s.save('lathe-anatomy.svg')


def lathe_motion():
    s=SVG('車削的兩種運動','旋轉提供切削速度；刀具的軸向與徑向移動決定形狀。')
    chuck(s,180,320,100,190)
    s.rect(280,270,595,100)
    s.ellipse(875,320,24,50)
    s.line(120,320,940,320,color=MUTED,width=2,dash='10 8')
    s.path('M205 230 C160 205 128 270 157 298',color=TEAL,width=5,arrow=True,
           arrow_tip=(157,298),arrow_dir=(29,28))
    s.text(50,178,'工件繞主軸旋轉',weight='bold')
    tool(s,730,370,'lower')
    s.line(850,470,560,470,color=TEAL,width=5,arrow=True)
    s.text(560,515,'軸向進給：沿主軸方向',weight='bold')
    s.line(962,443,962,338,color=ORANGE,width=5,arrow=True)
    s.lines(880,190,['徑向進給','靠近／離開軸線'],weight='bold')
    s.leader(985,245,966,336)
    s.text(590,345,'主軸中心線',size=24,color=MUTED,anchor='middle')
    s.text(804,424,'刀具',size=24); s.leader(796,416,771,390)
    s.note(['車外徑通常以軸向進給形成圓柱；車端面以徑向進給形成平面。','直徑減少量 = 2 * 徑向切深；手輪刻度是直徑值或半徑值，須先核對。'])
    s.save('lathe-motion.svg')


def lathe_setup():
    s=SVG('車床裝夾：短伸出、夾牢、刀尖對中心','裝夾與校正都在停機狀態完成；三爪自定心不代表沒有偏心。')
    s.rect(50,130,520,420,fill='white',stroke=GRAY,radius=12)
    s.text(75,172,'側視：工件縮短伸出',weight='bold')
    chuck(s,160,335,110,210)
    s.rect(270,292,200,86)
    s.rect(155,292,115,86,fill='#bed9dd')
    s.dim(270,470,250,'伸出長度',ext=291)
    s.text(92,465,'三爪均勻夾持'); s.leader(220,442,270,365)
    s.text(306,500,'必要時加頂尖支撐',size=24)
    s.rect(610,130,540,420,fill='white',stroke=GRAY,radius=12)
    s.text(635,172,'端視：刀尖位於軸線高度',weight='bold')
    s.circle(803,338,116,fill=GRAY)
    s.circle(803,338,63,fill=PALE)
    for a in (30,150,270):
        s.raw(f'<g transform="rotate({a} 803 338)">')
        s.rect(866,319,53,38,fill=MUTED)
        s.raw('</g>')
    s.line(648,338,1110,338,color=MUTED,width=2,dash='10 8')
    s.line(803,205,803,474,color=MUTED,width=2,dash='10 8')
    s.poly([(866,338),(1000,306),(1040,306),(1040,362),(1000,362)],fill=ORANGE)
    s.text(954,277,'刀尖',weight='bold'); s.leader(968,286,866,338)
    s.text(729,501,'停機以頂尖／量規校正',size=24)
    s.note(['工件與刀具接觸面先清潔；夾頭鑰匙使用完立即取下。','伸出與夾持長度由工件、夾具和切削負荷決定，不把示意比例當作安全極限。'])
    s.save('lathe-setup.svg')


def lathe_facing():
    s=SVG('車端面：從外緣向中心進給','先定位端面，再用小軸向切深；接近中心時注意切削速度下降。')
    chuck(s,200,360,90,220)
    s.rect(290,290,410,140)
    s.ellipse(700,360,18,70,fill='#bed9dd')
    s.line(155,360,815,360,color=MUTED,width=2,dash='10 8')
    tool(s,706,425,'lower')
    s.line(759,424,759,363,color=TEAL,width=5,arrow=True)
    s.text(845,364,'徑向進給',weight='bold'); s.leader(834,369,772,390)
    s.text(790,490,'刀尖由外緣接近中心',size=24)
    s.path('M218 250 C167 215 137 291 175 311',color=TEAL,width=5,arrow=True,
           arrow_tip=(175,311),arrow_dir=(38,20))
    s.text(71,181,'工件旋轉',weight='bold')
    s.text(471,225,'端面',weight='bold'); s.leader(530,235,703,312)
    s.line(787,277,735,277,color=ORANGE,width=4,arrow=True)
    s.text(785,244,'小量軸向切深',size=24)
    s.text(382,520,'端面與主軸軸線垂直',size=24)
    s.note(['1  停機設定刀尖中心高 → 2  在外緣留安全間隙 → 3  試轉 → 4  薄削端面。','完成一刀後先退離端面再返回；停機後才去毛邊與量測。'])
    s.save('lathe-facing.svg')


def lathe_turning():
    s=SVG('車外徑：徑向設定切深，軸向完成長度','箭頭表示本圖的切削方向；刀具型式與進刀方向須由教師確認。')
    chuck(s,170,350,100,200)
    s.path('M270 280 H605 V305 H920 V395 H605 V420 H270 Z',fill=PALE)
    s.line(135,350,1005,350,color=MUTED,width=2,dash='10 8')
    tool(s,605,305)
    s.line(853,218,621,218,color=TEAL,width=5,arrow=True)
    s.text(680,178,'軸向進給至肩部',weight='bold',anchor='middle')
    s.line(1000,276,1000,306,color=ORANGE,width=5,arrow=True)
    s.text(890,244,'徑向切深 ap',size=24)
    s.text(300,480,'未車削區'); s.leader(416,452,443,418)
    s.text(749,480,'已車削外徑'); s.leader(831,452,835,396)
    s.text(533,542,'肩部位置',size=24); s.leader(592,514,605,414)
    s.dim(607,920,520,'車削長度',ext=396)
    s.note(['先粗車並保留精車餘量；停機量測後，小量修正切深再精車。','外徑目標 D：徑向修正量 = (目前外徑 - D) / 2；勿在旋轉中用游標尺。'])
    s.save('lathe-turning.svg')


def lathe_drilling():
    s=SVG('車床鑽孔：工件旋轉，尾座鑽頭不旋轉','尾座沿主軸中心線推進；不得手持鑽頭或夾頭。')
    chuck(s,125,310,95,180)
    s.rect(220,260,370,100)
    s.ellipse(590,310,17,50)
    s.rect(810,235,250,150,fill=GRAY,radius=12)
    s.rect(724,287,90,46,fill=MUTED)
    s.poly([(604,310),(637,292),(725,292),(725,328),(637,328)],fill=GRAY)
    for x in range(648,717,20): s.line(x,293,x+20,327,color=MUTED,width=2)
    s.line(110,310,1090,310,color=MUTED,width=2,dash='10 8')
    s.path('M149 213 C112 187 81 246 113 277',color=TEAL,width=5,arrow=True,
           arrow_tip=(113,277),arrow_dir=(32,31))
    s.text(56,162,'工件旋轉',weight='bold')
    s.line(800,424,618,424,color=ORANGE,width=5,arrow=True)
    s.text(723,462,'套筒推進',weight='bold',anchor='middle')
    s.text(830,180,'尾座固定，鑽頭不轉',weight='bold')
    s.rect(100,496,458,73,fill=PALE,stroke=GRAY,radius=10)
    s.text(123,542,'① 短中心鑽建立起鑽位置',size=24)
    s.line(575,532,614,532,color=TEAL,width=4,arrow=True)
    s.rect(633,496,467,73,fill=PALE,stroke=GRAY,radius=10)
    s.text(657,542,'② 適當先導孔 → 目標孔徑',size=24)
    s.note(['選用適合材料與孔徑的鑽速，分段退出排屑；停止主軸後才清理與檢查。','中心鑽避免讓粗短錐部過度埋入；先導孔尺寸與鑽孔順序依刀具資料及教師指示。'])
    s.save('lathe-drilling.svg')


def lathe_project():
    s=SVG('車床練習：階梯軸與二次裝夾','毛胚 φ25 × 75 mm；成品總長 60 mm：φ20 × 40 + φ16 × 20。')
    s.text(60,149,'① 第一次裝夾：夾原料左端 25 mm',weight='bold')
    s.rect(100,185,600,74)
    s.rect(100,185,200,74,fill=GRAY)
    s.rect(100,176,200,17,fill=MUTED)
    s.rect(100,251,200,17,fill=MUTED)
    s.dim(300,700,179,'外露 50',ext=185)
    s.text(752,215,'右端 A',weight='bold')
    s.lines(752,249,['由 A 起 44 mm 車 φ20','再由 A 起 20 mm 車 φ16'],size=24,step=31)
    s.text(60,314,'② 反夾：保護已車 φ20 段，停機校正',weight='bold')
    s.path('M100 369 H260 V364 H452 V358 H692 V422 H452 V416 H260 V411 H100 Z',fill=PALE)
    s.rect(260,364,160,52,fill=GRAY)
    s.rect(260,347,160,17,fill=MUTED)
    s.rect(260,416,160,17,fill=MUTED)
    s.line(580,354,580,426,color=ORANGE,width=4,dash='6 5')
    s.text(442,345,'B 端外露約 34 mm',size=24)
    s.lines(760,378,['夾 A 起 20–40 mm 段','B 端車至總長 60 mm','補車 B 起 16 mm 為 φ20'],size=24,step=31)
    s.text(60,484,'③ 成品：取下後量總長與兩段直徑',weight='bold')
    s.path('M290 523 H690 V531 H890 V595 H690 V603 H290 Z',fill=PALE)
    s.dim(290,690,520,'40',ext=523)
    s.dim(690,890,520,'20',ext=531)
    s.text(450,571,'φ20',anchor='middle')
    s.text(787,571,'φ16',anchor='middle')
    s.note(['反夾接觸面使用教師核准的軟爪／夾套保護；圖中灰色為夾持區。','二次裝夾有同軸度限制；先確認校正結果，再進行端面與接續外徑加工。'],y=644)
    s.save('lathe-project.svg')


def mill_anatomy():
    s=SVG('立式膝式銑床：旋轉刀具切削工件','一般功能構造示意；不代表實機品牌、型號或手柄配置。')
    s.rect(450,175,290,74,fill=GRAY,radius=12)
    s.rect(446,236,185,97,fill=GRAY)
    s.rect(490,333,100,70,fill=MUTED)
    s.rect(517,399,47,52,fill=TEAL)
    s.rect(533,449,15,42,fill=ORANGE)
    s.rect(655,253,135,310,fill=GRAY)
    s.rect(410,540,380,56,fill=GRAY)
    s.rect(400,480,260,58,fill=GRAY)
    s.rect(250,458,650,36,fill=GRAY)
    for y in (465,477,489): s.line(263,y,885,y,color=MUTED,width=2)
    s.rect(438,428,175,30,fill=PALE)
    s.rect(438,417,30,43,fill=MUTED); s.rect(583,417,30,43,fill=MUTED)
    s.circle(945,476,31,fill='none'); s.line(900,476,973,476)
    s.circle(500,552,24,fill='none')
    s.text(820,183,'銑頭',weight='bold'); s.leader(811,190,739,215)
    s.text(81,228,'主軸與套筒',weight='bold'); s.leader(252,225,490,368)
    s.text(47,333,'刀具',weight='bold'); s.leader(115,324,538,467)
    s.text(47,424,'虎鉗與工件',weight='bold'); s.leader(214,417,439,438)
    s.text(835,407,'工作台（X）',weight='bold'); s.leader(890,421,841,459)
    s.text(930,549,'手輪',weight='bold'); s.leader(962,525,945,507)
    s.text(134,566,'鞍座（Y）',weight='bold'); s.leader(270,553,407,511)
    s.text(823,586,'膝座（Z）',weight='bold'); s.leader(818,572,735,552)
    s.note(['立式銑床的刀具繞垂直主軸旋轉；以工作台、鞍座與膝座控制工件位置。'])
    s.save('mill-anatomy.svg')


def mill_axes():
    s=SVG('銑床座標：先分清工作台與刀具的相對運動','本圖採操作員面向機台：工作台右移為 +X、遠離操作員為 +Y、上升為 +Z。')
    s.rect(553,180,95,85,fill=GRAY)
    s.rect(582,265,36,112,fill=TEAL)
    s.poly([(280,382),(900,382),(820,462),(200,462)],fill=PALE)
    s.poly([(200,462),(820,462),(820,499),(200,499)],fill=GRAY)
    s.poly([(820,462),(900,382),(900,419),(820,499)],fill=GRAY)
    s.poly([(440,371),(660,371),(614,414),(394,414)],fill=ORANGE)
    s.rect(394,414,220,30,fill='#fadfc9')
    s.line(530,534,850,534,color=TEAL,width=5,arrow=True)
    s.text(888,542,'+X 右移',weight='bold')
    s.line(282,491,376,392,color=TEAL,width=5,arrow=True)
    s.lines(45,306,['+Y 遠離操作員','（工作台向後）'],weight='bold')
    s.leader(250,344,355,413)
    s.line(982,493,982,281,color=ORANGE,width=5,arrow=True)
    s.text(1040,353,'+Z',weight='bold')
    s.text(1008,393,'上升',weight='bold')
    s.text(475,178,'刀具位置',size=24); s.leader(560,192,583,278)
    s.text(265,582,'操作員站位',size=24)
    s.note(['工作台往 +X 移動，固定刀具相對工件往 -X 移動；Y、Z 同理。','DRO 的正負號可能另有設定；先空行程確認各軸與數字變化，再定零點。'])
    s.save('mill-axes.svg')


def mill_workholding():
    s=SVG('銑床裝夾：工件確實支承，刀路避開夾具','清除接觸面切屑；以教師核准的方式敲實、夾緊並確認貼合。')
    s.rect(40,135,545,423,fill='white',stroke=GRAY,radius=12)
    s.text(63,177,'正視：虎鉗與平行墊鐵',weight='bold')
    s.rect(85,445,455,47,fill=GRAY)
    s.rect(85,300,88,144,fill=MUTED)
    s.rect(452,300,88,144,fill=MUTED)
    s.rect(173,280,279,132,fill=PALE)
    s.rect(183,412,38,32,fill=TEAL)
    s.rect(403,412,38,32,fill=TEAL)
    s.text(226,328,'工件',weight='bold')
    s.text(125,235,'兩側夾持面',size=24); s.leader(208,245,171,350)
    s.text(206,537,'底面貼緊兩支墊鐵',size=24); s.leader(260,510,220,428)
    s.rect(615,135,545,423,fill='white',stroke=GRAY,radius=12)
    s.text(638,177,'俯視：保留刀具與夾具間隙',weight='bold')
    s.rect(670,290,425,140,fill=PALE)
    s.rect(670,242,425,48,fill=MUTED)
    s.rect(670,430,425,48,fill=MUTED)
    s.circle(826,342,39,fill='#fadfc9',stroke=ORANGE)
    s.line(731,342,1021,342,color=TEAL,width=4,arrow=True)
    s.text(767,229,'刀路包絡',size=24); s.leader(840,240,829,302)
    s.text(763,527,'勿撞虎鉗、螺栓與墊鐵',size=24)
    s.note(['正式加工前，停轉檢查全刀路與換刀後長度；孔鑽透時更要避開下方墊鐵。','虎鉗夾得住不代表每處都有支承；長件、大懸伸或薄件另用合適夾具。'])
    s.save('mill-workholding.svg')


def mill_direction():
    s=SVG('順銑與逆銑：比較接觸處切向速度與工作台進給','俯視示意：兩圖刀具皆順時針旋轉；橘點是用來比較方向的接觸位置。')
    for cx,title,feed_right,chip in ((315,'逆銑',True,'切屑厚度：薄 → 厚'),(870,'順銑',False,'切屑厚度：厚 → 薄')):
        s.text(cx,162,title,anchor='middle',weight='bold',size=32)
        s.circle(cx,322,107,fill=PALE)
        for a in range(0,360,45):
            rad=math.radians(a)
            s.line(cx+91*math.cos(rad),322+91*math.sin(rad),cx+106*math.cos(rad),322+106*math.sin(rad),color=TEAL,width=7)
        s.path(f'M{cx-56} 227 A110 110 0 0 1 {cx+109} 322',color=TEAL,width=4,arrow=True,
               arrow_tip=(cx+109,322),arrow_dir=(0,1))
        s.rect(cx-190,429,380,74,fill=GRAY)
        s.circle(cx,429,7,fill=ORANGE,stroke=ORANGE)
        s.line(cx+87,413,cx-83,413,color=ORANGE,width=4,arrow=True)
        s.text(cx,380,'接觸處刀刃速度 ←',size=24,anchor='middle')
        x1,x2=(cx-135,cx+135) if feed_right else (cx+135,cx-135)
        s.line(x1,548,x2,548,color=TEAL,width=5,arrow=True)
        s.text(cx,584,'工作台進給' + (' →（相反）' if feed_right else ' ←（相同）'),size=24,anchor='middle')
        s.text(cx,206,chip,size=24,anchor='middle')
    s.line(590,140,590,590,color=GRAY,width=2)
    s.note(['有背隙的傳統手動銑床，順銑可能拉動工作台突然前衝；初學依教師指定採逆銑。','旋轉反向或改在刀具另一側切削時，必須重新比較接觸點方向，不能只看左右箭頭。'])
    s.save('mill-direction.svg')


def mill_datum():
    s=SVG('銑床基準：尋邊補半徑，Z 軸補量塊厚度','先決定工件基準，再記錄顯示值；尋邊器與量塊都須使用核准方法。')
    s.rect(45,137,520,415,fill='white',stroke=GRAY,radius=12)
    s.text(67,179,'X 基準：從左側尋邊',weight='bold')
    s.rect(246,293,250,174,fill=PALE)
    s.circle(216,351,30,fill=ORANGE)
    s.rect(207,244,18,77,fill=GRAY)
    s.line(216,225,216,445,color=MUTED,width=2,dash='8 6')
    s.line(246,255,246,486,color=TEAL,width=3,dash='8 6')
    s.text(90,219,'尋邊器中心',size=24)
    s.text(317,278,'真正邊界 X=0',size=24)
    s.dim(216,246,411,'R')
    s.text(80,519,'接觸時中心：X = -R',size=24)
    s.rect(615,137,540,415,fill='white',stroke=GRAY,radius=12)
    s.text(637,179,'Z 基準：停轉刀具接觸定厚量塊',weight='bold')
    s.rect(765,217,85,61,fill=GRAY)
    s.rect(791,278,33,68,fill=TEAL)
    s.rect(773,346,74,55,fill=ORANGE)
    s.rect(685,401,340,76,fill=PALE)
    s.line(679,401,1080,401,color=TEAL,width=3,dash='8 6')
    s.vdim(346,401,926,'h')
    s.text(954,348,'刀尖 Z=+h',size=24)
    s.text(954,431,'上表面 Z=0',size=24)
    s.text(646,519,'取出量塊後再加工；向下為負 Z',size=24)
    s.note(['X/Y 尋邊要補尋邊器有效半徑；不把中心位置直接當作材料邊界。','Z 圖採刀具相對工件座標；刀具已停轉，禁止拿紙或手碰旋轉刀具。'])
    s.save('mill-datum.svg')


def mill_face():
    s=SVG('平面銑削：薄切、多道、保持合理重疊','俯視與側視示意；走刀路徑、旋轉方向及順逆銑由教師確認。')
    s.rect(245,218,650,230,fill=PALE)
    s.circle(213,268,68,fill='#fadfc9',stroke=ORANGE)
    s.line(153,268,1000,268,color=TEAL,width=4,arrow=True)
    s.line(1000,348,150,348,color=TEAL,width=4,arrow=True)
    s.line(153,428,1000,428,color=TEAL,width=4,arrow=True)
    s.text(141,172,'刀具從工件外側接近',size=24)
    s.text(630,187,'相鄰刀道部分重疊',size=24)
    s.leader(733,195,708,310)
    s.text(983,466,'離開邊界',size=24,anchor='middle')
    s.leader(976,439,983,428)
    s.text(251,486,'俯視：整個上表面都被刀具掃過',size=24)
    s.rect(306,538,539,38,fill=PALE)
    s.line(306,530,845,530,color=ORANGE,width=3,dash='7 6')
    s.line(300,530,300,539,color=ORANGE,width=3)
    s.text(41,562,'側視：小切深',size=24)
    s.note(['先確認夾具高度與刀具下緣間隙，再選小切深試切；停機量厚度與表面平整度。','圖中箭頭僅表示覆蓋次序；不可把示意折返當作順逆銑或自動進給的固定設定。'])
    s.save('mill-face.svg')


def mill_slot():
    s=SVG('端銑槽：先建立入口，再分層加工','封閉槽不能把任意端銑刀直接壓下；刀具是否可下切須查原廠資料。')
    s.rect(215,205,770,210,fill=PALE)
    s.rect(370,265,445,90,fill='#c4dde1',radius=45)
    s.circle(415,310,45,fill='#fadfc9',stroke=ORANGE)
    s.line(415,310,770,310,color=TEAL,width=5,arrow=True)
    s.line(415,249,415,372,color=MUTED,width=2,dash='8 7')
    s.line(770,249,770,372,color=MUTED,width=2,dash='8 7')
    s.dim(370,815,177,'槽總長 L',ext=264)
    s.text(500,394,'中心行程 = L - 刀具直徑',size=24)
    s.text(986,319,'槽寬',size=24)
    s.leader(980,325,815,350)
    s.rect(365,503,475,57,fill=PALE)
    s.rect(415,503,355,37,fill='white',stroke='none')
    s.path('M415 503 V540 H770 V503',color=NAVY,width=3)
    for y in (514,527): s.line(415,y,770,y,color=TEAL,width=2,dash='8 6')
    s.rect(542,443,45,63,fill=GRAY)
    s.line(614,448,614,492,color=ORANGE,width=4,arrow=True)
    s.text(682,466,'分層至目標槽深',size=24)
    s.text(56,540,'側視',weight='bold')
    s.note(['只有具中心刃、且原廠允許下切的刀具，才可依核准條件直接下刀；否則先鑽入口孔。','入口孔、槽中心行程、刀徑與每層深度都要先算清楚；全槽切削負荷較大。'])
    s.save('mill-slot.svg')


def mill_project():
    s=SVG('銑床練習：平面、封閉槽與兩個通孔','毛胚 65 × 45 × 18 mm → 成品 60 × 40 × 15 mm；全部尺寸為 mm。')
    x0,y0,k=260,551,9
    s.rect(x0,y0-40*k,60*k,40*k,fill=PALE)
    s.rect(x0+15*k,y0-24*k,30*k,8*k,fill='#c4dde1',radius=4*k)
    for x,y in ((10,10),(50,30)):
        cx,cy=x0+x*k,y0-y*k
        s.circle(cx,cy,3*k,fill='white')
        s.line(cx-35,cy,cx+35,cy,color=MUTED,width=1.5,dash='5 5')
        s.line(cx,cy-35,cx,cy+35,color=MUTED,width=1.5,dash='5 5')
    s.line(x0+19*k,y0-20*k,x0+41*k,y0-20*k,color=TEAL,width=3,both=True)
    s.dim(x0,x0+60*k,161,'60',ext=191)
    s.vdim(y0-40*k,y0,217,'40',ext=x0)
    s.text(867,227,'2 × φ6 通孔',weight='bold')
    s.leader(858,242,710,282)
    s.lines(867,310,['孔中心 (10,10)','孔中心 (50,30)'],size=24,step=35)
    s.lines(854,410,['槽長 30、寬 8、深 3','兩端 R4','φ8 刀具中心：','X=19..41，Y=20'],size=24,step=35)
    s.leader(845,413,665,370)
    s.line(x0,y0,x0+120,y0,color=TEAL,width=4,arrow=True)
    s.line(x0,y0,x0,y0-90,color=TEAL,width=4,arrow=True)
    s.text(x0+129,y0+9,'+X',size=24)
    s.text(x0-16,y0-97,'+Y',size=24,anchor='end')
    s.text(63,585,'左前角 (0,0)',size=24)
    s.leader(223,571,x0,y0)
    s.note(['上表面 Z=0，槽底 Z=-3；成品厚度 15。俯視圖比例一致。','鑽透時下方必須留出鑽尖空間；孔的位置不得落在平行墊鐵或虎鉗上。'])
    s.save('mill-project.svg')


def safety_workflow():
    s=SVG('每一道加工都走一次安全循環','裝夾、量測、清屑和換刀在完全停轉後執行；緊急時先停機再求助。')
    stages=[('裝夾檢查',['鑰匙取下','刀具／工件鎖妥']),('空載試轉',['人員避開','確認轉向與干涉']),('小量切削',['穩定進給','觀察聲音與切屑']),('停機待停',['主軸完全停止','清屑使用刷／鉤']),('量測紀錄',['去毛邊與清潔','尺寸→修正量'])]
    for i,(title,ls) in enumerate(stages):
        x=40+i*229
        s.rect(x,272,200,222,fill=PALE,stroke=TEAL,radius=14)
        s.circle(x+100,257,27,fill=TEAL,stroke=TEAL)
        s.text(x+100,267,i+1,anchor='middle',color='white',weight='bold',size=28)
        s.text(x+100,335,title,anchor='middle',weight='bold')
        s.lines(x+100,398,ls,size=24,step=36,anchor='middle')
        if i<4:s.line(x+202,380,x+224,380,color=TEAL,width=4,arrow=True)
    s.path('M1060 512 V565 H140 V514',color=ORANGE,width=4,arrow=True,
           arrow_tip=(140,514),arrow_dir=(0,-1))
    s.text(591,550,'需要修正 → 回到檢查，再試切',size=24,anchor='middle')
    s.note(['異音、鬆動、振動、刀具卡住：立即停機，等完全停止後請教師檢查。','急停是危急時的動作；日常停機、復歸與重新啟動流程依實機規定。'])
    s.save('safety-workflow.svg')


def measurement():
    s=SVG('停機量測：外卡接觸面與分厘卡測砧','量測前先停機、去毛邊、清潔並等工件冷卻；尺寸公差決定量具選擇。')
    s.text(72,169,'游標卡尺：一般外徑／長度',weight='bold')
    s.circle(326,376,90,fill=PALE)
    s.rect(146,236,420,29,fill=GRAY)
    s.rect(210,214,49,81,fill=PALE)
    s.rect(391,214,67,81,fill=PALE)
    for x in range(280,556,15):s.line(x,237,x,250,color=MUTED,width=1.5)
    s.rect(219,265,17,127,fill=GRAY)
    s.rect(416,265,17,127,fill=GRAY)
    s.line(236,376,249,376,color=ORANGE,width=5)
    s.line(404,376,417,376,color=ORANGE,width=5)
    s.line(235,490,416,490,color=MUTED,width=2,both=True)
    s.text(326,530,'外測量爪輕貼兩側',size=24,anchor='middle')
    s.text(139,576,'保持垂直，避免斜量',size=24)
    s.text(674,169,'外徑分厘卡：更細的直徑判讀',weight='bold')
    s.circle(865,376,61,fill=PALE)
    s.path('M804 376 H770 C682 376 682 521 781 521 H970 V398',color=NAVY,width=24)
    s.rect(765,363,39,26,fill=GRAY)
    s.rect(926,363,98,26,fill=GRAY)
    s.rect(1005,344,83,65,fill=PALE)
    s.rect(1088,354,39,45,fill=GRAY)
    s.line(804,376,811,376,color=ORANGE,width=5)
    s.line(919,376,926,376,color=ORANGE,width=5)
    s.text(750,280,'固定測砧',size=24); s.leader(815,292,790,363)
    s.text(1030,474,'棘輪控測力',size=24,anchor='middle'); s.leader(1080,447,1107,401)
    s.note(['測量面避開毛邊與夾持傷痕；分厘卡用棘輪／摩擦套控制測力，勿用力旋緊。','接觸面對齊並多點量測；圖是接觸概念，不表示卡尺可以代替精密公差檢驗。'])
    s.save('measurement.svg')


def site_callouts(kind):
    is_mill=kind=='mill'
    title='實機照片導覽：立式膝式銑床' if is_mill else '實機照片導覽：WINHO 威赫車床'
    s=SVG(title,'使用者提供之現場照片；僅標註可見要素，未確認型號、手柄功能與設定。',height=790)
    x,y,w,h=45,125,750,562.5
    s.raw(f'<image href="site-{kind}.jpg" xlink:href="site-{kind}.jpg" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>')
    if is_mill:
        labels=['套筒（主軸外部）','主軸／刀具固定處','虎鉗','工作台','膝座','可見手輪']
        # Photo pixels mapped without cropping, with displaced numbered circles.
        targets=[(699,382),(704,431),(710,518),(990,551),(681,785),(711,735)]
        circles=[(550,285),(550,335),(570,402),(684,463),(553,574),(361,495)]
    else:
        labels=['WINHO 威赫銘牌','主軸轉速表','停機變速警示','螺紋／進給表','夾頭','床身導軌','可見絲桿']
        targets=[(823,468),(768,610),(1040,610),(273,766),(1363,442),(1344,850),(1328,980)]
        circles=[(653,284),(556,420),(711,456),(127,550),(739,221),(711,551),(674,647)]
    for i,((px,py),(cx,cy)) in enumerate(zip(targets,circles),1):
        tx=x+px*w/1477; ty=y+py*h/1108
        s.line(cx,cy,tx,ty,color=ORANGE,width=3)
        s.circle(cx,cy,19,fill='white',stroke=ORANGE,width=3)
        s.text(cx,cy+8,i,anchor='middle',size=24,weight='bold')
    for i,label in enumerate(labels,1):
        ly=164+(i-1)*68
        s.circle(837,ly-8,18,fill=PALE,stroke=TEAL)
        s.text(837,ly,i,anchor='middle',size=24,weight='bold')
        s.text(867,ly,label,size=24)
    s.note(['照片上散放的工具並非可開機配置；啟動前先清空機台與工作台。','操作程序仍須由現場教師核對；照片不能用來推定未知手柄功能。'],y=733)
    s.save(f'site-{kind}-callouts.svg')


def main():
    for fn in (lathe_anatomy,lathe_motion,lathe_setup,lathe_facing,lathe_turning,lathe_drilling,lathe_project,
               mill_anatomy,mill_axes,mill_workholding,mill_direction,mill_datum,mill_face,mill_slot,mill_project,
               safety_workflow,measurement): fn()
    site_callouts('mill'); site_callouts('lathe')
    readme='''# 教材技術圖

本目錄的 17 張 SVG 是原創、可編輯的技術示意，**不是朝陽科技大學機台照片或原廠手冊**。圖中比例、外觀、手柄與附件均簡化；操作前須以教師講解、實機標示及原廠資料核對。

`site-mill.jpg`、`site-lathe.jpg` 是使用者提供的現場照片，對應兩張 `site-*-callouts.svg`。照片導覽只標示可見位置，不推定型號、手柄功能、轉速設定或安全裝置。照片中的工具堆放不是可開機配置。

重建方式（不需第三方 Python 套件）：

```powershell
python scripts/generate_figures.py
```

所有圖使用 SVG `viewBox`、白色背景與繁體中文；一般標籤為 24–34 px。箭頭、尺寸和圖說均是可搜尋文字及向量路徑。

方向箭頭採顯式三角形向量，不依賴 SVG marker；可保留 svglib → ReportLab 的 PDF 箭頭。

|圖檔|主題|
|---|---|
|lathe-anatomy.svg|車床構造|
|lathe-motion.svg|車削運動|
|lathe-setup.svg|夾持與刀尖中心高|
|lathe-facing.svg|端面車削|
|lathe-turning.svg|外徑車削|
|lathe-drilling.svg|尾座鑽孔|
|lathe-project.svg|階梯軸二次裝夾|
|mill-anatomy.svg|立式膝式銑床構造|
|mill-axes.svg|工作台座標與相對刀具運動|
|mill-workholding.svg|虎鉗、平行墊鐵及避讓|
|mill-direction.svg|順逆銑接觸處方向|
|mill-datum.svg|尋邊半徑與 Z 量塊補償|
|mill-face.svg|平面覆蓋與薄切|
|mill-slot.svg|槽銑入口及分層|
|mill-project.svg|銑床成品尺寸與座標|
|safety-workflow.svg|每刀停機量測循環|
|measurement.svg|卡尺與分厘卡接觸概念|
|site-mill-callouts.svg|銑床實機照片導覽|
|site-lathe-callouts.svg|車床實機照片導覽|

技術核對重點：逆銑的工作台進給與接觸處刀刃速度相反，順銑相同；圖中兩刀皆順時針。車削直徑變化為徑向切深的兩倍。尋邊器中心由左側接觸時為 X=-R。槽長30、刀徑8對應中心行程22；練習槽中心X=19..41、Y=20。實機圖示不授權用未知手柄或表格配速。
'''
    (OUT/'README.md').write_text(readme,encoding='utf-8')
    print(f'Generated 19 SVG figures in {OUT}')


if __name__=='__main__':main()
