# -*- coding: utf-8 -*-
"""Схема архитектуры АСУ ТП одноколонного штабелёра на базе Weintek.

Уровни:
  - операторский: вызывные панели этажей (Weintek cMT-iV5) + главная HMI (cMT3072X);
  - управляющий: контроллер Weintek cMT3072X (cMT-сервер + CODESYS);
  - полевой ввод-вывод: Weintek iR (EtherCAT / Modbus TCP);
  - приводной: 2× ПЧ (подъём, вилы) с энкодерами и тормозом;
  - безопасности: реле безопасности (PL d / SIL 2), независимый аппаратный контур.

Выход: asu-tp-architecture.svg
"""

W, H = 1860, 1240

C_BLACK = "#1a1a1a"
C_RED = "#d40000"
C_BLUE = "#0050c8"
C_GREEN = "#0a8f3c"
C_GREY = "#888"
C_ORANGE = "#e07000"
C_PURPLE = "#7a2bbf"

svg = []
def add(s): svg.append(s)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
add('<defs>'
    f'<marker id="a" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C_BLACK}"/></marker>'
    f'<marker id="ar" markerWidth="9" markerHeight="9" refX="4.5" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{C_RED}"/></marker>'
    '</defs>')

def box(x, y, w, h, color=C_BLACK, fill="#fff", sw=2, rx=6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{d}/>')

def line(x1, y1, x2, y2, color=C_BLACK, sw=2, dash=None, arrow=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{arrow})"' if arrow else ''
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{m}/>')

def text(x, y, s, color=C_BLACK, fs=13, anchor="start", weight="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>')

def dev(x, y, w, h, title, sub, color=C_BLUE, fill="#f3f7ff", titlefs=13):
    box(x, y, w, h, color=color, fill=fill)
    text(x + w/2, y + 22, title, color=color, fs=titlefs, anchor="middle", weight="bold")
    for i, s in enumerate(sub):
        text(x + w/2, y + 42 + i*15, s, color="#333", fs=10.5, anchor="middle")

# ---------- Заголовок ----------
text(W/2, 36, 'АСУ ТП одноколонного штабелёра на базе Weintek — структурная схема', fs=22, anchor="middle", weight="bold")
text(W/2, 58, 'Контроллер cMT (CODESYS) · клиент-серверные панели на этажах · удалённый ввод-вывод iR · ПЧ · независимый контур безопасности', fs=12.5, anchor="middle", color="#555")

# ============ УРОВЕНЬ 1: ОПЕРАТОРСКИЙ (панели этажей) ============
text(40, 100, 'Операторский уровень', fs=14, weight="bold", color=C_BLUE)
panel_y = 112
pw, phh, gap = 150, 64, 18
x0 = 250
for i, f in enumerate([1, 2, 3, 4, 5]):
    x = x0 + i*(pw+gap)
    dev(x, panel_y, pw, phh, f'PU{f} · этаж {f}', ['Weintek cMT-iV5', 'вызывная панель'], color=C_BLUE, titlefs=12)
# главная HMI
xh = x0 + 5*(pw+gap) + 14
dev(xh, panel_y, pw+10, phh, 'HMI0 (гл. пульт)', ['Weintek cMT3072X', 'зона загрузки'], color=C_BLUE, fill="#e9f0ff", titlefs=12)

# ============ Ethernet-шина ============
busy = panel_y + phh + 40
line(220, busy, W-60, busy, color=C_BLUE, sw=3)
text(232, busy - 8, 'Ethernet / PoE — клиент-серверная сеть cMT (MQTT/проект cMT)', fs=12, color=C_BLUE, weight="bold")
# стойки от панелей к шине
for i in range(5):
    x = x0 + i*(pw+gap) + pw/2
    line(x, panel_y + phh, x, busy, color=C_BLUE, sw=1.5)
line(xh + (pw+10)/2, panel_y + phh, xh + (pw+10)/2, busy, color=C_BLUE, sw=1.5)

# ============ УРОВЕНЬ 2: КОНТРОЛЛЕР ============
text(40, busy + 46, 'Управляющий уровень', fs=14, weight="bold", color=C_BLUE)
ctrl_x, ctrl_y, ctrl_w, ctrl_h = 250, busy + 56, 360, 96
box(ctrl_x, ctrl_y, ctrl_w, ctrl_h, color=C_BLUE, fill="#e9f0ff", sw=2.5)
text(ctrl_x + ctrl_w/2, ctrl_y + 24, 'A1 — Контроллер Weintek cMT3072X', fs=14, anchor="middle", weight="bold", color=C_BLUE)
text(ctrl_x + ctrl_w/2, ctrl_y + 44, 'cMT-сервер + среда исполнения CODESYS', fs=11, anchor="middle", color="#333")
text(ctrl_x + ctrl_w/2, ctrl_y + 60, 'Логика вызовов, маршрутов, блокировок,', fs=10.5, anchor="middle", color="#333")
text(ctrl_x + ctrl_w/2, ctrl_y + 75, 'позиционирования и индикации', fs=10.5, anchor="middle", color="#333")
line(ctrl_x + ctrl_w/2, busy, ctrl_x + ctrl_w/2, ctrl_y, color=C_BLUE, sw=2)

# Управляющий ПК/SCADA (опционально) справа
box(ctrl_x + ctrl_w + 60, ctrl_y + 10, 200, 76, color=C_GREY, fill="#fafafa", sw=1.5, dash="5 4")
text(ctrl_x + ctrl_w + 160, ctrl_y + 32, 'АРМ / журнал (опц.)', fs=12, anchor="middle", weight="bold", color=C_GREY)
text(ctrl_x + ctrl_w + 160, ctrl_y + 50, 'cMT — EasyAccess 2.0,', fs=10.5, anchor="middle", color="#555")
text(ctrl_x + ctrl_w + 160, ctrl_y + 64, 'OPC UA / БД, удал. доступ', fs=10.5, anchor="middle", color="#555")
line(ctrl_x + ctrl_w, ctrl_y + 48, ctrl_x + ctrl_w + 60, ctrl_y + 48, color=C_GREY, sw=1.5, dash="5 4")

# ============ Полевая шина от контроллера ============
fb_y = ctrl_y + ctrl_h + 34
line(220, fb_y, W-60, fb_y, color=C_PURPLE, sw=3)
text(232, fb_y - 8, 'Полевая шина EtherCAT / Modbus TCP (ввод-вывод и приводы)', fs=12, color=C_PURPLE, weight="bold")
line(ctrl_x + ctrl_w/2, ctrl_y + ctrl_h, ctrl_x + ctrl_w/2, fb_y, color=C_PURPLE, sw=2)

# ============ УРОВЕНЬ 3: ПЧ и УДАЛЁННЫЙ ВВОД-ВЫВОД ============
lvl3_y = fb_y + 40
# ПЧ подъёма
uz1x = 250
dev(uz1x, lvl3_y, 200, 86, 'UZ1 — ПЧ подъёма', ['Векторный ПЧ + энкодер. карта', 'STO, торм. резистор', 'управление M1, тормоз YB1'], color=C_GREEN, fill="#f0fbf3", titlefs=12)
line(uz1x+100, fb_y, uz1x+100, lvl3_y, color=C_PURPLE, sw=1.5)
# ПЧ вил
uz2x = 250 + 230
dev(uz2x, lvl3_y, 200, 86, 'UZ2 — ПЧ вил', ['Векторный ПЧ + энкодер. карта', 'STO', 'управление M2'], color=C_GREEN, fill="#f0fbf3", titlefs=12)
line(uz2x+100, fb_y, uz2x+100, lvl3_y, color=C_PURPLE, sw=1.5)
# Удалённый ввод-вывод
iox = 250 + 2*230
iow = 470
box(iox, lvl3_y, iow, 86, color=C_PURPLE, fill="#f7f0fb", sw=2)
text(iox + iow/2, lvl3_y + 20, 'Удалённый ввод-вывод Weintek iR', fs=13, anchor="middle", weight="bold", color=C_PURPLE)
text(iox + 14, lvl3_y + 40, 'iR-ETN40R — шинный соединитель (EtherCAT/Modbus TCP)', fs=10.5, color="#333")
text(iox + 14, lvl3_y + 56, 'iR-DI16-K ×N — дискретные входы (датчики)', fs=10.5, color="#333")
text(iox + 14, lvl3_y + 72, 'iR-DO16-P ×N — дискретные выходы (замки, индикация)', fs=10.5, color="#333")
line(iox + iow/2, fb_y, iox + iow/2, lvl3_y, color=C_PURPLE, sw=1.5)

# ============ УРОВЕНЬ 4: ПОЛЕВЫЕ УСТРОЙСТВА ============
fld_y = lvl3_y + 130
text(40, fld_y - 14, 'Полевые устройства', fs=13, weight="bold", color=C_GREY)
# под UZ1
dev(uz1x, fld_y, 200, 64, 'M1 + YB1 + BR1', ['двигатель подъёма,', 'тормоз, энкодер'], color=C_BLACK, fill="#f6f6f6", titlefs=12)
line(uz1x+100, lvl3_y+86, uz1x+100, fld_y, color=C_BLACK, sw=1.5, arrow='a')
# под UZ2
dev(uz2x, fld_y, 200, 64, 'M2 + BR2', ['двигатель вил,', 'энкодер'], color=C_BLACK, fill="#f6f6f6", titlefs=12)
line(uz2x+100, lvl3_y+86, uz2x+100, fld_y, color=C_BLACK, sw=1.5, arrow='a')
# под iR — группы датчиков/исполнительных
gx = iox
groups = [
    ('Входы (DI)', [
        'SQna/b/c ×5 — датчики этажей',
        'SQ8.1…8.3 — положение вил',
        'BG0 — паллета на вилах',
        'BG1…5 — занятость мест',
        'SQ1.1…5.1 — закрытие ворот',
    ], C_BLACK),
    ('Выходы (DO)', [
        'YL1…YL5 — замки ворот',
        'Лампы/звук «занято»,',
        '«ворота открыты эт.N»',
        'Разрешение/индикация',
        'на панелях PU1…PU5',
    ], C_RED),
]
gw = (iow - 16) / 2
for j, (gt, items, gc) in enumerate(groups):
    bx = gx + j*(gw+16)
    box(bx, fld_y, gw, 110, color=gc, fill="#fff", sw=1.5)
    text(bx + gw/2, fld_y + 18, gt, fs=12, anchor="middle", weight="bold", color=gc)
    for k, it in enumerate(items):
        text(bx + 10, fld_y + 36 + k*15, it, fs=9.5, color="#333")
    line(bx + gw/2, lvl3_y+86, bx + gw/2, fld_y, color=C_PURPLE, sw=1.2, arrow='a')

# ============ КОНТУР БЕЗОПАСНОСТИ (независимый, справа) ============
sx, sy, sw_, sh = 1480, ctrl_y + 10, 330, 470
box(sx, sy, sw_, sh, color=C_RED, fill="#fff6f6", sw=2.5, dash="2 0")
text(sx + sw_/2, sy + 26, 'Контур безопасности (независимый)', fs=13, anchor="middle", weight="bold", color=C_RED)
text(sx + sw_/2, sy + 44, 'PL d / SIL 2 — аппаратный, не через ПЛК', fs=10.5, anchor="middle", color="#a33")
# реле безопасности
box(sx + 60, sy + 60, sw_-120, 56, color=C_RED, fill="#ffecec", sw=2)
text(sx + sw_/2, sy + 82, 'KSR — реле безопасности', fs=12, anchor="middle", weight="bold", color=C_RED)
text(sx + sw_/2, sy + 100, '(2-канальное, с самоконтролем)', fs=10, anchor="middle", color="#a33")
# входы безопасности
sin = [
    'SF1…SFn — кнопки «Авар. стоп»',
    'SQ1.1…SQ5.1 — концевики ворот (защ.)',
    'BL1…BL5 — лазерные сканеры (защ.)',
    'SQ0 / SQ9 — перебег по высоте',
]
text(sx + 20, sy + 142, 'Входы:', fs=11, weight="bold", color=C_RED)
for k, s in enumerate(sin):
    text(sx + 20, sy + 162 + k*17, '• ' + s, fs=10, color="#333")
    line(sx + 20, sy + 158 + k*17, sx + 16, sy + 158 + k*17, color=C_RED, sw=1)
# выходы безопасности
sout = [
    'STO → UZ1 и UZ2 (снятие момента)',
    'Размыкание питания тормоза YB1',
    'Сигнал «Безопасно» → контроллер A1',
]
text(sx + 20, sy + 250, 'Выходы:', fs=11, weight="bold", color=C_RED)
for k, s in enumerate(sout):
    text(sx + 20, sy + 270 + k*17, '• ' + s, fs=10, color="#333")
# связи безопасности к ПЧ (STO): горизонтальная цепь над уровнем приводов
sto_y = lvl3_y - 14
line(sx, sto_y, 360, sto_y, color=C_RED, sw=1.8, dash="6 4")
line(sx, sy + 296, sx, sto_y, color=C_RED, sw=1.8, dash="6 4")
line(uz1x + 60, sto_y, uz1x + 60, lvl3_y, color=C_RED, sw=1.8, dash="6 4", arrow='ar')
line(uz2x + 60, sto_y, uz2x + 60, lvl3_y, color=C_RED, sw=1.8, dash="6 4", arrow='ar')
text(uz2x + 66, sto_y - 4, 'STO → оба ПЧ + тормоз YB1', fs=9.5, color=C_RED)

# ============ ЛЕГЕНДА ЛИНИЙ ============
lx, ly = 40, H - 150
box(lx, ly, 560, 120, color=C_GREY, fill="#fafafa", sw=1.5)
text(lx + 14, ly + 24, 'Обозначения связей', fs=13, weight="bold")
items = [
    ('Ethernet / PoE (панели ↔ cMT-сервер)', C_BLUE, None),
    ('EtherCAT / Modbus TCP (ввод-вывод, приводы)', C_PURPLE, None),
    ('Дискретные сигналы 24 В (DI/DO к полю)', C_BLACK, None),
    ('Цепи безопасности (аппаратные, STO/тормоз)', C_RED, '6 4'),
]
for i, (t, c, dsh) in enumerate(items):
    yy = ly + 46 + i*18
    line(lx + 16, yy - 4, lx + 60, yy - 4, color=c, sw=2.5, dash=dsh)
    text(lx + 70, yy, t, fs=11)

# ============ ПРИМЕЧАНИЯ ============
nx, ny = 640, H - 150
box(nx, ny, W - nx - 40, 120, color=C_GREEN, fill="#f4fbf6", sw=1.5)
text(nx + 14, ny + 24, 'Ключевые функции АСУ ТП (по логике работы)', fs=13, weight="bold", color=C_GREEN)
notes = [
    '1. Вызов с панели любого этажа: контроллер фиксирует этаж-источник и этаж-назначения, строит маршрут.',
    '2. Забор паллеты с места погрузки источника (по BGn), доставка на этаж назначения.',
    '3. Если место выгрузки занято (BGn=1) — паллета НЕ выгружается, штабелёр только доезжает до этажа и сигналит.',
    '4. При открытии ворот на ЛЮБОМ этаже (SQn.1) — немедленный СТОП; на ВСЕХ панелях индикация «открыты ворота эт. N».',
    '5. Контур безопасности (аварийный стоп, ворота, сканеры, перебег) — аппаратный, со снятием момента и тормозом.',
]
for i, n in enumerate(notes):
    text(nx + 14, ny + 44 + i*15, n, fs=10, color="#234")

add('</svg>')
with open('/home/user/Claidegithub/schema/asu-tp-architecture.svg', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(svg))
print('ASU TP SVG written')
