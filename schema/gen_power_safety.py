# -*- coding: utf-8 -*-
"""Принципиальная электрическая схема силовой части и цепей безопасности
одноколонного штабелёра.

Силовая часть: ввод 3~400В, главный выключатель, два ПЧ (подъём, вилы) с
двигателями, тормоз, тормозной резистор, источник 24В.
Контур безопасности: реле безопасности, аварийный стоп, концевики ворот,
лазерные сканеры, перебег; выходы STO к ПЧ и размыкание питания тормоза.

Выход: power-safety-schematic.svg
"""

W, H = 1880, 980
C_BLACK = "#1a1a1a"; C_RED = "#d40000"; C_BLUE = "#0050c8"
C_GREEN = "#0a8f3c"; C_GREY = "#888"

svg = []
def add(s): svg.append(s)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="DejaVu Sans, Arial, sans-serif">')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')
add('<defs>'
    f'<marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C_BLACK}"/></marker>'
    f'<marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C_RED}"/></marker>'
    '</defs>')

def box(x,y,w,h,color=C_BLACK,fill="#fff",sw=2,rx=0,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{d}/>')
def line(x1,y1,x2,y2,color=C_BLACK,sw=2,dash=None,arrow=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    m=f' marker-end="url(#{arrow})"' if arrow else ''
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>')
def text(x,y,s,color=C_BLACK,fs=12,anchor="start",weight="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>')
def motor(x,y,label):
    add(f'<circle cx="{x}" cy="{y}" r="26" fill="#fff" stroke="{C_BLACK}" stroke-width="2"/>')
    text(x,y-2,label,fs=13,anchor="middle",weight="bold"); text(x,y+14,'3~',fs=11,anchor="middle")
def breaker(x,y,label,poles=3,color=C_BLACK):
    box(x-26,y-16,52,32,color=color,fill="#fff",sw=2,rx=3)
    text(x,y+4,label,fs=11,anchor="middle",weight="bold",color=color)
    text(x+32,y-3,f'{poles}P',fs=9,anchor="start",color=C_GREY)

# ---- Заголовок ----
text(W/2,34,'Принципиальная электрическая схема: силовая часть и цепи безопасности',fs=21,anchor="middle",weight="bold")
text(W/2,56,'Одноколонный штабелёр · 2 привода (подъём, вилы) · тормоз · реле безопасности (STO)',fs=12.5,anchor="middle",color="#555")

# ============ СИЛОВАЯ ЧАСТЬ ============
text(60,92,'СИЛОВАЯ ЧАСТЬ',fs=15,weight="bold")
rails=[('L1',120),('L2',136),('L3',152),('N',168),('PE',184)]
rail_x0=120
for nm,yy in rails:
    col=C_GREEN if nm=='PE' else (C_BLUE if nm=='N' else C_BLACK)
    line(rail_x0,yy,1140,yy,color=col,sw=2)
    text(rail_x0-8,yy+4,nm,fs=11,anchor="end",color=col,weight="bold")
text(rail_x0-8,104,'~3×400/230В, 50Гц',fs=11,anchor="end",color="#555")

# Главный выключатель QF0
qf0x=240
for nm,yy in rails[:3]: line(qf0x,yy,qf0x,212,color=C_BLACK)
breaker(qf0x,228,'QF0'); text(qf0x+44,232,'Гл. выключатель',fs=10,color="#444")
for k in range(3): line(qf0x,244,qf0x,266,color=C_BLACK)
sec_y=266
for k in range(3): line(qf0x,sec_y+k*8,1110,sec_y+k*8,color=C_BLACK,sw=2)

def branch_power(x,qf,vfd,motorlbl,subtitle):
    for k in range(3): line(x,sec_y+k*8,x,322,color=C_BLACK)
    breaker(x,340,qf)
    for k in range(3): line(x,356,x,388,color=C_BLACK)
    box(x-70,388,140,98,color=C_GREEN,fill="#f1fbf4",sw=2,rx=4)
    text(x,410,vfd,fs=13,anchor="middle",weight="bold",color=C_GREEN)
    text(x,428,subtitle,fs=10,anchor="middle",color="#333")
    text(x-64,450,'L1 L2 L3',fs=9,color="#555")
    text(x-64,470,'U   V   W',fs=9,color="#555")
    text(x+26,450,'STO',fs=9.5,color=C_RED,weight="bold")
    text(x+18,470,'+24 0В',fs=8.5,color="#555")
    for k in range(3): line(x-24+k*24,486,x-24+k*24,538,color=C_BLACK)
    motor(x,564,motorlbl)
    line(x,590,x,606,color=C_GREEN); text(x+8,604,'PE',fs=9,color=C_GREEN)
    return x

bx1=branch_power(420,'QF1','UZ1','M1','ПЧ подъёма')
bx2=branch_power(720,'QF2','UZ2','M2','ПЧ вил')

# Энкодеры
for bx,br in [(bx1,'BR1'),(bx2,'BR2')]:
    box(bx+74,428,54,22,color=C_BLUE,fill="#eef4ff",sw=1,rx=3)
    text(bx+101,443,br,fs=10,anchor="middle",color=C_BLUE)
    line(bx+70,439,bx+74,439,color=C_BLUE)

# Тормозной резистор R1 на UZ1
box(bx1-150,388,54,40,color=C_BLACK,fill="#fff",sw=1.5,rx=3)
text(bx1-123,409,'R1',fs=11,anchor="middle",weight="bold"); text(bx1-123,423,'торм.',fs=8,anchor="middle")
line(bx1-96,400,bx1-70,400,color=C_BLACK); line(bx1-96,416,bx1-70,416,color=C_BLACK)
text(bx1-150,382,'Тормозной резистор',fs=8.5,color="#555")

# Тормоз YB1 + выпрямитель UR1 + контактор KM1
box(bx1-70,628,140,38,color=C_BLACK,fill="#f6f6f6",sw=1.5,rx=3)
text(bx1,652,'YB1 — тормоз',fs=11,anchor="middle",weight="bold")
line(bx1,606,bx1,628,color=C_BLACK)
box(560,628,58,30,color=C_BLACK,fill="#fff",sw=1.5,rx=3); text(589,648,'UR1',fs=10,anchor="middle",weight="bold")
text(560,622,'Выпрямитель',fs=8.5,color="#555")
box(660,628,54,30,color=C_RED,fill="#fff5f5",sw=1.5,rx=3); text(687,648,'KM1',fs=10,anchor="middle",weight="bold",color=C_RED)
text(660,622,'Контактор тормоза',fs=8.5,color="#555")
line(618,643,660,643,color=C_BLACK)
line(bx1+70,647,560,647,color=C_BLACK); line(560,647,560,658,color=C_BLACK)
# +24 к KM1/UR1
line(714,643,760,643,color=C_BLUE); text(766,647,'+24В',fs=9,color=C_BLUE)

# Источник 24В G1
g1x=1000
breaker(g1x,340,'QF3',poles=2)
line(1110,sec_y,g1x-12,sec_y,color=C_BLACK); line(g1x-12,sec_y,g1x-12,324,color=C_BLACK)
line(1110,sec_y+8,g1x+12,sec_y+8,color=C_BLUE); line(g1x+12,sec_y+8,g1x+12,324,color=C_BLUE)
box(g1x-62,388,124,60,color=C_BLUE,fill="#eef4ff",sw=2,rx=4)
text(g1x,412,'G1 — БП 24В',fs=12,anchor="middle",weight="bold",color=C_BLUE)
text(g1x,432,'~230В → 24В DC',fs=9.5,anchor="middle",color="#333")
line(g1x-22,448,g1x-22,500,color=C_BLUE); line(g1x+22,448,g1x+22,500,color=C_BLACK)
text(g1x-62,514,'+24В',fs=10,color=C_BLUE,weight="bold"); text(g1x+26,514,'0В',fs=10,weight="bold")
text(g1x,540,'Питание ПЛК, iR, HMI, KSR,',fs=9,anchor="middle",color="#555")
text(g1x,553,'датчиков, замков YL',fs=9,anchor="middle",color="#555")

# ============ ШИНА STO / РАЗМЫКАНИЕ ТОРМОЗА ============
bus_y=710
line(380,bus_y,1500,bus_y,color=C_RED,sw=2,dash="7 5")
text(384,bus_y-8,'Цепь STO / размыкание питания тормоза (защитные контакты KSR)',fs=10.5,color=C_RED,weight="bold")
# дропы вверх к STO ПЧ (в обход блока тормоза) и к KM1
sx1=bx1+92
line(bx1+40,484,sx1,484,color=C_RED,sw=1.6,dash="6 4")
add(f'<line x1="{sx1}" y1="{bus_y}" x2="{sx1}" y2="484" stroke="{C_RED}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ar)"/>')
line(bx2+30,486,bx2+30,bus_y,color=C_RED,sw=1.6,dash="6 4"); add(f'<line x1="{bx2+30}" y1="{bus_y}" x2="{bx2+30}" y2="490" stroke="{C_RED}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ar)"/>')
line(687,658,687,bus_y,color=C_RED,sw=1.6,dash="6 4"); add(f'<line x1="687" y1="{bus_y}" x2="687" y2="662" stroke="{C_RED}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ar)"/>')
text(sx1+5,500,'STO',fs=9,color=C_RED); text(bx2+36,505,'STO',fs=9,color=C_RED); text(693,672,'размыкание KM1',fs=8.5,color=C_RED)

# ============ ЦЕПИ БЕЗОПАСНОСТИ (справа) ============
PX=1240
box(PX,86,W-PX-30,640,color=C_RED,fill="#fffafa",sw=1.5,rx=6,dash="3 0")
text(PX+(W-PX-30)/2,110,'ЦЕПИ БЕЗОПАСНОСТИ (независимый аппаратный контур, PL d / SIL 2)',fs=13,anchor="middle",weight="bold",color=C_RED)

# KSR
ksr_x,ksr_y,ksr_w,ksr_h=PX+330,150,260,150
box(ksr_x,ksr_y,ksr_w,ksr_h,color=C_RED,fill="#fff1f1",sw=2.5,rx=4)
text(ksr_x+ksr_w/2,ksr_y+26,'KSR — реле безопасности',fs=13,anchor="middle",weight="bold",color=C_RED)
text(ksr_x+ksr_w/2,ksr_y+46,'2 канала, самоконтроль',fs=10,anchor="middle",color="#a33")
text(ksr_x+12,ksr_y+74,'A1/A2 — питание 24В (от G1)',fs=9.5,color="#555")
text(ksr_x+12,ksr_y+96,'Входы: S11/S12, S21/S22, S33/S34',fs=9.5,color="#333")
text(ksr_x+12,ksr_y+118,'Защитные выходы: 13-14, 23-24,',fs=9.5,color="#333")
text(ksr_x+12,ksr_y+136,'33-34, 41-42',fs=9.5,color="#333")
# питание (стрелка от G1 концептуально)
text(ksr_x+ksr_w-6,ksr_y+74,'⟵ 24В',fs=9.5,color=C_BLUE,anchor="end")

# Входы безопасности (слева в панели)
inx=PX+16
iy=ksr_y+6
inputs=[
    ('SF1','Аварийный стоп · 2×НЗ',C_RED),
    ('SQ1.1…SQ5.1','Концевики ворот · НЗ посл.',C_RED),
    ('SQ0 / SQ9','Перебег верх/низ · НЗ',C_RED),
    ('BL1…BL5','Лаз. сканеры · OSSD',C_GREEN),
]
for nm,desc,c in inputs:
    box(inx,iy,150,40,color=c,fill="#fff",sw=1.5,rx=3)
    text(inx+75,iy+18,nm,fs=10.5,anchor="middle",weight="bold",color=c)
    text(inx+75,iy+33,desc,fs=8.3,anchor="middle",color="#555")
    ty=min(iy+20, ksr_y+ksr_h-16)
    line(inx+150,iy+20,ksr_x,ty,color=c,sw=1.4)
    iy+=48
text(inx,ksr_y-8,'Входы (двухканально):',fs=10,weight="bold",color=C_RED)

# Выходы KSR
outy=ksr_y+ksr_h+34
text(ksr_x,outy-10,'Защитные выходы → исполнение:',fs=10.5,weight="bold",color=C_RED)
outs=['STO → UZ1 (привод подъёма)','STO → UZ2 (привод вил)','KM1 — размыкание питания тормоза YB1','Кат. остановки 1: торможение, затем STO','«Безопасно» → ПЛК A1 (диагностика)']
oy=outy
for s in outs:
    box(ksr_x-20,oy,ksr_w+40,28,color=C_RED,fill="#ffecec",sw=1.3,rx=3)
    text(ksr_x+ksr_w/2,oy+18,s,fs=9.8,anchor="middle",color=C_RED,weight="bold")
    oy+=34
# связь выходов к шине STO (одна линия вниз-влево)
line(ksr_x-20,oy-34+14,1500,oy-34+14,color=C_RED,sw=1.6,dash="6 4")
line(1500,oy-34+14,1500,bus_y,color=C_RED,sw=1.6,dash="6 4"); add(f'<line x1="1500" y1="{oy-34+14}" x2="1500" y2="{bus_y}" stroke="{C_RED}" stroke-width="1.6" stroke-dasharray="6 4"/>')

# ============ ПРИМЕЧАНИЯ ============
ly=760
box(60,ly,W-120,150,color=C_GREY,fill="#fafafa",sw=1.5,rx=4)
text(74,ly+24,'Примечания',fs=13,weight="bold")
notes=[
    '• QF0 — главный выключатель; QF1, QF2 — защита ПЧ; QF3 — защита источника 24В (G1). Номиналы и сечения — по расчёту токов и длин кабелей.',
    '• Тормоз YB1 удерживает груз при обесточивании; контур безопасности через контактор KM1 снимает питание тормоза одновременно со STO обоих ПЧ.',
    '• STO обоих ПЧ и размыкание тормоза происходят при: аварийном стопе (SF), открытии любых ворот (SQn.1), срабатывании сканера (BLn), перебеге (SQ0/SQ9).',
    '• Концевики ворот SQn.1 и сканеры BLn заводятся двухканально: в реле KSR (останов) и в модули iR/ПЛК (логика работы и индикация этажа на панелях).',
    '• Энкодеры BR1/BR2 подключаются к энкодерным картам ПЧ. Категория остановки (0/1) и класс реле KSR уточняются по оценке рисков (ISO 13849 / IEC 62061).',
    '• Замки ворот YL1…YL5 и индикация — от выходов модулей Weintek iR (см. схему подключения io-wiring-diagram.svg).',
]
for i,n in enumerate(notes):
    text(74,ly+46+i*16,n,fs=9.5,color="#234")

add('</svg>')
open('/home/user/Claidegithub/schema/power-safety-schematic.svg','w',encoding='utf-8').write('\n'.join(svg))
print('power-safety SVG written')
