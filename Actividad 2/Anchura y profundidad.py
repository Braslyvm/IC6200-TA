class Grafo:
    def __init__(self):
        self.diccionario= {
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
        self.visitados = []

    def busqueda_anchura(self, inicio,objetivo) :
        cola = [[inicio]] 
        visitados = []

        while cola:
            camino = cola.pop(0) 
            nodo = camino[-1]

            if nodo == objetivo:
                return camino  

            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.diccionario[nodo]:
                    if vecino not in visitados:
                        nuevo_camino = camino + [vecino]
                        cola.append(nuevo_camino)

        return None

    def busqueda_profundidad(self, inicio, objetivo, visitados=None, optimo=None):
        if visitados is None:
            visitados = []
        if optimo is None:
            optimo = []
        if inicio == objetivo:
            optimo.append(visitados + [inicio])
            return optimo
        for vecino in self.diccionario[inicio]:
            if vecino not in visitados:
                self.busqueda_profundidad(vecino, objetivo, visitados + [inicio], optimo)
        return optimo
      