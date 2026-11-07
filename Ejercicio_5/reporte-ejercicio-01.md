# Reporte Ejercicio 1 - Búsqueda informada en el mapa de Rumania

## 1. Instancia y heurística

Se eligió la pareja `Oradea -> Bucharest`. Se utiliza la distancia en línea
recta a Bucharest como heurística `h(n)`, tomada de la tabla de AIMA. Para esta
meta la heurística es admisible y consistente.

```text
Oradea --151-- Sibiu --99-- Fagaras --211-- Bucharest
                    |
                    80
                    |
              Rimnicu Vilcea --97-- Pitesti --101-- Bucharest
```

Valores relevantes: `h(Oradea)=380`, `h(Sibiu)=253`, `h(Fagaras)=176`,
`h(Rimnicu Vilcea)=193`, `h(Pitesti)=100` y `h(Bucharest)=0`.

## 2. Resultados

| Algoritmo | Depth | Cost | Expanded | Generated | Path |
|---|---:|---:|---:|---:|---|
| Greedy best-first | 3 | 461 km | 3 | 9 | Oradea -> Sibiu -> Fagaras -> Bucharest |
| A* | 4 | 429 km | 5 | 15 | Oradea -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest |

## 3. Análisis

Greedy elige el nodo con menor `h(n)` y, desde Sibiu, prefiere Fagaras porque
`h(Fagaras)=176` es menor que `h(Rimnicu Vilcea)=193`. Obtiene una ruta de tres
saltos, pero de 461 km.

A* usa `f(n)=g(n)+h(n)`, por lo que considera tanto el costo ya recorrido como
la estimación restante. Encuentra la ruta óptima de 429 km, aunque tiene un
salto adicional.

En la ruta de A* los valores son:

```text
Oradea:          g=0   h=380  f=380
Sibiu:           g=151 h=253  f=404
Rimnicu Vilcea:  g=231 h=193  f=424
Pitesti:         g=328 h=100  f=428
Bucharest:       g=429 h=0    f=429
```

El valor de `f` no disminuye porque la heurística es consistente.

## 4. Evidencias de ejecución

```text
Algorithm: Greedy best-first search
Problem:   Oradea -> Bucharest
Status:    success
Path:      Oradea -> Sibiu -> Fagaras -> Bucharest
Depth:     3 roads
Cost:      461 km
Expanded:  3 nodes
Generated: 9 nodes
```

```text
Algorithm: A* search
Problem:   Oradea -> Bucharest
Status:    success
Path:      Oradea -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
Depth:     4 roads
Cost:      429 km
Expanded:  5 nodes
Generated: 15 nodes
```
