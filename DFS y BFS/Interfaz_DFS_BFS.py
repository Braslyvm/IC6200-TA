import tkinter as tk
from tkinter import ttk, messagebox


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


class InterfazGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda en Grafos")
        self.root.geometry("1400x850")
        self.root.configure(bg="#f3f4f6")

        self.grafo = Grafo()
        self.nodos = list(self.grafo.diccionario.keys())

        self.pasos = []
        self.indice_paso = 0
        self.camino_final = None
        self.animando = False

        self.posiciones = {
            "Oradea": (120, 100),
            "Zerind": (120, 180),
            "Arad": (120, 270),
            "Timisoara": (120, 400),
            "Lugoj": (220, 460),
            "Mehadia": (300, 520),
            "Drobeta": (390, 590),
            "Craiova": (530, 540),
            "Sibiu": (300, 230),
            "Fagaras": (470, 210),
            "Rimnicu Vilcea": (420, 340),
            "Pitesti": (580, 400),
            "Bucharest": (760, 400),
            "Giurgiu": (750, 570),
            "Urziceni": (890, 360),
            "Hirsova": (1020, 340),
            "Eforie": (1070, 470),
            "Vaslui": (960, 220),
            "Iasi": (900, 120),
            "Neamt": (800, 60)
        }

        self.crear_interfaz()
        self.dibujar_grafo()

    def crear_interfaz(self):
        barra = tk.Frame(self.root, bg="#e5e7eb", height=70)
        barra.pack(fill="x", padx=10, pady=10)

        tk.Label(barra, text="Inicio:", bg="#e5e7eb", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.combo_inicio = ttk.Combobox(barra, values=self.nodos, state="readonly", width=16)
        self.combo_inicio.pack(side="left", padx=5)
        self.combo_inicio.set("Arad")

        tk.Label(barra, text="Objetivo:", bg="#e5e7eb", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.combo_objetivo = ttk.Combobox(barra, values=self.nodos, state="readonly", width=16)
        self.combo_objetivo.pack(side="left", padx=5)
        self.combo_objetivo.set("Bucharest")

        tk.Label(barra, text="Método:", bg="#e5e7eb", font=("Arial", 11, "bold")).pack(side="left", padx=5)
        self.combo_metodo = ttk.Combobox(
            barra,
            values=["Anchura", "Profundidad"],
            state="readonly",
            width=16
        )
        self.combo_metodo.pack(side="left", padx=5)
        self.combo_metodo.set("Anchura")

        tk.Button(barra, text="Iniciar", width=12, bg="#2563eb", fg="white",
                  command=self.iniciar_busqueda).pack(side="left", padx=6)

        tk.Button(barra, text="Paso", width=12, bg="#059669", fg="white",
                  command=self.siguiente_paso).pack(side="left", padx=6)

        tk.Button(barra, text="Automático", width=12, bg="#7c3aed", fg="white",
                  command=self.iniciar_automatico).pack(side="left", padx=6)

        tk.Button(barra, text="Reiniciar", width=12, bg="#dc2626", fg="white",
                  command=self.reiniciar).pack(side="left", padx=6)

        contenedor = tk.Frame(self.root, bg="#f3f4f6")
        contenedor.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        izquierda = tk.Frame(contenedor, bg="white", bd=1, relief="solid")
        izquierda.pack(side="left", fill="both", expand=True, padx=(0, 10))

        derecha = tk.Frame(contenedor, bg="#f3f4f6", width=340)
        derecha.pack(side="right", fill="y")

        self.canvas = tk.Canvas(izquierda, bg="white", width=950, height=700)
        self.canvas.pack(fill="both", expand=True)

        self.lbl_estado = tk.Label(
            derecha,
            text="Estado: esperando",
            bg="#f3f4f6",
            font=("Arial", 11, "bold"),
            anchor="w",
            justify="left"
        )
        self.lbl_estado.pack(fill="x", pady=(0, 10))

        marco_visitados = tk.LabelFrame(derecha, text="Visitados", bg="#f3f4f6", font=("Arial", 10, "bold"))
        marco_visitados.pack(fill="both", pady=5)

        self.txt_visitados = tk.Text(marco_visitados, width=10, height=10, font=("Consolas", 10))
        self.txt_visitados.pack(padx=5, pady=5)

        marco_por_visitar = tk.LabelFrame(derecha, text="Por visitar", bg="#f3f4f6", font=("Arial", 10, "bold"))
        marco_por_visitar.pack(fill="both", pady=5)

        self.txt_por_visitar = tk.Text(marco_por_visitar, width=10, height=10, font=("Consolas", 10))
        self.txt_por_visitar.pack(padx=5, pady=5)

        marco_resultado = tk.LabelFrame(derecha, text="Resultado", bg="#f3f4f6", font=("Arial", 10, "bold"))
        marco_resultado.pack(fill="both", expand=True, pady=5)

        self.txt_resultado = tk.Text(marco_resultado, width=10, height=14, font=("Consolas", 10))
        self.txt_resultado.pack(padx=5, pady=5, fill="both", expand=True)

    def dibujar_grafo(self, visitados=None, por_visitar=None, camino=None, actual=None):
        if visitados is None:
            visitados = []
        if por_visitar is None:
            por_visitar = []
        if camino is None:
            camino = []

        self.canvas.delete("all")

        dibujadas = set()
        for origen in self.grafo.diccionario:
            x1, y1 = self.posiciones[origen]
            for destino, peso in self.grafo.diccionario[origen].items():
                if (destino, origen) not in dibujadas:
                    x2, y2 = self.posiciones[destino]

                    color_linea = "#9ca3af"
                    ancho_linea = 2

                    if self.es_arista_en_camino(origen, destino, camino):
                        color_linea = "#9333ea"
                        ancho_linea = 4

                    self.canvas.create_line(x1, y1, x2, y2, fill=color_linea, width=ancho_linea)

                    mx = (x1 + x2) / 2
                    my = (y1 + y2) / 2
                    self.canvas.create_text(mx, my - 10, text=str(peso), fill="#374151", font=("Arial", 8, "bold"))

                    dibujadas.add((origen, destino))

        inicio = self.combo_inicio.get()
        objetivo = self.combo_objetivo.get()

        radio = 20
        for nodo, (x, y) in self.posiciones.items():
            color = "#d1d5db"

            if nodo == inicio:
                color = "#22c55e"
            elif nodo == objetivo:
                color = "#ef4444"
            elif nodo == actual:
                color = "#f59e0b"
            elif nodo in camino:
                color = "#a855f7"
            elif nodo in visitados:
                color = "#60a5fa"
            elif nodo in por_visitar:
                color = "#fde047"

            self.canvas.create_oval(
                x - radio, y - radio, x + radio, y + radio,
                fill=color, outline="black", width=2
            )
            self.canvas.create_text(
                x, y,
                text=nodo,
                font=("Arial", 7, "bold"),
                width=55
            )

    def es_arista_en_camino(self, a, b, camino):
        if len(camino) < 2:
            return False

        for i in range(len(camino) - 1):
            n1 = camino[i]
            n2 = camino[i + 1]
            if (n1 == a and n2 == b) or (n1 == b and n2 == a):
                return True
        return False

    def iniciar_busqueda(self):
        inicio = self.combo_inicio.get()
        objetivo = self.combo_objetivo.get()
        metodo = self.combo_metodo.get()

        if not inicio or not objetivo or not metodo:
            messagebox.showwarning("Aviso", "Debes elegir inicio, objetivo y método.")
            return

        self.animando = False
        self.pasos = []
        self.indice_paso = 0
        self.camino_final = None

        if metodo == "Anchura":
            self.generar_pasos_anchura(inicio, objetivo)
            self.camino_final = self.grafo.busqueda_anchura(inicio, objetivo)
        else:
            self.generar_pasos_profundidad(inicio, objetivo)
            caminos = self.grafo.busqueda_profundidad(inicio, objetivo)
            if caminos:
                self.camino_final = caminos[0]

        self.txt_visitados.delete("1.0", tk.END)
        self.txt_por_visitar.delete("1.0", tk.END)
        self.txt_resultado.delete("1.0", tk.END)

        self.txt_resultado.insert(tk.END, f"Método: {metodo}\n")
        self.txt_resultado.insert(tk.END, f"Inicio: {inicio}\n")
        self.txt_resultado.insert(tk.END, f"Objetivo: {objetivo}\n\n")
        self.txt_resultado.insert(tk.END, "Use Paso o Automático.\n")

        self.lbl_estado.config(text="Estado: búsqueda preparada")
        self.dibujar_grafo()

    def generar_pasos_anchura(self, inicio, objetivo):
        cola = [[inicio]]
        visitados = []

        while cola:
            camino = cola.pop(0)
            nodo = camino[-1]

            self.pasos.append({
                "actual": nodo,
                "visitados": visitados.copy(),
                "por_visitar": [c[-1] for c in cola],
                "camino": camino.copy(),
                "mensaje": f"Se saca de la cola: {nodo}"
            })

            if nodo == objetivo:
                self.pasos.append({
                    "actual": nodo,
                    "visitados": visitados.copy() + [nodo],
                    "por_visitar": [c[-1] for c in cola],
                    "camino": camino.copy(),
                    "mensaje": f"Objetivo encontrado: {' -> '.join(camino)}"
                })
                return

            if nodo not in visitados:
                visitados.append(nodo)
                for vecino in self.grafo.diccionario[nodo]:
                    if vecino not in visitados:
                        nuevo_camino = camino + [vecino]
                        cola.append(nuevo_camino)

                        self.pasos.append({
                            "actual": nodo,
                            "visitados": visitados.copy(),
                            "por_visitar": [c[-1] for c in cola],
                            "camino": nuevo_camino.copy(),
                            "mensaje": f"Se agrega a la cola: {vecino}"
                        })

    def generar_pasos_profundidad(self, inicio, objetivo):
        visitados = []
        encontrado = {"valor": False}

        def recorrer(nodo, camino):
            if encontrado["valor"]:
                return

            self.pasos.append({
                "actual": nodo,
                "visitados": visitados.copy(),
                "por_visitar": [],
                "camino": camino.copy(),
                "mensaje": f"Visitando: {nodo}"
            })

            if nodo == objetivo:
                encontrado["valor"] = True
                self.pasos.append({
                    "actual": nodo,
                    "visitados": visitados.copy() + [nodo],
                    "por_visitar": [],
                    "camino": camino.copy(),
                    "mensaje": f"Objetivo encontrado: {' -> '.join(camino)}"
                })
                return

            visitados.append(nodo)

            vecinos_disponibles = []
            for vecino in self.grafo.diccionario[nodo]:
                if vecino not in visitados and vecino not in camino[:-1]:
                    vecinos_disponibles.append(vecino)

            self.pasos.append({
                "actual": nodo,
                "visitados": visitados.copy(),
                "por_visitar": vecinos_disponibles.copy(),
                "camino": camino.copy(),
                "mensaje": f"Vecinos pendientes desde {nodo}: {', '.join(vecinos_disponibles) if vecinos_disponibles else 'ninguno'}"
            })

            for vecino in self.grafo.diccionario[nodo]:
                if vecino not in visitados and vecino not in camino[:-1]:
                    recorrer(vecino, camino + [vecino])
                    if encontrado["valor"]:
                        return

        recorrer(inicio, [inicio])

    def siguiente_paso(self):
        if not self.pasos:
            messagebox.showinfo("Aviso", "Primero debes iniciar la búsqueda.")
            return

        if self.indice_paso >= len(self.pasos):
            self.mostrar_resultado_final()
            return

        paso = self.pasos[self.indice_paso]

        self.lbl_estado.config(text="Estado: " + paso["mensaje"])
        self.actualizar_cuadros(paso["visitados"], paso["por_visitar"])
        self.dibujar_grafo(
            visitados=paso["visitados"],
            por_visitar=paso["por_visitar"],
            camino=paso["camino"],
            actual=paso["actual"]
        )

        self.indice_paso += 1

        if self.indice_paso == len(self.pasos):
            self.mostrar_resultado_final()

    def iniciar_automatico(self):
        if not self.pasos:
            messagebox.showinfo("Aviso", "Primero debes iniciar la búsqueda.")
            return

        self.animando = True
        self.ejecutar_automatico()

    def ejecutar_automatico(self):
        if not self.animando:
            return

        if self.indice_paso < len(self.pasos):
            self.siguiente_paso()
            self.root.after(1000, self.ejecutar_automatico)
        else:
            self.animando = False

    def actualizar_cuadros(self, visitados, por_visitar):
        self.txt_visitados.delete("1.0", tk.END)
        self.txt_por_visitar.delete("1.0", tk.END)

        if visitados:
            for nodo in visitados:
                self.txt_visitados.insert(tk.END, nodo + "\n")
        else:
            self.txt_visitados.insert(tk.END, "Vacío")

        if por_visitar:
            for nodo in por_visitar:
                self.txt_por_visitar.insert(tk.END, nodo + "\n")
        else:
            self.txt_por_visitar.insert(tk.END, "Vacío")

    def mostrar_resultado_final(self):
        texto_actual = self.txt_resultado.get("1.0", tk.END)
        if "Camino encontrado:" in texto_actual or "No se encontró camino" in texto_actual:
            return

        self.txt_resultado.insert(tk.END, "\n")
        if self.camino_final:
            self.txt_resultado.insert(tk.END, "Camino encontrado:\n")
            self.txt_resultado.insert(tk.END, " -> ".join(self.camino_final) + "\n")
            self.txt_resultado.insert(tk.END, f"\nCantidad de nodos: {len(self.camino_final)}")
        else:
            self.txt_resultado.insert(tk.END, "No se encontró camino")

    def reiniciar(self):
        self.animando = False
        self.pasos = []
        self.indice_paso = 0
        self.camino_final = None

        self.txt_visitados.delete("1.0", tk.END)
        self.txt_por_visitar.delete("1.0", tk.END)
        self.txt_resultado.delete("1.0", tk.END)
        self.lbl_estado.config(text="Estado: esperando")

        self.dibujar_grafo()


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazGrafo(root)
    root.mainloop()