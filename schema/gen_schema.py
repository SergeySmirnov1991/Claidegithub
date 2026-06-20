# -*- coding: utf-8 -*-
"""Генератор детализированной функциональной схемы одноколонного штабелёра
(межэтажного подъёмника) для производственного здания.

Назначение: перемещение паллет 1000x1200 мм, грузоподъёмность до 2000 кг,
между 5 этажами производственного здания. Конструкция одноколонная —
горизонтального перемещения нет: грузовая каретка с телескопическими вилами
движется по единственной мачте (подъём/опускание) и выдвигает вилы в пост
приёма/выдачи на нужном этаже.

Выход: stacker-schema-detailed.svg
Схема — доработка исходного эскиза: добавлены позиционные обозначения по
ГОСТ 2.710, ПЛК, силовая часть (ПЧ), контур безопасности, легенда,
адресация сигналов и отмечены открытые вопросы.
"""

W, H = 1760, 1240
LEVELS = [5, 4, 3, 2, 1]
FY = {5: 250, 4: 405, 3: 555, 2: 705, 1: 855}   # y-центр этажа

MAST_X = 660
MAST_W = 34
CELL_X0 = 1030
CELL_X1 = 1230
GATE_X = 1290
LSENS_X = 560

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

def text(x, y, s, color=C_BLACK, fs=13, anchor="start", weight="normal", style="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" '
        f'font-weight="{weight}" font-style="{style}">{s}</text>')


# ---------- Заголовок ----------
text(W/2, 38, 'Одноколонный штабелёр (межэтажный подъёмник) производственного здания',
     fs=22, anchor="middle", weight="bold")
text(W/2, 60, 'Паллеты 1000×1200 мм · грузоподъёмность 2000 кг · перемещение между 5 этажами',
     fs=14, anchor="middle", color="#555")
text(W/2, 78, 'Функциональная схема приводов, датчиков и устройств безопасности (доработанная, детализированная)',
     fs=12, anchor="middle", color=C_GREY)

# ---------- Мачта (единственная колонна) ----------
mast_top, mast_bot = 120, 985
box(MAST_X - MAST_W/2, mast_top, MAST_W, mast_bot - mast_top, color=C_BLACK, fill="#f3f3f3")
text(MAST_X, mast_bot + 18, 'Мачта (одна колонна, без горизонт. перемещения)', fs=11, anchor="middle", color=C_GREY)

for f in LEVELS:
    y = FY[f]
    line(420, y, 1370, y, color=C_GREY, sw=1, dash="8 6")
    text(395, y - 6, f'{f} этаж', fs=14, anchor="end", weight="bold")

# ================= ПРИВОД ПОДЪЁМА =================
ly = 158
line(MAST_X, mast_top, MAST_X, ly, color=C_BLACK, sw=2)
line(MAST_X, ly, 720, ly)
circle(745, ly, 'M1', r=21)
line(766, ly, 800, ly)
circle(825, ly, 'BR1', color=C_GREEN, r=21, fs=12)
line(846, ly, 880, ly)
circle(905, ly, 'YB1', r=21, fs=12)
line(975, 120, 975, 205, color=C_BLACK, sw=2)
add(f'<line x1="975" y1="120" x2="975" y2="128" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
add(f'<line x1="975" y1="205" x2="975" y2="197" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
text(995, 142, 'Подъём-опускание грузовой каретки', fs=14, weight="bold")
text(995, 162, 'M1 — двигатель привода подъёма', fs=12, color="#444")
text(995, 179, 'BR1 — энкодер (положение/скорость каретки)', fs=12, color=C_GREEN)
text(995, 196, 'YB1 — тормоз электромагнитный (удержание груза)', fs=12, color="#444")
circle(MAST_X, mast_top + 8, 'SQ0', color=C_GREEN, r=15, fs=10)
text(MAST_X + 22, mast_top + 12, 'SQ0 — концевой выкл. «верх» (перебег)', fs=10, color=C_GREEN)
circle(MAST_X, mast_bot - 8, 'SQ9', color=C_GREEN, r=15, fs=10)
text(MAST_X + 22, mast_bot - 4, 'SQ9 — концевой выкл. «низ» (перебег)', fs=10, color=C_GREEN)

# ================= КАРЕТКА + ТЕЛЕСКОПИЧЕСКИЕ ВИЛЫ =================
cy = FY[5] + 70
# заголовок и стрелка выдвижения над кареткой
text(MAST_X, cy - 50, 'Выдвижение телескопических вил (захват паллеты)', fs=12, anchor="middle", weight="bold")
line(MAST_X - 60, cy - 40, MAST_X + 60, cy - 40, color=C_BLACK, sw=2)
add(f'<line x1="{MAST_X-60}" y1="{cy-40}" x2="{MAST_X-52}" y2="{cy-40}" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
add(f'<line x1="{MAST_X+60}" y1="{cy-40}" x2="{MAST_X+52}" y2="{cy-40}" stroke="{C_BLACK}" stroke-width="2" marker-start="url(#ar)"/>')
# тело каретки с двигателем M2 и энкодером BR2
box(MAST_X - 95, cy - 26, 190, 52, color=C_BLACK, fill="#eef")
circle(MAST_X - 34, cy, 'M2', r=19)
circle(MAST_X + 36, cy, 'BR2', color=C_GREEN, r=18, fs=11)
# вилы влево/вправо (захват паллеты)
line(MAST_X - 95, cy, MAST_X - 175, cy, color=C_BLACK)
add(f'<polygon points="{MAST_X-175},{cy-9} {MAST_X-215},{cy-9} {MAST_X-215},{cy+9} {MAST_X-175},{cy+9}" fill="none" stroke="{C_BLACK}" stroke-width="2"/>')
line(MAST_X + 95, cy, MAST_X + 120, cy, color=C_BLACK)
add(f'<polygon points="{MAST_X+120},{cy-9} {MAST_X+150},{cy-9} {MAST_X+150},{cy+9} {MAST_X+120},{cy+9}" fill="none" stroke="{C_BLACK}" stroke-width="2"/>')
text(MAST_X - 215, cy - 14, 'паллета', fs=8, color=C_GREY)
# датчики положения вил на каретке (один ряд под кареткой)
circle(MAST_X - 55, cy + 48, 'SQ8.1', r=17, fs=9)
circle(MAST_X, cy + 48, 'SQ8.2', r=17, fs=9)
circle(MAST_X + 55, cy + 48, 'SQ8.3', r=17, fs=9)
# описание блока каретки (в свободной зоне справа от мачты)
tx = 830
text(tx, cy - 22, 'Грузовая каретка (вся высота мачты):', fs=11, weight="bold")
text(tx, cy - 4, 'M2 — привод вил · BR2 — энкодер вил', fs=11)
text(tx, cy + 14, 'SQ8.1…8.3 — положение вил (убраны/влево/вправо)', fs=11)
text(tx, cy + 32, 'BG1 — наличие паллеты на вилах (предложено)', fs=11, color=C_ORANGE)

# ================= ДАТЧИКИ ЭТАЖА (слева) =================
for f in LEVELS:
    y = FY[f]
    line(MAST_X - MAST_W/2, y, LSENS_X + 18, y, color=C_BLACK)
    circle(LSENS_X, y, f'SQ{f}a', r=16, fs=10)
    circle(LSENS_X - 38, y, f'SQ{f}b', r=16, fs=10)
    circle(LSENS_X - 19, y - 30, f'SQ{f}c', color=C_GREEN, r=15, fs=9)
    line(LSENS_X - 19, y - 15, LSENS_X - 19, y, color=C_BLACK, sw=1)
yy = FY[5]
text(LSENS_X - 70, yy - 52, 'SQna, SQnb — сдвоенный датчик этажа (точная остановка по высоте)', fs=11, anchor="end")
text(LSENS_X - 70, yy - 36, 'SQnc — датчик перебега этажа', fs=11, anchor="end", color=C_GREEN)

# ================= ПОСТ ПРИЁМА/ВЫДАЧИ НА ЭТАЖЕ + КАЛИТКА (справа) =================
for f in LEVELS:
    y = FY[f]
    cy0, cy1 = y - 42, y + 42
    line(CELL_X0, cy0, CELL_X0, cy1, color=C_RED, sw=4)
    line(CELL_X1, cy0, CELL_X1, cy1, color=C_RED, sw=4)
    box(CELL_X0 + 8, cy0 + 6, CELL_X1 - CELL_X0 - 16, cy1 - cy0 - 12, color=C_RED, sw=1.5)
    for gx in range(1, 6):
        xx = CELL_X0 + 8 + gx * (CELL_X1 - CELL_X0 - 16) / 6
        line(xx, cy0 + 6, xx, cy1 - 6, color=C_RED, sw=1)
    for gy2 in range(1, 4):
        yy2 = cy0 + 6 + gy2 * (cy1 - cy0 - 12) / 4
        line(CELL_X0 + 8, yy2, CELL_X1 - 8, yy2, color=C_RED, sw=1)
    text((CELL_X0 + CELL_X1) / 2, y + 3, f'Пост {f} эт.', fs=11, anchor="middle", color=C_RED)
    line(CELL_X1, y - 25, GATE_X - 18, y - 25, color=C_RED)
    circle(GATE_X, y - 25, f'SQ{f}.1', color=C_RED, r=16, fs=9)
    circle(GATE_X + 40, y - 25, f'SQ{f}.2', color=C_RED, r=16, fs=9)
    line(CELL_X1, y, GATE_X - 18, y, color=C_RED)
    circle(GATE_X, y, f'YL{f}', color=C_RED, r=16, fs=10)
    line(CELL_X1, y + 25, GATE_X - 18, y + 25, color=C_RED)
    circle(GATE_X, y + 25, f'BL{f}', color=C_GREEN, r=16, fs=10)
yy = FY[5]
text(GATE_X + 70, yy - 38, 'Пост приёма/выдачи паллет на каждом этаже:', fs=11, weight="bold")
text(GATE_X + 70, yy - 22, 'SQn.1, SQn.2 — датчики закрытия калитки', fs=11)
text(GATE_X + 70, yy - 4, 'YLn — электромагнитный замок калитки', fs=11, color=C_RED)
text(GATE_X + 70, yy + 16, 'BLn — лазерный сканер безопасности', fs=11, color=C_GREEN)
text(GATE_X + 70, yy + 31, '(контроль присутствия человека в проёме)', fs=10, color=C_GREEN)

# ================= 1 ЭТАЖ: ВОРОТА + ПУЛЬТ =================
gy = 915
line(420, gy, 1370, gy, color=C_GREY, sw=1, dash="8 6")
text(395, gy - 6, 'Зона загрузки (1 эт.)', fs=12, anchor="end", color=C_GREY)
box(80, gy - 35, 70, 45, color=C_BLUE, fill="#eef4ff", rx=4)
text(115, gy - 8, 'PU1', color=C_BLUE, fs=14, anchor="middle", weight="bold")
text(115, gy - 48, 'Пульт управления', fs=12, anchor="middle", color=C_BLUE)
text(115, gy - 33, 'сенсорный (HMI)', fs=12, anchor="middle", color=C_BLUE)
box(300, gy - 60, 30, 55, color=C_BLACK, fill="#f0f0f0")
line(345, gy - 60, 345, gy, color=C_BLACK, sw=3)
text(300, gy - 70, 'Ворота загрузки', fs=12, weight="bold")
circle(420, gy, 'SQv1', r=16, fs=9)
circle(470, gy, 'SQv2', r=16, fs=9)
line(440, gy, 450, gy, color=C_BLACK)
text(400, gy + 32, 'SQv1, SQv2 — датчики положения ворот (открыто/закрыто)', fs=11)
circle(560, gy, 'M3', color=C_ORANGE, r=17, fs=11)
circle(610, gy, 'YL0', color=C_ORANGE, r=17, fs=11)
line(577, gy, 593, gy, color=C_ORANGE)
text(540, gy + 32, 'M3 — привод ворот, YL0 — замок ворот (предложено)', fs=11, color=C_ORANGE)

# ================= ПЛК + СИЛОВАЯ ЧАСТЬ =================
px, py, pw, ph = 80, gy + 70, 1280, 180
box(px, py, pw, ph, color=C_BLUE, fill="#f7faff", sw=2, rx=6)
text(px + 14, py + 24, 'A1 — Шкаф управления (ПЛК)', fs=15, color=C_BLUE, weight="bold")
text(px + 270, py + 24, '— добавлено при детализации', fs=11, color=C_GREEN)

def subbox(x, w, title, lines, color=C_BLUE):
    box(x, py + 40, w, ph - 54, color=color, fill="#fff", sw=1.5, rx=4)
    text(x + 10, py + 60, title, fs=12, color=color, weight="bold")
    for i, ln in enumerate(lines):
        text(x + 10, py + 80 + i * 16, ln, fs=10.5, color="#333")

subbox(px + 14, 250, 'Контроллер A1', [
    'CPU + модули DI/DO/AI', 'Ethernet/Modbus TCP → HMI',
    'Связь с ПЧ по полевой шине', 'Безопасный ПЛК / реле безопасности'])
subbox(px + 278, 250, 'Силовая часть', [
    'UZ1 — ПЧ привода подъёма M1', 'UZ2 — ПЧ привода вил M2',
    'UZ3 — ПЧ/пускатель ворот M3', 'QF1… — автоматы защиты, STO'])
subbox(px + 542, 250, 'Контур безопасности', [
    'SF1 — кнопка «Аварийный стоп»', 'SQ0/SQ9 — перебег по высоте',
    'BLn — лаз. сканеры калиток', 'YBx — тормоз в цепи STO'])
subbox(px + 806, 460, 'Адресация сигналов (сводно)', [
    'DI: датчики этажей SQna/b/c (15), положение вил (3), закрытие калиток (10),',
    '     положение ворот (2), перебег (2), наличие паллеты на вилах (1)',
    'DO: замки калиток YL1…5 (5), замок ворот YL0, тормоз YB1, разрешения ПЧ, индикация',
    'AI / энкодеры: BR1 (подъём), BR2 (вилы) · Безопасность: SF1, BLn, реле — отдельный контур'])

# ================= ЛЕГЕНДА =================
lx, lyy, lw, lh = 80, 120, 300, 500
box(lx, lyy, lw, lh, color=C_BLACK, fill="#fafafa", sw=1.5, rx=6)
text(lx + 14, lyy + 26, 'Условные обозначения', fs=15, weight="bold")
legend = [
    ('M', 'Электродвигатель привода', C_BLACK),
    ('BR', 'Энкодер / датчик положения вала', C_GREEN),
    ('YB', 'Тормоз электромагнитный', C_BLACK),
    ('SQ', 'Путевой / концевой выключатель, датчик', C_BLACK),
    ('YL', 'Замок электромагнитный', C_RED),
    ('BL', 'Лазерный сканер безопасности', C_GREEN),
    ('BG', 'Датчик наличия паллеты (предложено)', C_ORANGE),
    ('PU', 'Пульт управления / HMI', C_BLUE),
    ('UZ', 'Преобразователь частоты (ПЧ)', C_BLUE),
    ('A1', 'ПЛК / шкаф управления', C_BLUE),
    ('SF', 'Кнопка аварийного останова', C_RED),
]
for i, (sym, desc, col) in enumerate(legend):
    yy = lyy + 54 + i * 38
    circle(lx + 36, yy, sym, color=col, r=15, fs=10)
    text(lx + 62, yy + 4, desc, fs=11)
text(lx + 14, lyy + lh - 30, 'Зелёным — добавленные/уточнённые элементы.', fs=10, color=C_GREEN)
text(lx + 14, lyy + lh - 14, 'Оранжевым — предложено к добавлению.', fs=10, color=C_ORANGE)

# ================= ОТКРЫТЫЕ ВОПРОСЫ =================
qx, qy = 80, 645
box(qx, qy, 300, 150, color=C_ORANGE, fill="#fff8f0", sw=1.5, rx=6)
text(qx + 12, qy + 22, '⚠ Уточнить:', fs=13, color=C_ORANGE, weight="bold")
notes = [
    '1. Тип лаз. сканеров BLn (исх. «????»):',
    '   сканер безопасности проёма или',
    '   контроль габарита/наличия паллеты?',
    '2. Вилы телескопические одинарного',
    '   или двойного хода (double-deep)?',
    '3. Противовес/полиспаст подъёма —',
    '   уточнить кинематику и расчёт M1.',
    '4. Загрузка только с 1 этажа или с любого?',
]
for i, n in enumerate(notes):
    text(qx + 12, qy + 44 + i * 14, n, fs=10.5, color="#7a4")

add('</svg>')

with open('/home/user/Claidegithub/schema/stacker-schema-detailed.svg', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(svg))
print('SVG written')
