# Reporte Ejercicio 7: K-medias con Blobs Separados

**Estudiante:** srdz-af  
**Materia:** Inteligencia Artificial  

---

## 1. Centros y desviaciones utilizados

Para que los 5 grupos fueran visualmente identificables y no se solaparan, se redefinieron los centros y desviaciones:

```python
blob_centers = np.array([
    [-6.5,  5.0],
    [-2.5, -4.0],
    [ 1.5,  4.5],
    [ 5.5, -3.5],
    [ 8.0,  3.5]
])
blob_std = np.array([0.4, 0.35, 0.3, 0.4, 0.35])
```

Se mantuvo `n_samples = 2000` y `random_state = 7`.

---

## 2. Inercia y Silueta para $k = 1 \dots 9$

| $k$ | Inercia ($J$) | Coeficiente de Silueta |
| :---: | :---: | :---: |
| 1 | 87378.1 | - |
| 2 | 43719.5 | 0.5156 |
| 3 | 21987.2 | 0.6329 |
| 4 | 9211.7 | 0.7660 |
| **5** | **509.9** *(Codo)* | **0.9134** *(Máximo)* |
| 6 | 468.0 | 0.7969 |
| 7 | 429.8 | 0.6745 |
| 8 | 395.6 | 0.5610 |
| 9 | 364.5 | 0.4359 |

---

## 3. Respuestas a las preguntas del ejercicio

### 1. ¿Por qué el codo "prefiere" $k = 4$ en los datos originales de Géron si se usaron 5 centros?
En los datos originales, tres de los cinco centros comparten la coordenada $x = -2.8$ (`[-2.8, 1.8]`, `[-2.8, 2.8]`, `[-2.8, 1.3]`) con desviaciones muy pequeñas ($0.1$). Al estar casi pegados entre sí en comparación con la distancia hacia los otros dos grupos, la inercia baja drásticamente cuando se separan los clusters lejanos ($k=2, 3, 4$), pero pasar de $k=4$ a $k=5$ solo divide nubes que ya están juntas, reduciendo la inercia de forma marginal. Por eso el codo geométrico se forma en $k = 4$.

### 2. Con los blobs modificados, ¿el codo y la silueta coinciden en el mismo $k$? ¿Ese $k$ es 5?
Sí, ambos coinciden en $k = 5$:
- **Codo:** La inercia se desploma de 9211.7 en $k=4$ a **509.9 en $k=5$**, y a partir de ahí la curva se aplana. El codo queda marcado en $k = 5$.
- **Silueta:** El valor más alto de silueta se obtiene en **$k = 5$** con un puntaje de **0.9134**, superando con creces a $k=4$ (0.7660) y $k=6$ (0.7969).

### 3. ¿Qué factor determina que el codo detecte los clusters (distancia entre centros vs. $\sigma$)?
Depende de la distancia relativa entre centroides respecto a sus desviaciones estándar ($\|\mu_i - \mu_j\| / (\sigma_i + \sigma_j)$). Si la distancia entre dos centros es menor a unas 2 o 3 desviaciones estándar, las colas de las campanas se solapan y K-means las trata como una sola masa densa. Para que el codo marque 5 grupos de forma limpia, la separación entre centros debe ser bastante mayor que el radio de dispersión de cada nube.

