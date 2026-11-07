# Reporte Ejercicio 6: MLP en Iris (NumPy y Keras)

**Estudiante:** srdz-af  
**Materia:** Inteligencia Artificial  

## 1. Resultados (500 épocas, lr = 0.03)

| Implementación | Capas | Activación | Pérdida | Error final |
| :--- | :---: | :---: | :---: | :---: |
| NumPy (a mano) | 4x3x3 | Sigmoide | MSE | 0.0596 |
| NumPy (a mano) | 4x3x3x3x3 | Sigmoide | MSE | 0.4134 |
| Keras | 4x3x3 | Sigmoide | MSE | 0.1786 |
| Keras | 4x3x3x3x3 | Sigmoide | MSE | 0.2223 |
| Keras (Reto) | 4x3x3x3x3 | ReLU + Softmax | CCE | 0.1937 (acc: 94%) |

## 2. Preguntas

### ¿El error bajó al meter dos capas extra, o se estancó? ¿Pasó igual en NumPy y en Keras?
Empeoró en los dos lados.

Con NumPy, la red chica de 2 capas bajó el MSE hasta 0.0596 sin problemas, pero al meterle dos capas ocultas intermedias (dejándola en 4x3x3x3x3) se quedó trabada en 0.4134. La gráfica se aplana casi desde la época 80 y de ahí ya no se mueve.

En Keras pasó algo similar: la red de 2 capas terminó con 0.1786 de pérdida y la profunda subió a 0.2223. Keras no colapsó tan feo porque los pesos arrancan con la escala de Glorot y los gradientes se promedian en bloques de 32, pero de todas formas la red profunda rindió peor que la original.

### ¿Se parecen las curvas de NumPy y Keras en la misma topología? ¿Qué diferencias hay?
Tienen la misma caída inicial rápida, pero Keras genera una curva mucho más limpia.

Hay dos causas principales:
1. Modo de entrenamiento: el script de NumPy corre muestra por muestra (batch size = 1) y barre las flores en el orden que vienen en scikit-learn (50 setosas seguidas, luego 50 versicolor, luego 50 virginica). Eso mete brincos en cada época porque los pesos se ajustan hacia la última clase vista. Keras en cambio usa mini-batches de 32 y revuelve los datos (`shuffle=True`) antes de cada época.
2. Escala numérica del eje Y: en NumPy dividimos el error cuadrático entre 150 ejemplos, mientras que `tf.keras.losses.MeanSquaredError` divide entre los 150 ejemplos y también entre las 3 neuronas de salida. Por eso la pérdida de Keras se ve numéricamente más chica aunque mida el mismo concepto.

### ¿Tiene sentido que una red más profunda con sigmoides y MSE no aprenda en Iris?
Sí. La derivada de la sigmoide alcanza como máximo 0.25 (justo en z = 0). Cuando encadenas cuatro capas en retropropagación, multiplicas esos factores una y otra vez; para cuando el gradiente llega a la primera capa oculta, el valor se redujo a menos de $(0.25)^4 \approx 0.0039$. El gradiente se apaga, los pesos de entrada apenas se enteran del error y la red deja de aprender. A eso se suma que Iris es un problema chico de 150 filas que se resuelve con fronteras casi planas: meterle 4 capas solo añadió pesos difíciles de mover sin aportar ninguna ventaja real.

## 3. Reto con ReLU y Softmax
Cambiando las capas intermedias a ReLU y la salida a Softmax con entropía cruzada, la red de 4 capas entrenó en Keras sin atorarse y llegó a 94% de exactitud (ver `notebook2_relu_softmax.png`). Como la derivada de ReLU vale 1 cuando la entrada es positiva, el gradiente pasa completo hacia atrás y la profundidad deja de ser un estorbo.
