import os
import numpy as np
import pandas as pd
import cv2 as cv

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import accuracy_score



# Rutas

data_dir = 'signs'
train_path = 'signs/Train'
test_path = 'signs/Test.csv'
model_path = 'modelo_senales.h5'

#clases

classes = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing veh over 3.5 tons',
    11: 'Right-of-way at intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Veh > 3.5 tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve left',
    20: 'Dangerous curve right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End speed + passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End no passing veh > 3.5 tons'
}



# Parámetros del modelo


batch_size = 32
seed = 42
width, height = 50 , 50
num_classes = 43

orden_carpetas = [str(i) for i in range(num_classes)]



# Variable global del modelo


modelo_cargado = None




def crear_modelo():
    """
    crear modelo CNN con la siguiente arquitectura:
    - Conv2D (16 filtros, kernel 5x5, sin bias)
    - BatchNormalization
    - ReLU
    - Conv2D (32 filtros, kernel 5x5, sin bias)
    - BatchNormalization
    - ReLU
    - MaxPool2D
    """
    cnn_model = keras.models.Sequential([
        keras.layers.Input(shape=(width, height, 3)),

        keras.layers.Conv2D(filters=16, kernel_size=5, use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),

        keras.layers.Conv2D(filters=32, kernel_size=5, use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.MaxPool2D(),

        keras.layers.Conv2D(filters=64, kernel_size=3, use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),

        keras.layers.Conv2D(filters=128, kernel_size=3, use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.MaxPool2D(),

        keras.layers.Flatten(),

        keras.layers.Dense(units=512, use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation('relu'),
        keras.layers.Dropout(0.3),

        keras.layers.Dense(num_classes, activation='softmax')
    ])

    cnn_model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return cnn_model


def cargar_datos_entrenamiento():
    """
    Cargar datos de entrenamiento usando ImageDataGenerator de Keras.
    Se aplicará un rescaling de 1./255 para normalizar las imágenes.
    """
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    X_train = train_datagen.flow_from_directory(
        directory=train_path,
        classes=orden_carpetas,
        target_size=(width, height),
        batch_size=batch_size,
        seed=seed,
        subset='training',
        interpolation='hamming',
        class_mode='categorical'
    )

    X_validation = train_datagen.flow_from_directory(
        directory=train_path,
        classes=orden_carpetas,
        target_size=(width, height),
        batch_size=batch_size,
        seed=seed,
        subset='validation',
        interpolation='hamming',
        class_mode='categorical'
    )

    return X_train, X_validation



def cargar_datos_prueba():
    """
    Cargar datos de prueba desde el archivo CSV. Se leerán las imágenes usando OpenCV,
    """
    X_test_df = pd.read_csv(test_path)

    X_test_labels = X_test_df.ClassId
    imgs = X_test_df.Path

    data = []

    for img in imgs:
        image_path = data_dir + '/' + img
        image = cv.imread(image_path)

        if image is None:
            print("No se pudo leer la imagen:", image_path)
            continue

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (width, height))

        data.append(image)

    X_test = np.array(data, dtype='float32') / 255.0

    return X_test, np.array(X_test_labels)



def entrenar_modelo():
    """
    Entrenar el modelo CNN con los datos de entrenamiento. Si ya existe un modelo entrenado, se cargará en lugar de entrenar nuevamente.
    """
    print("Cargando datos de entrenamiento...")

    X_train, X_validation = cargar_datos_entrenamiento()

    print("Creando modelo CNN...")

    cnn_model = crear_modelo()
    cnn_model.summary()

    print("Entrenando modelo...")

    cnn_model.fit(
        X_train,
        validation_data=X_validation,
        epochs=10
    )
    cnn_model.save(model_path)
    return cnn_model




def preparar_modelo():
    """
    Preparar el modelo para su uso. Si ya existe un modelo entrenado, se cargará. De lo contrario, se entrenará un nuevo modelo.
    """
    global modelo_cargado

    if modelo_cargado is not None:
        return modelo_cargado

    if os.path.exists(model_path):
        modelo_cargado = tf.keras.models.load_model(model_path)
        return modelo_cargado

    modelo_cargado = entrenar_modelo()

    return modelo_cargado




def evaluar_modelo():
    """
    Evaluar el modelo con los datos de prueba y calcular la exactitud.
    """
    modelo = preparar_modelo()

    print("Cargando datos de prueba...")

    X_test, X_test_labels = cargar_datos_prueba()

    print("Evaluando modelo...")

    predicciones = modelo.predict(X_test)
    pred_indices = np.argmax(predicciones, axis=1)

    accuracy = accuracy_score(X_test_labels, pred_indices)

    print("Exactitud en prueba:", accuracy)

    return accuracy


def predecir_senal(ruta_imagen):
    """
    Predecir la clase de una señal de tráfico a partir de una imagen. Se devuelve el nombre de la clase y la confianza de la predicción.
    """
    modelo = preparar_modelo()

    image = cv.imread(ruta_imagen)

    if image is None:
        return "No se pudo leer la imagen", 0

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.resize(image, (width, height))
    image = image.astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    prediccion = modelo.predict(image)

    clase_indice = np.argmax(prediccion)
    confianza = np.max(prediccion) * 100

    nombre_clase = classes[clase_indice]

    return nombre_clase, confianza