# Red Neuronal para Reconocimiento de Señales de Tránsito

## Instrucciones de ejecución

Primero se debe descargar el dataset **GTSRB - German Traffic Sign Recognition Benchmark** desde Kaggle:

https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign/code

Después de descargar el archivo `.zip`, se debe descomprimir y colocar su contenido dentro de una carpeta llamada `signs`, ubicada en la carpeta principal del proyecto.

Para ejecutar la interfaz nada mas ejecute el siguiente comando:

```bash
python3 interfaz.py
```

Si es la primera ves tardara un poco mas, ya que se debe entrenar el modelo, pero las siguientes veces que se ejecute el comando, el modelo ya estará entrenado y la interfaz se abrirá de forma rápida.

---

## Descripción del problema

Es la creación de una interfaz que use una red neuronal para reconocer señales de tránsito.

Para esta tarea se solicita el uso de la base de datos **GTSRB**, la cual cuenta con **43 clases** de distintas señales de tránsito. Cada clase cuenta con muchas imágenes; esta cantidad de imágenes facilita el entrenamiento de la red neuronal y permite obtener mejores resultados en el reconocimiento.

El sistema debe ser capaz de recibir una imagen de entrada, procesarla y predecir a qué clase pertenece. Además, la interfaz permite cargar imágenes de forma sencilla y mostrar el resultado de la predicción junto con el porcentaje de confianza del modelo.

---

## Arquitectura del modelo

El modelo utilizado es una red neuronal conocida como **CNN**. Este tipo de red se usa para trabajar con imágenes, ya que puede aprender detalles importantes como colores, formas, bordes, números y símbolos.

En este taller, el modelo recibe imágenes de señales de tránsito con un tamaño de `50x50` píxeles. Luego, la red analiza la imagen por partes para encontrar características importantes y finalmente decide a cuál de las **43 clases** pertenece.

La red está formada por varias capas que ayudan a extraer información de la imagen y una capa final que entrega la predicción. Como el dataset **GTSRB** tiene 43 clases, la salida del modelo también tiene **43 posibles resultados**.

---

## Métricas obtenidas

Para evaluar el rendimiento del modelo se utilizó la métrica de exactitud, conocida como `accuracy`. Esta métrica indica qué porcentaje de imágenes fueron clasificadas correctamente por la red neuronal.

El modelo fue entrenado durante `10 epochs`. En cada epoch, la red neuronal ajusta sus parámetros y muestra los resultados obtenidos con los datos de entrenamiento y validación. La validación permite comprobar cómo se comporta el modelo con imágenes que no usa directamente para aprender.

La cantidad de epochs influye en el entrenamiento: con menos epochs el modelo entrena más rápido, pero puede obtener menor precisión porque aprende menos de los datos. En cambio, con más epochs puede mejorar su precisión, aunque el entrenamiento tarda más y también puede existir riesgo de sobreajuste si se entrena demasiado.

Los resultados obtenidos fueron:

```text
Epoch 1/10
Accuracy de entrenamiento: 0.9454
Loss de entrenamiento: 0.2151
Accuracy de validación: 0.9222
Loss de validación: 0.2875

Epoch 2/10
Accuracy de entrenamiento: 0.9934
Loss de entrenamiento: 0.0257
Accuracy de validación: 0.9351
Loss de validación: 0.2188

Epoch 3/10
Accuracy de entrenamiento: 0.9945
Loss de entrenamiento: 0.0202
Accuracy de validación: 0.9684
Loss de validación: 0.1099

Epoch 4/10
Accuracy de entrenamiento: 0.9962
Loss de entrenamiento: 0.0136
Accuracy de validación: 0.9718
Loss de validación: 0.0934

Epoch 5/10
Accuracy de entrenamiento: 0.9947
Loss de entrenamiento: 0.0182
Accuracy de validación: 0.9665
Loss de validación: 0.1349

Epoch 6/10
Accuracy de entrenamiento: 0.9972
Loss de entrenamiento: 0.0106
Accuracy de validación: 0.9440
Loss de validación: 0.1873

Epoch 7/10
Accuracy de entrenamiento: 0.9971
Loss de entrenamiento: 0.0089
Accuracy de validación: 0.9728
Loss de validación: 0.1026

Epoch 8/10
Accuracy de entrenamiento: 0.9972
Loss de entrenamiento: 0.0084
Accuracy de validación: 0.9768
Loss de validación: 0.0831

Epoch 9/10
Accuracy de entrenamiento: 0.9967
Loss de entrenamiento: 0.0120
Accuracy de validación: 0.9744
Loss de validación: 0.0889

Epoch 10/10
Accuracy de entrenamiento: 0.9985
Loss de entrenamiento: 0.0053
Accuracy de validación: 0.9633
Loss de validación: 0.1578
```

---

## Conclusiones

El modelo reconoció muchas imágenes, pero falla con imágenes simples o distintas a las del conjunto de entrenamiento.

El problema principal es la falta de variedad en los datos. Si una imagen tiene un color diferente al esperado, el modelo puede fallar. Lo mismo ocurre cuando incluye texto adicional, el modelo se confunde.

Se realizaron pruebas con imágenes descargadas de internet. El modelo reconoce sin problema una señal de límite de velocidad con solo el círculo rojo y el número 80. Pero si esa misma señal incluye texto como `"km/h"` u otro elemento extra, el resultado cambia; a veces predice una clase incorrecta, otras veces la reconoce, pero con confianza baja.

La solución más directa es ampliar el conjunto de datos con imágenes de ese estilo, o aplicar **data augmentation** para generar variaciones similares. Con imágenes dentro de la base de conocimiento del modelo, la detección es notablemente más precisa.

---

# Referencias

* Greenwarbler. (s. f.). *Traffic Signs Classification | CNN - ResNet*. Kaggle.
  https://www.kaggle.com/code/greenwarbler/traffic-signs-classification-cnn-resnet/notebook
