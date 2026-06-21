# -*- coding: utf-8 -*-
"""Схема подключения удалённого ввода-вывода Weintek iR с адресацией клемм.

Состав: соединитель iR-ETN40R + 2× iR-DI16-K (входы) + 1× iR-DO16-P (выходы).
Адреса приведены в стиле CODESYS (%IX/%QX) и являются ориентировочными —
уточняются при конфигурировании проекта.

Выход: io-wiring-diagram.svg
"""

W, H = 1720, 1180
C_BLACK="#1a1a1a"; C_RED="#d40000"; C_BLUE="#0050c8"; C_GREEN="#0a8f3c"
C_GREY="#888"; C_ORANGE="#e07000"; C_PURPLE="#7a2bbf"

svg=[]
def add(s): svg.append(s)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="DejaVu Sans, Arial, sans-serif">')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')
def box(x,y,w,h,color=C_BLACK,fill="#fff",sw=1.5,rx=0):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,color=C_BLACK,sw=1.5,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')
def text(x,y,s,color=C_BLACK,fs=11,anchor="start",weight="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>')

# ---- Заголовок ----
text(W/2,34,'Схема подключения удалённого ввода-вывода Weintek iR — адресация клемм',fs=21,anchor="middle",weight="bold")
text(W/2,56,'iR-ETN40R (шинный соединитель) + 2× iR-DI16-K (входы) + iR-DO16-P (выходы) · EtherCAT / Modbus TCP',fs=12.5,anchor="middle",color="#555")

# ---- Соединитель + питание + шина ----
box(60,80,300,84,color=C_PURPLE,fill="#f7f0fb",sw=2,rx=5)
text(210,104,'iR-ETN40R',fs=15,anchor="middle",weight="bold",color=C_PURPLE)
text(210,124,'Шинный соединитель',fs=10.5,anchor="middle",color="#333")
text(210,140,'EtherCAT / Modbus TCP → контроллер cMT',fs=9.5,anchor="middle",color="#333")
text(210,156,'Питание шины/логики 24В DC (от G1)',fs=9.5,anchor="middle",color="#555")
# линия EtherCAT к контроллеру
line(360,100,470,100,color=C_PURPLE,sw=2)
box(470,82,150,40,color=C_BLUE,fill="#eef4ff",sw=1.5,rx=4)
text(545,100,'Контроллер',fs=11,anchor="middle",weight="bold",color=C_BLUE)
text(545,114,'Weintek cMT3072X',fs=9,anchor="middle",color="#333")
# питание 24В
box(660,82,150,40,color=C_BLUE,fill="#eef4ff",sw=1.5,rx=4)
text(735,100,'G1 — БП 24В',fs=11,anchor="middle",weight="bold",color=C_BLUE)
text(735,114,'+24В / 0В',fs=9.5,anchor="middle",color="#333")
line(620,100,660,100,color=C_BLUE,sw=2)
# шина модулей
line(210,164,210,196,color=C_PURPLE,sw=2)
line(110,196,1660,196,color=C_PURPLE,sw=2.5)
text(120,190,'Локальная шина iR (модули пристыковываются к соединителю)',fs=10,color=C_PURPLE)

# ---- Хелпер таблицы модуля ----
def module(x,y,w,title,sub,headcol,rows):
    rowh=27; n=len(rows)
    th=n*rowh
    # шапка
    box(x,y,w,46,color=headcol,fill="#fff",sw=2,rx=4)
    text(x+w/2,y+20,title,fs=13,anchor="middle",weight="bold",color=headcol)
    text(x+w/2,y+37,sub,fs=9.5,anchor="middle",color="#444")
    line(x+w/2,196,x+w/2,y,color=C_PURPLE,sw=1.5)
    # столбцы
    cx=[x+6, x+58, x+150, x+250]
    hdr=['Клемма','Адрес','Сигнал','Описание']
    box(x,y+46,w,22,color=headcol,fill="#f4f4f4",sw=1)
    for i,h in enumerate(hdr): text(cx[i],y+61,h,fs=9.5,weight="bold",color="#333")
    ty=y+68
    for (term,addr,sig,desc,col) in rows:
        box(x,ty,w,rowh,color="#ccc",fill="#fff",sw=0.7)
        text(cx[0],ty+17,term,fs=9.5)
        text(cx[1],ty+17,addr,fs=9,color=C_PURPLE)
        text(cx[2],ty+17,sig,fs=9.5,weight="bold",color=col)
        text(cx[3],ty+17,desc,fs=9,color="#333")
        ty+=rowh
    return th+90

# ====== DI модуль 1 ======
di1=[
 ('X1:0','%IX0.0','SQ1a','Этаж 1 — остановка A',C_BLACK),
 ('X1:1','%IX0.1','SQ1b','Этаж 1 — остановка B',C_BLACK),
 ('X1:2','%IX0.2','SQ1c','Этаж 1 — перебег',C_GREEN),
 ('X1:3','%IX0.3','SQ2a','Этаж 2 — остановка A',C_BLACK),
 ('X1:4','%IX0.4','SQ2b','Этаж 2 — остановка B',C_BLACK),
 ('X1:5','%IX0.5','SQ2c','Этаж 2 — перебег',C_GREEN),
 ('X1:6','%IX0.6','SQ3a','Этаж 3 — остановка A',C_BLACK),
 ('X1:7','%IX0.7','SQ3b','Этаж 3 — остановка B',C_BLACK),
 ('X1:8','%IX1.0','SQ3c','Этаж 3 — перебег',C_GREEN),
 ('X1:9','%IX1.1','SQ4a','Этаж 4 — остановка A',C_BLACK),
 ('X1:10','%IX1.2','SQ4b','Этаж 4 — остановка B',C_BLACK),
 ('X1:11','%IX1.3','SQ4c','Этаж 4 — перебег',C_GREEN),
 ('X1:12','%IX1.4','SQ5a','Этаж 5 — остановка A',C_BLACK),
 ('X1:13','%IX1.5','SQ5b','Этаж 5 — остановка B',C_BLACK),
 ('X1:14','%IX1.6','SQ5c','Этаж 5 — перебег',C_GREEN),
 ('X1:15','%IX1.7','SQ8.1','Вилы убраны',C_BLACK),
]
# ====== DI модуль 2 ======
di2=[
 ('X2:0','%IX2.0','SQ8.2','Вилы выдвинуты влево',C_BLACK),
 ('X2:1','%IX2.1','SQ8.3','Вилы выдвинуты вправо',C_BLACK),
 ('X2:2','%IX2.2','BG0','Паллета на вилах',C_ORANGE),
 ('X2:3','%IX2.3','BG1','Занятость места — эт.1',C_ORANGE),
 ('X2:4','%IX2.4','BG2','Занятость места — эт.2',C_ORANGE),
 ('X2:5','%IX2.5','BG3','Занятость места — эт.3',C_ORANGE),
 ('X2:6','%IX2.6','BG4','Занятость места — эт.4',C_ORANGE),
 ('X2:7','%IX2.7','BG5','Занятость места — эт.5',C_ORANGE),
 ('X2:8','%IX3.0','SQ1.1','Ворота эт.1 закрыты',C_RED),
 ('X2:9','%IX3.1','SQ2.1','Ворота эт.2 закрыты',C_RED),
 ('X2:10','%IX3.2','SQ3.1','Ворота эт.3 закрыты',C_RED),
 ('X2:11','%IX3.3','SQ4.1','Ворота эт.4 закрыты',C_RED),
 ('X2:12','%IX3.4','SQ5.1','Ворота эт.5 закрыты',C_RED),
 ('X2:13','%IX3.5','KSR_OK','«Безопасно» от реле KSR',C_RED),
 ('X2:14','%IX3.6','—','Резерв',C_GREY),
 ('X2:15','%IX3.7','—','Резерв',C_GREY),
]
# ====== DO модуль ======
do=[
 ('Y1:0','%QX0.0','YL1','Замок ворот эт.1',C_RED),
 ('Y1:1','%QX0.1','YL2','Замок ворот эт.2',C_RED),
 ('Y1:2','%QX0.2','YL3','Замок ворот эт.3',C_RED),
 ('Y1:3','%QX0.3','YL4','Замок ворот эт.4',C_RED),
 ('Y1:4','%QX0.4','YL5','Замок ворот эт.5',C_RED),
 ('Y1:5','%QX0.5','HL1','Лампа «штабелёр в работе»',C_BLUE),
 ('Y1:6','%QX0.6','HL2','Лампа/сирена «Авария»',C_BLUE),
 ('Y1:7','%QX0.7','HL3','Лампа «Место занято»',C_BLUE),
 ('Y1:8','%QX1.0','HA1','Звуковой сигнал движения',C_BLUE),
 ('Y1:9','%QX1.1','KM2','Разрешение/готовность ПЧ',C_GREEN),
 ('Y1:10','%QX1.2','—','Резерв',C_GREY),
 ('Y1:11','%QX1.3','—','Резерв',C_GREY),
 ('Y1:12','%QX1.4','—','Резерв',C_GREY),
 ('Y1:13','%QX1.5','—','Резерв',C_GREY),
 ('Y1:14','%QX1.6','—','Резерв',C_GREY),
 ('Y1:15','%QX1.7','—','Резерв',C_GREY),
]

module(60,  220, 500, 'iR-DI16-K (модуль входов №1)','16 дискретных входов 24В DC', C_BLACK, di1)
module(600, 220, 500, 'iR-DI16-K (модуль входов №2)','16 дискретных входов 24В DC', C_BLACK, di2)
module(1140,220, 500, 'iR-DO16-P (модуль выходов)','16 дискретных выходов 24В DC', C_RED, do)

# ---- Примечания ----
ly=H-156
box(60,ly,W-120,128,color=C_GREY,fill="#fafafa",sw=1.5,rx=4)
text(74,ly+24,'Примечания по подключению',fs=13,weight="bold")
notes=[
 '• Адреса %IX / %QX — ориентировочные (CODESYS на cMT3072X); фактическое отображение задаётся при конфигурировании iR-ETN. Для Modbus TCP — соответствующие',
 '  дискретные входы (1xxxx) и катушки (0xxxx).',
 '• Датчики — 3-проводные PNP (24В, 0В, сигнал); общий «минус» и питание датчиков — от шины 24В источника G1; экраны кабелей — на PE.',
 '• Защитные сигналы (SQn.1 ворота, BLn сканеры, SQ0/SQ9 перебег, SF аварийный стоп) дублируются в реле безопасности KSR (см. power-safety-schematic.svg);',
 '  в модули iR заводится диагностический «информационный» канал для логики и индикации этажа на панелях.',
 '• Энкодеры BR1/BR2 подключаются к энкодерным картам ПЧ UZ1/UZ2 и читаются контроллером по полевой шине (не через дискретные модули iR).',
 '• Замки YL1…YL5 — индуктивная нагрузка: применять выходы с защитой или внешние диоды/варисторы. При необходимости — промежуточные реле.',
]
for i,n in enumerate(notes):
    text(74,ly+44+i*14,n,fs=9,color="#234")

add('</svg>')
open('/home/user/Claidegithub/schema/io-wiring-diagram.svg','w',encoding='utf-8').write('\n'.join(svg))
print('io-wiring SVG written')
