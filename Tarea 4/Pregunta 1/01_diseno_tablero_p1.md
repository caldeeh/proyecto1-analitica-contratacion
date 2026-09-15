# Tarea 4. Diseño del tablero
## Pregunta 1 — Concentración de la contratación

**Rol:** Tablero de datos
**Responsable:** Jhoiner Javier Ramos Ramírez

---

### 1. Pregunta de negocio

**¿En qué proveedores, modalidades y tipos de contrato se concentra la contratación de INVIAS, y existen patrones de concentración que requieran seguimiento por parte de la Dirección y los organismos de control?**

### 2. Usuario objetivo

El módulo está dirigido a la Alta Dirección del INVIAS y a las áreas de contratación y control interno.

Es un usuario que necesita saber con quién contrata la entidad y mediante qué mecanismos, sin tener que revisar los 17.477 contratos uno por uno. No busca un listado: busca saber dónde mirar.

### 3. Necesidad del usuario

El usuario necesita pasar de una visión agregada de la contratación a la identificación de proveedores y mecanismos que concentren una parte relevante de los recursos.

Por esa razón el módulo debe permitir:

- Conocer el tamaño del universo contractual y cuántos proveedores participan.
- Medir qué tan concentrada está la contratación con indicadores comparables.
- Identificar los proveedores con mayor peso económico.
- Distinguir entre concentración en número de contratos y concentración en valor, que no coinciden.
- Comparar el comportamiento entre modalidades de contratación y tipos de contrato.
- Observar si la concentración aumenta o disminuye en el tiempo.
- Consultar el detalle de un proveedor específico.

### 4. Valores que puede seleccionar el usuario

| Filtro | Campo de datos | Propósito |
|---|---|---|
| Año de firma | `anio_firma` | Acotar el periodo de análisis mediante un rango deslizante. |
| Tipo de contrato | `tipo_de_contrato` | Comparar la concentración según el objeto contractual. |
| Modalidad de contratación | `modalidad_de_contratacion` | Analizar la concentración según el mecanismo de selección. |

Todos los indicadores y visualizaciones se recalculan sobre el subconjunto filtrado. Los índices de concentración no son agregables: se vuelven a calcular sobre los proveedores que quedan después de aplicar los filtros, no se acumulan a partir de valores previos.

El filtro de año advierte que **2017 y 2026 son periodos parciales**, y que la comparación temporal principal se restringe a los años completos entre 2018 y 2025.

### 5. Criterio de medición de la concentración

Se trabaja con dos universos distintos, y la diferencia se declara en el tablero para que el usuario no compare cifras que no son comparables:

| Universo | Contratos | Proveedores | Uso |
|---|---|---|---|
| Conteo | 17.477 formalizados | 8.748 | Frecuencia contractual |
| Valor | 17.244 con valor positivo | 8.640 | Todos los análisis monetarios |

Los indicadores de concentración son los de uso estándar en análisis de competencia:

- **CR1, CR5, CR10** — participación acumulada del primero, los cinco y los diez mayores proveedores sobre el valor contratado.
- **Punto del 80 %** — cuántos proveedores hacen falta para acumular el 80 % del valor.

Sobre el periodo completo, el mayor proveedor concentra el 4,54 % del valor, los cinco mayores el 12,79 % y los diez mayores el 20,38 %. Se necesitan 216 proveedores, el 2,49 % del total, para llegar al 80 % del valor contratado.

### 6. Resultados que genera el tablero

#### 6.1. Indicadores principales (KPI)

| Indicador | Qué responde |
|---|---|
| Contratos formalizados / aptos para conteo | Tamaño del universo bajo los filtros aplicados |
| Valor total contratado | Magnitud económica del periodo seleccionado |
| Proveedores únicos | Cuántos actores participan |
| CR5 · participación de los 5 principales | Concentración en la cúspide |
| CR10 · participación de los 10 principales | Concentración ampliada |

Bajo los indicadores se declara explícitamente cuántos contratos y proveedores entran en los cálculos monetarios, para que el usuario sepa que esos números no son los mismos que los de conteo.

#### 6.2. Reparto entre proveedores

Identifica los proveedores con mayor valor contratado y muestra qué proporción del total representan.

#### 6.3. Forma de la concentración

Muestra cuántos proveedores hacen falta para acumular una fracción dada del valor, y señala el punto en que se alcanza el 80 %.

#### 6.4. Frecuencia frente a peso económico

Compara, para cada modalidad y cada tipo de contrato, el porcentaje de contratos contra el porcentaje del valor. Un mecanismo puede representar muchos contratos pequeños o pocos contratos grandes, y esa diferencia es la que interesa al control.

#### 6.5. Comportamiento en el tiempo

Muestra si la concentración se mantiene, aumenta o disminuye entre 2018 y 2025.

#### 6.6. Detalle por proveedor

Permite consultar un proveedor específico y ver su número de contratos, su valor contratado y su participación.

### 7. Visualizaciones propuestas

#### 7.1. Top 10 proveedores por valor contratado

Barras horizontales ordenadas de mayor a menor. Al pasar el cursor se muestra el valor, el número de contratos y la participación porcentual de cada proveedor.

#### 7.2. Concentración acumulada

Curva de Pareto: porcentaje acumulado de proveedores frente a porcentaje acumulado del valor contratado. Dos líneas de referencia marcan el punto en que se alcanza el 80 % del valor.

Es la visualización central del módulo, porque traduce un índice abstracto en una lectura directa: *cuántos proveedores concentran la mayor parte del dinero*.

#### 7.3. Contratos frente a valor por modalidad

Barras agrupadas con dos series por modalidad: porcentaje de contratos y porcentaje del valor. La distancia entre las dos barras es el hallazgo.

#### 7.4. Contratos frente a valor por tipo de contrato

La misma lectura aplicada al objeto contractual.

#### 7.5. Evolución de la concentración

Series de CR5 y CR10 por año de firma, restringidas a los años completos 2018–2025 para no comparar periodos incompletos.

#### 7.6. Detalle de proveedores

Tabla paginada con buscador por nombre. Columnas: proveedor, número de contratos, valor contratado, porcentaje del valor total y porcentaje acumulado. La participación acumulada se calcula sobre el universo monetario filtrado, no sobre el total general.

### 8. Distribución de los elementos en el tablero

La disposición sigue una lectura de arriba hacia abajo, de lo general a lo particular:

1. **Pregunta de negocio** — encabezado con la pregunta que responde el módulo, para que el usuario sepa qué está mirando.
2. **Fila de indicadores** — los cinco KPI, con la nota sobre los universos de conteo y valor.
3. **Filtros** — año, tipo de contrato y modalidad, con la advertencia sobre los periodos parciales.
4. **Dos tarjetas en paralelo** — Top 10 proveedores a la izquierda, curva de concentración acumulada a la derecha.
5. **Dos tarjetas en paralelo** — modalidad y tipo de contrato.
6. **Tarjeta completa** — evolución de la concentración en el tiempo.
7. **Tarjeta completa** — tabla de detalle por proveedor.

El módulo comparte la hoja de estilos y la estructura de tarjetas del tablero general, de modo que al cambiar de pestaña el usuario no cambia de lenguaje visual.

### 9. Flujo de interacción esperado

1. El usuario abre el módulo y lee los cinco indicadores para dimensionar el universo.
2. Acota el periodo o filtra por modalidad o tipo de contrato según lo que quiera revisar.
3. Mira el Top 10 para identificar los proveedores con mayor peso.
4. Consulta la curva acumulada para saber si ese peso es excepcional o si la concentración es generalizada.
5. Compara modalidades y tipos para ver por qué mecanismo se está concentrando.
6. Revisa la evolución para saber si es un patrón reciente o sostenido.
7. Busca un proveedor concreto en la tabla de detalle.

### 10. Principio de diseño

**Los indicadores describen, no acusan.** La concentración de contratos en pocos proveedores puede responder a la naturaleza del mercado —obras viales de gran escala tienen pocos oferentes capaces— y no constituye por sí sola evidencia de irregularidad.

Por eso el módulo presenta los datos sin calificarlos: muestra dónde está la concentración y deja que el usuario, con la información adicional que él sí tiene sobre los procesos de selección y el número de oferentes, decida qué merece revisión.

Dos decisiones concretas se derivan de ese principio:

- Se declaran los dos universos de análisis en el propio tablero, en lugar de mostrar un solo número que mezcle conteo y valor.
- Se advierte que 2017 y 2026 son periodos parciales, para que nadie lea una caída aparente donde solo hay menos meses.

### 11. Resultado esperado

Un módulo que permite responder, en menos de un minuto y sin conocimiento técnico, en qué proveedores y mediante qué mecanismos se concentra la contratación del INVIAS, con qué intensidad y desde cuándo, y que entrega ese resultado con las salvedades necesarias para que no se interprete de más.
