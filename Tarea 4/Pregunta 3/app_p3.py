import pandas as pd

from dash import Dash, html, dcc, Input, Output, dash_table
from plotly import graph_objects as go


# ============================================================
# 1. CARGA DE DATOS
# ============================================================

df = pd.read_csv(
    "Tarea 2/Pregunta 3/df_analitico_p3.csv"
)


# ============================================================
# CARGAR LAS COLUMNAS DE LA TABLA DE CONTRATOS
# ============================================================

columnas_tabla = [
    {"name": "ID contrato", "id": "id_contrato"},
    {"name": "Proveedor", "id": "proveedor_adjudicado"},
    {"name": "Estado", "id": "estado_contrato"},
    {"name": "Tipo", "id": "tipo_de_contrato"},
    {"name": "Modalidad", "id": "modalidad_de_contratacion"},
    {"name": "Valor contrato", "id": "valor_del_contrato"},
    {"name": "% ejecución", "id": "porcentaje_ejecutado"},
    {"name": "% pago", "id": "porcentaje_pagado"},
    {"name": "Pendiente ejecución", "id": "valor_pendiente_de_ejecucion"},
    {"name": "Pendiente pago", "id": "valor_pendiente_de_pago"},
    {"name": "Días adicionados", "id": "dias_adicionados"},
    {"name": "Prioritario", "id": "contrato_prioritario"},
]

datos_tabla = df[
    [
        "id_contrato",
        "proveedor_adjudicado",
        "estado_contrato",
        "tipo_de_contrato",
        "modalidad_de_contratacion",
        "valor_del_contrato",
        "porcentaje_ejecutado",
        "porcentaje_pagado",
        "valor_pendiente_de_ejecucion",
        "valor_pendiente_de_pago",
        "dias_adicionados",
        "contrato_prioritario",
    ]
].to_dict("records")

# ============================================================
# 2. APLICACIÓN DASH
# ============================================================

app = Dash(__name__)


# ============================================================
# 3. DISEÑO DEL TABLERO
# ============================================================

app.layout = html.Div(
    [

        # ----------------------------------------------------
        # ENCABEZADO
        # ----------------------------------------------------

        html.Div(
            [
                html.H1(
                    "INVIAS — Ejecución financiera y modificaciones contractuales"
                ),

                html.H3(
                    "Pregunta 3 — Ejecución financiera y modificaciones de los contratos"
                ),

                html.P(
                    "¿Cómo se comporta la ejecución financiera de los contratos de INVIAS "
                    "y cuáles presentan mayores niveles de recursos pendientes de ejecución, "
                    "recursos pendientes de pago o extensiones en el plazo contractual "
                    "que puedan requerir seguimiento?"
                ),
            ]
        ),

        # ----------------------------------------------------
        # FILTROS
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Filtros de análisis"),

                html.Div(
                    [

                        html.Div(
                            [
                                html.Label("Estado del contrato"),
                                dcc.Dropdown(
                                    id="filtro_estado",
                                    options=[
                                        {"label": valor, "value": valor}
                                        for valor in sorted(
                                            df["estado_contrato"]
                                            .dropna()
                                            .unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"width": "19%"},
                        ),

                        html.Div(
                            [
                                html.Label("Tipo de contrato"),
                                dcc.Dropdown(
                                    id="filtro_tipo",
                                    options=[
                                        {"label": valor, "value": valor}
                                        for valor in sorted(
                                            df["tipo_de_contrato"]
                                            .dropna()
                                            .unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"width": "19%"},
                        ),

                        html.Div(
                            [
                                html.Label("Modalidad de contratación"),
                                dcc.Dropdown(
                                    id="filtro_modalidad",
                                    options=[
                                        {"label": valor, "value": valor}
                                        for valor in sorted(
                                            df["modalidad_de_contratacion"]
                                            .dropna()
                                            .unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"width": "19%"},
                        ),

                        html.Div(
                            [
                                html.Label("Extensión contractual"),
                                dcc.Dropdown(
                                    id="filtro_extension",
                                    options=[
                                        {"label": "Todos", "value": "Todos"},
                                        {"label": "Con extensión", "value": "Sí"},
                                        {"label": "Sin extensión", "value": "No"},
                                    ],
                                    value="Todos",
                                    clearable=False,
                                ),
                            ],
                            style={"width": "19%"},
                        ),

                        html.Div(
                            [
                                html.Label("Nivel de ejecución"),
                                dcc.Dropdown(
                                    id="filtro_ejecucion",
                                    options=[
                                        {"label": "Todos", "value": "Todos"},
                                        {"label": "0 %", "value": "0%"},
                                        {"label": "1 % - 49 %", "value": "1%-49%"},
                                        {"label": "50 % - 99 %", "value": "50%-99%"},
                                        {"label": "≥ 100 %", "value": ">=100%"},
                                        {"label": "Sin dato", "value": "Sin dato"},
                                    ],
                                    value="Todos",
                                    clearable=False,
                                ),
                            ],
                            style={"width": "19%"},
                        ),

                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "gap": "10px",
                    },
                ),
            ],
            style={
                "padding": "20px",
                "border": "1px solid #ddd",
                "borderRadius": "10px",
                "marginTop": "20px",
            },
        ),

        # ----------------------------------------------------
        # KPI
        # ----------------------------------------------------

        html.H2("Resumen de ejecución"),

        html.Div(
            [

                html.Div(
                    [
                        html.H4("Contratos analizados"),
                        html.H2(
                            id="kpi_contratos",
                            children="20,718"
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "23%",
                    },
                ),

                html.Div(
                    [
                        html.H4("Recursos pendientes de ejecución"),
                        html.H2(
                            id="kpi_pendiente_ejecucion",
                            children="$ 0",
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "23%",
                    },
                ),

                html.Div(
                    [
                        html.H4("Recursos pendientes de pago"),
                        html.H2(
                            id="kpi_pendiente_pago",
                            children="$ 0",
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "23%",
                    },
                ),

                html.Div(
                    [
                        html.H4("Contratos prioritarios"),
                        html.H2(
                            id="kpi_prioritarios",
                            children="750",
                        ),
                    ],
                    style={
                        "padding": "20px",
                        "border": "1px solid #ddd",
                        "borderRadius": "10px",
                        "textAlign": "center",
                        "width": "23%",
                    },
                ),

            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "15px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 1: DISTRIBUCIÓN DE LA EJECUCIÓN
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Comportamiento de la ejecución financiera"),

                dcc.Graph(
                    id="grafico_ejecucion"
                ),
            ],
            style={
                "marginTop": "25px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 2: TOP CONTRATOS POR RECURSOS PENDIENTES
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Recursos pendientes de ejecución"),

                dcc.Graph(
                    id="grafico_pendientes"
                ),
            ],
            style={
                "marginTop": "25px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 3: EXTENSIONES CONTRACTUALES
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Extensiones contractuales"),

                dcc.Graph(
                    id="grafico_extensiones"
                ),
            ],
            style={
                "marginTop": "25px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 4: EJECUCIÓN VS PAGO
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Ejecución financiera frente a pago"),

                dcc.Graph(
                    id="grafico_ejecucion_pago"
                ),
            ],
            style={
                "marginTop": "25px",
            },
        ),

        # ----------------------------------------------------
        # SECCIÓN: CONTRATOS PRIORITARIOS
        # ----------------------------------------------------

        html.Div(
            [
                html.H2("Contratos prioritarios para seguimiento"),

                html.P(
                    "Contratos que superan simultáneamente los percentiles "
                    "90 de recursos pendientes de ejecución y días adicionados."
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("Contratos prioritarios"),
                                html.H2(
                                    id="total_prioritarios",
                                    children="750",
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "padding": "20px",
                                "border": "1px solid #ddd",
                                "borderRadius": "10px",
                            },
                        ),

                        html.Div(
                            [
                                html.H4("Con extensión contractual"),
                                html.H2(
                                    id="prioritarios_extension",
                                    children="100 %",
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "padding": "20px",
                                "border": "1px solid #ddd",
                                "borderRadius": "10px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "20px",
                    },
                ),

                dcc.Graph(
                    id="grafico_prioritarios_tipo"
                ),

                dcc.Graph(
                    id="grafico_prioritarios_modalidad"
                ),

                html.H3("Detalle de contratos"),

                    html.P(
                        "Detalle de los contratos que cumplen con los filtros seleccionados."
                    ),

                    dash_table.DataTable(
                        id="tabla_contratos",
                        columns=columnas_tabla,
                        data=datos_tabla,
                        page_size=15,
                        sort_action="native",
                        filter_action="native",
                        style_table={"overflowX": "auto"},
                    ),
            ],
            style={
                "marginTop": "30px",
            },
        ),

    ]
)

# ============================================================
# 5. CALLBACK PARA ACTUALIZAR LOS KPI
# ============================================================

@app.callback(
    Output("kpi_contratos", "children"),
    Output("kpi_pendiente_ejecucion", "children"),
    Output("kpi_pendiente_pago", "children"),
    Output("kpi_prioritarios", "children"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_kpi(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    # Copiamos la base original
    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTRO: ESTADO
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    # --------------------------------------------------------
    # FILTRO: TIPO DE CONTRATO
    # --------------------------------------------------------

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    # --------------------------------------------------------
    # FILTRO: MODALIDAD
    # --------------------------------------------------------

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    # --------------------------------------------------------
    # FILTRO: EXTENSIÓN
    # --------------------------------------------------------

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # FILTRO: NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    if nivel_ejecucion and nivel_ejecucion != "Todos":

        if nivel_ejecucion == "0%":
            df_filtrado = df_filtrado[
                df_filtrado["porcentaje_ejecutado"] == 0
            ]

        elif nivel_ejecucion == "1%-49%":
            df_filtrado = df_filtrado[
                (df_filtrado["porcentaje_ejecutado"] > 0)
                & (df_filtrado["porcentaje_ejecutado"] < 50)
            ]

        elif nivel_ejecucion == "50%-99%":
            df_filtrado = df_filtrado[
                (df_filtrado["porcentaje_ejecutado"] >= 50)
                & (df_filtrado["porcentaje_ejecutado"] < 100)
            ]

        elif nivel_ejecucion == ">=100%":
            df_filtrado = df_filtrado[
                df_filtrado["porcentaje_ejecutado"] >= 100
            ]

        elif nivel_ejecucion == "Sin dato":
            df_filtrado = df_filtrado[
                df_filtrado["porcentaje_ejecutado"].isna()
            ]

    # --------------------------------------------------------
    # CÁLCULO DE KPI
    # --------------------------------------------------------

    numero_contratos = len(df_filtrado)

    pendiente_ejecucion = (
        df_filtrado["valor_pendiente_de_ejecucion"]
        .fillna(0)
        .sum()
    )

    pendiente_pago = (
        df_filtrado["valor_pendiente_de_pago"]
        .fillna(0)
        .sum()
    )

    prioritarios = (
        df_filtrado["contrato_prioritario"]
        .eq("Sí")
        .sum()
    )

    # --------------------------------------------------------
    # FORMATO DE RESULTADOS
    # --------------------------------------------------------

    contratos_texto = f"{numero_contratos:,}"

    ejecucion_texto = (
        f"$ {pendiente_ejecucion:,.0f}"
    )

    pago_texto = (
        f"$ {pendiente_pago:,.0f}"
    )

    prioritarios_texto = f"{prioritarios:,}"

    return (
        contratos_texto,
        ejecucion_texto,
        pago_texto,
        prioritarios_texto,
    )

# ============================================================
# 6. CALLBACK DEL GRÁFICO DE EJECUCIÓN
# ============================================================

@app.callback(
    Output("grafico_ejecucion", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_ejecucion(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    # Copia de la base
    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # CLASIFICACIÓN DEL NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    # --------------------------------------------------------
    # APLICAR FILTRO DE NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # CONTAR CONTRATOS
    # --------------------------------------------------------

    orden = [
        "0 %",
        "1 % - 49 %",
        "50 % - 99 %",
        "≥ 100 %",
        "Sin dato",
    ]

    conteo = (
        df_filtrado["nivel_ejecucion_grafico"]
        .value_counts()
        .reindex(orden, fill_value=0)
    )

    # --------------------------------------------------------
    # CREAR GRÁFICO DISTRIBUCIÓN DE LA EJECUCIÓN
    # --------------------------------------------------------

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=conteo.index,
            y=conteo.values,
            text=conteo.values,
            textposition="outside",
        )
    )

    figura.update_layout(
        title="Distribución de contratos por nivel de ejecución",
        xaxis_title="Nivel de ejecución",
        yaxis_title="Número de contratos",
        template="plotly_white",
        height=450,
    )

    return figura

# ============================================================
# 7. CALLBACK DEL GRÁFICO DE RECURSOS PENDIENTES
# ============================================================

@app.callback(
    Output("grafico_pendientes", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_pendientes(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    # Copia de la base
    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # CLASIFICACIÓN DEL NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    # --------------------------------------------------------
    # FILTRO DE NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # TOP 10
    # --------------------------------------------------------

    top10 = (
        df_filtrado[
            [
                "id_contrato",
                "proveedor_adjudicado",
                "valor_pendiente_de_ejecucion",
            ]
        ]
        .sort_values(
            "valor_pendiente_de_ejecucion",
            ascending=False
        )
        .head(10)
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    figura = go.Figure()

    # --------------------------------------------------------
    # FORMATO EJECUTIVO DE VALORES
    # --------------------------------------------------------

    def formato_monetario(valor):

        if abs(valor) >= 1_000_000_000_000:
            return f"$ {valor / 1_000_000_000_000:.1f} billones"

        elif abs(valor) >= 1_000_000_000:
            return f"$ {valor / 1_000_000_000:.1f} mil millones"

        elif abs(valor) >= 1_000_000:
            return f"$ {valor / 1_000_000:.1f} millones"

        elif abs(valor) >= 1_000:
            return f"$ {valor / 1_000:.1f} mil"

        else:
            return f"$ {valor:,.0f}"

    top10["valor_formateado"] = (
        top10["valor_pendiente_de_ejecucion"]
        .apply(formato_monetario)
    )

    figura.add_trace(
        go.Bar(
            x=top10["valor_pendiente_de_ejecucion"],
            y=top10["id_contrato"],
            orientation="h",

            text=top10["valor_formateado"],
            textposition="outside",

            customdata=top10[
                [
                    "proveedor_adjudicado",
                    "valor_pendiente_de_ejecucion",
                ]
            ],

            hovertemplate=(
                "<b>Contrato:</b> %{y}<br>"
                "<b>Proveedor:</b> %{customdata[0]}<br>"
                "<b>Recursos pendientes:</b> $%{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        title="Top 10 contratos con mayores recursos pendientes de ejecución",
        xaxis_title="Recursos pendientes de ejecución ($)",
        yaxis_title="ID del contrato",
        template="plotly_white",
        height=450,
        yaxis={"autorange": "reversed"},
    )

    return figura

# ============================================================
# 8. CALLBACK DEL GRÁFICO DE EXTENSIONES
# ============================================================

@app.callback(
    Output("grafico_extensiones", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_extensiones(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    # Copia de la base
    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # CLASIFICACIÓN DEL NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    # --------------------------------------------------------
    # FILTRO DE NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # PREPARAR INFORMACIÓN
    # --------------------------------------------------------

    resumen = (
        df_filtrado
        .groupby(
            ["tipo_de_contrato", "tiene_extension"]
        )
        .size()
        .reset_index(name="numero_contratos")
    )

    # --------------------------------------------------------
    # SELECCIONAR PRINCIPALES TIPOS
    # --------------------------------------------------------

    principales_tipos = (
        df_filtrado["tipo_de_contrato"]
        .value_counts()
        .head(7)
        .index
    )

    resumen = resumen[
        resumen["tipo_de_contrato"]
        .isin(principales_tipos)
    ]

    # --------------------------------------------------------
    # CREAR GRÁFICO
    # --------------------------------------------------------

    figura = go.Figure()

    for extension_valor in ["No", "Sí"]:

        datos = resumen[
            resumen["tiene_extension"] == extension_valor
        ]

        figura.add_trace(
            go.Bar(
                x=datos["tipo_de_contrato"],
                y=datos["numero_contratos"],
                name=(
                    "Con extensión"
                    if extension_valor == "Sí"
                    else "Sin extensión"
                ),
            )
        )

    figura.update_layout(
        title="Contratos con y sin extensión por tipo de contrato",
        xaxis_title="Tipo de contrato",
        yaxis_title="Número de contratos",
        barmode="group",
        template="plotly_white",
        height=450,
    )

    return figura

# ============================================================
# 9. CALLBACK DEL GRÁFICO EJECUCIÓN VS PAGO
# ============================================================

@app.callback(
    Output("grafico_ejecucion_pago", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_ejecucion_pago(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    # Copia de la base
    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # CLASIFICACIÓN DEL NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    # --------------------------------------------------------
    # FILTRO DE NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # ELIMINAR DATOS SIN EJECUCIÓN O PAGO
    # --------------------------------------------------------

    datos = df_filtrado[
        [
            "id_contrato",
            "proveedor_adjudicado",
            "porcentaje_ejecutado",
            "porcentaje_pagado",
            "dias_adicionados",
            "contrato_prioritario",
        ]
    ].dropna(
        subset=[
            "porcentaje_ejecutado",
            "porcentaje_pagado",
        ]
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=datos["porcentaje_ejecutado"],
            y=datos["porcentaje_pagado"],
            mode="markers",
            name = "Contratos",

            customdata=datos[
                [
                    "id_contrato",
                    "proveedor_adjudicado",
                    "dias_adicionados",
                    "contrato_prioritario",
                ]
            ],

            hovertemplate=(
                "<b>Contrato:</b> %{customdata[0]}<br>"
                "<b>Proveedor:</b> %{customdata[1]}<br>"
                "<b>% ejecutado:</b> %{x:.1f}%<br>"
                "<b>% pagado:</b> %{y:.1f}%<br>"
                "<b>Días adicionados:</b> %{customdata[2]}<br>"
                "<b>Prioritario:</b> %{customdata[3]}"
                "<extra></extra>"
            ),
        )
    )

    # --------------------------------------------------------
    # LÍNEA DE REFERENCIA 1:1
    # --------------------------------------------------------

    figura.add_trace(
        go.Scatter(
            x=[0, 125],
            y=[0, 125],
            mode="lines",
            name="Relación 1:1",
            line={
                "dash": "dash",
            },
        )
    )

    figura.update_layout(
        title="Relación entre porcentaje ejecutado y porcentaje pagado",
        xaxis_title="Porcentaje ejecutado (%)",
        yaxis_title="Porcentaje pagado (%)",
        template="plotly_white",
        height=500,
        xaxis={
            "range": [0, 125],
        },
        yaxis={
            "range": [0, 125],
        },
    )

    return figura

# ============================================================
# 10. CALLBACK DE CONTRATOS PRIORITARIOS
# ============================================================

@app.callback(
    Output("total_prioritarios", "children"),
    Output("prioritarios_extension", "children"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_prioritarios(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # CONTRATOS PRIORITARIOS
    # --------------------------------------------------------

    prioritarios = df_filtrado[
        df_filtrado["contrato_prioritario"] == "Sí"
    ]

    total = len(prioritarios)

    # --------------------------------------------------------
    # PORCENTAJE CON EXTENSIÓN
    # --------------------------------------------------------

    if total > 0:

        porcentaje_extension = (
            prioritarios["tiene_extension"]
            .eq("Sí")
            .mean()
            * 100
        )

    else:

        porcentaje_extension = 0

    return (
        f"{total:,}",
        f"{porcentaje_extension:.0f} %",
    )

# ============================================================
# 11. CALLBACK: PRIORITARIOS POR TIPO DE CONTRATO
# ============================================================

@app.callback(
    Output("grafico_prioritarios_tipo", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_prioritarios_tipo(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # SELECCIONAR PRIORITARIOS
    # --------------------------------------------------------

    prioritarios = df_filtrado[
        df_filtrado["contrato_prioritario"] == "Sí"
    ]

    # --------------------------------------------------------
    # AGRUPAR POR TIPO
    # --------------------------------------------------------

    resumen = (
        prioritarios["tipo_de_contrato"]
        .value_counts()
        .sort_values(ascending=True)
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen.values,
            y=resumen.index,
            orientation="h",
            text=resumen.values,
            textposition="outside",
            name="Contratos prioritarios",
        )
    )

    figura.update_layout(
        title="Contratos prioritarios por tipo de contrato",
        xaxis_title="Número de contratos",
        yaxis_title="Tipo de contrato",
        template="plotly_white",
        height=500,
    )

    return figura

# ============================================================
# 12. CALLBACK: PRIORITARIOS POR MODALIDAD
# ============================================================

@app.callback(
    Output("grafico_prioritarios_modalidad", "figure"),

    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_grafico_prioritarios_modalidad(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    df_filtrado = df.copy()

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    if extension and extension != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == extension
        ]

    # --------------------------------------------------------
    # NIVEL DE EJECUCIÓN
    # --------------------------------------------------------

    def clasificar_ejecucion(valor):

        if pd.isna(valor):
            return "Sin dato"

        elif valor == 0:
            return "0 %"

        elif valor < 50:
            return "1 % - 49 %"

        elif valor < 100:
            return "50 % - 99 %"

        else:
            return "≥ 100 %"

    df_filtrado["nivel_ejecucion_grafico"] = (
        df_filtrado["porcentaje_ejecutado"]
        .apply(clasificar_ejecucion)
    )

    if nivel_ejecucion and nivel_ejecucion != "Todos":
        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == nivel_ejecucion
        ]

    # --------------------------------------------------------
    # SELECCIONAR PRIORITARIOS
    # --------------------------------------------------------

    prioritarios = df_filtrado[
        df_filtrado["contrato_prioritario"] == "Sí"
    ]

    # --------------------------------------------------------
    # AGRUPAR POR MODALIDAD
    # --------------------------------------------------------

    resumen = (
        prioritarios["modalidad_de_contratacion"]
        .value_counts()
        .sort_values(ascending=True)
    )

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen.values,
            y=resumen.index,
            orientation="h",
            text=resumen.values,
            textposition="outside",
            name="Contratos prioritarios",
        )
    )

    figura.update_layout(
        title="Contratos prioritarios por modalidad de contratación",
        xaxis_title="Número de contratos",
        yaxis_title="Modalidad de contratación",
        template="plotly_white",
        height=550,
    )

    return figura

# =================================================================
# CALLBACK 13 — ACTUALIZACIÓN DINÁMICA DE LA TABLA DE CONTRATOS
# =================================================================

@app.callback(
    Output("tabla_contratos", "data"),
    Input("filtro_estado", "value"),
    Input("filtro_tipo", "value"),
    Input("filtro_modalidad", "value"),
    Input("filtro_extension", "value"),
    Input("filtro_ejecucion", "value"),
)
def actualizar_tabla(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
):

    df_filtrado = df.copy()

    # Filtro por estado
    if estado:
        df_filtrado = df_filtrado[
            df_filtrado["estado_contrato"] == estado
        ]

    # Filtro por tipo
    if tipo:
        df_filtrado = df_filtrado[
            df_filtrado["tipo_de_contrato"] == tipo
        ]

    # Filtro por modalidad
    if modalidad:
        df_filtrado = df_filtrado[
            df_filtrado["modalidad_de_contratacion"] == modalidad
        ]

    # Filtro por extensión
    if extension == "Sí":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == "Sí"
        ]
    elif extension == "No":
        df_filtrado = df_filtrado[
            df_filtrado["tiene_extension"] == "No"
        ]

    # Filtro por nivel de ejecución
    if nivel_ejecucion and nivel_ejecucion != "Todos":

        def clasificar_ejecucion(valor):
            if pd.isna(valor):
                return "Sin dato"
            elif valor == 0:
                return "0 %"
            elif valor < 50:
                return "1 %-49 %"
            elif valor < 100:
                return "50 %-99 %"
            else:
                return "≥100 %"

        nivel = df_filtrado["porcentaje_ejecutado"].apply(
            clasificar_ejecucion
        )

        df_filtrado = df_filtrado[
            nivel == nivel_ejecucion
        ]

    # Columnas que se mostrarán en la tabla
    columnas = [
        "id_contrato",
        "proveedor_adjudicado",
        "estado_contrato",
        "tipo_de_contrato",
        "modalidad_de_contratacion",
        "valor_del_contrato",
        "porcentaje_ejecutado",
        "porcentaje_pagado",
        "valor_pendiente_de_ejecucion",
        "valor_pendiente_de_pago",
        "dias_adicionados",
        "contrato_prioritario",
    ]

    return df_filtrado[columnas].to_dict("records")

# ============================================================
# 4. EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)