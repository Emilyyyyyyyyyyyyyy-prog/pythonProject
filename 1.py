import sys
import pygame
import math

pygame.init()

width = 1400
height = 900

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('FLIGHT')
clock = pygame.time.Clock()
FPS = 60
bg = pygame.image.load("stars.jpg")
bg = pygame.transform.scale(bg, (width, height))

M1 = 80000  # кг
U1 = 4000  # м/с
mu1 = 300  # кг/с
k = 0.05
M1b = M1 * k
ro0 = 1.2  # кг/м3
h0 = 9000  # м
S = 2  # м2
Cx = 0.4
g = 9.81  # м/с2, начальное ускорение свободного падения
R_earth = 6378100  # м
G = 6.67 * pow(10, -11)  # гравитационная постоянная
M_earth = 5.974 * pow(10, 24)  # кг, масса Земли
T_earth = 23 * 3600 + 56 * 60 + 4  # с, период вращения Земли вокруг оси

M2 = 30000  # кг
M2b = M2 * k  # кг
U2 = 3000  # м/с
mu2 = 200  # кг/с
v_t_start = 2 * math.pi * R_earth / T_earth  # м/с, линейная скорость на экваторе Земли
v_t = v_t_start  # м/с
alf = 0  # угол в радианах
v_l = 0

x0 = 450
y0 = 450  # координаты центра Земли

scale = 100000  # масштаб: в 1 пикселе 100000 м
x_R = round(R_earth / scale)  # радиус Земли в масштабе для прорисовки
orbit = pow(G * M_earth * pow(T_earth, 2) / (4 * pow(math.pi, 2)), 1 / 3)
x_Orbit = round(orbit / scale)
# целевая геостационарная орбита - радиус в пикселях

t = 0
h = 0
v = 0
a_scale = 0
h_3 = 0

flag = False
flag2 = False
flag3 = False
flag4 = False
stage = 1

x1 = x0  # начальные координаты ракеты для прорисовки
y1 = y0 + x_R - 20  # учитывается радиус Земли и поправка на картинку
trace = [(x1, y1)]  # данные траектории
x_start = 0
y_start = R_earth

x = 0  # координаты в системе x,y в метрах
y = R_earth

while True:
    dt = clock.tick(50) / 1000.0
    screen.blit(bg, (0, 0))
    pygame.draw.line(screen, (150, 10, 50), (900, 0), (900, 900), 2)
    font1 = pygame.font.Font(None, 60)
    font2 = pygame.font.Font(None, 35)
    font3 = pygame.font.Font(None, 20)
    text1 = font1.render("Выход на орбиту", True, (150, 0, 0))
    place1 = text1.get_rect(center=(1100, 50))
    screen.blit(text1, place1)
    text3 = font2.render("Время полёта " + str(int(t)) + " с", True, (150, 0, 0))
    place3 = text1.get_rect(center=(1100, 100))
    screen.blit(text3, place3)
    text4 = font2.render("Ступень = " + str(stage), True, (150, 0, 0))
    place4 = text1.get_rect(center=(1100, 130))
    screen.blit(text4, place4)

    if not flag4:
        h_earth = abs(((x ** 2 + y ** 2) ** 0.5 - R_earth) / 1000)
    else:
        h_earth = h_3
    text5 = font2.render("Высота " + str(round(h_earth, 2)) + " км", True, (150, 0, 0))
    place5 = text1.get_rect(center=(1100, 160))
    screen.blit(text5, place5)

    if stage == 3:
        if not flag2:
            h_2 = str(round(h_earth)) + " км"
            flag2 = True
        if not flag4:
            text6 = font2.render("После 2-ой ступени: высота =" + h_2, True, (150, 0, 0))
            place6 = text1.get_rect(center=(1100, 200))
            screen.blit(text6, place6)
            text7 = font2.render("Идём по эллипсу", True, (150, 0, 0))
            place7 = text1.get_rect(center=(1100, 230))
            screen.blit(text7, place7)

    if not flag:
        text2 = font2.render("Нажмите любую клавишу, чтобы запустить", True, (150, 100, 0))
        place2 = text2.get_rect(center=(450, 750))
        screen.blit(text2, place2)

    #    pygame.draw.circle(screen, (255, 255, 255), (round(x0), round(y0)), x_Orbit, 2)
    earth = pygame.image.load("earth.png")
    earth = pygame.transform.scale(earth, (x_R + 36, x_R + 36))
    screen.blit(earth, (x0 - x_R + 50 - 36, y0 - x_R + 50 - 36))

    pygame.draw.line(screen, (150, 150, 50), (450, 450), (450, 700), 1)
    pygame.draw.line(screen, (150, 150, 50), (450, 450), (700, 450), 1)
    text8 = font3.render("Y", True, (150, 150, 50))
    place8 = text8.get_rect(center=(470, 650))
    screen.blit(text8, place8)
    text9 = font3.render("X", True, (150, 150, 50))
    place9 = text9.get_rect(center=(650, 470))
    screen.blit(text9, place9)
    text12 = font3.render("V", True, (150, 150, 50))
    place12 = text12.get_rect(center=(450, 700))
    screen.blit(text12, place12)
    text13 = font3.render(">", True, (150, 150, 50))
    place13 = text13.get_rect(center=(700, 450))
    screen.blit(text13, place13)

    pygame.draw.line(screen, (150, 150, 50), (950, 350), (950, 700), 1)
    pygame.draw.line(screen, (150, 150, 50), (950, 700), (1300, 700), 1)
    text10 = font3.render("h", True, (150, 150, 50))
    place10 = text10.get_rect(center=(970, 370))
    screen.blit(text10, place10)
    text11 = font3.render("t", True, (150, 150, 50))
    place11 = text11.get_rect(center=(1280, 680))
    screen.blit(text11, place11)
    text14 = font3.render("Λ", True, (150, 150, 50))
    place14 = text14.get_rect(center=(950, 350))
    screen.blit(text14, place14)
    text14 = font3.render(">", True, (150, 150, 50))
    place14 = text14.get_rect(center=(1300, 700))
    screen.blit(text14, place14)

    for point in trace:
        pygame.draw.circle(screen, (255, 0, 0), (point[0], point[1]), 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            flag = True
    if flag:
        g = G * M_earth / pow(h_earth * 1000 + R_earth, 2)
        ro = ro0 * math.exp(-h / h0)
        if h < 10 * h0:
            Fc = Cx * ro * v ** 2 * S / 2
        else:
            Fc = 0
        if M1 > M1b:
            t += 1
            Ft = M1 * g
            F = -Ft - Fc
            a = (F + mu1 * U1) / M1
            v += a
            h += v
            y += v
            M1 = M1 - mu1
            z = (round((x - x_start) / scale + x0), round((y - y_start) / scale + y0 + x_R - 20))
            pygame.draw.circle(screen, (255, 100, 0), z, 4)
            z1 = (950 + int(t / 100), 700 - int(h_earth / 100))
            pygame.draw.circle(screen, (255, 100, 0), (z1), 2)
            if z not in trace:
                trace.append(z)
            if z1 not in trace:
                trace.append(z1)

        elif M2 > M2b and v < 10000 and not flag3:
            t += 1
            stage = 2
            Ft = M2 * g
            Fcb = pow(v_t, 2) / h_earth
            F = Fcb - Ft
            # находим угол приложения тяги, чтобы результирующая сила была перпендикулярна
            # направлению на центр Земли. Это позволит увеличить линейную скорость. Чем выше
            # линейная скорость в перигее, тем дальше будет апогей.
            beta = math.asin(abs(F / (mu2 * U2)))
            Frez = mu2 * U2 * math.cos(beta)
            a = Frez / M2
            v += a
            v_t = v * math.cos(beta)
            v_l = 0
            y += v_l
            x += v_t
            y1 += v_l
            x1 += (v_t - v_t_start)
            M2 = M2 - mu2
            z = (round((x - x_start) / scale + x0), round((y - y_start) / scale + y0 + x_R - 20))
            pygame.draw.circle(screen, (255, 100, 0), z, 4)
            z1 = (950 + int(t / 100), 700 - int(h_earth / 100))
            pygame.draw.circle(screen, (255, 100, 0), (z1), 2)
            if z not in trace:
                trace.append(z)
            if z1 not in trace:
                trace.append(z1)
        elif not flag4:
            if stage == 2:
                rp = h_earth * 1000 + R_earth  # м, расстояние перигея
                vp = v  # м/с, скорость в перигее
                a = (rp + orbit) / 2  # большая полуось для элиптической орбиты
                e = 1 - rp / a  # эксцентриситет
                k1 = (1 - e ** 2) ** 0.5  # коэффициент сжатия
                b = k1 * a  # малая полуось
                x_2 = z[0]  # координаты завершения 2-ой стадии на карте
                y_2 = z[1]
                t_2 = 2 * math.pi * (a ** 3 / (G * M_earth)) ** 0.5 / 2  # полупериод эллипт. орбиты
                a_scale = a / scale  # м / пиксель по вертикали
                b_scale = b / scale
                x0_2 = x_2  # центр эллипса на картинке
                y0_2 = (y_2 - (x0 - x_Orbit)) / 2 + (x0 - x_Orbit)  # центр эллипса на картинке
                dt1 = int(round(t_2 / ((y_2 - y0_2) * 2)))
                flag3 = True
                x1_2 = 0
                y1_2 = y - a

            t += dt1
            y -= scale
            if (y - y1_2) <= a and y > -42000000:
                x = x1_2 + b * (1 - (y - y1_2) ** 2 / a ** 2) ** 0.5
                z = (round(x / scale + x0), round(((y - y_start) / scale + y0 + x_R) * 0.955 + 3))
                pygame.draw.circle(screen, (255, 100, 0), z, 4)
                z1 = (950 + int(t / 100), 700 - int(h_earth / 100))
                pygame.draw.circle(screen, (255, 100, 0), (z1), 2)
                if z not in trace:
                    trace.append(z)
                if z1 not in trace:
                    trace.append(z1)
            else:
                y_3 = y
                x_3 = x
                gamma = -0.05
                h_3 = h_earth
                a_3 = orbit
                t_3 = 2 * math.pi * (a_3 ** 3 / (G * M_earth)) ** 0.5  # период круг.орбиты
                dt_3 = t_3 * 0.01 / (2 * math.pi)
                flag4 = True
            stage = 3
        else:
            t += dt_3
            y = + (y_3 / 0.955) * math.cos(gamma) + 2000000
            x = + y_3 * math.sin(gamma)
            gamma += 0.01
            z = (round(x / scale + x0), round(((y - y_start) / scale + y0 + x_R) * 0.955 + 3))
            pygame.draw.circle(screen, (255, 100, 0), z, 4)
            z1 = (950 + int(t / 100), 700 - int(h_earth / 100))
            pygame.draw.circle(screen, (255, 100, 0), (z1), 2)
            if z not in trace:
                trace.append(z)
            if z1 not in trace:
                trace.append(z1)

    pygame.time.delay(10)
    pygame.display.flip()
