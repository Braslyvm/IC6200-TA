import tkinter as tk
from tkinter import messagebox

optimo = []
pasos = []

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

# Posiciones de los nodos en la pantalla
posiciones = {
    "Oradea": (150, 80),
    "Zerind": (80, 160),
    "Arad": (120, 260),
    "Timisoara": (120, 400),
    "Lugoj": (230, 450),
    "Mehadia": (280, 530),
    "Drobeta": (250, 630),
    "Craiova": (430, 630),
    "Sibiu": (310, 220),
    "Fagaras": (500, 240),
    "Rimnicu Vilcea": (390, 360),
    "Pitesti": (520, 470),
    "Bucharest": (710, 490),
    "Giurgiu": (690, 640),
    "Urziceni": (880, 450),
    "Hirsova": (1030, 410),
    "Eforie": (1080, 550),
    "Vaslui": (980, 280),
    "Iasi": (1040, 170),
    "Neamt": (950, 80)
}


def busqueda_profundidad(inicio, objetivo, visitados):
    global optimo, pasos

    pasos.append({
        "tipo": "visita",
        "actual": inicio,
        "visitados": visitados + [inicio]
    })

    if inicio == objetivo:
        optimo.append(visitados + [inicio])
        pasos.append({
            "tipo": "encontrado",
            "actual": inicio,
            "visitados": visitados + [inicio]
        })
        return True

    for vecino in grafo[inicio]:
        if vecino not in visitados and vecino != inicio:
            pasos.append({
                "tipo": "explorar",
                "desde": inicio,
                "hacia": vecino,
                "visitados": visitados + [inicio]
            })

            resultado = busqueda_profundidad(vecino, objetivo, visitados + [inicio])

            if resultado == True:
                return True

    pasos.append({
        "tipo": "retroceso",
        "actual": inicio,
        "visitados": visitados
    })

    if visitados == []:
        print(optimo)

    return None


class InterfazDFS:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda en Profundidad")
        self.root.geometry("1400x850")
        self.root.config(bg="#f5f5f5")

        self.paso_actual = 0
        self.nodos_canvas = {}
        self.textos_canvas = {}
        self.aristas_canvas = {}

        self.frame_top = tk.Frame(root, bg="#f5f5f5")
        self.frame_top.pack(fill="x", pady=10)

        tk.Label(
            self.frame_top,
            text="Búsqueda en Profundidad (DFS)",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5",
            fg="#222222"
        ).pack()

        self.frame_controls = tk.Frame(root, bg="#f5f5f5")
        self.frame_controls.pack(fill="x", pady=5)

        tk.Label(self.frame_controls, text="Inicio:", font=("Arial", 11), bg="#f5f5f5").pack(side="left", padx=(20, 5))
        self.entry_inicio = tk.Entry(self.frame_controls, font=("Arial", 11), width=15)
        self.entry_inicio.insert(0, "Lugoj")
        self.entry_inicio.pack(side="left", padx=5)

        tk.Label(self.frame_controls, text="Objetivo:", font=("Arial", 11), bg="#f5f5f5").pack(side="left", padx=(20, 5))
        self.entry_objetivo = tk.Entry(self.frame_controls, font=("Arial", 11), width=15)
        self.entry_objetivo.insert(0, "Bucharest")
        self.entry_objetivo.pack(side="left", padx=5)

        tk.Button(
            self.frame_controls,
            text="Iniciar",
            command=self.iniciar_busqueda,
            font=("Arial", 11, "bold"),
            bg="#222222",
            fg="white",
            relief="flat",
            padx=18,
            pady=6
        ).pack(side="left", padx=15)

        tk.Button(
            self.frame_controls,
            text="Paso siguiente",
            command=self.siguiente_paso,
            font=("Arial", 11, "bold"),
            bg="#555555",
            fg="white",
            relief="flat",
            padx=18,
            pady=6
        ).pack(side="left", padx=5)

        tk.Button(
            self.frame_controls,
            text="Automático",
            command=self.automatico,
            font=("Arial", 11, "bold"),
            bg="#777777",
            fg="white",
            relief="flat",
            padx=18,
            pady=6
        ).pack(side="left", padx=5)

        tk.Button(
            self.frame_controls,
            text="Reiniciar",
            command=self.reiniciar,
            font=("Arial", 11, "bold"),
            bg="#999999",
            fg="white",
            relief="flat",
            padx=18,
            pady=6
        ).pack(side="left", padx=5)

        self.lbl_estado = tk.Label(
            root,
            text="Configure inicio y objetivo, luego presione Iniciar.",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#333333"
        )
        self.lbl_estado.pack(pady=8)

        self.canvas = tk.Canvas(root, width=1300, height=700, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.dibujar_grafo()

    def dibujar_grafo(self):
        self.canvas.delete("all")
        self.nodos_canvas.clear()
        self.textos_canvas.clear()
        self.aristas_canvas.clear()

        dibujadas = set()

        for ciudad in grafo:
            x1, y1 = posiciones[ciudad]
            for vecino, peso in grafo[ciudad].items():
                par = tuple(sorted([ciudad, vecino]))
                if par not in dibujadas:
                    x2, y2 = posiciones[vecino]
                    linea = self.canvas.create_line(x1, y1, x2, y2, fill="#bdbdbd", width=2)
                    self.aristas_canvas[(ciudad, vecino)] = linea
                    self.aristas_canvas[(vecino, ciudad)] = linea

                    mx = (x1 + x2) / 2
                    my = (y1 + y2) / 2
                    self.canvas.create_text(mx, my - 8, text=str(peso), font=("Arial", 8), fill="#777777")
                    dibujadas.add(par)

        radio = 30
        for ciudad, (x, y) in posiciones.items():
            ovalo = self.canvas.create_oval(
                x - radio, y - radio, x + radio, y + radio,
                fill="#e8e8e8", outline="#444444", width=2
            )
            texto = self.canvas.create_text(
                x, y, text=ciudad, font=("Arial", 8, "bold"), fill="#222222", width=55
            )
            self.nodos_canvas[ciudad] = ovalo
            self.textos_canvas[ciudad] = texto

    def iniciar_busqueda(self):
        global optimo, pasos

        inicio = self.entry_inicio.get().strip()
        objetivo = self.entry_objetivo.get().strip()

        if inicio not in grafo or objetivo not in grafo:
            messagebox.showerror("Error", "El nodo de inicio o el objetivo no existen.")
            return

        optimo = []
        pasos = []
        self.paso_actual = 0

        self.dibujar_grafo()

        busqueda_profundidad(inicio, objetivo, [])

        if len(pasos) == 0:
            self.lbl_estado.config(text="No hubo pasos para mostrar.")
        else:
            self.lbl_estado.config(text="Búsqueda cargada. Presione 'Paso siguiente' o 'Automático'.")

    def siguiente_paso(self):
        global pasos, optimo

        if self.paso_actual >= len(pasos):
            if len(optimo) > 0:
                camino = " -> ".join(optimo[0])
                self.lbl_estado.config(text=f"Camino encontrado: {camino}")
                self.pintar_camino_final(optimo[0])
            else:
                self.lbl_estado.config(text="No se encontró solución.")
            return

        paso = pasos[self.paso_actual]
        self.mostrar_paso(paso)
        self.paso_actual += 1

    def mostrar_paso(self, paso):
        self.reset_colores()

        visitados = paso.get("visitados", [])
        for nodo in visitados:
            self.canvas.itemconfig(self.nodos_canvas[nodo], fill="#bde0fe")

        if paso["tipo"] == "visita":
            actual = paso["actual"]
            self.canvas.itemconfig(self.nodos_canvas[actual], fill="#ffe08a", outline="#222222", width=3)
            self.lbl_estado.config(text=f"Visitando nodo: {actual}")

        elif paso["tipo"] == "explorar":
            desde = paso["desde"]
            hacia = paso["hacia"]

            self.canvas.itemconfig(self.nodos_canvas[desde], fill="#ffd6a5", outline="#222222", width=3)
            self.canvas.itemconfig(self.nodos_canvas[hacia], fill="#caffbf", outline="#222222", width=3)

            if (desde, hacia) in self.aristas_canvas:
                self.canvas.itemconfig(self.aristas_canvas[(desde, hacia)], fill="#4a90e2", width=4)

            self.lbl_estado.config(text=f"Explorando desde {desde} hacia {hacia}")

        elif paso["tipo"] == "retroceso":
            actual = paso["actual"]
            self.canvas.itemconfig(self.nodos_canvas[actual], fill="#ffadad", outline="#222222", width=3)
            self.lbl_estado.config(text=f"Retrocediendo desde: {actual}")

        elif paso["tipo"] == "encontrado":
            actual = paso["actual"]
            self.canvas.itemconfig(self.nodos_canvas[actual], fill="#80ed99", outline="#222222", width=4)
            self.lbl_estado.config(text=f"Objetivo encontrado en: {actual}")

    def pintar_camino_final(self, camino):
        self.reset_colores()

        for nodo in camino:
            self.canvas.itemconfig(self.nodos_canvas[nodo], fill="#80ed99", outline="#1b5e20", width=3)

        for i in range(len(camino) - 1):
            a = camino[i]
            b = camino[i + 1]
            if (a, b) in self.aristas_canvas:
                self.canvas.itemconfig(self.aristas_canvas[(a, b)], fill="#00b894", width=4)

    def reset_colores(self):
        for ciudad in self.nodos_canvas:
            self.canvas.itemconfig(self.nodos_canvas[ciudad], fill="#e8e8e8", outline="#444444", width=2)

        lineas_ya = set()
        for clave, linea in self.aristas_canvas.items():
            if linea not in lineas_ya:
                self.canvas.itemconfig(linea, fill="#bdbdbd", width=2)
                lineas_ya.add(linea)

    def automatico(self):
        if self.paso_actual < len(pasos):
            self.siguiente_paso()
            self.root.after(900, self.automatico)
        else:
            self.siguiente_paso()

    def reiniciar(self):
        global optimo, pasos
        optimo = []
        pasos = []
        self.paso_actual = 0
        self.dibujar_grafo()
        self.lbl_estado.config(text="Configure inicio y objetivo, luego presione Iniciar.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazDFS(root)
    root.mainloop()