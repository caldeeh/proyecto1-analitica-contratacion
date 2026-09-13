# Tarea 4. Diseño del tablero
## Pregunta 2 — Distribución territorial de los recursos

**Rol:** Tablero de datos
**Integrante:** Cristian Camilo Rodríguez Cagueñas

### 1. Pregunta de negocio

**¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el lugar de ejecución del contrato, ¿qué proporción de la contratación es territorialmente identificable a partir del objeto contractual, y cómo se distribuyen y evolucionan en el territorio los recursos que sí lo son?**

### 2. Usuario objetivo

El tablero se dirige a la alta Dirección del INVIAS y a los organismos de control interno.

Es un usuario que necesita responder dos cosas distintas con la misma herramienta: dónde se están ejecutando los recursos de la entidad, y qué tan confiable es esa respuesta. La segunda pregunta no es habitual en un tablero, pero en este caso es inseparable de la primera: la ubicación no viene registrada en la fuente, se infiere del objeto contractual, y el usuario tiene derecho a saber sobre qué porción de la contratación está mirando.

### 3. Necesidad del usuario

El usuario necesita pasar de una visión nacional agregada a la identificación de dónde se concentra la contratación, sin perder de vista la cobertura de la información que sustenta esa lectura.

El tablero debe permitirle:

- Conocer qué proporción de los recursos puede ubicarse en el territorio.
- Identificar los departamentos que concentran el mayor valor contratado.
- Comparar el peso de cada departamento en número de contratos y en monto.
- Observar cómo cambia la distribución territorial en el tiempo.
- Segmentar por tipo de contrato y modalidad, para distinguir el tipo de intervención.
- Distinguir en todo momento qué parte de la contratación queda fuera del análisis territorial y por qué.

### 4. Valores que puede seleccionar el usuario

| Filtro | Campo de datos | Propósito |
|---|---|---|
| Año de firma | `anio` | Acotar el periodo y observar la evolución. |
| Tipo de contrato | `tipo_de_contrato` | Distinguir obra, interventoría, consultoría y prestación de servicios. |
| Modalidad de contratación | `modalidad_de_contratacion` | Comparar el comportamiento territorial según la modalidad. |
| Contratos sin fecha de firma | — | Incluir o excluir los 2.374 contratos que no tienen fecha registrada. |

El último control merece explicación. Hay 2.374 contratos con valor registrado pero sin fecha de firma, que suman $5,87 billones y de los cuales solo el 19,6 % del valor es territorialmente identificable. Si se excluyeran de forma silenciosa por efecto del filtro de años, el indicador de cobertura pasaría de 77,9 % a 88,2 % sin que el usuario supiera por qué. Se expone entonces como una casilla explícita, marcada por defecto, y las series anuales los excluyen siempre porque no pueden ubicarse en el tiempo.

### 5. Criterio de atribución territorial

El departamento no se lee de una variable de la fuente: se infiere del objeto contractual mediante el extractor construido en la Tarea 2. La atribución solo se considera válida cuando el texto menciona **un único** departamento.

Los contratos que mencionan varios se conservan como categoría propia y **no se replican** entre departamentos, porque replicarlos duplicaría el valor contratado e invalidaría los rankings y las participaciones porcentuales.

En consecuencia, el mapa y el ranking se construyen únicamente sobre los contratos con atribución inequívoca, mientras que los indicadores de cobertura consideran las tres categorías.

### 6. Resultados que genera el tablero

Los cuatro indicadores superiores se recalculan con cada filtro:

| Indicador | Qué responde |
|---|---|
| Contratos con valor registrado | El tamaño del universo bajo análisis. |
| Valor total contratado | Los recursos en juego. |
| % del valor ubicable en el territorio | La confiabilidad territorial de la lectura. |
| Departamentos con contratación identificada | La cobertura geográfica. |

### 7. Visualizaciones propuestas

| # | Visualización | Forma | Por qué esa forma |
|---|---|---|---|
| 1 | Dónde se ejecutan los recursos | Mapa coroplético por departamento | La pregunta es geográfica; el mapa la responde de un vistazo y revela patrones regionales que un ranking esconde. |
| 2 | Departamentos por valor contratado | Barras horizontales, top 15 | El mapa muestra el patrón pero no permite comparar magnitudes con precisión. Las barras sí, y el nombre se lee sin esfuerzo. |
| 3 | Trazabilidad territorial en el tiempo | Líneas, dos series | La brecha entre el % de contratos y el % del valor es el hallazgo central; dos líneas sobre el mismo eje la hacen visible. |
| 4 | Evolución por departamento | Áreas apiladas, seis principales | Muestra a la vez el total del periodo y la composición por departamento. |

**Decisiones de forma que vale la pena justificar:**

- **Un solo eje en cada gráfica.** No se usan ejes duales. En la gráfica de trazabilidad ambas series son porcentajes y comparten escala, así que la comparación es legítima.
- **Escala secuencial de un solo tono para el mapa.** La variable es magnitud continua, no categoría; una escala de un tono de claro a oscuro la representa correctamente, mientras que una paleta de varios colores sugeriría categorías inexistentes.
- **Paleta validada para daltonismo.** Los colores categóricos se asignan siempre en el mismo orden y nunca se reciclan.
- **El mapa no depende de internet.** Se implementa con `Choroplethmapbox` y estilo `white-bg` sobre el geojson local. La alternativa (`Choropleth`) descarga un archivo topojson desde `cdn.plot.ly` al renderizar, lo que haría fallar el mapa en una instancia de EC2 sin salida a internet.

### 8. Distribución de los elementos en el tablero

El diseño sigue un orden de lectura de arriba hacia abajo, de lo general a lo específico:

```
┌────────────────────────────────────────────────────────────────┐
│  Contratación pública del INVIAS                               │
│  Instituto Nacional de Vías · SECOP II, corte 24-ago-2026      │
├────────────────────────────────────────────────────────────────┤
│  [Concentración]   [ DISTRIBUCIÓN TERRITORIAL ]   [Ejecución]  │
├────────────────────────────────────────────────────────────────┤
│  │ Pregunta de negocio                                         │
├────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  19.617  │ │ $39,1 bn │ │  77,9 %  │ │    33    │           │
│  │ contratos│ │  valor   │ │ ubicable │ │  deptos  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
├────────────────────────────────────────────────────────────────┤
│  FILTROS                                                       │
│  Año ──●────────────●──   Tipo [▾]        Modalidad [▾]        │
│  ☑ Incluir los 2.374 contratos sin fecha de firma              │
├────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────┐  ┌───────────────────────┐          │
│  │ Dónde se ejecutan     │  │ Departamentos por     │          │
│  │ los recursos          │  │ valor contratado      │          │
│  │                       │  │  Antioquia ████████   │          │
│  │    [ mapa de          │  │  Nariño    ██████     │          │
│  │      Colombia ]       │  │  Cauca     █████      │          │
│  │                       │  │  Putumayo  ████       │          │
│  │                       │  │  ...                  │          │
│  └───────────────────────┘  └───────────────────────┘          │
├────────────────────────────────────────────────────────────────┤
│  Trazabilidad territorial en el tiempo                         │
│   100% ┤                                                       │
│        │  ●───●───●───●  % del valor                           │
│    50% ┤      ○───○───○  % de contratos                        │
│      0 └────────────────────────────────                       │
├────────────────────────────────────────────────────────────────┤
│  Evolución por departamento                                    │
│        │      ▲                                                │
│        │    ▄███▄        [ áreas apiladas, 6 deptos ]          │
│      0 └────────────────────────────────                       │
└────────────────────────────────────────────────────────────────┘
```

La lógica del orden: primero **cuánto** (indicadores), luego **dónde** (mapa y ranking, lado a lado porque se leen juntos), después **cuándo** (las dos series de tiempo). Los filtros se ubican entre los indicadores y las gráficas para que el usuario vea de inmediato el efecto de lo que selecciona.

### 9. Flujo de interacción esperado

1. El usuario abre el tablero y ve el panorama completo: 19.617 contratos, $39,1 billones, 77,9 % ubicable.
2. Observa en el mapa que la contratación se concentra en la periferia — Antioquia, Nariño, Cauca, Putumayo — y no en el centro económico del país.
3. Contrasta con el ranking la magnitud exacta de cada departamento.
4. Revisa la serie de trazabilidad y nota que el porcentaje del valor identificable cae en los últimos años.
5. Filtra por tipo de contrato "Obra" para aislar la inversión en infraestructura, y observa cómo cambia el mapa.
6. Acota el rango de años a un periodo de interés y compara.

### 10. Principio de diseño

El tablero declara su propia limitación en lugar de ocultarla. El indicador de cobertura territorial ocupa un lugar destacado, junto a las cifras de contratos y valor, y no en una nota al pie.

La razón es de utilidad para el usuario: un mapa que presenta el 78 % de los recursos como si fuera el 100 % induce a error, mientras que uno que declara su cobertura permite decidir cuánto peso darle. Para un organismo de control, además, el hecho de que uno de cada cinco pesos no sea rastreable territorialmente desde la información publicada es en sí mismo un hallazgo.

### 11. Resultado esperado

Un módulo que responde dónde ejecuta INVIAS sus recursos con el detalle de departamento, año, tipo y modalidad, y que al mismo tiempo informa al usuario qué proporción de la contratación queda fuera de esa respuesta y por qué.
