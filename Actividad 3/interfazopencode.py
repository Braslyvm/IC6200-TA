import pygame
import sys
import time

# ================= TU LOGICA ORIGINAL (NO MODIFICADA) =================
Matriz = [
    [0,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,0,0,0,0,0,0,0,0,0,1],
    [0,1,0,1,1,1,1,1,1,1,0,1],
    [0,1,0,1,0,0,0,0,0,1,0,1],
    [0,1,1,1,0,1,1,1,1,1,0,1],
    [0,0,0,1,0,1,0,0,0,0,0,1], 
    [1,1,1,1,0,1,1,1,1,1,1,1]
]

def mahantan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def vecinos(camino):
    ultimo = camino[-1]
    x = ultimo[0]
    y = ultimo[1]
    lista = []
    if x - 1 >= 0:
        if Matriz[x-1][y] == 1:
            if (x-1, y) not in camino:
                lista.append((x-1, y))
    if x + 1 < len(Matriz):
        if Matriz[x+1][y] == 1:
            if (x+1, y) not in camino:
                lista.append((x+1, y))
    if y - 1 >= 0:
        if Matriz[x][y-1] == 1:
            if (x, y-1) not in camino:
                lista.append((x, y-1))
    if y + 1 < len(Matriz[0]):
        if Matriz[x][y+1] == 1:
            if (x, y+1) not in camino:
                lista.append((x, y+1))
    return lista

def Calcularpeso(camino, fin):
    ruta = camino[0]
    pasos = camino[1]
    ult = ruta[-1]
    return pasos + mahantan(ult, fin)

def mejor(lista, fin):
    m = lista[0]
    for cam in lista:
        if Calcularpeso(cam, fin) < Calcularpeso(m, fin):
            m = cam
    return m

# ================= PYGAME =================
pygame.init()

TAM = 60
FILAS = len(Matriz)
COLS = len(Matriz[0])

WIDTH = COLS * TAM + 220
HEIGHT = FILAS * TAM

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Visual")

# Colores
BG = (25,25,35)
CAMINO = (50,50,70)
MURO = (10,10,10)
GRID = (90,90,120)
INICIO_C = (0,255,120)
FIN_C = (255,80,80)
EXPLORADO = (255,200,0)
FINAL = (100,180,255)
TEXTO = (240,240,240)
BOTON = (120,140,255)

inicio = None
fin = None

font = pygame.font.SysFont("consolas", 20)

btn_start = pygame.Rect(WIDTH-200, 40, 160, 50)
btn_reset = pygame.Rect(WIDTH-200, 110, 160, 50)

# ================= DIBUJO =================
def draw():
    screen.fill(BG)

    for i in range(FILAS):
        for j in range(COLS):
            color = CAMINO if Matriz[i][j] == 1 else MURO
            pygame.draw.rect(screen, color, (j*TAM, i*TAM, TAM, TAM))
            pygame.draw.rect(screen, GRID, (j*TAM, i*TAM, TAM, TAM), 1)

    if inicio:
        pygame.draw.rect(screen, INICIO_C, (inicio[1]*TAM, inicio[0]*TAM, TAM, TAM))
    if fin:
        pygame.draw.rect(screen, FIN_C, (fin[1]*TAM, fin[0]*TAM, TAM, TAM))

    # Panel lateral
    pygame.draw.rect(screen, (30,30,50), (COLS*TAM, 0, 220, HEIGHT))

    # Texto
    textos = [
        "CLICK: Inicio",
        "CLICK: Final",
        "",
        "START: Ejecutar",
        "RESET: Reiniciar",
        "",
        "Colores:",
        "Verde = Inicio",
        "Rojo = Fin",
        "Amarillo = Explora",
        "Azul = Camino"
    ]

    for i, t in enumerate(textos):
        txt = font.render(t, True, TEXTO)
        screen.blit(txt, (COLS*TAM + 10, 200 + i*22))

    # Botones
    pygame.draw.rect(screen, BOTON, btn_start, border_radius=8)
    pygame.draw.rect(screen, BOTON, btn_reset, border_radius=8)

    screen.blit(font.render("START", True, (0,0,0)), (btn_start.x + 45, btn_start.y + 15))
    screen.blit(font.render("RESET", True, (0,0,0)), (btn_reset.x + 45, btn_reset.y + 15))

# ================= ANIMACION (USA TU LOGICA) =================
def animar(inicio, fin):
    camino = [inicio]
    caminos = [camino, 0]
    lista = [caminos]
    vistos = []
    resultado = None

    while True:
        draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for caminos in lista:
            if fin in caminos[0]:
                resultado = caminos[0]
                break

        if resultado != None:
            break

        if len(lista) == 0:
            break

        act = mejor(lista, fin)
        lista.remove(act)

        ruta = act[0]
        pasos = act[1]
        posicion = ruta[-1]

        # Dibujar TODO el camino recorrido hasta ahora
        for p in ruta:
            pygame.draw.rect(screen, EXPLORADO, (p[1]*TAM, p[0]*TAM, TAM, TAM))
        pygame.display.update()
        time.sleep(0.08)

        if posicion not in vistos:
            vistos.append(posicion)

        for v in vecinos(ruta):
            if v not in ruta and v not in vistos:
                nueva_ruta = ruta + [v]
                nuevos_pasos = pasos + 1
                lista.append([nueva_ruta, nuevos_pasos])

    # Dibujar camino final
    if resultado:
        for p in resultado:
            pygame.draw.rect(screen, FINAL, (p[1]*TAM, p[0]*TAM, TAM, TAM))
            pygame.display.update()
            time.sleep(0.05)

# ================= LOOP =================
running = True

while running:
    draw()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if btn_start.collidepoint(x, y):
                if inicio and fin:
                    animar(inicio, fin)

            elif btn_reset.collidepoint(x, y):
                inicio = None
                fin = None

            else:
                col = x // TAM
                fila = y // TAM

                if col < COLS and fila < FILAS:
                    if Matriz[fila][col] == 1:
                        if not inicio:
                            inicio = (fila, col)
                        elif not fin:
                            fin = (fila, col)

pygame.quit()
