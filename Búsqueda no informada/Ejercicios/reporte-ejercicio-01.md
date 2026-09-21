# Reporte Ejercicio 1 - Búsqueda no informada en el mapa de Rumania

## 1. Instancia

Se eligió la pareja `Oradea -> Bucharest`, distinta de la instancia por
defecto. Todos los algoritmos utilizan el mismo grafo y el orden alfabético de
vecinos.

## 2. Resultados

| Algoritmo | Status | Depth | Cost | Expanded | Generated | Path |
|---|---|---:|---:|---:|---:|---|
| BFS | success | 3 | 461 km | 5 | 13 | Oradea -> Sibiu -> Fagaras -> Bucharest |
| UCS | success | 4 | 429 km | 10 | 27 | Oradea -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest |
| DFS | success | 9 | 1024 km | 9 | 24 | Oradea -> Sibiu -> Arad -> Timisoara -> Lugoj -> Mehadia -> Drobeta -> Craiova -> Pitesti -> Bucharest |
| DLS, limite 2 | cutoff | - | - | 3 | 9 | No encuentra solución dentro del límite |
| DLS, límite 3 | success | 3 | 461 km | 4 | 8 | Oradea -> Sibiu -> Fagaras -> Bucharest |
| IDS | success | 3 | 461 km | 8 | 21 | Oradea -> Sibiu -> Fagaras -> Bucharest |

## 3. Subgrafo relevante

```text
Oradea --151-- Sibiu --99-- Fagaras --211-- Bucharest
                    |
                    80
                    |
              Rimnicu Vilcea --97-- Pitesti --101-- Bucharest
```

La ruta de DFS también aparecen las carreteras `Sibiu-Arad`, `Arad-Timisoara`,
`Timisoara-Lugoj`, `Lugoj-Mehadia`, `Mehadia-Drobeta` y `Drobeta-Craiova`.

## 4. Análisis

BFS encuentra el camino con menos carreteras: tres saltos y 461 km. UCS no
minimiza el número de saltos; minimiza el costo acumulado y por eso acepta
cuatro carreteras para obtener la ruta de 429 km, que es la más barata.

DFS sigue una rama profunda según el orden de expansión y no garantiza ni el
menor número de carreteras ni el menor costo. Por eso devuelve una ruta de
nueve saltos y 1024 km aunque trabaja sobre el mismo grafo.

Con límite 2, DLS devuelve `cutoff` porque la solución mínima tiene profundidad
3. Con límite 3 encuentra la misma ruta que BFS. IDS prueba límites crecientes y
termina en 3, por lo que coincide con BFS en profundidad y camino en esta
instancia, aunque reexpande nodos y realiza más trabajo acumulado.

## 5. Evidencias

Los valores de la tabla corresponden a las salidas de los scripts `02` a `06`
ejecutados con `--from-city Oradea --to Bucharest`.
