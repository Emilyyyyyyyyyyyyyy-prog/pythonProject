import math
import matplotlib.pyplot as plt

G = 6.67e-11  # гравитационная постоянная
M_earth = 5.974e24  # масса Земли
g = 9.81  # начальное ускорение свободного падения
R_earth = 6378100  # радиус Земли
T_earth = 23 * 3600 + 56 * 60 + 4  # период вращения Земли вокруг оси
orbit = (G * M_earth * T_earth ** 2 / (4 * math.pi ** 2)) ** (1 / 3)  # целевая орбита
print("\nРадиус целевой геостационарной орбиты =", round(orbit / 1000, ), "км")
k = 0.05  # - отношение массы баков к массе заправленной ступени
k0 = round((1 - k) / k, 8)
mas_max = 4000 * 300 * 6378100 ** 2 / (G * M_earth)

M1 = 84000  # масса заправленной 1 ступени
M2 = 6505  # масса заправленной 2 ступени
M3 = 1450  # масса заправленной 3 ступени
m3p = 5  # масса полезной нагрузки 3 ступени
m3b = M3 * k  # масса баков 3 ступени
m3t = M3 * (1 - k)  # масса топлива 3 ступени
m2p = M3 + m3p  # масса полезной нагрузки 2 ступени
m2b = M2 * k  # масса баков 2 ступени
m2t = M2 * (1 - k)  # масса топлива 2 ступени
m1p = M2 + m2p  # масса полезной нагрузки 1 ступени
m1b = M1 * k  # масса баков 1 ступени
m1t = M1 * (1 - k)  # масса топлива 1 ступени
mt = m1t  # текущая масса топлива
m = M1 + M2 + M3 + m3p  # текущая масса КА

U1 = 4000
U2 = 3000
U3 = 461
mu1 = 300
mu2 = 200
mu3 = 50
mu = mu1  # текущий расход топлива
U = U1  # текущий удельный имульс двигателя

ro0 = 1.2
h0 = 9000
S = 2  # эффективная площадь головного обтекателя
Cx = 0.4  # аэродинамический коэффициент головного обтекателя

x0 = 0  # координата x центра Земли
y0 = 0  # координата y центра Земли

x = x0  # стартовая координата x КА
y = y0 + R_earth  # стартовая координата y КА
stage = 1  # номер активной ступени
v = (0, 0)  # стартовая скорость: 0 м/с, угол к оси y = 0
t = 0  # время от старта
dt = 0.1  # текущее изменение времени
t_fin = 0  # время завершения работы ступени

trace = []  # координаты точек для прорисовки графика

engine = True

print("Исходные параметры ракеты не позволяют вывести ракету на заданную орбиту.")
print("Рассчитаем, какие параметры ракеты нужны для успешного запуска.")
print("Максимальная подъёмная масса для двигателя 1 ступени =", round(mas_max, 3), "кг")
print("При такой массе не получается вывести 3-ю ступень с массой более 1450 кг.")
print("1 ступень выводит ракету на высоту примерно в 400 км,")
print("2 ступень для выхода на геостационарную орбиту увеличивает скорость примерно до 10, "
      "1 км/с,")
print("в таком случае в апогее эллипса скорость становится около 1,5 км/с.")
print("Целевая орбитальная скорость - около 3 км/с,")
print("необходимо увеличить скорость на 1,5 км/с, но топлива в 3 ступени массой 1450 кг хватает "
      "только примерно на +0,5 км/с.")
print("Увеличение скорости на 1 км/с за счёт сброса")
print("3 ступени, скорее всего, приведёт к повреждению спутника.")
print("Поэтому необходимо изменить параметры ракеты.")
print("Чтобы увеличить топливо на 3 ступени в 3 раза, нужно примерно во столько же раз увеличить "
      "массу 1 ступени,")
print("то есть поставить 3 двигателя и увеличить в 3 раза расход топлива.")
print("Это в несколько раз увеличит стоимость миссии.")
print("Выгоднее будет поставить на 3 ступень более эффективный двигатель,")
print("который с тем же объёмом топлива даст больший импульс.")
print("Новые параметры ступеней: M1 = 84000 кг, M2 = 6505 кг, M3 = 1450 кг, U3 = 461 м/с.")
print()


def fgr():  # расчёт силы гравитационного притяжения Земли
    return G * M_earth * m / (x ** 2 + y ** 2)


def fair():  # расчёт силы сопротивления воздуха
    if stage != 1:
        return 0
    h = dist() - R_earth
    if h >= 10 * h0:
        f = 0
    else:
        ro = ro0 * math.exp(-h / h0)
        f = Cx * ro * v[0] ** 2 * S / 2
    return f


def angle_sort(v1, v2):  # сортировка векторов в порядке уменьшения угла
    if v1[1] - v2[1] > math.pi:
        v1 = (v1[0], v1[1] - math.pi * 2)
    if v1[1] < v2[1]:
        v1, v2 = v2, v1
    return v1, v2


def angle_norm(angle):  # нормировка угла в область от 0 до 2pi
    return (angle + math.pi * 20) % (math.pi * 2)


def v12sum(v1, v2):  # сумма двух векторов скоростей
    if v1[0] == 0:
        return v2
    elif v2[0] == 0:
        return v1
    v1, v2 = angle_sort(v1, v2)
    if v1[1] == v2[1]:
        v_val = v1[0] + v2[0]
        v_ang = v1[1]
    else:
        ang = math.pi - (v1[1] - v2[1])
        v_val = (v1[0] ** 2 + v2[0] ** 2 - 2 * v1[0] * v2[0] * math.cos(ang)) ** 0.5
        cos_gamma = (v2[0] ** 2 - v_val ** 2 - v1[0] ** 2) / (-2 * v_val * v1[0])
        cos_gamma = round(cos_gamma, 6)
        v_ang = angle_norm(v1[1] - math.acos(cos_gamma))
        v_ang = round(v_ang, 6)
    return v_val, v_ang


def speed(v0, a):  # расчёт изменения скорости под влиянием ускорения (величина, угол к оси y)
    a = (a[0] * dt, a[1])
    v1, v2 = angle_sort(v0, a)
    v_val, v_ang = v12sum(v1, v2)
    return v_val, v_ang


def fen():  # расчёт силы ракетного двигателя
    if not engine:
        return 0
    global mt, t_fin, m
    if mt == 0:
        f = 0
    else:
        f = mu * U
        if mt <= mu * dt:
            f = f * mt / (mu * dt)
            m -= (mu - mt)
            t_fin = mt / (mu * dt) + t
            mt = 0
            if stage < 4:
                stage_change()
        else:
            mt -= mu * dt
            m -= mu * dt
        return f


def angle():  # расчёт угла направления на Землю
    if y == 0 and x > 0:
        ang = math.pi * 3 / 2
    elif y == 0 and x < 0:
        ang = math.pi * 1 / 2
    elif x == 0 and y > 0:
        ang = math.pi
    elif x == 0 and y < 0:
        ang = 0
    elif y < 0:
        ang = (math.atan(x / y)) % (math.pi * 2)
    else:
        ang = (math.pi + math.atan(x / y)) % (math.pi * 2)
    return ang


def acc():  # расчёт ускорения под действием сил
    f1 = fgr()
    a_f1 = f1 / m
    f1_ang = angle()
    f2 = fen() - fair()
    a_f2 = f2 / m
    if f2 == 0:
        return a_f1, f1_ang
    if stage == 3 and engine:
        f2_ang = (angle() + math.pi * 3 / 2 + 0.48) % (math.pi * 2)
    else:
        f2_ang = v[1]
    a1 = (a_f1, f1_ang)
    a2 = (a_f2, f2_ang)
    a1, a2 = angle_sort(a1, a2)
    a_val, a_ang = v12sum(a1, a2)
    return a_val, a_ang


def dist():  # расчёт расстояния до центра координат (центра Земли)
    return (x ** 2 + y ** 2) ** 0.5


def move():  # расчёт перемещения
    global v, x, y
    a = acc()
    v = speed(v, a)
    x += v[0] * math.sin(v[1]) * dt
    y += v[0] * math.cos(v[1]) * dt
    trace.append((t, x, y, dist()))
    return x, y


def flight_graf(stage):  # построение графиков
    x1 = [i[1] for i in trace]
    y1 = [i[2] for i in trace]
    fig1, ax1 = plt.subplots()
    ax1.plot(x1, y1)
    ax1.grid()
    name1 = "stage" + str(stage) + "_1.png"
    fig1.savefig(name1)

    x2 = [i[0] for i in trace]
    y2 = [i[3] for i in trace]
    fig2, ax2 = plt.subplots()
    ax2.plot(x2, y2)
    ax2.grid()
    name2 = "stage" + str(stage) + "_2.png"
    fig1.savefig(name2)


def stage_change():  # смена ступени
    global v
    print("Cтупень", stage, "завершила работать на", round(t_fin, 2), "с")
    r = round(((x ** 2 + y ** 2) ** 0.5) / 1000, 3)
    h = round(r - R_earth / 1000, 3)
    print("Растояние до центра Земли =", r, "км, высота =", h, "км")
    print("Скорость КА =", round(v[0] / 1000, 3), "км/с")
    if stage < 3:
        print("Ступень", stage, "отделилась.\n")
    flight_graf(stage)
    if stage == 1:
        stage_1_fin()
    elif stage == 2:
        stage_2_fin()
    elif stage == 3:
        stage_3_fin()


def alf():  # расчёт угола альфа
    f1 = fgr()
    f2 = mu * U
    f2_ang = math.acos(f1 / f2)
    return f2_ang


def stage_1_fin():  # завершение работы 1 ступени
    global v, stage, m, mt, U, mu
    v_hor = 2 * math.pi * (R_earth + h) / T_earth
    print("Меняем систему отсчёта - учитываем вращение Земли. "
          "Будем считать, что КА стартовал с экватора,\nдобавляем ему горизонтальную скорость"
          ", равную", round(v_hor, 2), "м/с")
    v2 = (v_hor, math.pi / 2)
    v = v12sum(v, v2)
    print("Принцип расчёта угла поворота альфа: результирующая сила должна быть направлена"
          " перпендикулярно направлению на Землю.")
    stage = 2
    m = M2 + M3 + m3p
    mt = m2t
    U = U2
    mu = mu2
    ang = alf()
    ang_deg = round(ang / (2 * math.pi) * 360, 2)
    print("Угол альфа =", round(ang, 4), "рад или", ang_deg, "градуса")
    print()
    v = (v[0], ang)


def stage_2_fin():  # завершение работы 2 ступени
    global stage, m, mt, U, mu, engine
    stage = 3
    m = M3 + m3p
    mt = m3t
    U = U3
    mu = mu3
    engine = False


def stage_3_fin():  # завершение работы 3 ступени
    global stage, m, mt, engine, v
    print("Завершилась отработка 3 ступени.")
    print("Высота орбиты =", round(dist() / 1000, 3), "км")
    angle_change = v[1] - (angle() - math.pi / 2)
    print("Третья ступень при сбрасывании используется для корректировки угла движения КА на угол",
          round(angle_change, 4), "то есть", round(angle_change * 360 / (2 * math.pi), 2),
          "градуса")
    print("Масса КА =", m3p, "кг,", "масса отработанной ступени =", m3b, "кг.")
    imp = (2 * v[0] ** 2 - 2 * v[0] ** 2 * math.cos(angle_change)) ** 0.5 * m3p
    print("Для смены траектории передаётся импульс, равный", round(imp), "кг * м / с")
    print("Выход на геостационарную орбиту завершён!")

    v = (v[0], v[1] - angle_change)
    stage = 4
    m = m3p
    mt = 0
    engine = False


while t < 300000:
    if not engine:
        dt = 10
    else:
        dt = .1
    t += dt
    x, y = move()
    h = (dist() - R_earth) / 1000
    if dist() >= orbit:
        if not engine and stage == 3:
            engine = True

flight_graf(stage)
plt.show()
