# Tarea 5. Evaluación

**Roles involucrados:** Análisis de negocio, Análisis de datos, Tablero de datos.
**Lidera:** Análisis de negocio.

El objetivo de esta tarea es revisar, pregunta por pregunta, si lo que construimos responde de verdad a lo que planteamos en la Tarea 1: qué encontramos, qué tan confiable es, qué quedó por fuera y qué puede hacer el usuario con el tablero.

---

## 1. Evaluación de la Pregunta 1 — Concentración de la contratación

**Responsable:** Jhoiner Javier Ramos Ramírez

> PENDIENTE — Javier completa esta sección.
>
> Estructura sugerida, para que las tres queden parejas:
> - Qué respondió el análisis frente a la pregunta original.
> - Hallazgos principales, con las cifras que los sostienen.
> - Qué tan confiable es el resultado (pruebas estadísticas, supuestos, datos faltantes).
> - Qué quedó por fuera o no se pudo responder con estos datos.
> - Qué puede decidir el usuario a partir del módulo del tablero.

---

## 2. Evaluación de la Pregunta 2 — Distribución territorial de los recursos

**Responsable:** Cristian Camilo Rodríguez Cagueñas

### 2.1 Qué respondió el análisis

La pregunta original no se podía responder con los datos tal como vienen. La auditoría lo dejó claro: las variables geográficas de SECOP II registran el domicilio de la entidad, no el lugar de ejecución. Reformulamos la pregunta para que la trazabilidad territorial dejara de ser un supuesto y pasara a ser parte de lo que se mide.

Con esa reformulación, el análisis sí responde las dos partes: cuánto de la contratación es territorialmente identificable, y cómo se distribuye y evoluciona lo que sí lo es.

### 2.2 Hallazgos principales

1. **La cobertura en contratos y en dinero no coinciden.** Solo el 43 % de los contratos puede ubicarse en un departamento, pero esos contratos concentran el 78 % del valor contratado. Es decir: se pierde de vista casi seis de cada diez contratos, pero apenas uno de cada cinco pesos.

2. **Lo que no se ubica es mucho y pequeño.** El 84 % de los contratos sin departamento identificable son de prestación de servicios de la sede central. La prueba chi-cuadrado confirma que la falta de trazabilidad no es aleatoria: está asociada al tipo de contrato, con una V de Cramér de 0,645.

3. **Los recursos van a la periferia, no al centro económico.** Antioquia (2.565 mil millones), Nariño (2.149), Cauca (2.026) y Putumayo (1.476) encabezan el ranking por valor. El patrón es coherente con el mandato de INVIAS sobre la red vial no concesionada.

4. **La trazabilidad se deteriora en los últimos años.** Entre 2018 y 2022 se mantuvo entre 85 % y 95 %; bajó a 76 % en 2023 y 2024, y a 46 % en 2025. Es una tendencia que vale la pena mirar, porque significa que el objeto contractual describe cada vez menos dónde se ejecuta.

### 2.3 Qué tan confiable es

- **Validación de la extracción territorial.** Se revisó una muestra de 60 contratos comparando el departamento asignado contra el texto del objeto contractual. 58 quedaron correctos y 2 dudosos, lo que da una precisión estimada del 96,7 %.
- **Topónimos ambiguos.** Se identificaron seis casos que asignaban mal el departamento (San Juan del Cesar, Magdalena Medio, Ciudad Bolívar, y los municipios homónimos de Bolívar, Sucre y Córdoba). El tratamiento corrigió 80 asignaciones.
- **Precedencia por longitud de alias.** Sin ella, "Norte de Santander" también activaba "Santander" y el contrato quedaba en dos departamentos. Se resolvió ordenando los alias de más largo a más corto y consumiendo el fragmento de texto ya emparejado.
- **Lo que no se validó.** La precisión se estimó sobre una muestra, no sobre el total. Y la validación mide si el departamento mencionado en el texto se extrajo bien, no si el contrato realmente se ejecutó allí: si el objeto contractual dice algo distinto de lo que pasó en campo, el método no lo detecta.

### 2.4 Qué quedó por fuera

- No se puede desagregar por municipio de forma confiable. El diccionario trabaja a nivel de departamento porque los nombres de municipio se repiten entre departamentos y el texto no siempre desambigua.
- Los contratos que mencionan varios departamentos se cuentan en todos. Para el valor contratado eso implica que un contrato multiterritorial aparece completo en cada uno, no repartido.
- El 22 % del valor que no es territorializable queda sin explicación geográfica. Se sabe qué tipo de contratos son, pero no dónde se ejecutaron.

### 2.5 Qué puede decidir el usuario con el módulo

El módulo de distribución territorial le permite a la Dirección y a los organismos de control:

- Ver el reparto de recursos por departamento y por año, con filtros de tipo de contrato y modalidad.
- Saber, en el mismo tablero y no en una nota al pie, qué porcentaje de lo que está viendo es efectivamente rastreable. El indicador de cobertura está arriba por decisión de diseño: un mapa que presenta el 78 % como si fuera el 100 % induce a error.
- Decidir con evidencia si vale la pena exigir que el lugar de ejecución se registre como campo estructurado en la fuente. El hallazgo 4 es el argumento: la trazabilidad se está deteriorando.

### 2.6 Una decisión de diseño que vale la pena registrar

Los 2.374 contratos sin `fecha_de_firma` se incluyen por defecto mediante una casilla explícita. Excluirlos en silencio con el filtro de año subía el indicador de cobertura de 77,9 % a 88,2 %, y el tablero habría contradicho al informe sin que nadie notara por qué.

---

## 3. Evaluación de la Pregunta 3 — Ejecución financiera y modificaciones

**Responsable:** Edwin H. Calderón García

> PENDIENTE — Edwin completa esta sección, con la misma estructura de la sección 1.

---

## 4. Evaluación del tablero como producto

### 4.1 Frente a la necesidad del usuario

El tablero está organizado en tres pestañas, una por pregunta de negocio. La decisión fue modular a propósito: cada pregunta tiene su propio usuario y su propia lectura, y mezclarlas en una sola vista habría obligado a quien entra buscando una cosa a filtrar lo demás.

### 4.2 Qué funciona

- Cada módulo responde su pregunta sin depender de los otros.
- Los filtros son los mismos conceptos que el usuario ya maneja (año, tipo de contrato, modalidad), no categorías inventadas para el análisis.
- Los indicadores de contexto —cobertura territorial en la Pregunta 2— están a la vista y no escondidos.

### 4.3 Limitaciones reconocidas

- El tablero consume archivos agregados precalculados, no la base completa. Es una decisión deliberada por el tamaño de la instancia de EC2, pero significa que no permite consultas ad hoc fuera de los cortes previstos.
- El mapa se dibuja con `Choroplethmapbox` sobre fondo plano, sin mapa base externo. Se hizo así porque la versión con mapa base descarga geometría desde un CDN y falla si la instancia no tiene salida a internet.
- Para actualizar los datos hay que volver a correr `preparar_datos.py` y volver a desplegar. No hay recarga automática.

### 4.4 Qué haríamos distinto con más tiempo

> PENDIENTE — cerrar entre los tres. Sugerencias desde la Pregunta 2:
> - Cruzar el departamento inferido contra los códigos de vía y rutas nacionales para subir la trazabilidad del 43 % de contratos.
> - Desagregar a nivel de municipio con un diccionario desambiguado.
> - Añadir una vista que compare las tres preguntas sobre el mismo contrato.

---

## 5. Conclusión general

> PENDIENTE — la escribe Análisis de negocio (lidera Javier), después de que estén las tres secciones.
>
> Debería cerrar con: qué aprendió el equipo sobre la contratación del INVIAS, y qué debería hacer distinto la entidad a partir de lo que muestra el tablero.
