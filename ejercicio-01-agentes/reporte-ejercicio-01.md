# Reporte Ejercicio 1 - Mundo de Wumpus

## 1. Configuración de la cueva

La cueva conserva el tamaño 4x4 y el agente comienza en `(1,1)` mirando al
este. El Wumpus y los tres pozos fueron movidos respecto al mapa clásico. El
oro está en `(3,2)`.

```text
y=4 | .   .   P   W
y=3 | P   .   .   .
y=2 | .   .   G   .
y=1 | A>  .   .   P
      x=1 x=2 x=3 x=4
```

Una ruta segura de ida y vuelta es:

```text
(1,1) -> (2,1) -> (2,2) -> (3,2)
(3,2) -> (2,2) -> (2,1) -> (1,1)
```

## 2. Resultados

Las ejecuciones se realizaron con `config/mi_cueva_4x4.yaml` y un máximo de
200 pasos.

| Agente | Resultado | Pasos | Puntaje final |
|---|---|---:|---:|
| Reflejo simple | Se detuvo sin oro | 200 | -200 |
| Basado en modelo | Salió con oro | 27 | 973 |
| Basado en metas | Salió con oro | 27 | 973 |
| Basado en utilidad | Salió con oro | 25 | 975 |
| Aprendizaje | Salió con oro | 11 | 989 |

## 3. Análisis

El agente de reflejo simple no consiguió salir con el oro. Solo reacciona al
percepto actual y no conserva un modelo de la cueva; al recibir brisa cerca de
los pozos, termina repitiendo giros sin construir una ruta segura.

Los agentes basado en modelo y basado en metas sí llegaron al oro y regresaron
a la salida. El modelo mantiene información sobre casillas visitadas y
perceptos, mientras que el agente basado en metas organiza sus acciones para
alcanzar el oro y volver. El agente basado en utilidad encontró una ruta
similar con menos pasos. El agente de aprendizaje obtuvo la mejor ejecución de
la prueba porque ya había aprendido una política para esta configuración.

Si un pozo se acerca a `(1,1)`, la casilla inicial puede producir brisa desde
el primer paso. El agente basado en modelo tendrá menos información segura y
puede quedarse girando o evitar avanzar. Si el pozo se aleja de la entrada,
puede explorar más casillas seguras, actualizar su modelo y encontrar la ruta
al oro con mayor facilidad.

## 4. Evidencias

Las salidas completas de los programas se encuentran en la carpeta
`evidencias/`.
