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


def Aestrella(inicio, fin):
    camino = [inicio]
    caminos = [camino, 0]
    lista = [caminos]
    vistos = []
    resultado = None

    while True:
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

        if posicion not in vistos:
            vistos.append(posicion)
        for v in vecinos(ruta):
            if v not in ruta and v not in vistos:
                nueva_ruta = ruta + [v]
                nuevos_pasos = pasos + 1
                lista.append([nueva_ruta, nuevos_pasos])

    return resultado

camino = Aestrella((6,0), (0,11))
print(camino)