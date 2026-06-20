# -*- coding: utf-8 -*-
"""Генератор детализированной функциональной схемы одноколонного штабелёра
(межэтажного подъёмника) для производственного здания.

Назначение: перемещение паллет 1000x1200 мм, грузоподъёмность до 2000 кг,
между 5 этажами. Конструкция одноколонная — грузовая каретка с
телескопическими вилами движется по единственной мачте (подъём/опускание)
и выдвигает вилы к посту погрузки/выгрузки на нужном этаже.

На каждом этаже: вызывная панель, ворота (с датчиком закрытия и замком),
место погрузки/выгрузки с датчиком занятости, лазерный сканер безопасности.

Выход: stacker-schema-detailed.svg
"""

W, H = 2020, 1320
MARGIN = 24
LEVELS = [5, 4, 3, 2, 1]
FY = {5: 250, 4: 405, 3: 560, 2: 715, 1: 870}   # y-центр этажа

MAST_X = 815
MAST_W = 34
LSENS_X = 715           # датчики этажа слева от мачты
CELL_X0 = 1150          # место погрузки/выгрузки
CELL_X1 = 1340
GATE_X = 1400           # элементы ворот (датчик/замок/лазер)
PANEL_X = 1560          # вызывная панель этажа

C_BLACK = "#1a1a1a"
C_RED = "#d40000"
C_BLUE = "#0050c8"
C_GREEN = "#0a8f3c"
C_GREY = "#888"
C_ORANGE = "#e07000"

svg = []
def add(s): svg.append(s)

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="DejaVu Sans, Arial, sans-serif">')
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
add(f'<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="5" refY="5" '
    f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C_BLACK}"/></marker></defs>')


def circle(cx, cy, txt, color=C_BLACK, r=20, fs=13, fill="#fff"):
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{color}" stroke-width="2"/>')
    add(f'<text x="{cx}" y="{cy+fs*0.35:.0f}" font-size="{fs}" text-anchor="middle" '
        f'fill="{color}" font-weight="bold">{txt}</text>')

def box(x, y, w, h, color=C_BLACK, fill="#fff", sw=2, rx=0):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{color}" stroke-width="{sw}"/>')

def line(x1, y1, x2, y2, color=C_BLACK, sw=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')

def text(x, y, s, color=C_BLACK, fs=13, anchor="start", weight="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" '
        f'font-weight="{weight}">{s}</text>')


# ---------- Заголовок ----------
text(W/2, 38, 'Одноколонный штабелёр (межэтажный подъёмник) — функциональная схема',
     fs=22, anchor="middle", weight="bold")
text(W/2, 60, 'Паллеты 1000×1200 мм · грузоподъёмность 2000 кг · 5 этажей · одна колонна (без горизонт. перемещения)',
     fs=13, anchor="middle", color="#555")

# ---------- Мачта ----------
mast_top, mast_bot = 120, 1005
box(MAST_X - MAST_W/2, mast_top, MAST_W, mast_bot - mast_top, color=C_BLACK, fill="#f3f3f3")
text(MAST_X, mast_bot + 18, 'Мачта (колонна)', fs=11, anchor="middle", color=C_GREY)

for f in LEVELS:
    y = FY[f]
    line(470, y, GATE_X + 110, y, color=C_GREY, sw=1, dash="8 6")
    text(455, y - 6, f'{f} этаж', fs=14, anchor="end", weight="bold")

# ================= ПРИВОД ПОДЪЁМА =================
ly = 150
line(MAST_X, mast_top, MAST_X, ly, color=C_BLACK, sw=2)
line(MAST_X, ly, 875, ly)
circle(900, ly, 'M1', r=21)
line(921, ly, 955, ly)
circle(980, ly, 'BR1', color=C_GREEN, r=21, fs=12)
line(1001, ly, 1035, ly)
circle(1060, ly, 'YB1', r=21, fs=12)
line(1130, 118, 1130, 200, color=C_BLACK, sw=2)
add(f'<line x1="1130" y1="118" x2="1130" y2="126" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
add(f'<line x1="1130" y1="200" x2="1130" y2="192" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
text(1150, 132, 'Подъём-опускание грузовой каретки', fs=14, weight="bold")
text(1150, 152, 'M1 — двигатель привода подъёма (через ПЧ UZ1)', fs=12, color="#444")
text(1150, 169, 'BR1 — энкодер (положение/скорость каретки)', fs=12, color=C_GREEN)
text(1150, 186, 'YB1 — тормоз электромагнитный (удержание груза)', fs=12, color="#444")
circle(MAST_X, mast_top + 8, 'SQ0', color=C_GREEN, r=15, fs=10)
text(MAST_X + 22, mast_top + 12, 'SQ0 — концевой выкл. «верх» (перебег)', fs=10, color=C_GREEN)
circle(MAST_X, mast_bot - 8, 'SQ9', color=C_GREEN, r=15, fs=10)
text(MAST_X + 22, mast_bot - 4, 'SQ9 — концевой выкл. «низ» (перебег)', fs=10, color=C_GREEN)

# ================= КАРЕТКА + ТЕЛЕСКОПИЧЕСКИЕ ВИЛЫ (показана в середине мачты) =================
cy = (FY[4] + FY[3]) // 2
text(MAST_X, cy - 50, 'Выдвижение телескопических вил (захват паллеты)', fs=12, anchor="middle", weight="bold")
line(MAST_X - 60, cy - 40, MAST_X + 60, cy - 40, color=C_BLACK, sw=2)
add(f'<line x1="{MAST_X-60}" y1="{cy-40}" x2="{MAST_X-52}" y2="{cy-40}" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
add(f'<line x1="{MAST_X+60}" y1="{cy-40}" x2="{MAST_X+52}" y2="{cy-40}" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
box(MAST_X - 95, cy - 26, 190, 52, color=C_BLACK, fill="#eef")
circle(MAST_X - 34, cy, 'M2', r=19)
circle(MAST_X + 36, cy, 'BR2', color=C_GREEN, r=18, fs=11)
# вилы влево (с паллетой) и вправо
line(MAST_X - 95, cy, MAST_X - 175, cy, color=C_BLACK)
add(f'<polygon points="{MAST_X-175},{cy-9} {MAST_X-215},{cy-9} {MAST_X-215},{cy+9} {MAST_X-175},{cy+9}" fill="none" stroke="{C_BLACK}" stroke-width="2"/>')
line(MAST_X + 95, cy, MAST_X + 120, cy, color=C_BLACK)
add(f'<polygon points="{MAST_X+120},{cy-9} {MAST_X+150},{cy-9} {MAST_X+150},{cy+9} {MAST_X+120},{cy+9}" fill="none" stroke="{C_BLACK}" stroke-width="2"/>')
text(MAST_X - 215, cy - 14, 'паллета', fs=8, color=C_GREY)
# датчики положения вил на каретке + датчик паллеты на вилах
circle(MAST_X - 55, cy + 48, 'SQ8.1', r=17, fs=9)
circle(MAST_X, cy + 48, 'SQ8.2', r=17, fs=9)
circle(MAST_X + 55, cy + 48, 'SQ8.3', r=17, fs=9)
circle(MAST_X - 150, cy, 'BG0', color=C_ORANGE, r=16, fs=10)
line(MAST_X - 134, cy, MAST_X - 95, cy, color=C_ORANGE, sw=1)
# описание блока каретки (справа от мачты, в свободной зоне)
tx = MAST_X + 175
text(tx, cy - 26, 'Грузовая каретка (вся высота мачты):', fs=11, weight="bold")
text(tx, cy - 9, 'M2 — привод вил, BR2 — энкодер (ПЧ UZ2)', fs=11)
text(tx, cy + 8, 'SQ8.1…8.3 — положение вил', fs=11)
text(tx, cy + 25, 'BG0 — наличие паллеты на вилах', fs=11, color=C_ORANGE)

# ================= ДАТЧИКИ ЭТАЖА (слева от мачты) =================
for f in LEVELS:
    y = FY[f]
    line(MAST_X - MAST_W/2, y, LSENS_X + 18, y, color=C_BLACK)
    circle(LSENS_X, y, f'SQ{f}a', r=16, fs=10)
    circle(LSENS_X - 38, y, f'SQ{f}b', r=16, fs=10)
    circle(LSENS_X - 19, y - 30, f'SQ{f}c', color=C_GREEN, r=15, fs=9)
    line(LSENS_X - 19, y - 15, LSENS_X - 19, y, color=C_BLACK, sw=1)
# пояснение датчиков этажа — компактный блок в свободной зоне сверху слева
ex, ey = 462, 250
box(ex, ey - 70, 190, 92, color=C_GREY, fill="#fbfbfb", sw=1, rx=4)
text(ex + 10, ey - 50, 'Датчики этажа (слева):', fs=10.5, weight="bold")
text(ex + 10, ey - 32, 'SQna, SQnb —', fs=10.5)
text(ex + 10, ey - 18, 'сдвоенный (остановка)', fs=10.5)
text(ex + 10, ey - 2, 'SQnc — перебег', fs=10.5, color=C_GREEN)

# ================= ПОСТ ПОГРУЗКИ/ВЫГРУЗКИ + ВОРОТА + ПАНЕЛЬ (справа) =================
for f in LEVELS:
    y = FY[f]
    cy0, cy1 = y - 42, y + 42
    # ворота этажа (красные стойки)
    line(CELL_X0, cy0, CELL_X0, cy1, color=C_RED, sw=4)
    line(CELL_X1, cy0, CELL_X1, cy1, color=C_RED, sw=4)
    # площадка места погрузки/выгрузки
    box(CELL_X0 + 8, cy0 + 6, CELL_X1 - CELL_X0 - 16, cy1 - cy0 - 12, color=C_RED, sw=1.5)
    for gx in range(1, 6):
        xx = CELL_X0 + 8 + gx * (CELL_X1 - CELL_X0 - 16) / 6
        line(xx, cy0 + 6, xx, cy1 - 6, color=C_RED, sw=1)
    for gy2 in range(1, 4):
        yy2 = cy0 + 6 + gy2 * (cy1 - cy0 - 12) / 4
        line(CELL_X0 + 8, yy2, CELL_X1 - 8, yy2, color=C_RED, sw=1)
    text((CELL_X0 + CELL_X1) / 2, cy0 - 4, f'Место погр./выгр. {f} эт.', fs=9.5, anchor="middle", color=C_RED)
    # датчик занятости места
    circle(CELL_X0 - 26, y, f'BG{f}', color=C_ORANGE, r=16, fs=10)
    line(CELL_X0 - 10, y, CELL_X0, y, color=C_ORANGE, sw=1)
    # элементы ворот
    line(CELL_X1, y - 25, GATE_X - 18, y - 25, color=C_RED)
    circle(GATE_X, y - 25, f'SQ{f}.1', color=C_RED, r=15, fs=9)
    line(CELL_X1, y, GATE_X - 18, y, color=C_RED)
    circle(GATE_X, y, f'YL{f}', color=C_RED, r=15, fs=10)
    line(CELL_X1, y + 25, GATE_X - 18, y + 25, color=C_GREEN)
    circle(GATE_X, y + 25, f'BL{f}', color=C_GREEN, r=15, fs=10)
    # вызывная панель этажа
    box(PANEL_X, y - 20, 64, 40, color=C_BLUE, fill="#eef4ff", rx=4)
    text(PANEL_X + 32, y + 4, f'PU{f}', color=C_BLUE, fs=13, anchor="middle", weight="bold")

# легенда правого блока (в правом верхнем углу, выше панелей)
rx, ry = 1500, 70
box(rx, ry, 380, 154, color=C_GREY, fill="#fbfbfb", sw=1, rx=4)
text(rx + 10, ry + 20, 'Пост этажа (на каждом из 5 этажей):', fs=11, weight="bold")
text(rx + 10, ry + 38, 'BGn — датчик занятости места погр./выгр.', fs=10.5, color=C_ORANGE)
text(rx + 10, ry + 54, 'SQn.1 — датчик закрытия ворот этажа', fs=10.5, color=C_RED)
text(rx + 10, ry + 70, 'YLn — электромагнитный замок ворот', fs=10.5, color=C_RED)
text(rx + 10, ry + 86, 'BLn — лазерный сканер безопасности проёма', fs=10.5, color=C_GREEN)
text(rx + 10, ry + 104, 'PUn — вызывная панель этажа (Weintek)', fs=10.5, color=C_BLUE)
text(rx + 10, ry + 122, 'Выбор этажа назначения; индикация открытых', fs=10, color="#555")
text(rx + 10, ry + 138, 'ворот и состояния штабелёра — на всех панелях', fs=10, color="#555")

# ================= 1 ЭТАЖ: ВОРОТА ЗАГРУЗКИ + ГЛАВНЫЙ ПУЛЬТ =================
gy = 945
line(470, gy, GATE_X + 110, gy, color=C_GREY, sw=1, dash="8 6")
text(455, gy - 6, 'Зона загрузки', fs=12, anchor="end", color=C_GREY)
box(80, gy - 35, 80, 45, color=C_BLUE, fill="#eef4ff", rx=4)
text(120, gy - 8, 'HMI0', color=C_BLUE, fs=13, anchor="middle", weight="bold")
text(120, gy - 48, 'Главная панель', fs=12, anchor="middle", color=C_BLUE)
text(120, gy - 33, 'оператора (Weintek)', fs=11, anchor="middle", color=C_BLUE)

# ================= ШКАФ УПРАВЛЕНИЯ (Weintek + ПЧ + безопасность) =================
px, py, pw, ph = 80, gy + 60, 1700, 200
box(px, py, pw, ph, color=C_BLUE, fill="#f7faff", sw=2, rx=6)
text(px + 14, py + 24, 'A1 — Шкаф управления АСУ ТП', fs=15, color=C_BLUE, weight="bold")
text(px + 320, py + 24, '(подробно — на схеме АСУ ТП, asu-tp-architecture.svg)', fs=11, color=C_GREEN)

def subbox(x, w, title, lines, color=C_BLUE):
    box(x, py + 40, w, ph - 54, color=color, fill="#fff", sw=1.5, rx=4)
    text(x + 10, py + 60, title, fs=12, color=color, weight="bold")
    for i, ln in enumerate(lines):
        text(x + 10, py + 80 + i * 17, ln, fs=10.5, color="#333")

subbox(px + 14, 360, 'Контроллер (Weintek cMT)', [
    'Сенсорная HMI + CODESYS-логика', 'Сервер cMT → клиентские панели этажей',
    'Ethernet / Modbus TCP / EtherCAT', 'Обработка вызовов, маршрутов, блокировок'])
subbox(px + 388, 360, 'Силовая часть', [
    'UZ1 — ПЧ привода подъёма M1 (+энкодер)', 'UZ2 — ПЧ привода вил M2',
    'QF… — автоматы защиты', 'Контакторы, питание тормоза YB1'])
subbox(px + 762, 360, 'Контур безопасности', [
    'Реле безопасности (PL d / SIL 2)', 'SF1 — аварийный стоп',
    'Ворота SQn.1 + сканеры BLn → СТОП', 'STO ПЧ + наложение тормоза YB1'])
subbox(px + 1136, 350, 'Удалённый ввод-вывод', [
    'Weintek iR (EtherCAT/Modbus TCP)', 'DI: датчики этажей, ворот, вил, занятости',
    'DO: замки YLn, тормоз, индикация', 'Энкодеры BR1/BR2 → ПЧ/счётчик'])

# ================= ЛЕГЕНДА =================
lx, lyy, lw, lh = 24, 110, 330, 470
box(lx, lyy, lw, lh, color=C_BLACK, fill="#fafafa", sw=1.5, rx=6)
text(lx + 14, lyy + 26, 'Условные обозначения', fs=15, weight="bold")
legend = [
    ('M', 'Электродвигатель привода', C_BLACK),
    ('BR', 'Энкодер / датчик положения вала', C_GREEN),
    ('YB', 'Тормоз электромагнитный', C_BLACK),
    ('SQ', 'Концевой выключатель / датчик', C_BLACK),
    ('YL', 'Замок электромагнитный', C_RED),
    ('BL', 'Лазерный сканер безопасности', C_GREEN),
    ('BG', 'Датчик наличия/занятости (паллеты)', C_ORANGE),
    ('PU', 'Вызывная панель этажа (HMI)', C_BLUE),
    ('UZ', 'Преобразователь частоты (ПЧ)', C_BLUE),
    ('A1', 'Шкаф управления / контроллер', C_BLUE),
    ('SF', 'Кнопка аварийного останова', C_RED),
]
for i, (sym, desc, col) in enumerate(legend):
    yy = lyy + 54 + i * 37
    circle(lx + 34, yy, sym, color=col, r=15, fs=10)
    text(lx + 58, yy + 4, desc, fs=11)
text(lx + 14, lyy + lh - 14, 'Зелёным/оранжевым — добавленные элементы.', fs=10, color=C_GREEN)

add('</svg>')

with open('/home/user/Claidegithub/schema/stacker-schema-detailed.svg', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(svg))
print('SVG written')
