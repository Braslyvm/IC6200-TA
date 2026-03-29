# Gato 

## Descripción del algoritmo

se implementa el algoritmo minimax para jugar gato de manera óptima.

El algoritmo evalúa todos los movimientos posibles del tablero y selecciona la mejor jugada según el turno del jugador. Para esto, utiliza dos funciones recursivas: una que busca maximizar la utilidad del jugador X y otra que busca minimizar la utilidad del jugador O.

---

## Instrucciones de instalación

1. Tener instalado **Python 3** en la computadora.
2. Tener instalado **tkinter** para poder ejecutar la interfaz gráfica.
2. Tener instalado **pytest** .
2. Tener instalado **coverage** .


---

## Instrucciones de ejecucion

### Archivos de prueba
#### Utils 
```bash
python3 -m pytest tic-tac-toe/tests/test_utils.py
```
#### Utils 
```bash
python3 -m pytest tic-tac-toe/tests/test_minimax.py
```

### Interfaz 
```bash
python3 interfaz.py
```