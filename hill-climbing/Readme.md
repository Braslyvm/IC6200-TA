# hill-climbing

## Descripción del algoritmo
El algoritmo Hill Climbing empieza con un mapa inicial y trata de mejorarlo poco a poco.
Primero calcula el costo del mapa. Luego prueba mover cada hospital a todas las posiciones posibles.
Si encuentra un movimiento que hace que el costo sea menor, se mueve a ese nuevo mapa.

---

## Instrucciones de instalación

1. Tener instalado **Python 3** en la computadora.
2. Tener instalado **pyQt5** para poder ejecutar la interfaz gráfica.
3. Tener instalado **pytest coverage tabulate** para poder ejecutar las pruebas

```bash
pip install pytest coverage tabulate PyQt5
```


---

## Instrucciones de ejecucion de la interfaz

### Archivo

```bash
python3 Interfaz/Interfaz.py
```


## Instrucciones de ejecucion de las pruebas de utils

### Archivo

```bash
pytest hill-climbing/tests/test_utils.py 
```

## Instrucciones de ejecucion de las pruebas de hill-climbing

### Archivo

```bash
pytest hill-climbing/tests/test_hill_climbing.py 
```





