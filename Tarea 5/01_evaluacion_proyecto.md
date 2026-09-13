# Tarea 5 — Evaluación del proyecto

## 1. Evaluación frente a las preguntas de negocio

### Pregunta 1 — Concentración de la contratación

La evaluación de esta pregunta queda pendiente de incorporación de los resultados del análisis correspondiente. Esta sección será actualizada una vez se complete el análisis de concentración de la contratación del INVIAS.

### Pregunta 2 — Distribución territorial

**Hallazgo.** El análisis evidencia que la información territorial disponible en SECOP II es parcial, debido a que los campos geográficos estructurados no representan necesariamente el lugar de ejecución del contrato. Por esta razón, se utilizó la información textual del objeto y la descripción del proceso para inferir el territorio asociado. El análisis permitió identificar un departamento de manera inequívoca para una parte relevante de los contratos y estos representan una proporción mayor del valor total contratado.

**Análisis.** La metodología permitió separar los contratos con una atribución territorial inequívoca de aquellos cuya ubicación no podía determinarse con suficiente confiabilidad. Para evitar una sobreestimación, los contratos asociados a múltiples departamentos no fueron asignados de manera arbitraria a un único territorio. Adicionalmente, se generaron agregaciones por departamento, año, tipo de contrato y modalidad, permitiendo analizar tanto la distribución como su evolución.

**Conclusión.** La pregunta de negocio puede responderse de manera parcial pero útil para la toma de decisiones. El análisis permite identificar patrones territoriales relevantes; sin embargo, la principal limitación corresponde a la calidad y estructura de la información disponible en SECOP II. Una identificación estructurada del lugar de ejecución permitiría mejorar considerablemente la trazabilidad territorial de los recursos.

### Pregunta 3 — Ejecución financiera y modificaciones

**Hallazgo.** El análisis permitió caracterizar el comportamiento de la ejecución financiera y establecer una metodología para identificar contratos que requieren mayor atención. Se encontraron 18.228 contratos con recursos pendientes de ejecución y se identificaron 750 contratos que superan simultáneamente los percentiles 90 de recursos pendientes de ejecución y días adicionados. Todos estos contratos presentan extensión del plazo contractual.

**Análisis.** Los resultados muestran una relación muy fuerte entre los niveles de ejecución y pago. Asimismo, los contratos con extensión presentan niveles superiores de recursos pendientes de ejecución. Los contratos priorizados se concentran principalmente en estados como *Modificado* y *Suspendido*, y en tipos contractuales como *Obra*, *Otro*, *Prestación de servicios*, *Interventoría* y *Consultoría*. Estos patrones permiten establecer una señal objetiva de priorización para seguimiento, sin interpretar dicha clasificación como evidencia de irregularidad.

**Conclusión.** La pregunta de negocio se responde mediante la integración de variables financieras y contractuales en un mecanismo de priorización. El principal aporte es transformar un conjunto amplio de registros en una herramienta que permite orientar el seguimiento hacia contratos con mayores niveles relativos de recursos pendientes y extensión del plazo.

## 2. Evaluación del análisis descriptivo y estadístico

El análisis descriptivo permitió pasar de una revisión general de la base a la identificación de patrones relevantes para las preguntas de negocio. Se utilizaron medidas de tendencia central, percentiles, distribuciones, segmentaciones, análisis temporal y relaciones entre variables, complementadas con visualizaciones.

### 2.1. Pregunta 2 — Distribución territorial

El análisis mostró que la información territorial no está disponible directamente en los campos estructurados de SECOP II. Como respuesta, se construyó una variable territorial a partir del texto contractual, utilizando normalización, un diccionario de 33 entidades territoriales y reglas para evitar falsos positivos. El tratamiento de topónimos ambiguos permitió corregir 80 asignaciones potencialmente erróneas en 98 contratos identificados con expresiones ambiguas.

Desde el punto de vista descriptivo, de los 19.617 contratos con valor válido, el 40,9 % presentó un departamento único identificable y el 2,3 % correspondió a contratos multidepartamentales. En conjunto, estos contratos representan el 77,9 % del valor contratado. Los contratos no territorializables representan el 56,7 % de los registros, pero solamente el 22,1 % del valor.

Entre los departamentos con mayor valor contratado se encuentran Antioquia (12,8 %), Nariño (10,7 %), Cauca (10,1 %), Putumayo (7,4 %) y Norte de Santander (6,5 %). Esto evidencia que la distribución territorial de los recursos no es homogénea y que existen territorios con una participación relevante dentro de la contratación territorialmente identificable.

La principal fortaleza de este análisis es que permite recuperar información territorial que no estaba disponible de manera estructurada. Su principal limitación es que la asignación depende del contenido textual del contrato, por lo que los resultados deben interpretarse como una aproximación territorial y no como un registro oficial del lugar de ejecución.

### 2.2. Pregunta 3 — Ejecución financiera

El análisis descriptivo evidenció una distribución altamente asimétrica de las variables financieras. La diferencia entre media y mediana muestra que unos pocos contratos con valores elevados pueden afectar significativamente los promedios, por lo que se utilizaron medidas robustas como la mediana y los percentiles.

En ejecución financiera, la media fue de 34,73 % y la mediana de 0 %. Se identificaron 11.310 contratos con ejecución registrada de 0 %. Sin embargo, este resultado no puede interpretarse de forma aislada: la segmentación por estado contractual mostró que los contratos cerrados presentan una mediana de ejecución de 88,72 %, mientras que los contratos en ejecución presentan una mediana de 48,89 %.

La relación entre ejecución y pago fue muy alta, con una correlación de 0,989. Adicionalmente, en al menos el 90 % de los contratos la diferencia entre ambos porcentajes fue igual a cero, lo que evidencia una elevada consistencia entre ambas variables en la información analizada.

El análisis de recursos pendientes permitió identificar 18.228 contratos con valores positivos pendientes de ejecución, por aproximadamente $38,07 billones. La diferencia entre la mediana ($56 millones) y el promedio ($2.088,7 millones) confirma la presencia de una distribución sesgada hacia valores altos.

Finalmente, el cruce del percentil 90 de recursos pendientes de ejecución ($970,15 millones) con el percentil 90 de días adicionados (58 días) permitió identificar 750 contratos prioritarios. El 100 % de estos contratos presenta extensión contractual, y el grupo se concentra principalmente en estados modificados y suspendidos. Este resultado permite transformar el análisis descriptivo en una señal objetiva para orientar el seguimiento.

En conjunto, el análisis descriptivo y estadístico fue suficiente para identificar patrones, segmentar comportamientos y establecer criterios de priorización. No obstante, los resultados deben interpretarse considerando la calidad de los datos y evitando inferencias causales que no pueden ser sustentadas por el análisis realizado.

---

## 3. Evaluación de los modelos predictivos

En el alcance desarrollado para el proyecto no se implementaron modelos predictivos. El análisis se concentró en técnicas descriptivas, estadísticas y visuales orientadas a responder las preguntas de negocio y a identificar patrones de comportamiento y señales de seguimiento.

Esta decisión es consistente con el objetivo alcanzado por el proyecto: antes de realizar predicciones resulta necesario contar con variables suficientemente completas, consistentes y representativas. En particular, el análisis territorial evidenció limitaciones de cobertura y el análisis financiero identificó valores extremos que requieren validación.

Como oportunidad de desarrollo futuro, una base histórica con mayor calidad y variables adicionales podría permitir construir modelos orientados, por ejemplo, a estimar probabilidad de extensión contractual, niveles esperados de ejecución o probabilidad de pertenecer a grupos que requieran seguimiento.

---

## 4. Evaluación del tablero desarrollado

El tablero constituye el producto que integra los resultados analíticos en una herramienta orientada a la consulta y toma de decisiones. La aplicación organiza las tres preguntas de negocio como módulos independientes y está dirigida a usuarios de la Alta Dirección del INVIAS y organismos de control interno.

Desde el punto de vista funcional, el tablero permite explorar la información territorial y financiera mediante indicadores, gráficos y filtros. En la Pregunta 3, la interacción entre estado, tipo, modalidad, extensión y nivel de ejecución permite pasar de una visión general a la identificación de contratos específicos que pueden requerir seguimiento.

Una decisión técnica relevante fue utilizar datos agregados para alimentar el tablero. En lugar de cargar la base analítica completa de 25.605 registros, se generan archivos específicos para las visualizaciones, con un tamaño conjunto inferior a 250 KB. Esto reduce el consumo de memoria y facilita el funcionamiento de la aplicación en una instancia pequeña de AWS EC2.

El tablero también incorpora una estructura modular que facilita la integración de los aportes de los diferentes integrantes y permite mantener separadas las lógicas correspondientes a cada pregunta de negocio.

En términos de utilidad, el tablero cumple con el objetivo de convertir los resultados del análisis en información accesible para usuarios no técnicos. Su principal limitación es que la calidad de las conclusiones continúa dependiendo de la calidad de los datos de origen y de las reglas metodológicas utilizadas para construir algunas variables.

---

## 5. Limitaciones y oportunidades de mejora

Las principales limitaciones identificadas durante el proyecto fueron:

- La información territorial no está estructurada como lugar de ejecución, por lo que fue necesario inferirla a partir del texto contractual.
- La extracción territorial presenta cobertura parcial y requiere validación adicional mediante revisión manual de una muestra.
- La distribución financiera presenta valores extremos. En particular, 14 contratos concentran aproximadamente el 99,996 % del valor pendiente de pago reportado, por lo que este indicador debe interpretarse con precaución y no utilizarse directamente para rankings sin una revisión previa.
- La identificación de contratos prioritarios constituye una regla de seguimiento y no una evidencia de irregularidad o incumplimiento.
- El proyecto no incorporó modelos predictivos, por lo que el análisis se limita a describir y priorizar situaciones observadas en los datos disponibles.

Como oportunidades de mejora se plantea fortalecer la calidad y estructura de la información territorial y financiera, incorporar nuevos cortes periódicos de SECOP II y desarrollar posteriormente modelos predictivos sobre variables previamente validadas.

---

## 6. Conclusión general de la evaluación

La evaluación del proyecto muestra que el análisis desarrollado permitió transformar los datos de contratación del INVIAS en información útil para responder preguntas concretas de negocio.

El análisis descriptivo y estadístico permitió identificar patrones territoriales, financieros y contractuales, mientras que la construcción de indicadores y criterios de priorización permitió orientar el análisis hacia situaciones que pueden requerir seguimiento. El tablero integra estos resultados y facilita su consulta mediante una interfaz interactiva.

Aunque existen limitaciones asociadas principalmente a la calidad y estructura de los datos, estas fueron identificadas y documentadas durante el proceso. En consecuencia, el principal resultado del proyecto no es solamente la descripción de la contratación, sino la construcción de una herramienta analítica que permite organizar, visualizar y priorizar información para apoyar la toma de decisiones.

Los resultados deben interpretarse como señales analíticas que orientan revisiones posteriores y no como conclusiones definitivas sobre el comportamiento o la gestión de los contratos.