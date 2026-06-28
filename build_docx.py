#!/usr/bin/env python3
"""Генерация DOCX со сводной таблицей чехлов для iPhone 17 Pro Max."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "18")  # 9pt
    rPr.append(sz)
    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink


# (name, url, material, thickness, protection, magsafe, usd, eur, rub)
ROWS = [
    ("Pitaka MagEZ 5 Edge", "https://www.ipitaka.com/collections/iphone-17-pro-max-cases",
     "Арамид 600D", "Ультратонкий", "Средняя (царапины / лёгкие падения)", "✓ + экосистема", "$60–80", "€55–74", "5700–7600 ₽"),
    ("Pitaka MagEZ 5 Summa/Cairn", "https://www.ipitaka.com/collections/iphone-17-pro-max-cases",
     "Арамид + бампер", "Тонкий", "Средняя–высокая", "✓ + экосистема", "$70–100", "€64–92", "6700–9500 ₽"),
    ("Thinborne Carbon/Aramid", "https://thinborne.com/collections/iphone-17-pro-max-carbon-fiber-case",
     "Арамид / карбон", "Ультратонкий (~1 мм)", "Низкая–средняя", "✓", "~$70", "~€64", "~6700 ₽"),
    ("Carbon Fiber Gear CarboFend", "https://carbonfibergear.com/collections/iphone-17",
     "Настоящий 3K карбон", "Тонкий", "Средняя", "✓", "$60–80", "€55–74", "5700–7600 ₽"),
    ("Simply Carbon Fiber CLASSIC", "https://www.simplycarbonfiber.com/products/iphone-real-carbon-fiber-case-classic-series",
     "Настоящий 3K twill", "Тонкий", "Средняя", "✓", "$90–100", "€83–92", "8600–9500 ₽"),
    ("Ridge Carbon", "https://ridge.com/products/iphone-17-pro-max-case-carbon",
     "Карбон + TPU-бампер", "Тонкий", "Высокая (углы)", "✓", "~$60", "~€55", "~5700 ₽"),
    ("MonCarbone Ballistic", "https://moncarbone.com/collections/iphone-17/products/ballistic-fiber-magnetic-minimalist-iphone-17-pro-pro-max-case-racing-black",
     "Баллистическое волокно", "Ультратонкий", "Низкая–средняя", "✓", "$70–90", "€64–83", "6700–8600 ₽"),
    ("Spigen Rugged Armor MagFit", "https://www.spigen.com/collections/iphone-17-pro-max",
     "TPU", "Средний", "Высокая", "✓", "~$22", "~€20", "~2100 ₽"),
    ("OtterBox Symmetry", "https://www.otterbox.com/en-us/iphone-17-pro-max-cases/",
     "Поликарбонат / TPU", "Средний", "Высокая (3× MIL)", "✓", "$50–60", "€46–55", "4800–5700 ₽"),
    ("UNIQ Heldro Air", "https://www.uniqliving.com/collections/iphone-17-pro-max",
     "TPU / поликарбонат", "Тонкий", "Средняя–высокая (до 4 м)", "✓", "~$24", "~€22", "~2300 ₽"),
    ("TORRAS Translucent", "https://www.torras.com/collections/iphone-17-pro-max-case",
     "Полупрозрачный PC/TPU", "Тонкий", "Высокая (X-SHOCK)", "✓ (38 магнитов)", "$30–40", "€28–37", "2900–3800 ₽"),
    ("Dropguys Ultra Slim Clear", "https://www.dropguys.com/blogs/news/best-iphone-17-pro-max-cases",
     "Прозрачный TPU", "Тонкий", "Средняя–высокая", "✓", "$25–35", "€23–32", "2400–3300 ₽"),
    ("Mujjo Full Leather", "https://www.mujjo.com/products/full-leather-case-for-iphone-17-pro-max",
     "Натуральная кожа", "Тонкий", "Средняя", "✓", "~$65", "~€60", "~6200 ₽"),
    ("Nomad Traditional Leather", "https://nomadgoods.com/collections/iphone-17-pro-max",
     "Кожа Horween", "Средний", "Средняя–высокая (бамперы)", "✓", "$65–85", "€60–78", "6200–8100 ₽"),
    ("Bellroy 3-Card", "https://bellroy.com/products/category/iphone-17-pro-max",
     "Кожа + полимер", "Средний", "Средняя", "✓", "~$79", "~€73", "~7500 ₽"),
    ("Casekoo (кольцо-подставка)", "https://www.casekoo.com/collections/iphone-17-pro-max",
     "PC / TPU", "Средний", "Средняя–высокая", "✓ + подставка", "$20–30", "€18–28", "1900–2900 ₽"),
    ("Moft Movas", "https://www.moft.us/collections/iphone-17-pro-max",
     "TPU / металл", "Тонкий", "Средняя", "✓", "~$50", "~€46", "~4800 ₽"),
]

HEADERS = ["Чехол", "Материал", "Толщина", "Защита", "MagSafe", "≈ $", "≈ €", "≈ ₽"]

# (rank, name, url, why)
TOP5 = [
    ("1", "Pitaka MagEZ Case 5 (Edge)", "https://www.ipitaka.com/collections/iphone-17-pro-max-cases",
     "Лучший в целом: арамид, ультратонкий, не выцветает, идеальный хват и экосистема MagSafe"),
    ("2", "Spigen Rugged Armor MagFit", "https://www.spigen.com/collections/iphone-17-pro-max",
     "Лучший универсал по цене / защите на каждый день"),
    ("3", "Mujjo Full Leather", "https://www.mujjo.com/products/full-leather-case-for-iphone-17-pro-max",
     "Лучший для статусного образа и тактильности"),
    ("4", "Bellroy 3-Card", "https://bellroy.com/products/category/iphone-17-pro-max",
     "Лучший для города без кошелька (телефон + карты)"),
    ("5", "UNIQ Heldro Air", "https://www.uniqliving.com/collections/iphone-17-pro-max",
     "Лучший по соотношению «тонкость + цена»"),
]

doc = Document()

# Шрифт по умолчанию
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10)

# Поля страницы (альбомная для широкой таблицы)
section = doc.sections[0]
section.orientation = 1  # landscape
section.page_width, section.page_height = section.page_height, section.page_width
for m in ("left_margin", "right_margin"):
    setattr(section, m, Inches(0.5))

# Заголовок
title = doc.add_heading("Лучшие чехлы для iPhone 17 Pro Max для города", level=0)
sub = doc.add_paragraph()
run = sub.add_run("Сводная таблица сравнения · актуально на июнь 2026")
run.italic = True
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)

doc.add_paragraph(
    "Цены — ориентир без скидок; € и ₽ пересчитаны по курсу ≈ $1 = €0,92 = 95 ₽ и могут отличаться. "
    "Названия чехлов кликабельны — ведут на страницы товаров/производителей."
).runs[0].font.size = Pt(9)

# --- Топ-5 «Лучшие из всех» ---
doc.add_heading("Лучшие из всех (итог)", level=1)
top = doc.add_table(rows=1, cols=3)
top.style = "Light Grid Accent 1"
top.alignment = WD_TABLE_ALIGNMENT.CENTER
th = top.rows[0].cells
for i, h in enumerate(["#", "Чехол", "Почему лучший"]):
    th[i].text = ""
    r = th[i].paragraphs[0].add_run(h)
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(th[i], "2E5496")
for k, (rank, name, url, why) in enumerate(TOP5):
    cells = top.add_row().cells
    cells[0].paragraphs[0].text = ""
    rr = cells[0].paragraphs[0].add_run(rank)
    rr.bold = True
    rr.font.size = Pt(11)
    cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cells[1].paragraphs[0].text = ""
    add_hyperlink(cells[1].paragraphs[0], name, url)
    cells[2].paragraphs[0].text = ""
    cells[2].paragraphs[0].add_run(why).font.size = Pt(9)
    if k % 2 == 1:
        for c in cells:
            set_cell_bg(c, "EEF3FB")
for row in top.rows:
    row.cells[0].width = Inches(0.4)
    row.cells[1].width = Inches(2.6)
    row.cells[2].width = Inches(6.5)

doc.add_paragraph()
doc.add_heading("Полная таблица сравнения", level=1)

# Таблица
table = doc.add_table(rows=1, cols=len(HEADERS))
table.style = "Light Grid Accent 1"
table.alignment = WD_TABLE_ALIGNMENT.CENTER

# Заголовки
hdr = table.rows[0].cells
for i, h in enumerate(HEADERS):
    hdr[i].text = ""
    p = hdr[i].paragraphs[0]
    r = p.add_run(h)
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    set_cell_bg(hdr[i], "2E5496")

# Данные
for idx, (name, url, material, thick, prot, mag, usd, eur, rub) in enumerate(ROWS):
    cells = table.add_row().cells
    # Чехол — гиперссылка
    cells[0].paragraphs[0].text = ""
    add_hyperlink(cells[0].paragraphs[0], name, url)
    for j, val in enumerate([material, thick, prot, mag, usd, eur, rub], start=1):
        cells[j].text = ""
        run = cells[j].paragraphs[0].add_run(val)
        run.font.size = Pt(8)
    # Зебра
    if idx % 2 == 1:
        for c in cells:
            set_cell_bg(c, "EEF3FB")

# Ширины колонок
widths = [Inches(1.9), Inches(1.5), Inches(1.2), Inches(2.3), Inches(1.3), Inches(0.7), Inches(0.7), Inches(0.9)]
for row in table.rows:
    for i, w in enumerate(widths):
        row.cells[i].width = w

# Блок «Ориентир по бюджету»
doc.add_paragraph()
doc.add_heading("Ориентир по бюджету", level=2)
budget = [
    ("До $30 (бюджет):", "UNIQ Heldro Air, Spigen Rugged Armor, Casekoo, Dropguys Clear"),
    ("$30–60 (средний):", "TORRAS, OtterBox Symmetry, Moft Movas, Ridge Carbon"),
    ("$60–100 (премиум):", "Pitaka MagEZ 5, Mujjo, Nomad, Bellroy, Carbon Fiber Gear, Simply Carbon Fiber"),
]
for label, items in budget:
    p = doc.add_paragraph(style="List Bullet")
    r = p.add_run(label + " ")
    r.bold = True
    p.add_run(items)

doc.save("iPhone17ProMax_chehly_sravnenie.docx")
print("saved iPhone17ProMax_chehly_sravnenie.docx")
