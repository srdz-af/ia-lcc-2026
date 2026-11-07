# Reporte Ejercicio 8: Q-learning en Cliff Walking

**Estudiante:** srdz-af  
**Materia:** Inteligencia Artificial  

## 1. Parámetros del entorno y algoritmo

Los valores vienen del archivo `envs/cliff.yaml`:

- **Mundo:** Cuadrícula de 4 filas por 12 columnas.
- **Puntos clave:** Inicio S en `(3, 0)`, meta G en `(3, 11)`, acantilado en las casillas `(3, 1)` a `(3, 10)`.
- **Costos:** Cada paso resta 1 punto. Caer al precipicio cuesta 100 puntos y regresa al agente al inicio sin abortar el episodio. Llegar a G cuesta 1 punto y cierra el episodio.
- **Aprendizaje:**
  - Tasa $\alpha = 0.5$
  - Descuento $\gamma = 1.0$ (problema episódico sin descuento)
  - Exploración $\varepsilon = 0.1$ durante 500 episodios de entrenamiento
  - Desempate fijo de acciones: N, E, S, W
  - Semilla fija: 42

## 2. Política greedy obtenida

Al apagar la exploración ($\varepsilon = 0$), el agente sigue exactamente el camino pegado al acantilado:

- **Retorno total:** -13.0
- **Pasos totales:** 13
- **Trayectoria:**  
  `(3, 0) -> (2, 0) -> (2, 1) -> (2, 2) -> (2, 3) -> (2, 4) -> (2, 5) -> (2, 6) -> (2, 7) -> (2, 8) -> (2, 9) -> (2, 10) -> (2, 11) -> (3, 11)`
- **Acciones ejecutadas:**  
  `N -> E -> E -> E -> E -> E -> E -> E -> E -> E -> E -> E -> S`

### Mapa de flechas aprendidas

```text
      0  1  2  3  4  5  6  7  8  9 10 11
    +------------------------+
  0 |  ↓  ↑  ←  →  →  ↑  →  ↓  ↓  ↓  →  ↓ |
  1 |  →  →  ↓  ↓  →  ↓  →  →  →  ↓  ↓  ↓ |
  2 |  →  →  →  →  →  →  →  →  →  →  →  ↓ |
  3 |  ↑  C  C  C  C  C  C  C  C  C  C  G |
    +------------------------+
```

La fila 2 quedó apuntando toda hacia el este; el agente camina sobre la cornisa hasta topar con la columna 11 y recién ahí baja hacia la meta.

## 3. Q-learning vs. SARSA en este entorno

Q-learning es un método *off-policy*: actualiza con $\max_{a'} Q(s', a')$, asumiendo que después tomará la decisión perfecta. Como ignora que el 10% de exploración ($\varepsilon = 0.1$) puede tirarlo al pozo en el siguiente paso, aprende la ruta más corta posible (13 pasos, retorno de -13).

SARSA en cambio es *on-policy*; aprende con la acción real que va a ejecutar. Al ver que caminar junto al borde causa caídas frecuentes de -100 por culpa del $\varepsilon$-greedy, SARSA prefiere dar la vuelta larga por arriba (fila 0), sacrificando pasos para alejarse del peligro (termina con retornos alrededor de -17).

En la curva de aprendizaje (`curva_aprendizaje.png`) se nota que los episodios de entrenamiento oscilan entre -30 y -60 justamente por esas caídas aleatorias. Una vez entrenado y evaluado con $\varepsilon = 0$, el agente no comete fallos y clava el -13 óptimo.
