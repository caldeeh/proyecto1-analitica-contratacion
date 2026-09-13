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
                html.Div(
                    [
                        html.H1(
                            "INVIAS",
                            style={
                                "margin": "0",
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "30px",
                                "fontWeight": "700",
                                "color": "#FFFFFF",
                            },
                        ),

                        html.Div(
                            "Ejecución financiera y modificaciones contractuales",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "21px",
                                "fontWeight": "500",
                                "color": "#FFFFFF",
                                "marginTop": "4px",
                            },
                        ),
                    ],
                ),

                html.Div(
                    [
                        html.Div(
                            "PREGUNTA 3",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "12px",
                                "fontWeight": "700",
                                "letterSpacing": "1px",
                                "color": "#DCE8F5",
                                "marginBottom": "6px",
                            },
                        ),

                        html.P(
                            "¿Cómo se comporta la ejecución financiera de los contratos de INVIAS "
                            "y cuáles presentan mayores niveles de recursos pendientes de ejecución, "
                            "recursos pendientes de pago o extensiones en el plazo contractual "
                            "que puedan requerir seguimiento?",
                            style={
                                "margin": "0",
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "13px",
                                "lineHeight": "1.5",
                                "color": "#EAF1F8",
                                "maxWidth": "900px",
                            },
                        ),
                    ],
                    style={
                        "marginTop": "14px",
                    },
                ),

                html.Img(
                    src="/assets/logo_invias.png",
                    style={
                        "position": "absolute",
                        "right": "30px",
                        "top": "30px",
                        "height": "130px",
                        "width": "auto",
            },
        ),
            ],
            style={
                "backgroundColor": "#17365D",
                "padding": "24px 30px",
                "borderRadius": "10px",
                "marginBottom": "22px",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.08)",
                "fontFamily": "Arial, sans-serif",
            },
        ),

        # ----------------------------------------------------
        # FILTROS
        # ----------------------------------------------------

        html.Div(
            [
                html.H2(
                    "Filtros de análisis",
                    style={
                        "margin": "0 0 15px 0",
                        "fontFamily": "Arial, sans-serif",
                        "fontSize": "18px",
                        "fontWeight": "600",
                    },
                ),

                html.Div(
                    [
                        # Filtro: Estado del contrato
                        html.Div(
                            [
                                html.Label(
                                    "Estado del contrato",
                                    style={
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "marginBottom": "6px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="filtro_estado",
                                    options=[
                                        {"label": x, "value": x}
                                        for x in sorted(
                                            df["estado_contrato"].dropna().unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"flex": "1"},
                        ),

                        # Filtro: Tipo de contrato
                        html.Div(
                            [
                                html.Label(
                                    "Tipo de contrato",
                                    style={
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "marginBottom": "6px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="filtro_tipo",
                                    options=[
                                        {"label": x, "value": x}
                                        for x in sorted(
                                            df["tipo_de_contrato"].dropna().unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"flex": "1"},
                        ),

                        # Filtro: Modalidad de contratación
                        html.Div(
                            [
                                html.Label(
                                    "Modalidad de contratación",
                                    style={
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "marginBottom": "6px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="filtro_modalidad",
                                    options=[
                                        {"label": x, "value": x}
                                        for x in sorted(
                                            df["modalidad_de_contratacion"].dropna().unique()
                                        )
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"flex": "1"},
                        ),

                        # Filtro: Extensión contractual
                        html.Div(
                            [
                                html.Label(
                                    "Extensión contractual",
                                    style={
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "marginBottom": "6px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="filtro_extension",
                                    options=[
                                        {"label": "Todos", "value": "Todos"},
                                        {"label": "Con extensión", "value": "Sí"},
                                        {"label": "Sin extensión", "value": "No"},
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"flex": "1"},
                        ),

                        # Filtro: Nivel de ejecución
                        html.Div(
                            [
                                html.Label(
                                    "Nivel de ejecución",
                                    style={
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "13px",
                                        "fontWeight": "600",
                                        "marginBottom": "6px",
                                        "display": "block",
                                    },
                                ),
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
                                    placeholder="Todos",
                                    clearable=True,
                                ),
                            ],
                            style={"flex": "1"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "12px",
                        "flexWrap": "wrap",
                    },
                ),
            ],
            style={
                "padding": "18px 20px",
                "backgroundColor": "#F7F9FC",
                "border": "1px solid #D9E1EA",
                "borderRadius": "8px",
                "marginBottom": "25px",
                "position": "sticky",
                "top": "10px",
                "zIndex": "1000",
            },
        ),

        # ----------------------------------------------------
        # KPI
        # ----------------------------------------------------
        html.H2(
            "Resumen de ejecución",
            style={
                "margin": "0 0 15px 0",
                "fontFamily": "Arial, sans-serif",
                "fontSize": "20px",
                "fontWeight": "600",
            },
        ),

        html.Div(
            [
                # KPI 1
                html.Div(
                    [
                        html.Div(
                            "CONTRATOS ANALIZADOS",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "12px",
                                "fontWeight": "700",
                                "letterSpacing": "0.5px",
                                "marginBottom": "8px",
                            },
                        ),
                        html.Div(
                            id="kpi_contratos",
                            children="20,718",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "700",
                            },
                        ),
                    ],
                    style={
                        "flex": "1",
                        "padding": "18px 20px",
                        "border": "1px solid #D9E1EA",
                        "borderRadius": "8px",
                        "backgroundColor": "#FFFFFF",
                    },
                ),

                # KPI 2
                html.Div(
                    [
                        html.Div(
                            "PENDIENTE DE EJECUCIÓN",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "12px",
                                "fontWeight": "700",
                                "letterSpacing": "0.5px",
                                "marginBottom": "8px",
                            },
                        ),
                        html.Div(
                            id="kpi_pendiente_ejecucion",
                            children="$ 38.1 billones",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "700",
                            },
                        ),
                    ],
                    style={
                        "flex": "1",
                        "padding": "18px 20px",
                        "border": "1px solid #D9E1EA",
                        "borderRadius": "8px",
                        "backgroundColor": "#FFFFFF",
                    },
                ),

                # KPI 3
                html.Div(
                    [
                        html.Div(
                            "PENDIENTE DE PAGO REPORTADO",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "12px",
                                "fontWeight": "700",
                                "letterSpacing": "0.5px",
                                "marginBottom": "8px",
                            },
                        ),
                        html.Div(
                            id="kpi_pendiente_pago",
                            children="$ 0",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "700",
                            },
                        ),
                    ],
                    style={
                        "flex": "1",
                        "padding": "18px 20px",
                        "border": "1px solid #D9E1EA",
                        "borderRadius": "8px",
                        "backgroundColor": "#FFFFFF",
                    },
                ),

                # KPI 4
                html.Div(
                    [
                        html.Div(
                            "CONTRATOS PRIORITARIOS",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "12px",
                                "fontWeight": "700",
                                "letterSpacing": "0.5px",
                                "marginBottom": "8px",
                            },
                        ),
                        html.Div(
                            id="kpi_prioritarios",
                            children="750",
                            style={
                                "fontFamily": "Arial, sans-serif",
                                "fontSize": "28px",
                                "fontWeight": "700",
                            },
                        ),
                    ],
                    style={
                        "flex": "1",
                        "padding": "18px 20px",
                        "border": "1px solid #D9E1EA",
                        "borderRadius": "8px",
                        "backgroundColor": "#FFFFFF",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "15px",
                "flexWrap": "wrap",
                "marginBottom": "25px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 1: DISTRIBUCIÓN DE LA EJECUCIÓN
        # ----------------------------------------------------

       html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Comportamiento de la ejecución financiera",
                            style={"fontSize": "18px", "margin": "0 0 10px 0"},
                        ),

                        dcc.Graph(
                            id="grafico_ejecucion"
                        ),
                    ],
                    style={
                        "width": "49%",
                        "backgroundColor": "#FFFFFF",
                        "border": "1px solid #E1E6ED",
                        "borderRadius": "10px",
                        "padding": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.05)",
                    },
                ),

        # ----------------------------------------------------
        # GRÁFICO 2: TOP CONTRATOS POR RECURSOS PENDIENTES
        # ----------------------------------------------------

        html.Div(
                    [
                        html.H2(
                            "Recursos pendientes de ejecución",
                            style={"fontSize": "18px", "margin": "0 0 10px 0"},
                        ),

                        dcc.Graph(
                            id="grafico_pendientes"
                        ),
                    ],
                    style={
                        "width": "49%",
                        "backgroundColor": "#FFFFFF",
                        "border": "1px solid #E1E6ED",
                        "borderRadius": "10px",
                        "padding": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.05)",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginTop": "25px",
                "marginBottom": "20px",
            },
        ),

        # ----------------------------------------------------
        # GRÁFICO 3: EXTENSIONES CONTRACTUALES
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            "Extensiones contractuales",
                            style={"fontSize": "18px", "margin": "0 0 10px 0"},
                        ),

                        dcc.Graph(
                            id="grafico_extensiones"
                        ),
                    ],
                    style={
                        "width": "49%",
                        "backgroundColor": "#FFFFFF",
                        "border": "1px solid #E1E6ED",
                        "borderRadius": "10px",
                        "padding": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.05)",
                    },
                ),

        # ----------------------------------------------------
        # GRÁFICO 4: EJECUCIÓN VS PAGO
        # ----------------------------------------------------

        html.Div(
                    [
                        html.H2(
                            "Ejecución financiera frente a pago",
                            style={"fontSize": "18px", "margin": "0 0 10px 0"},
                        ),

                        dcc.Graph(
                            id="grafico_ejecucion_pago"
                        ),
                    ],
                    style={
                        "width": "49%",
                        "backgroundColor": "#FFFFFF",
                        "border": "1px solid #E1E6ED",
                        "borderRadius": "10px",
                        "padding": "10px",
                        "boxShadow": "0 1px 4px rgba(0,0,0,0.05)",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginBottom": "20px",
            },
        ),

        # ----------------------------------------------------
        # SECCIÓN: CONTRATOS PRIORITARIOS
        # ----------------------------------------------------

        html.Div(
            [
                html.H2(
                    "Contratos prioritarios para seguimiento",
                    style={
                        "fontSize": "20px",
                        "margin": "0 0 6px 0",
                    },
                ),

                html.P(
                    "Contratos que superan simultáneamente los percentiles "
                    "90 de recursos pendientes de ejecución y días adicionados.",
                    style={
                        "fontSize": "13px",
                        "color": "#64748B",
                        "margin": "0 0 15px 0",
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "Contratos prioritarios",
                                    style={"margin": "0"},
                                ),
                                html.H2(
                                    id="total_prioritarios",
                                    children="750",
                                    style={"margin": "5px 0 0 0"},
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "padding": "14px",
                                "backgroundColor": "#FFFFFF",
                                "border": "1px solid #E1E6ED",
                                "borderRadius": "10px",
                            },
                        ),

                        html.Div(
                            [
                                html.H4(
                                    "Con extensión contractual",
                                    style={"margin": "0"},
                                ),
                                html.H2(
                                    id="prioritarios_extension",
                                    children="100 %",
                                    style={"margin": "5px 0 0 0"},
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "padding": "14px",
                                "backgroundColor": "#FFFFFF",
                                "border": "1px solid #E1E6ED",
                                "borderRadius": "10px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "15px",
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id="grafico_prioritarios_tipo"
                                )
                            ],
                            style={"width": "49%", "minWidth": "0"},
                        ),

                        html.Div(
                            [
                                dcc.Graph(
                                    id="grafico_prioritarios_modalidad"
                                )
                            ],
                            style={"width": "49%", "minWidth": "0"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "gap": "20px",
                    },
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
                        sort_action="custom",
                        filter_action="native",
                        style_table={
                            "overflowX": "auto",
                            "border": "1px solid #E1E6ED",
                            "borderRadius": "8px",
                        },
                        style_cell={
                            "textAlign": "left",
                            "whiteSpace": "normal",
                            "height": "auto",
                            "fontFamily": "Arial, sans-serif",
                            "fontSize": "13px",
                            "padding": "8px 10px",
                            "border": "1px solid #E5E7EB",
                        },

                        style_header={
                            "backgroundColor": "#17365D",
                            "color": "#FFFFFF",
                            "fontWeight": "700",
                            "textAlign": "center",
                            "fontSize": "13px",
                        },

                        style_cell_conditional=[
                            {
                                "if": {"column_id": "id_contrato"},
                                "width": "110px",
                            },
                            {
                                "if": {"column_id": "proveedor_adjudicado"},
                                "width": "220px",
                            },
                            {
                                "if": {"column_id": "estado_contrato"},
                                "width": "120px",
                            },
                            {
                                "if": {"column_id": "tipo_de_contrato"},
                                "width": "150px",
                            },
                            {
                                "if": {"column_id": "modalidad_de_contratacion"},
                                "width": "210px",
                            },
                            {
                                "if": {"column_id": "valor_del_contrato"},
                                "width": "150px",
                            },
                            {
                                "if": {"column_id": "porcentaje_ejecutado"},
                                "width": "100px",
                            },
                            {
                                "if": {"column_id": "porcentaje_pagado"},
                                "width": "100px",
                            },
                            {
                                "if": {"column_id": "valor_pendiente_de_ejecucion"},
                                "width": "160px",
                            },
                            {
                                "if": {"column_id": "valor_pendiente_de_pago"},
                                "width": "150px",
                            },
                            {
                                "if": {"column_id": "dias_adicionados"},
                                "width": "110px",
                            },
                            {
                                "if": {"column_id": "contrato_prioritario"},
                                "width": "100px",
                            },
                        ],
                  
                        style_data_conditional=[
                        {
                            "if": {
                                "filter_query": '{contrato_prioritario} = "Sí"',
                                "column_id": "contrato_prioritario",
                            },
                            "fontWeight": "bold",
                        },
                        {
                            "if": {"column_id": "valor_del_contrato"},
                            "textAlign": "right",
                        },
                        {
                            "if": {"column_id": "porcentaje_ejecutado"},
                            "textAlign": "right",
                        },
                        {
                            "if": {"column_id": "porcentaje_pagado"},
                            "textAlign": "right",
                        },
                        {
                            "if": {"column_id": "valor_pendiente_de_ejecucion"},
                            "textAlign": "right",
                        },
                        {
                            "if": {"column_id": "valor_pendiente_de_pago"},
                            "textAlign": "right",
                        },
                        {
                            "if": {"column_id": "dias_adicionados"},
                            "textAlign": "right",
                        },
                    ],
                ),
            ],
            style={
                "marginTop": "30px",
            },
        ),

    ]
)

# --------------------------------------------------------
# FORMATO EJECUTIVO DE VALORES
# --------------------------------------------------------

def formato_monetario(valor):
    if pd.isna(valor):
        return "$ 0"

    if valor >= 1_000_000_000_000_000:
        return f"$ {valor / 1_000_000_000_000_000:,.1f} mil billones"

    elif valor >= 1_000_000_000_000:
        return f"$ {valor / 1_000_000_000_000:,.1f} billones"

    elif valor >= 1_000_000_000:
        return f"$ {valor / 1_000_000_000:,.1f} mil millones"

    elif valor >= 1_000_000:
        return f"$ {valor / 1_000_000:,.1f} millones"

    elif valor >= 1_000:
        return f"$ {valor / 1_000:,.1f} mil"

    else:
        return f"$ {valor:,.0f}"

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
        df_filtrado.loc[
            df_filtrado["valor_pendiente_de_ejecucion"] > 0,
            "valor_pendiente_de_ejecucion"
        ]
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
        formato_monetario(pendiente_ejecucion)
    )

    pago_texto = (
        formato_monetario(pendiente_pago)
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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
            cliponaxis=False,

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
        xaxis_range=[0, top10["valor_pendiente_de_ejecucion"].max() * 1.20],
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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

        equivalencia_nivel = {
            "0%": "0 %",
            "1%-49%": "1 % - 49 %",
            "50%-99%": "50 % - 99 %",
            ">=100%": "≥ 100 %",
            "Sin dato": "Sin dato",
        }

        df_filtrado = df_filtrado[
            df_filtrado["nivel_ejecucion_grafico"]
            == equivalencia_nivel[nivel_ejecucion]
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
        xaxis_range=[0, resumen.max() * 1.20 if not resumen.empty else 1],
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
    Input("tabla_contratos", "sort_by"),
)
def actualizar_tabla(
    estado,
    tipo,
    modalidad,
    extension,
    nivel_ejecucion,
    sort_by,
):
    # ---------------------------------------------------------
    # 1. Aplicar los filtros seleccionados
    # ---------------------------------------------------------

    df_filtrado = df.copy()

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

    # ---------------------------------------------------------
    # 2. Ordenar NUMÉRICAMENTE antes de aplicar formatos
    # ---------------------------------------------------------

    if sort_by:
        columnas_orden = [item["column_id"] for item in sort_by]
        direcciones = [
            item["direction"] == "asc"
            for item in sort_by
        ]

        df_filtrado = df_filtrado.sort_values(
            by=columnas_orden,
            ascending=direcciones,
            na_position="last",
            kind="mergesort",
        )

    # ---------------------------------------------------------
    # 3. Seleccionar columnas para la tabla
    # ---------------------------------------------------------

    df_tabla = df_filtrado[
        [columna["id"] for columna in columnas_tabla]
    ].copy()

    # ---------------------------------------------------------
    # 4. Formatear porcentajes SOLO para presentación
    # ---------------------------------------------------------

    df_tabla["porcentaje_ejecutado"] = (
        df_tabla["porcentaje_ejecutado"]
        .round(1)
        .map(lambda x: f"{x:.1f} %" if pd.notna(x) else "")
    )

    df_tabla["porcentaje_pagado"] = (
        df_tabla["porcentaje_pagado"]
        .round(1)
        .map(lambda x: f"{x:.1f} %" if pd.notna(x) else "")
    )

    # ---------------------------------------------------------
    # 5. Formatear valores monetarios SOLO para presentación
    # ---------------------------------------------------------

    df_tabla["valor_del_contrato"] = (
        df_tabla["valor_del_contrato"]
        .apply(formato_monetario)
    )

    df_tabla["valor_pendiente_de_ejecucion"] = (
        df_tabla["valor_pendiente_de_ejecucion"]
        .apply(formato_monetario)
    )

    df_tabla["valor_pendiente_de_pago"] = (
        df_tabla["valor_pendiente_de_pago"]
        .apply(formato_monetario)
    )

    # ---------------------------------------------------------
    # 6. Entregar los datos a Dash
    # ---------------------------------------------------------

    return df_tabla.to_dict("records")

# ============================================================
# 4. EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)