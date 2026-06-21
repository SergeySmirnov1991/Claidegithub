# -*- coding: utf-8 -*-
"""Диаграмма состояний (конечный автомат) управления штабелёром для CODESYS.

Рабочий цикл: Ожидание → к этажу-источнику → захват паллеты → к этажу
назначения → проверка места → выгрузка / ожидание освобождения → Ожидание.
Глобальные обработчики (из любого состояния): блокировка по воротам,
аварийный останов, авария привода.

Выход: state-machine.svg
"""

W,H=1580,1080
C_BLACK="#1a1a1a"; C_RED="#d40000"; C_BLUE="#0050c8"; C_GREEN="#0a8f3c"
C_GREY="#888"; C_ORANGE="#e07000"

svg=[]
def add(s): svg.append(s)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="DejaVu Sans, Arial, sans-serif">')
add(f'<rect width="{W}" height="{H}" fill="#fff"/>')
add('<defs>'
    f'<marker id="a" markerWidth="10" markerHeight="10" refX="8.5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C_BLACK}"/></marker>'
    f'<marker id="ag" markerWidth="10" markerHeight="10" refX="8.5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C_GREEN}"/></marker>'
    f'<marker id="ar" markerWidth="10" markerHeight="10" refX="8.5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C_RED}"/></marker>'
    f'<marker id="ao" markerWidth="10" markerHeight="10" refX="8.5" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{C_ORANGE}"/></marker>'
    '</defs>')

def text(x,y,s,color=C_BLACK,fs=12,anchor="start",weight="normal"):
    add(f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>')

STATES={}
def state(key,x,y,name,desc,color=C_BLUE,w=250,h=58,fill="#f3f7ff"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2.2"/>')
    text(x+w/2,y+24,name,fs=13,anchor="middle",weight="bold",color=color)
    if desc: text(x+w/2,y+43,desc,fs=9.5,anchor="middle",color="#444")
    STATES[key]=(x,y,w,h)

def edge(k1,side1,k2,side2,label,color=C_BLACK,mk='a',lx=None,ly=None,dash=None,bend=None):
    x1,y1,w1,h1=STATES[k1]; x2,y2,w2,h2=STATES[k2]
    def pt(x,y,w,h,side):
        return {'t':(x+w/2,y),'b':(x+w/2,y+h),'l':(x,y+h/2),'r':(x+w,y+h/2)}[side]
    p1=pt(x1,y1,w1,h1,side1); p2=pt(x2,y2,w2,h2,side2)
    d=f' stroke-dasharray="{dash}"' if dash else ''
    if bend is None:
        add(f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" stroke="{color}" stroke-width="1.8"{d} marker-end="url(#{mk})"/>')
    else:
        # ортогональный изгиб через промежуточную x=bend
        add(f'<polyline points="{p1[0]},{p1[1]} {bend},{p1[1]} {bend},{p2[1]} {p2[0]},{p2[1]}" fill="none" stroke="{color}" stroke-width="1.8"{d} marker-end="url(#{mk})"/>')
    if label:
        mx=lx if lx is not None else (p1[0]+p2[0])/2
        my=ly if ly is not None else (p1[1]+p2[1])/2
        # подложка под текст
        wpx=len(label)*5.6
        add(f'<rect x="{mx-wpx/2-3}" y="{my-11}" width="{wpx+6}" height="15" fill="#ffffff" opacity="0.85"/>')
        text(mx,my,label,fs=9.5,anchor="middle",color=color)

# ---- Заголовок ----
text(W/2,34,'Конечный автомат управления штабелёром (для реализации в CODESYS)',fs=21,anchor="middle",weight="bold")
text(W/2,56,'Рабочий цикл «вызов → забор → доставка → выгрузка/ожидание» и глобальные обработчики безопасности',fs=12.5,anchor="middle",color="#555")

CX=330  # левый край центральной колонки
# ---- Основная цепочка ----
state('INIT',  CX,86, 'S0 · ИНИЦИАЛИЗАЦИЯ','самотест, чтение состояния',C_GREY,fill="#f6f6f6")
state('HOME',  CX,176,'S1 · КАЛИБРОВКА (HOMING)','поиск референса по высоте',C_GREY,fill="#f6f6f6")
state('IDLE',  CX,276,'S2 · ОЖИДАНИЕ ВЫЗОВА','очередь заданий с панелей',C_BLUE,fill="#e9f0ff")
state('TOSRC', CX,376,'S3 · К ЭТАЖУ-ИСТОЧНИКУ','позиционирование по BR1/SQ',C_BLUE)
state('PICK',  CX,476,'S4 · ЗАХВАТ ПАЛЛЕТЫ','вилы → подъём → возврат',C_BLUE)
state('TODST', CX,576,'S5 · К ЭТАЖУ НАЗНАЧЕНИЯ','позиционирование по BR1/SQ',C_BLUE)
state('CHECK', CX,676,'S6 · ПРОВЕРКА МЕСТА','чтение датчика занятости BGy',C_BLUE)
state('UNLOAD',CX-170,790,'S7 · ВЫГРУЗКА','вилы → опускание → возврат',C_GREEN,fill="#f0fbf3")
state('WAIT',  CX+170,790,'S8 · ОЖИДАНИЕ МЕСТА','паллета на вилах, сигнал «занято»',C_ORANGE,w=250,fill="#fff7ed")

# ---- Глобальные обработчики (справа) ----
GX=1060
state('GATE', GX,300,'G1 · БЛОКИРОВКА — ВОРОТА','СТОП; индикация «ворота эт.N»',C_RED,w=300,fill="#fff1f1")
state('SAFE', GX,430,'G2 · АВАРИЙНЫЙ ОСТАНОВ','STO + тормоз (контур KSR)',C_RED,w=300,fill="#ffe9e9")
state('FAULT',GX,560,'G3 · АВАРИЯ','ошибка ПЧ / таймаут / позиция',C_RED,w=300,fill="#fff1f1")

# ---- Переходы основной цепочки ----
edge('INIT','b','HOME','t','авто')
edge('HOME','b','IDLE','t','референс найден')
edge('IDLE','b','TOSRC','t','вызов эт.X + выбран Y; ворота закрыты; безоп. OK',color=C_BLUE)
edge('TOSRC','b','PICK','t','прибыл на этаж X (SQXa·SQXb)',color=C_BLUE)
edge('PICK','b','TODST','t','паллета на вилах BG0=1; SQ8.1',color=C_BLUE)
edge('TODST','b','CHECK','t','прибыл на этаж Y',color=C_BLUE)
# ветвление проверки места
edge('CHECK','l','UNLOAD','t','место свободно (BGy=0)',color=C_GREEN,mk='ag',lx=CX-60,ly=748)
edge('CHECK','r','WAIT','t','место занято (BGy=1)',color=C_ORANGE,mk='ao',lx=CX+300,ly=748)
# возвраты в IDLE
edge('UNLOAD','b','IDLE','l',None,color=C_GREEN,mk='ag',bend=120)
text(150,520,'выгружено (BG0=0)',fs=9.5,color=C_GREEN,anchor="middle")
text(150,535,'→ в ОЖИДАНИЕ',fs=9.5,color=C_GREEN,anchor="middle")
edge('WAIT','b','UNLOAD','b',None,color=C_ORANGE,mk='ao',bend=CX-220)
text(CX-220,866,'место освободилось → выгрузка',fs=9,color=C_ORANGE,anchor="middle")
# отмена в PICK (нет паллеты)
edge('PICK','r','IDLE','r',None,color=C_GREY,mk='a',dash="5 4",bend=720)
text(720,430,'нет паллеты (BGx=0) → отмена',fs=9,color=C_GREY,anchor="middle")

# ---- Глобальные переходы «из любого состояния» ----
brace_x=GX-40
add(f'<path d="M{brace_x},250 q-14,0 -14,16 v520 q0,16 14,16" fill="none" stroke="{C_RED}" stroke-width="1.6"/>')
add(f'<text x="{brace_x-18}" y="520" font-size="10" fill="{C_RED}" text-anchor="middle" transform="rotate(-90 {brace_x-18},520)" font-weight="bold">из любого рабочего состояния</text>')
# стрелки к обработчикам
add(f'<line x1="{brace_x-32}" y1="332" x2="{GX}" y2="332" stroke="{C_RED}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
text((brace_x-32+GX)/2,326,'ворота открылись (SQn.1=0)',fs=9,color=C_RED,anchor="middle")
add(f'<line x1="{brace_x-32}" y1="462" x2="{GX}" y2="462" stroke="{C_RED}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
text((brace_x-32+GX)/2,456,'авар. стоп / контур KSR',fs=9,color=C_RED,anchor="middle")
add(f'<line x1="{brace_x-32}" y1="592" x2="{GX}" y2="592" stroke="{C_RED}" stroke-width="1.8" stroke-dasharray="5 4" marker-end="url(#ar)"/>')
text((brace_x-32+GX)/2,586,'ошибка ПЧ / таймаут',fs=9,color=C_RED,anchor="middle")
# возвраты обработчиков
add(f'<line x1="{GX}" y1="318" x2="{CX+250}" y2="300" stroke="{C_GREEN}" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#ag)"/>')
text(GX-90,300,'ворота закрыты + квитирование → возврат',fs=8.5,color=C_GREEN,anchor="end")
add(f'<line x1="{GX}" y1="455" x2="{CX+250}" y2="120" stroke="{C_GREEN}" stroke-width="1.4" stroke-dasharray="6 4" marker-end="url(#ag)"/>')
text(GX-30,150,'сброс → S0',fs=9,color=C_GREEN,anchor="end")
add(f'<line x1="{GX}" y1="585" x2="{CX+250}" y2="130" stroke="{C_GREEN}" stroke-width="1.2" stroke-dasharray="3 4" marker-end="url(#ag)"/>')

# ---- Легенда ----
lx,ly=70,900
add(f'<rect x="{lx}" y="{ly}" width="760" height="150" rx="6" fill="#fafafa" stroke="{C_GREY}" stroke-width="1.5"/>')
text(lx+14,ly+24,'Пояснения',fs=13,weight="bold")
leg=[
 '• Синие состояния — рабочий цикл; зелёное — выгрузка; оранжевое — ожидание освобождения места; красные — обработчики безопасности.',
 '• Открытие ворот на любом этаже переводит автомат в блокировку с немедленным СТОП; на всех панелях — индикация этажа с открытыми воротами.',
 '• Если место выгрузки занято (BGy=1) — паллета остаётся на вилах (S8), штабелёр стоит на этаже назначения до освобождения места.',
 '• Аварийный стоп и контур KSR действуют аппаратно (STO + тормоз) параллельно логике; выход — только через сброс и квитирование.',
 '• Позиционирование — по энкодеру BR1 с точной остановкой по сдвоенным датчикам этажа SQna/SQnb; контроль вил — по SQ8.1…8.3.',
]
for i,n in enumerate(leg):
    text(lx+14,ly+46+i*16,n,fs=9.5,color="#234")

# ---- Скелет ST в углу ----
sx,sy=870,900
add(f'<rect x="{sx}" y="{sy}" width="{W-sx-40}" height="150" rx="6" fill="#0f1720" stroke="#0f1720"/>')
code=[
 'CASE eState OF',
 '  S2_IDLE:    IF Call AND GatesClosed AND SafeOK THEN eState:=S3; END_IF',
 '  S3_TO_SRC:  IF AtFloor(src) THEN eState:=S4; END_IF',
 '  S4_PICK:    IF PalletOnFork THEN eState:=S5;',
 '              ELSIF NoPallet THEN eState:=S2; END_IF',
 '  S6_CHECK:   IF NOT DestOccupied THEN eState:=S7; ELSE eState:=S8; END_IF',
 '  S8_WAIT:    IF NOT DestOccupied THEN eState:=S7; END_IF',
 'END_CASE',
 'IF AnyGateOpen OR EStop OR Fault THEN eState:=G_HANDLER; END_IF',
]
for i,c in enumerate(code):
    add(f'<text x="{sx+12}" y="{sy+24+i*15}" font-size="10" font-family="DejaVu Sans Mono, monospace" fill="#9ef0a0">{c}</text>')

add('</svg>')
open('/home/user/Claidegithub/schema/state-machine.svg','w',encoding='utf-8').write('\n'.join(svg))
print('state-machine SVG written')
