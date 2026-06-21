(*
  Управление одноколонным штабелёром — скелет на CODESYS (Structured Text).
  Реализует конечный автомат из state-machine.svg и логику из
  asu-tp-specification.md (раздел 4): вызов с этажа, выбор этажа назначения,
  забор паллеты с места погрузки, доставка, блокировка по открытым воротам
  с индикацией на всех панелях, контроль занятости места выгрузки.

  Назначение файла — каркас для переноса в проект cMT3072X (CODESYS).
  Адреса входов/выходов — см. io-wiring-diagram.svg и io-list.csv.
  Платформа: Weintek cMT3072X (CODESYS), удалённый в/в Weintek iR.
*)

(* ---------- Типы ---------- *)
TYPE E_State :
(
    S0_INIT := 0,      // инициализация, самотест
    S1_HOME,           // калибровка (поиск референса по высоте)
    S2_IDLE,           // ожидание вызова
    S3_TO_SRC,         // движение к этажу-источнику
    S4_PICK,           // захват паллеты с места погрузки
    S5_TO_DST,         // движение к этажу назначения
    S6_CHECK,          // проверка занятости места выгрузки
    S7_UNLOAD,         // выгрузка паллеты
    S8_WAIT_PLACE,     // ожидание освобождения места (паллета на вилах)
    G1_GATE_STOP,      // блокировка: открыты ворота на каком-то этаже
    G2_ESTOP,          // аварийный останов / контур безопасности
    G3_FAULT           // авария привода / таймаут / рассогласование
);
END_TYPE

(* ---------- Программа ---------- *)
PROGRAM StackerControl
VAR CONSTANT
    NFL : INT := 5;                         // число этажей
END_VAR
VAR
    eState   : E_State := S0_INIT;          // текущее состояние
    eReturn  : E_State;                     // состояние возврата после блокировки ворот

    (* --- Входы (DI), отображаются на модули Weintek iR --- *)
    xFloorA   : ARRAY[1..NFL] OF BOOL;      // SQna — точная остановка, канал A
    xFloorB   : ARRAY[1..NFL] OF BOOL;      // SQnb — точная остановка, канал B
    xOverrun  : ARRAY[1..NFL] OF BOOL;      // SQnc — перебег этажа
    xGateClosed : ARRAY[1..NFL] OF BOOL;    // SQn.1 — ворота этажа закрыты
    xPlaceBusy  : ARRAY[1..NFL] OF BOOL;    // BGn  — место погр./выгр. занято
    xCall       : ARRAY[1..NFL] OF BOOL;    // вызов с панели этажа (по сети cMT)
    iCallDest   : ARRAY[1..NFL] OF INT;     // выбранный этаж назначения с панели n
    xForkIn   : BOOL;                       // SQ8.1 — вилы убраны
    xForkLeft : BOOL;                       // SQ8.2 — вилы влево
    xForkRight: BOOL;                       // SQ8.3 — вилы вправо
    xPalletOnFork : BOOL;                   // BG0 — паллета на вилах
    xTopLimit : BOOL;                       // SQ0 — перебег верх
    xBotLimit : BOOL;                       // SQ9 — перебег низ
    xSafeOK   : BOOL;                       // KSR_OK — контур безопасности замкнут

    (* --- Выходы (DO) --- *)
    xLock     : ARRAY[1..NFL] OF BOOL;      // YLn — замки ворот
    xLampRun  : BOOL;                       // HL1 — «штабелёр в работе»
    xLampAlarm: BOOL;                       // HL2 — «авария»
    xLampBusy : BOOL;                       // HL3 — «место занято»
    xDriveEnable : BOOL;                    // KM2 — разрешение/готовность ПЧ

    (* --- Интерфейс к приводам (по полевой шине) --- *)
    rTargetPos : REAL;                      // задание положения каретки (этаж)
    xLiftDone  : BOOL;                      // каретка достигла цели (по BR1 + SQ)
    xForkCmdExtend, xForkCmdRetract : BOOL; // команды вил
    xLiftFault, xForkFault : BOOL;          // авария ПЧ

    (* --- Тэги для индикации на ВСЕХ панелях (общие в cMT-сервере) --- *)
    sStatus     : STRING;                   // текстовое состояние
    iOpenGate   : INT;                      // номер этажа с открытыми воротами (0 — нет)
    xAnyGateOpen: BOOL;

    (* --- Рабочие переменные задания --- *)
    iSrc : INT;                             // этаж-источник
    iDst : INT;                             // этаж-назначения
    i    : INT;
END_VAR

(* === 1. Общая диагностика (выполняется каждый цикл) === *)
xAnyGateOpen := FALSE;
iOpenGate := 0;
FOR i := 1 TO NFL DO
    IF NOT xGateClosed[i] THEN
        xAnyGateOpen := TRUE;
        iOpenGate := i;                     // последний открытый (для индикации)
    END_IF
END_FOR

xLampAlarm := (eState = G2_ESTOP) OR (eState = G3_FAULT);
xLampRun   := (eState >= S3_TO_SRC) AND (eState <= S8_WAIT_PLACE);

(* === 2. Глобальные приоритетные переходы (из любого рабочего состояния) === *)
IF NOT xSafeOK THEN
    eState := G2_ESTOP;
ELSIF xLiftFault OR xForkFault OR xTopLimit OR xBotLimit THEN
    eState := G3_FAULT;
ELSIF xAnyGateOpen AND (eState >= S3_TO_SRC) AND (eState <= S8_WAIT_PLACE) THEN
    eReturn := eState;                      // запомнить, куда вернуться
    eState := G1_GATE_STOP;
END_IF

(* === 3. Основной автомат === *)
CASE eState OF

    S0_INIT:
        sStatus := 'Инициализация';
        xDriveEnable := FALSE;
        FOR i := 1 TO NFL DO xLock[i] := TRUE; END_FOR   // все ворота заперты
        IF xSafeOK THEN eState := S1_HOME; END_IF

    S1_HOME:
        sStatus := 'Калибровка';
        xDriveEnable := TRUE;
        (* поиск референса: опустить до SQ9 / известный этаж *)
        IF xLiftDone THEN eState := S2_IDLE; END_IF

    S2_IDLE:
        sStatus := 'Ожидание вызова';
        // выбор задания из очереди вызовов
        FOR i := 1 TO NFL DO
            IF xCall[i] AND (iCallDest[i] >= 1) AND (iCallDest[i] <= NFL)
               AND (iCallDest[i] <> i) THEN
                iSrc := i;
                iDst := iCallDest[i];
                xCall[i] := FALSE;
                EXIT;
            END_IF
        END_FOR
        // пуск только при закрытых воротах и исправном контуре
        IF (iSrc >= 1) AND (NOT xAnyGateOpen) AND xSafeOK THEN
            eState := S3_TO_SRC;
        END_IF

    S3_TO_SRC:
        sStatus := CONCAT('К этажу-источнику ', INT_TO_STRING(iSrc));
        rTargetPos := FloorPos(iSrc);
        IF AtFloor(iSrc) THEN eState := S4_PICK; END_IF

    S4_PICK:
        sStatus := 'Захват паллеты';
        IF NOT xPlaceBusy[iSrc] THEN
            // на месте погрузки нет паллеты — отмена задания
            sStatus := 'Нет паллеты на месте — отмена';
            iSrc := 0;
            eState := S2_IDLE;
        ELSE
            xForkCmdExtend := TRUE;                  // выдвинуть, поднять, убрать
            IF xPalletOnFork AND xForkIn THEN
                xForkCmdExtend := FALSE;
                eState := S5_TO_DST;
            END_IF
        END_IF

    S5_TO_DST:
        sStatus := CONCAT('К этажу назначения ', INT_TO_STRING(iDst));
        rTargetPos := FloorPos(iDst);
        IF AtFloor(iDst) THEN eState := S6_CHECK; END_IF

    S6_CHECK:
        sStatus := 'Проверка места выгрузки';
        IF NOT xPlaceBusy[iDst] THEN
            eState := S7_UNLOAD;                     // свободно — выгружаем
        ELSE
            eState := S8_WAIT_PLACE;                 // занято — ждём
        END_IF

    S7_UNLOAD:
        sStatus := 'Выгрузка';
        xForkCmdExtend := TRUE;                      // выдвинуть, опустить, убрать
        IF (NOT xPalletOnFork) AND xForkIn THEN
            xForkCmdExtend := FALSE;
            iSrc := 0; iDst := 0;
            eState := S2_IDLE;                       // цикл завершён
        END_IF

    S8_WAIT_PLACE:
        sStatus := CONCAT('Место занято, этаж ', INT_TO_STRING(iDst));
        xLampBusy := TRUE;                           // сигнал «занято» на всех панелях
        // штабелёр стоит на этаже Y, паллета на вилах
        IF NOT xPlaceBusy[iDst] THEN
            xLampBusy := FALSE;
            eState := S7_UNLOAD;                     // место освободилось — выгрузка
        END_IF

    G1_GATE_STOP:
        sStatus := CONCAT('БЛОКИРОВКА: открыты ворота, этаж ', INT_TO_STRING(iOpenGate));
        xDriveEnable := FALSE;                        // СТОП движения
        // индикация iOpenGate транслируется на все панели (общий тэг)
        IF NOT xAnyGateOpen THEN
            // ворота закрыты — ждём квитирования и возвращаемся
            eState := eReturn;
        END_IF

    G2_ESTOP:
        sStatus := 'АВАРИЙНЫЙ ОСТАНОВ';
        xDriveEnable := FALSE;                        // STO + тормоз — аппаратно (KSR)
        IF xSafeOK THEN eState := S0_INIT; END_IF     // после сброса/квитирования

    G3_FAULT:
        sStatus := 'АВАРИЯ ПРИВОДА';
        xDriveEnable := FALSE;
        IF xSafeOK AND NOT (xLiftFault OR xForkFault) THEN
            eState := S0_INIT;                        // после устранения и сброса
        END_IF

END_CASE

(* === 4. Вспомогательные функции (заглушки) ===
   FloorPos(n) — координата этажа n (мм / отсчёты энкодера BR1)
   AtFloor(n)  — TRUE, если каретка на этаже n: xLiftDone AND xFloorA[n] AND xFloorB[n]
   Реализуются как FUNCTION в проекте.
*)
END_PROGRAM
