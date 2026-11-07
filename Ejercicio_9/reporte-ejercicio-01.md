# Reporte Ejercicio 9: Inferencia Lógica en la Biblioteca

**Estudiante:** srdz-af  
**Materia:** Inteligencia Artificial  

---

## 1. Base de conocimiento (`biblioteca.yaml`)

```yaml
facts:
  - Estudiante(Ana)
  - Estudiante(Luis)
  - Profesor(Marta)
  - TieneCredencial(Ana)
  - TieneCredencial(Marta)
  - HorarioNocturno(Hoy)

rules:
  - id: R_miembro_est
    if:
      - Estudiante(x)
      - TieneCredencial(x)
    then: Miembro(x)

  - id: R_miembro_prof
    if:
      - Profesor(x)
    then: Miembro(x)

  - id: R_acceso
    if:
      - Miembro(x)
      - HorarioNocturno(Hoy)
    then: AccesoNoche(x)

  - id: R_beca
    if:
      - Estudiante(x)
      - TieneCredencial(x)
    then: Becario(x)
```

---

## 2. Resumen de resultados

| Consulta | Hacia adelante (FC) | Hacia atrás (BC) | Acceso |
| :--- | :---: | :---: | :---: |
| `AccesoNoche(Ana)` | **SÍ** | **SÍ** | Permitido |
| `AccesoNoche(Luis)` | **NO** | **NO** | Denegado (no tiene credencial) |
| `AccesoNoche(Marta)` | **SÍ** | **SÍ** | Permitido |

---

## 3. Trazas de ejecución

### Consulta 1: `AccesoNoche(Ana)`

#### Hacia adelante (Forward Chaining)
- **Hechos iniciales:** `Estudiante(Ana)`, `Estudiante(Luis)`, `Profesor(Marta)`, `TieneCredencial(Ana)`, `TieneCredencial(Marta)`, `HorarioNocturno(Hoy)`.
- **Ronda 1:**
  - `R_miembro_est` con $\{x=\text{Ana}\} \implies$ deriva **`Miembro(Ana)`**
  - `R_miembro_prof` con $\{x=\text{Marta}\} \implies$ deriva **`Miembro(Marta)`**
  - `R_beca` con $\{x=\text{Ana}\} \implies$ deriva **`Becario(Ana)`**
- **Ronda 2:**
  - `R_acceso` con $\{x=\text{Ana}\} \implies$ deriva **`AccesoNoche(Ana)`**
  - `R_acceso` con $\{x=\text{Marta}\} \implies$ deriva **`AccesoNoche(Marta)`**
- **Ronda 3:**
  - Ninguna regla produce hechos nuevos. Se detiene el algoritmo.
- **Resultado:** `AccesoNoche(Ana)` está en los hechos inferidos $\implies$ **PROBADA**.

#### Hacia atrás (Backward Chaining)
```text
Probando meta: AccesoNoche(Ana)
  Intentando regla R_acceso para AccesoNoche(Ana)
    Probando meta: Miembro(Ana)
      Intentando regla R_miembro_est para Miembro(Ana)
        Probando meta: Estudiante(Ana)
          [Éxito con hecho]: Estudiante(Ana)
        Probando meta: TieneCredencial(Ana)
          [Éxito con hecho]: TieneCredencial(Ana)
      [Éxito con regla]: R_miembro_est prueba Miembro(Ana)
    Probando meta: HorarioNocturno(Hoy)
      [Éxito con hecho]: HorarioNocturno(Hoy)
  [Éxito con regla]: R_acceso prueba AccesoNoche(Ana)
Resultado: PROBADA
```

---

### Consulta 2: `AccesoNoche(Luis)`

#### Hacia adelante (Forward Chaining)
Ni en la ronda 1 ni en la 2 se puede disparar `R_miembro_est` para Luis porque falta `TieneCredencial(Luis)`. Tampoco es profesor. Por ende, nunca se genera `Miembro(Luis)` ni `AccesoNoche(Luis)`.
- **Resultado:** **NO PROBADA**.

#### Hacia atrás (Backward Chaining)
```text
Probando meta: AccesoNoche(Luis)
  Intentando regla R_acceso para AccesoNoche(Luis)
    Probando meta: Miembro(Luis)
      Intentando regla R_miembro_est para Miembro(Luis)
        Probando meta: Estudiante(Luis)
          [Éxito con hecho]: Estudiante(Luis)
        Probando meta: TieneCredencial(Luis)
        [Fallo]: No se pudo probar TieneCredencial(Luis)
      [Fallo en premisa TieneCredencial(Luis)] => Regla R_miembro_est descartada.
      Intentando regla R_miembro_prof para Miembro(Luis)
        Probando meta: Profesor(Luis)
        [Fallo]: No se pudo probar Profesor(Luis)
      [Fallo en premisa Profesor(Luis)] => Regla R_miembro_prof descartada.
    [Fallo]: No se pudo probar Miembro(Luis)
  [Fallo en premisa Miembro(Luis)] => Regla R_acceso descartada.
Resultado: NO PROBADA
```

---

### Consulta 3: `AccesoNoche(Marta)`

#### Hacia adelante (Forward Chaining)
Se deriva `Miembro(Marta)` en la ronda 1 mediante `R_miembro_prof`, y en la ronda 2 se deriva `AccesoNoche(Marta)` con `R_acceso` $\implies$ **PROBADA**.

#### Hacia atrás (Backward Chaining)
```text
Probando meta: AccesoNoche(Marta)
  Intentando regla R_acceso para AccesoNoche(Marta)
    Probando meta: Miembro(Marta)
      Intentando regla R_miembro_est para Miembro(Marta)
        Probando meta: Estudiante(Marta)
        [Fallo]: No se pudo probar Estudiante(Marta)
      [Fallo en premisa Estudiante(Marta)] => Regla R_miembro_est descartada.
      Intentando regla R_miembro_prof para Miembro(Marta)
        Probando meta: Profesor(Marta)
          [Éxito con hecho]: Profesor(Marta)
      [Éxito con regla]: R_miembro_prof prueba Miembro(Marta)
    Probando meta: HorarioNocturno(Hoy)
      [Éxito con hecho]: HorarioNocturno(Hoy)
  [Éxito con regla]: R_acceso prueba AccesoNoche(Marta)
Resultado: PROBADA
```

---

## 4. Respuestas a las preguntas del ejercicio

### 1. ¿Por qué `Becario(Ana)` sale en el encadenamiento hacia adelante de `AccesoNoche(Ana)` y no en el de hacia atrás?
- **Hacia adelante es guiado por los datos (*data-driven*):** Dispara cualquier regla cuyas premisas estén completas en los hechos actuales. Como Ana es estudiante y tiene credencial, `R_beca` se dispara y genera `Becario(Ana)`, aunque la consulta solo pregunte por su acceso nocturno.
- **Hacia atrás es guiado por la meta (*goal-driven*):** Empieza en la consulta `AccesoNoche(Ana)` y solo busca reglas que ayuden a probar esa meta (`R_acceso` y `R_miembro_est`). Como ninguna parte de la regla de acceso pide que alguien sea becario, `R_beca` nunca entra en la pila de metas.

---

### 2. ¿Por qué hacia atrás prueba `R_miembro_est` al buscar `Miembro(Marta)`, si Marta es profesora?
El algoritmo no "sabe" de antemano quién es profesor o estudiante; solo revisa las reglas en el orden de la tabla. 
Para resolver la meta `Miembro(Marta)`, busca qué reglas tienen `Miembro(x)` como conclusión. La primera en la lista es `R_miembro_est`, así que unifica $x = \text{Marta}$ y evalúa su primera premisa (`Estudiante(Marta)`). Al no encontrar ese hecho, la regla falla y recién ahí salta a la siguiente opción (`R_miembro_prof`), donde sí tiene éxito.

---

### 3. Si se añade el hecho `TieneCredencial(Luis)` y se vuelve a preguntar `AccesoNoche(Luis)`, ¿qué átomos nuevos aparecen y la consulta queda probada?
Se probó agregando `TieneCredencial(Luis)` a la base:
- **Resultado:** La consulta `AccesoNoche(Luis)` queda **PROBADA** en ambos algoritmos.
- **Átomos nuevos que aparecen:**
  - En la ronda 1 se agregan **`Miembro(Luis)`** (por `R_miembro_est`) y **`Becario(Luis)`** (por `R_beca`).
  - En la ronda 2 se agrega **`AccesoNoche(Luis)`** (por `R_acceso`).
- La lista completa de átomos derivados en FC pasa a ser:  
  `['Miembro(Ana)', 'Miembro(Luis)', 'Miembro(Marta)', 'Becario(Ana)', 'Becario(Luis)', 'AccesoNoche(Ana)', 'AccesoNoche(Luis)', 'AccesoNoche(Marta)']`.
