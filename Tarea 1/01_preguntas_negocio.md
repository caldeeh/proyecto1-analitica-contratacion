# Tarea 1 — Determinación de las preguntas de negocio

## 1. Contexto

La entidad seleccionada para el proyecto es el Instituto Nacional de Vías (INVIAS).

A partir del entendimiento del propósito de los datos disponibles de contratación pública, el equipo definió desarrollar una solución de analítica orientada a identificar patrones, concentraciones y señales de alerta que requieran seguimiento respecto de la contratación de INVIAS.

La solución busca apoyar la toma de decisiones de la Alta Dirección, los procesos financieros y de contratación, así como las actividades de los organismos de control interno.

**Roles involucrados:** Análisis de negocio y análisis de datos.

---

## 2. Preguntas de negocio

### Pregunta 1 — Concentración de la contratación

**Responsable:** Jhoiner Javier Ramos Ramírez

**Pregunta:**

> ¿En qué proveedores, modalidades y tipos de contrato se concentra la contratación de INVIAS, y existen patrones de concentración que requieran seguimiento por parte de la Dirección y los organismos de control?

### Variables principales

- `proveedor_adjudicado`
- `valor_del_contrato`
- `modalidad_de_contratacion`
- `tipo_de_contrato`
- `estado_contrato`
- `fecha_de_firma`
- `es_grupo`
- `es_pyme`

### Análisis y visualizaciones propuestas

- Pareto de proveedores por valor contratado.
- Top de proveedores por número de contratos.
- Participación porcentual de cada proveedor.
- Curva acumulada de concentración.
- Distribución del valor de los contratos por proveedor.
- Concentración por modalidad de contratación.
- Relación entre proveedor, modalidad y valor contratado.
- Evolución temporal de la contratación de los principales proveedores.

El objetivo es identificar concentraciones relevantes de recursos o contratos que puedan orientar el seguimiento de la gestión contractual.

---

### Pregunta 2 — Distribución territorial de los recursos

**Responsable:** Cristian Camilo Rodríguez Cagueñas

**Pregunta inicialmente planteada:**

> ¿Dónde ejecuta INVIAS sus recursos?

Durante la etapa de análisis y alistamiento se identificó que los campos geográficos estructurados disponibles en SECOP II no representan directamente el lugar de ejecución del contrato, sino principalmente el domicilio de la entidad.

Por esta razón, la pregunta fue reformulada para incorporar explícitamente la limitación de trazabilidad territorial:

> ¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el lugar de ejecución del contrato, ¿qué proporción de la contratación de la entidad es territorialmente identificable a partir del objeto contractual, y cómo se distribuyen y evolucionan en el territorio los recursos que sí lo son?

### Variables principales

- `objeto_del_contrato`
- `descripcion_del_proceso`
- `departamento_inferido`
- `trazabilidad_territorial`
- `n_departamentos`
- `direccion_territorial`
- `codigo_via`
- `ruta_nacional`
- `valor_del_contrato`
- `fecha_de_firma`
- `tipo_de_contrato`
- `modalidad_de_contratacion`
- `destino_gasto`

### Análisis y visualizaciones propuestas

- Mapa de Colombia por departamento según valor contratado.
- Ranking de departamentos por valor contratado.
- Ranking de departamentos por número de contratos.
- Evolución anual de la cobertura territorial de la contratación.
- Evolución del valor contratado por departamento.
- Departamento × tipo de contrato.
- Departamento × modalidad de contratación.
- Comparación entre contratación territorializable y contratación de la sede central.
- Distribución del valor contratado por Dirección Territorial.

La reformulación permite analizar la dimensión territorial sin asumir que los campos geográficos originales representan el lugar efectivo de ejecución.

---

### Pregunta 3 — Ejecución financiera y modificaciones de los contratos

**Responsable:** Edwin H. Calderón García

**Pregunta:**

> ¿Cómo se comporta la ejecución financiera de los contratos de INVIAS y cuáles presentan mayores niveles de recursos pendientes de ejecución, recursos pendientes de pago o extensiones en el plazo contractual que puedan requerir seguimiento?

### Variables principales

- `valor_del_contrato`
- `valor_facturado`
- `valor_pagado`
- `valor_pendiente_de_pago`
- `valor_pendiente_de_ejecucion`
- `saldo_cdp`
- `dias_adicionados`
- `estado_contrato`
- `duracion_del_contrato`
- `fecha_de_inicio_del_contrato`
- `fecha_de_fin_del_contrato`
- `el_contrato_puede_ser_prorrogado`

### Análisis y visualizaciones propuestas

- Distribución del porcentaje ejecutado.
- Distribución del porcentaje pagado.
- Boxplots de ejecución por tipo de contrato.
- Boxplots de ejecución por modalidad.
- Top de contratos con mayor valor pendiente.
- Relación entre valor del contrato y porcentaje ejecutado.
- Relación entre días adicionados y valor del contrato.
- Estado del contrato × ejecución financiera.
- Ranking de contratos que requieren mayor seguimiento.

El análisis busca identificar patrones de ejecución financiera, recursos pendientes y modificaciones en los plazos que permitan establecer señales de seguimiento sobre la gestión contractual.

---

## 3. Enfoque general de la solución

Las tres preguntas fueron diseñadas para analizar la contratación de INVIAS desde perspectivas complementarias:

| Pregunta | Dimensión | Responsable |
|---|---|---|
| 1 | Concentración de la contratación | Jhoiner Javier Ramos Ramírez |
| 2 | Distribución y trazabilidad territorial | Cristian Camilo Rodríguez Cagueñas |
| 3 | Ejecución financiera y modificaciones contractuales | Edwin H. Calderón García |

En conjunto, las preguntas permiten analizar:

1. **En quién y mediante qué mecanismos se concentra la contratación.**
2. **Dónde es posible identificar territorialmente la contratación y cómo se distribuyen los recursos.**
3. **Cómo se ejecutan financieramente los contratos y cuáles presentan señales que ameritan seguimiento.**

La solución analítica se orientará a generar evidencia descriptiva y visual que facilite la identificación de patrones y señales de seguimiento, sin interpretar por sí misma la existencia de irregularidades o conductas indebidas.

---

## 4. Relación con las etapas posteriores del proyecto

Las preguntas de negocio definidas en esta etapa constituyen el eje para las actividades posteriores de:

- Selección, limpieza y alistamiento de datos.
- Análisis exploratorio y descriptivo.
- Diseño y desarrollo del tablero de analítica.
- Evaluación de resultados.
- Despliegue de la solución.

Cada integrante desarrollará el análisis correspondiente a su pregunta y sus resultados serán integrados posteriormente en el tablero general del proyecto.