# Tarea 4. Diseño del tablero
## Pregunta 3 — Ejecución financiera y modificaciones de los contratos

### 1. Pregunta de negocio

**¿Cómo se comporta la ejecución financiera de los contratos de INVIAS y cuáles presentan mayores niveles de recursos pendientes de ejecución, recursos pendientes de pago o extensiones en el plazo contractual que puedan requerir seguimiento?**

### 2. Usuario objetivo

El tablero está dirigido a funcionarios o analistas responsables del seguimiento de la contratación pública de INVIAS.

El usuario requiere una herramienta que le permita analizar de manera rápida el comportamiento de la ejecución financiera de los contratos y facilitar la identificación de aquellos que, por sus recursos pendientes de ejecución, recursos pendientes de pago o extensiones en el plazo contractual, puedan requerir seguimiento.

### 3. Necesidad del usuario

El usuario necesita pasar de una visión general de la ejecución contractual a una identificación concreta de los contratos que requieren mayor atención.

Por esta razón, el tablero debe permitir:

- Conocer el panorama general de la ejecución financiera.
- Analizar los recursos pendientes de ejecución y de pago.
- Identificar la presencia y concentración de extensiones contractuales.
- Comparar el comportamiento de los contratos según sus principales características.
- Priorizar contratos que presenten simultáneamente altos niveles de recursos pendientes de ejecución y extensiones en el plazo contractual.
- Consultar el detalle de los contratos seleccionados para facilitar su seguimiento.

El tablero debe presentar la información de manera clara y orientada a la toma de decisiones, evitando sobrecargar al usuario con visualizaciones que no aporten directamente a la pregunta de negocio.

### 4. Valores que puede seleccionar el usuario

El tablero permitirá al usuario segmentar la información mediante filtros relacionados con las principales características de los contratos.

Los filtros propuestos son:

| Filtro | Campo de datos | Propósito |
|---|---|---|
| Estado del contrato | `estado_contrato` | Analizar la ejecución según la situación contractual. |
| Tipo de contrato | `tipo_de_contrato` | Comparar el comportamiento financiero entre tipos de contrato. |
| Modalidad de contratación | `modalidad_de_contratacion` | Identificar diferencias en la ejecución y las extensiones según la modalidad. |
| Extensión contractual | `tiene_extension` | Comparar contratos con y sin extensiones. |
| Nivel de ejecución | `nivel_ejecucion` | Concentrar el análisis en contratos con diferentes niveles de ejecución financiera. |

Adicionalmente, el usuario podrá seleccionar si desea consultar únicamente los contratos identificados como prioritarios para seguimiento.

### 5. Criterio de priorización

Para facilitar el seguimiento, se utilizará como criterio de priorización la identificación de contratos que presentan simultáneamente:

- Un valor pendiente de ejecución superior al percentil 90 de la distribución.
- Un número de días adicionados superior al percentil 90 de la distribución.

Con este criterio se identificaron **750 contratos prioritarios** en la etapa de exploración.

El criterio busca concentrar la atención del usuario en contratos que combinan un nivel elevado de recursos pendientes de ejecución con extensiones relevantes del plazo contractual.

La priorización constituye una herramienta de apoyo al seguimiento y **no implica que exista una irregularidad en los contratos identificados**.

### 6. Resultados que genera el tablero

A partir de los filtros seleccionados por el usuario, el tablero actualizará dinámicamente los principales indicadores y visualizaciones relacionados con la ejecución financiera y las modificaciones contractuales.

Los resultados principales serán:

#### 6.1. Indicadores principales (KPI)

El tablero mostrará cuatro indicadores principales:

| Indicador | Descripción |
|---|---|
| Contratos analizados | Número de contratos incluidos después de aplicar los filtros. |
| Recursos pendientes de ejecución | Valor total de los recursos pendientes de ejecución de los contratos seleccionados. |
| Recursos pendientes de pago | Valor total de los recursos pendientes de pago de los contratos seleccionados. |
| Contratos prioritarios | Número de contratos que cumplen simultáneamente el criterio de priorización definido. |

Estos indicadores permitirán obtener rápidamente una visión general de la situación contractual bajo los filtros seleccionados.

#### 6.2. Comportamiento de la ejecución financiera

El tablero permitirá analizar la distribución de los contratos según su nivel de ejecución financiera, facilitando la identificación de concentraciones de contratos con niveles bajos, intermedios o altos de ejecución.

#### 6.3. Recursos pendientes

Se mostrará el comportamiento de los recursos pendientes de ejecución y de pago, permitiendo identificar los contratos con mayores valores pendientes y facilitar su priorización para seguimiento.

#### 6.4. Extensiones contractuales

Se mostrará la presencia de extensiones contractuales y su comportamiento según las principales características de los contratos.

Esto permitirá identificar categorías de contratos en las que se concentra una mayor proporción de extensiones.

#### 6.5. Relación entre ejecución y pago

El tablero permitirá comparar el porcentaje ejecutado frente al porcentaje pagado para identificar el grado de correspondencia entre ambos indicadores y detectar casos que presenten diferencias relevantes.

#### 6.6. Contratos prioritarios

El tablero permitirá identificar y consultar los contratos que superan simultáneamente los umbrales establecidos para recursos pendientes de ejecución y días adicionados.

Estos contratos serán presentados como un grupo de seguimiento prioritario, permitiendo analizar sus principales características y consultar su información individual.

#### 6.7. Detalle contractual

Finalmente, el usuario podrá consultar el detalle de los contratos seleccionados mediante una tabla interactiva que incluirá, entre otros:

- ID del contrato.
- Proveedor.
- Tipo de contrato.
- Modalidad de contratación.
- Valor del contrato.
- Porcentaje ejecutado.
- Porcentaje pagado.
- Recursos pendientes de ejecución.
- Recursos pendientes de pago.
- Días adicionados.
- Estado del contrato.

### 7. Visualizaciones propuestas

Las visualizaciones se seleccionarán de acuerdo con su capacidad para responder directamente a la pregunta de negocio y facilitar la identificación de contratos que puedan requerir seguimiento.

#### 7.1. Comportamiento de la ejecución financiera

**Visualización:** distribución de contratos por nivel de ejecución.

Permitirá observar cómo se distribuyen los contratos según su porcentaje de ejecución financiera.

Se utilizarán categorías de ejecución que permitan diferenciar contratos con:

- 0 % de ejecución.
- Ejecución baja.
- Ejecución intermedia.
- Ejecución alta o superior al 100 %.

**Propósito:** identificar rápidamente concentraciones de contratos con bajos niveles de ejecución.

---

#### 7.2. Recursos pendientes de ejecución y de pago

**Visualización:** ranking de contratos con mayores recursos pendientes.

Se presentarán los contratos con mayores valores pendientes de ejecución y, de manera complementaria, los valores pendientes de pago.

**Propósito:** identificar los contratos que concentran los mayores recursos pendientes y facilitar su selección para seguimiento.

---

#### 7.3. Extensiones contractuales

**Visualización:** gráfico de barras por tipo de contrato.

El gráfico mostrará la proporción o cantidad de contratos con extensión contractual para los principales tipos de contrato.

**Propósito:** identificar dónde se concentra la presencia de extensiones contractuales.

---

#### 7.4. Ejecución financiera frente a pago

**Visualización:** gráfico de dispersión.

Se relacionará el porcentaje ejecutado con el porcentaje pagado para cada contrato.

**Propósito:** identificar el grado de correspondencia entre ejecución y pago y detectar observaciones que se aparten del comportamiento general.

---

#### 7.5. Contratos prioritarios

**Visualización:** resumen de contratos prioritarios acompañado de gráficos de caracterización.

Se mostrarán los contratos que superan simultáneamente los percentiles 90 de recursos pendientes de ejecución y días adicionados.

La caracterización se realizará principalmente mediante:

- Tipo de contrato.
- Modalidad de contratación.

**Propósito:** facilitar la identificación de patrones dentro del grupo de contratos prioritarios.

---

#### 7.6. Detalle de contratos

**Visualización:** tabla interactiva.

La tabla permitirá ordenar, filtrar y consultar los contratos seleccionados.

Entre los campos principales se incluirán:

- ID del contrato.
- Proveedor.
- Tipo de contrato.
- Modalidad.
- Valor del contrato.
- Porcentaje ejecutado.
- Porcentaje pagado.
- Recursos pendientes de ejecución.
- Recursos pendientes de pago.
- Días adicionados.
- Estado del contrato.

**Propósito:** permitir al usuario pasar del análisis agregado al seguimiento de contratos específicos.

### 8. Instrucciones para el usuario

El tablero incluirá un botón o sección de información que explique de manera breve:

- El objetivo del tablero.
- El significado de los principales indicadores.
- El funcionamiento de los filtros.
- El criterio utilizado para identificar los contratos prioritarios.
- La interpretación de los principales gráficos.

Las instrucciones estarán disponibles mediante un elemento informativo ubicado en la parte superior del tablero, evitando ocupar espacio permanente en el área principal de análisis.

El usuario podrá consultar esta información cuando la necesite sin abandonar el tablero.

### 9. Distribución de los elementos en el tablero

El tablero se organizará siguiendo una secuencia de análisis que facilite pasar de una visión general a la identificación de contratos específicos:

**Panorama → Diagnóstico → Priorización → Detalle**

La distribución conceptual será la siguiente:

#### 9.1. Encabezado

En la parte superior se presentará:

- Nombre del tablero.
- Pregunta de negocio.
- Botón de información con las instrucciones de uso.

#### 9.2. Área de filtros

Debajo del encabezado se ubicarán los filtros principales:

- Estado del contrato.
- Tipo de contrato.
- Modalidad de contratación.
- Extensión contractual.
- Nivel de ejecución.
- Opción para consultar únicamente contratos prioritarios.

Los filtros permitirán modificar dinámicamente los resultados mostrados en el tablero.

#### 9.3. Área de indicadores

Después de los filtros se ubicarán los principales KPI:

- Contratos analizados.
- Recursos pendientes de ejecución.
- Recursos pendientes de pago.
- Contratos prioritarios.

Esta sección permitirá al usuario obtener rápidamente una visión general de los contratos seleccionados.

#### 9.4. Área de análisis

En la sección central se ubicarán las principales visualizaciones:

- Distribución del nivel de ejecución financiera.
- Ranking de contratos con mayores recursos pendientes.
- Comportamiento de las extensiones contractuales.
- Relación entre porcentaje ejecutado y porcentaje pagado.

Esta sección constituye el núcleo analítico del tablero.

#### 9.5. Área de priorización

Posteriormente se presentará el grupo de contratos prioritarios, acompañado de su caracterización por tipo y modalidad de contratación.

Esta sección permitirá concentrar la atención del usuario en los contratos que cumplen el criterio de priorización.

#### 9.6. Área de detalle

En la parte inferior se ubicará una tabla interactiva con el detalle de los contratos.

Esta tabla permitirá pasar del análisis agregado a la consulta individual de los contratos y facilitará las actividades de seguimiento.

### 10. Flujo de interacción esperado

El usuario podrá utilizar el tablero siguiendo el siguiente flujo:

1. Revisar los indicadores generales.
2. Aplicar los filtros de interés.
3. Analizar el comportamiento de la ejecución financiera.
4. Revisar los recursos pendientes y las extensiones contractuales.
5. Identificar los contratos prioritarios.
6. Consultar el detalle de los contratos seleccionados.
7. Utilizar la información obtenida como insumo para las actividades de seguimiento.


### 11. Matriz de diseño funcional

La siguiente matriz relaciona las necesidades del usuario con los elementos que tendrá el tablero y las decisiones que estos permitirán apoyar.

| Necesidad del usuario | Indicador / información | Visualización | Interacción | Decisión que permite apoyar |
|---|---|---|---|---|
| Conocer el universo de contratos analizados | Número de contratos | KPI | Filtros | Dimensionar el análisis |
| Conocer el nivel general de ejecución | Porcentaje de ejecución | Distribución por niveles | Filtros | Identificar concentración de contratos con baja ejecución |
| Identificar recursos pendientes | Recursos pendientes de ejecución y de pago | KPI y ranking | Ordenar, filtrar y seleccionar | Priorizar revisión financiera |
| Analizar las extensiones contractuales | Contratos con extensión | Gráfico de barras | Filtros por tipo y modalidad | Identificar categorías con mayor presencia de extensiones |
| Comparar ejecución y pago | Porcentaje ejecutado vs. porcentaje pagado | Gráfico de dispersión | Selección y filtros | Identificar diferencias relevantes entre ejecución y pago |
| Identificar contratos prioritarios | Contratos que superan los umbrales definidos | KPI y listado | Filtro de prioritarios | Concentrar el seguimiento en contratos de mayor interés |
| Caracterizar los contratos prioritarios | Tipo y modalidad | Gráficos de barras | Selección | Identificar patrones dentro del grupo prioritario |
| Consultar contratos específicos | Información contractual y financiera | Tabla interactiva | Ordenar, filtrar y consultar | Facilitar el seguimiento individual |

### 12. Principio de diseño

El diseño del tablero seguirá el principio de **"potente pero no saturado"**.

Se priorizarán las visualizaciones que aporten directamente a la pregunta de negocio y se evitará duplicar información entre gráficos.

La interacción mediante filtros permitirá que una misma visualización responda a diferentes segmentos de contratos, reduciendo la necesidad de incorporar múltiples gráficos.

El tablero estará orientado a la identificación y seguimiento de contratos, por lo que la información agregada se complementará con la posibilidad de consultar el detalle contractual.

### 13. Resultado esperado

El resultado esperado es un módulo interactivo que permita al usuario:

1. Obtener una visión general de la ejecución financiera de los contratos.
2. Analizar los recursos pendientes de ejecución y de pago.
3. Identificar la presencia de extensiones contractuales.
4. Detectar diferencias relevantes entre ejecución y pago.
5. Identificar los contratos que cumplen el criterio de priorización.
6. Caracterizar los contratos prioritarios.
7. Consultar el detalle de los contratos para apoyar las actividades de seguimiento.

Este módulo será posteriormente integrado con los módulos correspondientes a las Preguntas 1 y 2 en un único tablero desarrollado en Dash.