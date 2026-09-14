# Tarea 1. Definición de las preguntas de negocio

**Roles involucrados:** Análisis de negocio, Análisis de datos (los tres integrantes).

**Equipo:** Jhoiner Javier Ramos Ramírez · Cristian Camilo Rodríguez Cagueñas · Edwin H. Calderón García

---

## 1. Entidad seleccionada

**Instituto Nacional de Vías (INVIAS).**

La entidad se anunció por Slack, como pide el enunciado, y quedó registrada a nombre del equipo.

INVIAS es la entidad del orden nacional encargada de la red vial no concesionada del país. Nos interesó por tres razones: mueve un volumen de contratación alto, ejecuta obra en todo el territorio nacional, y es una entidad sobre la que existe interés permanente de los organismos de control.

El conjunto de datos extraído de SECOP II tiene **25.605 contratos**.

## 2. Qué problema queremos resolver

Quien dirige una entidad como INVIAS no tiene un problema de falta de datos: SECOP II publica todo. El problema es que la información está dispersa en miles de registros y no hay una lectura rápida que permita saber dónde mirar.

Por eso el equipo decidió construir una solución de analítica que identifique **patrones, concentraciones y señales de alerta** en la contratación del INVIAS. La solución está pensada para apoyar la toma de decisiones de la alta Dirección, de las áreas financiera y de contratación, y de los organismos de control interno.

A partir de ahí definimos tres preguntas, una por integrante, que cubren tres ángulos distintos del mismo conjunto de datos: **con quién** se contrata, **dónde** se ejecuta y **cómo** se ejecuta.

---

## 3. Pregunta 1 — Concentración de la contratación

**Responsable:** Jhoiner Javier Ramos Ramírez

> ¿En qué proveedores, modalidades y tipos de contrato se concentra la contratación de INVIAS, y existen patrones de concentración que requieran seguimiento por parte de la Dirección y los organismos de control?

### Variables disponibles

- `proveedor_adjudicado`
- `valor_del_contrato`
- `modalidad_de_contratacion`
- `tipo_de_contrato`
- `estado_contrato`
- `fecha_de_firma`
- `es_grupo`
- `es_pyme`

### Análisis y visualizaciones previstas

- Pareto de proveedores por valor contratado.
- Top de proveedores por número de contratos.
- Participación porcentual de cada proveedor.
- Curva acumulada de concentración.
- Distribución del valor de contratos por proveedor.
- Concentración por modalidad de contratación.
- Relación entre proveedor × modalidad × valor contratado.
- Evolución temporal de la contratación de los principales proveedores.

---

## 4. Pregunta 2 — Distribución territorial de los recursos

**Responsable:** Cristian Camilo Rodríguez Cagueñas

> ¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el lugar de ejecución del contrato, ¿qué proporción de la contratación de la entidad es territorialmente identificable a partir del objeto contractual, y cómo se distribuyen y evolucionan en el territorio los recursos que sí lo son?

### Nota sobre la reformulación

La pregunta original era simplemente *dónde ejecuta INVIAS sus recursos*. Durante la Tarea 2 la auditoría de los datos mostró que ninguna variable geográfica del conjunto sirve para responderla: `departamento`, `ciudad` y `localizacion` traen el mismo valor en el 100 % de los registros (Bogotá), y `direccion_de_ejecucion_del_contrato` está vacía en 25.602 de 25.605 filas. Lo que SECOP II registra es el **domicilio de la entidad**, no el lugar de ejecución.

En lugar de descartar el eje territorial, se reformuló la pregunta para incorporar la trazabilidad como parte del análisis. La justificación completa está en `Tarea 2/Pregunta 2/01_auditoria_territorial_p2.ipynb`.

### Variables disponibles

- `objeto_del_contrato` y `descripcion_del_proceso` — fuente de la inferencia territorial
- `departamento_inferido`, `trazabilidad_territorial` y `n_departamentos` — variables construidas
- `direccion_territorial`, `codigo_via` y `ruta_nacional` — variables complementarias construidas
- `valor_del_contrato`
- `fecha_de_firma`
- `tipo_de_contrato`
- `modalidad_de_contratacion`
- `destino_gasto`

### Análisis y visualizaciones previstas

- Mapa de Colombia por departamento según valor contratado.
- Ranking de departamentos por valor y por número de contratos.
- Evolución anual de la cobertura territorial de la contratación.
- Evolución del valor contratado por departamento.
- Departamento × tipo de contrato y departamento × modalidad de contratación.
- Comparación entre contratación territorializable y contratación de la sede central.
- Distribución del valor contratado por Dirección Territorial.

---

## 5. Pregunta 3 — Ejecución financiera y modificaciones de los contratos

**Responsable:** Edwin H. Calderón García

> ¿Cómo se comporta la ejecución financiera de los contratos de INVIAS y cuáles presentan mayores niveles de recursos pendientes de ejecución, recursos pendientes de pago o extensiones en el plazo contractual que puedan requerir seguimiento?

### Variables disponibles

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

### Análisis y visualizaciones previstas

- Distribución del porcentaje ejecutado.
- Distribución del porcentaje pagado.
- Boxplots de ejecución por tipo de contrato.
- Boxplots por modalidad.
- Top de contratos con mayor valor pendiente.
- Dispersión de valor del contrato frente a porcentaje ejecutado.
- Dispersión de días adicionados frente a valor del contrato.

---

## 6. Por qué estas tres preguntas y no otras

Las tres se apoyan en el mismo conjunto de datos pero no se solapan, y juntas cubren el ciclo que le interesa a un organismo de control:

| Pregunta | Ángulo | Qué permite decidir |
|---|---|---|
| 1 | Con quién se contrata | Si hay dependencia de pocos proveedores o modalidades |
| 2 | Dónde se ejecuta | Si los recursos llegan al territorio y si eso es verificable |
| 3 | Cómo se ejecuta | Qué contratos están atrasados en ejecución, pago o plazo |

Descartamos preguntas que los datos no podían sostener. El caso más claro fue la versión inicial de la Pregunta 2: mantenerla tal cual habría producido un mapa con toda la contratación asignada a Bogotá, que es exactamente el tipo de respuesta que induce a error a quien toma la decisión.
