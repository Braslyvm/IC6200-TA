optimo = []
  
grafo = {
    "Oradea": {"Zerind":71, "Sibiu": 151},
    "Zerind": {"Oradea": 71, "Arad": 75},
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Sibiu": {"Oradea": 151, "Arad": 140, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Rimnicu Vilcea": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti":138},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},  
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87} 
}

def calcularcosto():
    costos = []
    for ruta in optimo:
        costo = 0
        for i in range(len(ruta) - 1):
            costo += grafo[ruta[i]][ruta[i + 1]]
        costos.append(costo)
    if costos:
        return min(costos)
    else:
        return None

def imprimirlista(lista):
    print("inicio")
    for i in lista:
        print(" -> " + str(i))
    print("")   

def busqueda_profundidad(inicio, objetivo, visitados):
    if inicio == objetivo:
        optimo.append(visitados + [inicio])
        return None
    for vecino in grafo[inicio]:
        if vecino not in visitados:
            busqueda_profundidad(vecino, objetivo, visitados + [inicio])

    if visitados == []:
        mejor = calcularcosto()
        print(len(optimo))
    return None


busqueda_profundidad("Lugoj", "Bucharest", [])