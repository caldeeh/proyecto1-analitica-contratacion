"""Pregunta 1 — Concentración de la contratación.

Autor: Jhoiner Javier Ramos Ramírez

Módulo integrado al tablero general de contratación pública del INVIAS.

Este archivo es la versión modular de `Tarea 4/Pregunta 1/app_p1.py`.
A diferencia de la aplicación independiente:
- no crea una instancia propia de Dash;
- expone `layout` para que `despliegue/app.py` lo cargue como pestaña;
- registra sus callbacks con `@callback`;
- todos los IDs usan el prefijo `conc-` para evitar choques con otros módulos.
"""

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html, dash_table


# ============================================================
# 1. CARGA DE DATOS
# ============================================================

RAIZ = Path(__file__).resolve().parents[2]
RUTA_DATOS = RAIZ / "Tarea 2" / "Pregunta 1" / "df_analitico_p1.csv"

df = pd.read_csv(RUTA_DATOS, low_memory=False)


def _mascara_booleana(serie):
    """Convierte True/False o su representación en texto a una máscara booleana."""
    if serie.dtype == bool:
        return serie

    return (
        serie.astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "si", "sí", "yes"])
    )


# Dos universos de análisis:
# - conteo: contratos formalizados
# - valor: contratos formalizados con valor positivo
df_conteo = df[_mascara_booleana(df["apto_conteo_p1"])].copy()
df_valor = df[_mascara_booleana(df["apto_valor_p1"])].copy()

ANIO_MIN = int(df_conteo["anio_firma"].dropna().min())
ANIO_MAX = int(df_conteo["anio_firma"].dropna().max())

TIPOS = sorted(
    df_conteo["tipo_de_contrato"]
    .dropna()
    .astype(str)
    .unique()
)

MODALIDADES = sorted(
    df_conteo["modalidad_de_contratacion"]
    .dropna()
    .astype(str)
    .unique()
)


# ============================================================
# 2. PALETA
# ============================================================

AZUL = "#2a78d6"
AZUL_CLARO = "#9ec5f4"
ROJO_SUAVE = "#e98383"

TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRIS = "#898781"
LINEA = "#e1e0d9"
BLANCO = "#ffffff"


# ============================================================
# 3. FUNCIONES AUXILIARES
# ============================================================

def _es(texto):
    """Convierte formato numérico inglés a formato visual español."""
    return (
        texto
        .replace(",", "\x00")
        .replace(".", ",")
        .replace("\x00", ".")
    )


def entero(valor):
    return _es(f"{valor:,.0f}")


def porcentaje(valor, decimales=2):
    return _es(f"{valor:,.{decimales}f}") + " %"


def pesos(valor):
    if pd.isna(valor) or valor == 0:
        return "$0"

    if abs(valor) >= 1e12:
        return "$" + _es(f"{valor / 1e12:,.2f}") + " billones"

    if abs(valor) >= 1e9:
        return "$" + _es(f"{valor / 1e9:,.1f}") + " mil millones"

    if abs(valor) >= 1e6:
        return "$" + _es(f"{valor / 1e6:,.1f}") + " millones"

    return "$" + _es(f"{valor:,.0f}")


def abreviar(texto, maximo=38):
    texto = str(texto)
    if len(texto) <= maximo:
        return texto
    return texto[: maximo - 1] + "…"


def filtrar(base, anios, tipo, modalidad):
    """Aplica los filtros del usuario sobre una base de contratos."""
    datos = base.copy()

    if anios and len(anios) == 2:
        datos = datos[
            datos["anio_firma"].between(
                anios[0],
                anios[1],
                inclusive="both",
            )
        ]

    if tipo:
        datos = datos[
            datos["tipo_de_contrato"] == tipo
        ]

    if modalidad:
        datos = datos[
            datos["modalidad_de_contratacion"] == modalidad
        ]

    return datos


def resumen_proveedores(datos):
    """Agrega los contratos monetarios por proveedor y calcula participaciones."""
    if datos.empty:
        return pd.DataFrame(
            columns=[
                "proveedor_id",
                "proveedor_etiqueta",
                "numero_contratos",
                "valor_contratado",
                "participacion_pct",
                "participacion_acumulada_pct",
            ]
        )

    resumen = (
        datos.groupby(
            ["proveedor_id", "proveedor_etiqueta"],
            dropna=False,
            as_index=False,
        )
        .agg(
            numero_contratos=("id_contrato", "size"),
            valor_contratado=("valor_del_contrato", "sum"),
        )
        .sort_values("valor_contratado", ascending=False)
        .reset_index(drop=True)
    )

    total = resumen["valor_contratado"].sum()

    if total > 0:
        resumen["participacion_pct"] = (
            100 * resumen["valor_contratado"] / total
        )
        resumen["participacion_acumulada_pct"] = (
            resumen["participacion_pct"].cumsum()
        )
    else:
        resumen["participacion_pct"] = 0.0
        resumen["participacion_acumulada_pct"] = 0.0

    return resumen


def calcular_cr(resumen, n):
    """Participación acumulada de los n proveedores con mayor valor."""
    if resumen.empty:
        return 0.0

    return float(
        resumen.head(n)["participacion_pct"].sum()
    )


def resumen_categoria(
    conteo,
    valor,
    columna,
    max_categorias=7,
):
    """Compara % de contratos y % del valor para una variable categórica."""
    tabla_conteo = (
        conteo.groupby(columna, dropna=False)
        .size()
        .reset_index(name="contratos")
    )

    tabla_valor = (
        valor.groupby(columna, dropna=False)["valor_del_contrato"]
        .sum()
        .reset_index(name="valor_contratado")
    )

    resumen = tabla_conteo.merge(
        tabla_valor,
        on=columna,
        how="outer",
    ).fillna(0)

    total_contratos = resumen["contratos"].sum()
    total_valor = resumen["valor_contratado"].sum()

    resumen["pct_contratos"] = (
        100 * resumen["contratos"] / total_contratos
        if total_contratos > 0
        else 0
    )

    resumen["pct_valor"] = (
        100 * resumen["valor_contratado"] / total_valor
        if total_valor > 0
        else 0
    )

    # La relevancia considera simultáneamente frecuencia y peso económico.
    resumen["relevancia"] = resumen[
        ["pct_contratos", "pct_valor"]
    ].max(axis=1)

    resumen = (
        resumen
        .nlargest(max_categorias, "relevancia")
        .sort_values("relevancia", ascending=True)
        .copy()
    )

    return resumen


def figura_vacia(
    mensaje="Sin datos para los filtros seleccionados",
):
    figura = go.Figure()

    figura.add_annotation(
        text=mensaje,
        showarrow=False,
        font=dict(size=13, color=GRIS),
    )

    figura.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor=BLANCO,
        paper_bgcolor=BLANCO,
        margin=dict(l=10, r=10, t=10, b=10),
        height=390,
    )

    return figura


DISENO_BASE = dict(
    plot_bgcolor=BLANCO,
    paper_bgcolor=BLANCO,
    font=dict(
        family="-apple-system, Segoe UI, Roboto, sans-serif",
        size=12,
        color=TINTA_2,
    ),
    margin=dict(l=45, r=20, t=20, b=45),
    hoverlabel=dict(
        bgcolor=BLANCO,
        font_size=12,
        bordercolor=LINEA,
    ),
)


# ============================================================
# 4. COMPONENTES
# ============================================================

def _indicador(id_valor, etiqueta):
    return html.Div(
        className="kpi",
        children=[
            html.Div(
                id=id_valor,
                className="valor",
            ),
            html.Div(
                etiqueta,
                className="etiqueta",
            ),
        ],
    )


def _filtros():
    return html.Div(
        className="tarjeta",
        children=[
            html.H2("Filtros"),
            html.Div(
                style={
                    "display": "flex",
                    "gap": "22px",
                    "flexWrap": "wrap",
                    "alignItems": "flex-end",
                },
                children=[
                    html.Div(
                        style={"flex": "2 1 340px"},
                        children=[
                            html.Label(
                                "Año de firma",
                                style={
                                    "fontSize": "12px",
                                    "color": TINTA_2,
                                },
                            ),
                            dcc.RangeSlider(
                                id="conc-anios",
                                min=ANIO_MIN,
                                max=ANIO_MAX,
                                step=1,
                                value=[ANIO_MIN, ANIO_MAX],
                                marks={
                                    a: str(a)
                                    for a in range(
                                        ANIO_MIN,
                                        ANIO_MAX + 1,
                                    )
                                },
                                tooltip={
                                    "placement": "bottom",
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        style={"flex": "1 1 240px"},
                        children=[
                            html.Label(
                                "Tipo de contrato",
                                style={
                                    "fontSize": "12px",
                                    "color": TINTA_2,
                                },
                            ),
                            dcc.Dropdown(
                                id="conc-tipo",
                                options=[
                                    {
                                        "label": valor,
                                        "value": valor,
                                    }
                                    for valor in TIPOS
                                ],
                                placeholder="Todos",
                                clearable=True,
                            ),
                        ],
                    ),
                    html.Div(
                        style={"flex": "1 1 240px"},
                        children=[
                            html.Label(
                                "Modalidad",
                                style={
                                    "fontSize": "12px",
                                    "color": TINTA_2,
                                },
                            ),
                            dcc.Dropdown(
                                id="conc-modalidad",
                                options=[
                                    {
                                        "label": valor,
                                        "value": valor,
                                    }
                                    for valor in MODALIDADES
                                ],
                                placeholder="Todas",
                                clearable=True,
                            ),
                        ],
                    ),
                ],
            ),
            html.P(
                "2017 y 2026 son periodos parciales. "
                "La comparación temporal principal utiliza "
                "años completos entre 2018 y 2025.",
                className="nota",
                style={
                    "marginTop": "14px",
                    "marginBottom": "0",
                },
            ),
        ],
    )


# ============================================================
# 5. LAYOUT DEL MÓDULO
# ============================================================

layout = html.Div(
    [
        # Pregunta
        html.Div(
            className="pregunta-negocio",
            children=[
                html.Strong("Pregunta de negocio. "),
                "¿En qué proveedores, modalidades y tipos de contrato "
                "se concentra la contratación de INVIAS, y existen "
                "patrones de concentración que requieran seguimiento "
                "por parte de la Dirección y los organismos de control?",
            ],
        ),

        # KPI
        html.Div(
            className="fila-kpi",
            children=[
                _indicador(
                    "conc-kpi-contratos",
                    "Contratos formalizados / aptos para conteo",
                ),
                _indicador(
                    "conc-kpi-valor",
                    "Valor total contratado",
                ),
                _indicador(
                    "conc-kpi-proveedores",
                    "Proveedores únicos",
                ),
                _indicador(
                    "conc-kpi-cr5",
                    "CR5 · participación de los 5 principales",
                ),
                _indicador(
                    "conc-kpi-cr10",
                    "CR10 · participación de los 10 principales",
                ),
            ],
        ),

        html.Div(
            id="conc-nota-universo",
            style={
                "fontSize": "12px",
                "color": TINTA_2,
                "margin": "2px 0 20px",
            },
        ),

        # Filtros
        _filtros(),

        # Top 10 + Pareto
        html.Div(
            className="rejilla-dos",
            children=[
                html.Div(
                    className="tarjeta",
                    children=[
                        html.H2(
                            "Top 10 proveedores por valor contratado"
                        ),
                        html.P(
                            "Proveedores con mayor valor contratado "
                            "dentro de los filtros seleccionados.",
                            className="nota",
                        ),
                        dcc.Graph(
                            id="conc-top10",
                            config={
                                "displayModeBar": False,
                            },
                            style={"height": "420px"},
                        ),
                    ],
                ),
                html.Div(
                    className="tarjeta",
                    children=[
                        html.H2(
                            "Concentración acumulada"
                        ),
                        html.P(
                            "Porcentaje acumulado de proveedores frente "
                            "al porcentaje acumulado del valor contratado. "
                            "Las líneas señalan el punto en que se alcanza "
                            "el 80 % del valor.",
                            className="nota",
                        ),
                        dcc.Graph(
                            id="conc-pareto",
                            config={
                                "displayModeBar": False,
                            },
                            style={"height": "420px"},
                        ),
                    ],
                ),
            ],
        ),

        # Modalidad + tipo
        html.Div(
            className="rejilla-dos",
            children=[
                html.Div(
                    className="tarjeta",
                    children=[
                        html.H2(
                            "Contratos vs. valor por modalidad"
                        ),
                        html.P(
                            "Compara la participación de cada modalidad "
                            "en número de contratos y en valor contratado.",
                            className="nota",
                        ),
                        dcc.Graph(
                            id="conc-modalidades",
                            config={
                                "displayModeBar": False,
                            },
                            style={"height": "440px"},
                        ),
                    ],
                ),
                html.Div(
                    className="tarjeta",
                    children=[
                        html.H2(
                            "Contratos vs. valor por tipo de contrato"
                        ),
                        html.P(
                            "Compara la frecuencia contractual con el "
                            "peso económico de los principales tipos.",
                            className="nota",
                        ),
                        dcc.Graph(
                            id="conc-tipos",
                            config={
                                "displayModeBar": False,
                            },
                            style={"height": "440px"},
                        ),
                    ],
                ),
            ],
        ),

        # Evolución
        html.Div(
            className="tarjeta",
            children=[
                html.H2(
                    "Evolución de la concentración"
                ),
                html.P(
                    "CR5 y CR10 por año de firma. La serie se restringe "
                    "a los años completos 2018–2025.",
                    className="nota",
                ),
                dcc.Graph(
                    id="conc-evolucion",
                    config={
                        "displayModeBar": False,
                    },
                    style={"height": "360px"},
                ),
            ],
        ),

        # Tabla
        html.Div(
            className="tarjeta",
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "gap": "16px",
                        "alignItems": "flex-start",
                        "flexWrap": "wrap",
                    },
                    children=[
                        html.Div(
                            children=[
                                html.H2(
                                    "Detalle de proveedores"
                                ),
                                html.P(
                                    "Vista de los proveedores con los filtros "
                                    "aplicados. La participación acumulada se "
                                    "calcula sobre el universo monetario filtrado.",
                                    className="nota",
                                ),
                            ],
                        ),
                        dcc.Input(
                            id="conc-buscar",
                            type="text",
                            placeholder="Buscar proveedor...",
                            debounce=True,
                            style={
                                "width": "220px",
                                "height": "34px",
                                "border": f"1px solid {LINEA}",
                                "borderRadius": "6px",
                                "padding": "0 10px",
                                "fontSize": "12px",
                            },
                        ),
                    ],
                ),

                dash_table.DataTable(
                    id="conc-tabla",
                    columns=[
                        {
                            "name": "Proveedor",
                            "id": "proveedor",
                        },
                        {
                            "name": "Nº contratos",
                            "id": "numero_contratos",
                        },
                        {
                            "name": "Valor contratado",
                            "id": "valor_contratado",
                        },
                        {
                            "name": "% del valor total",
                            "id": "participacion_pct",
                        },
                        {
                            "name": "% acumulado",
                            "id": "participacion_acumulada_pct",
                        },
                    ],
                    data=[],
                    page_size=10,
                    sort_action="native",
                    page_action="native",
                    style_table={
                        "overflowX": "auto",
                        "border": f"1px solid {LINEA}",
                        "borderRadius": "6px",
                    },
                    style_cell={
                        "fontFamily": (
                            "-apple-system, Segoe UI, Roboto, sans-serif"
                        ),
                        "fontSize": "12px",
                        "padding": "9px 10px",
                        "textAlign": "left",
                        "border": "none",
                        "borderBottom": "1px solid #ecebe6",
                        "color": TINTA_2,
                        "whiteSpace": "normal",
                        "height": "auto",
                    },
                    style_header={
                        "backgroundColor": "#f1f3f5",
                        "fontWeight": "600",
                        "color": TINTA_2,
                        "border": "none",
                        "borderBottom": f"1px solid {LINEA}",
                    },
                    style_cell_conditional=[
                        {
                            "if": {
                                "column_id": "proveedor",
                            },
                            "width": "36%",
                        },
                        {
                            "if": {
                                "column_id": "numero_contratos",
                            },
                            "textAlign": "right",
                        },
                        {
                            "if": {
                                "column_id": "valor_contratado",
                            },
                            "textAlign": "right",
                        },
                        {
                            "if": {
                                "column_id": "participacion_pct",
                            },
                            "textAlign": "right",
                        },
                        {
                            "if": {
                                "column_id": (
                                    "participacion_acumulada_pct"
                                ),
                            },
                            "textAlign": "right",
                        },
                    ],
                ),
            ],
        ),
    ]
)


# ============================================================
# 6. ENTRADAS COMUNES
# ============================================================

ENTRADAS = [
    Input("conc-anios", "value"),
    Input("conc-tipo", "value"),
    Input("conc-modalidad", "value"),
]


# ============================================================
# 7. CALLBACK KPI
# ============================================================

@callback(
    Output(
        "conc-kpi-contratos",
        "children",
    ),
    Output(
        "conc-kpi-valor",
        "children",
    ),
    Output(
        "conc-kpi-proveedores",
        "children",
    ),
    Output(
        "conc-kpi-cr5",
        "children",
    ),
    Output(
        "conc-kpi-cr10",
        "children",
    ),
    Output(
        "conc-nota-universo",
        "children",
    ),
    *ENTRADAS,
)
def actualizar_indicadores(
    anios,
    tipo,
    modalidad,
):
    conteo = filtrar(
        df_conteo,
        anios,
        tipo,
        modalidad,
    )

    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    resumen = resumen_proveedores(valor)

    contratos = len(conteo)
    contratos_valor = len(valor)

    valor_total = (
        valor["valor_del_contrato"].sum()
        if not valor.empty
        else 0
    )

    proveedores_conteo = (
        conteo["proveedor_id"].nunique()
        if not conteo.empty
        else 0
    )

    proveedores_valor = (
        valor["proveedor_id"].nunique()
        if not valor.empty
        else 0
    )

    cr5 = calcular_cr(resumen, 5)
    cr10 = calcular_cr(resumen, 10)

    nota = (
        f"{entero(contratos_valor)} contratos con valor positivo y "
        f"{entero(proveedores_valor)} proveedores se utilizan en "
        f"los análisis monetarios de concentración."
    )

    return (
        entero(contratos),
        pesos(valor_total),
        entero(proveedores_conteo),
        porcentaje(cr5),
        porcentaje(cr10),
        nota,
    )


# ============================================================
# 8. CALLBACK TOP 10 PROVEEDORES
# ============================================================

@callback(
    Output(
        "conc-top10",
        "figure",
    ),
    *ENTRADAS,
)
def actualizar_top10(
    anios,
    tipo,
    modalidad,
):
    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    resumen = resumen_proveedores(valor)

    if resumen.empty:
        return figura_vacia()

    top10 = resumen.head(10).copy()

    top10["proveedor_corto"] = (
        top10["proveedor_etiqueta"]
        .map(abreviar)
    )

    top10 = top10.sort_values(
        "valor_contratado",
        ascending=True,
    )

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=top10["valor_contratado"] / 1e9,
            y=top10["proveedor_corto"],
            orientation="h",
            marker_color=AZUL_CLARO,
            customdata=top10[
                [
                    "proveedor_etiqueta",
                    "numero_contratos",
                    "participacion_pct",
                ]
            ],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Valor: $%{x:,.1f} mil millones<br>"
                "Contratos: %{customdata[1]}<br>"
                "Participación: %{customdata[2]:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        **DISENO_BASE,
        height=410,
        showlegend=False,
    )

    figura.update_xaxes(
        title="Valor contratado (miles de millones COP)",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    figura.update_yaxes(
        title=None,
        showgrid=False,
    )

    return figura


# ============================================================
# 9. CALLBACK CONCENTRACIÓN ACUMULADA
# ============================================================

@callback(
    Output(
        "conc-pareto",
        "figure",
    ),
    *ENTRADAS,
)
def actualizar_pareto(
    anios,
    tipo,
    modalidad,
):
    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    resumen = resumen_proveedores(valor)

    if resumen.empty:
        return figura_vacia()

    resumen = resumen.copy()

    resumen["porcentaje_proveedores"] = (
        100
        * (resumen.index + 1)
        / len(resumen)
    )

    candidatos = resumen[
        resumen[
            "participacion_acumulada_pct"
        ] >= 80
    ]

    if candidatos.empty:
        n_80 = len(resumen)
        pct_80 = 100.0
    else:
        posicion = int(
            candidatos.index[0]
        )

        n_80 = posicion + 1

        pct_80 = float(
            resumen.loc[
                posicion,
                "porcentaje_proveedores",
            ]
        )

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=resumen[
                "porcentaje_proveedores"
            ],
            y=resumen[
                "participacion_acumulada_pct"
            ],
            mode="lines",
            line={
                "color": AZUL,
                "width": 2.5,
            },
            hovertemplate=(
                "% proveedores: %{x:.2f}%<br>"
                "% valor acumulado: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.add_trace(
        go.Scatter(
            x=[pct_80],
            y=[80],
            mode="markers",
            marker={
                "size": 8,
                "color": ROJO_SUAVE,
            },
            showlegend=False,
            hovertemplate=(
                f"{n_80} proveedores<br>"
                f"{pct_80:.2f}% del total<br>"
                "80% del valor"
                "<extra></extra>"
            ),
        )
    )

    figura.add_hline(
        y=80,
        line_dash="dash",
        line_color=ROJO_SUAVE,
        line_width=1.2,
    )

    figura.add_vline(
        x=pct_80,
        line_dash="dash",
        line_color=ROJO_SUAVE,
        line_width=1.2,
    )

    figura.add_annotation(
        x=pct_80,
        y=80,
        text=(
            f"<b>{n_80} proveedores</b><br>"
            f"{pct_80:.2f}% concentran "
            f"el 80% del valor"
        ),
        showarrow=True,
        arrowhead=2,
        ax=95,
        ay=-40,
        font={
            "size": 10,
            "color": TINTA,
        },
        bgcolor="rgba(255,255,255,0.92)",
        bordercolor=LINEA,
        borderpad=4,
    )

    figura.update_layout(
        **DISENO_BASE,
        height=410,
        showlegend=False,
    )

    figura.update_xaxes(
        title="% acumulado de proveedores",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    figura.update_yaxes(
        title="% acumulado del valor",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    return figura


# ============================================================
# 10. CALLBACK MODALIDAD
# ============================================================

@callback(
    Output(
        "conc-modalidades",
        "figure",
    ),
    *ENTRADAS,
)
def actualizar_modalidades(
    anios,
    tipo,
    modalidad,
):
    conteo = filtrar(
        df_conteo,
        anios,
        tipo,
        modalidad,
    )

    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    if conteo.empty:
        return figura_vacia()

    resumen = resumen_categoria(
        conteo,
        valor,
        "modalidad_de_contratacion",
        max_categorias=7,
    )

    etiquetas = resumen[
        "modalidad_de_contratacion"
    ].map(
        lambda x: abreviar(x, 31)
    )

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen["pct_contratos"],
            y=etiquetas,
            orientation="h",
            name="% Nº contratos",
            marker_color=AZUL,
            hovertemplate=(
                "%{y}<br>"
                "% contratos: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.add_trace(
        go.Bar(
            x=resumen["pct_valor"],
            y=etiquetas,
            orientation="h",
            name="% Valor contratado",
            marker_color=AZUL_CLARO,
            hovertemplate=(
                "%{y}<br>"
                "% valor: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        **DISENO_BASE,
        height=430,
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            font=dict(size=10),
        ),
    )

    figura.update_xaxes(
        title="Participación (%)",
        ticksuffix="%",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    figura.update_yaxes(
        title=None,
        showgrid=False,
    )

    return figura


# ============================================================
# 11. CALLBACK TIPO DE CONTRATO
# ============================================================

@callback(
    Output(
        "conc-tipos",
        "figure",
    ),
    *ENTRADAS,
)
def actualizar_tipos(
    anios,
    tipo,
    modalidad,
):
    conteo = filtrar(
        df_conteo,
        anios,
        tipo,
        modalidad,
    )

    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    if conteo.empty:
        return figura_vacia()

    resumen = resumen_categoria(
        conteo,
        valor,
        "tipo_de_contrato",
        max_categorias=7,
    )

    etiquetas = resumen[
        "tipo_de_contrato"
    ].map(
        lambda x: abreviar(x, 31)
    )

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen["pct_contratos"],
            y=etiquetas,
            orientation="h",
            name="% Nº contratos",
            marker_color=AZUL,
            hovertemplate=(
                "%{y}<br>"
                "% contratos: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.add_trace(
        go.Bar(
            x=resumen["pct_valor"],
            y=etiquetas,
            orientation="h",
            name="% Valor contratado",
            marker_color=AZUL_CLARO,
            hovertemplate=(
                "%{y}<br>"
                "% valor: %{x:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        **DISENO_BASE,
        height=430,
        barmode="group",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            font=dict(size=10),
        ),
    )

    figura.update_xaxes(
        title="Participación (%)",
        ticksuffix="%",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    figura.update_yaxes(
        title=None,
        showgrid=False,
    )

    return figura


# ============================================================
# 12. CALLBACK EVOLUCIÓN CR5 Y CR10
# ============================================================

@callback(
    Output(
        "conc-evolucion",
        "figure",
    ),
    *ENTRADAS,
)
def actualizar_evolucion(
    anios,
    tipo,
    modalidad,
):
    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    # La tendencia utiliza únicamente años completos.
    valor = valor[
        valor["anio_firma"].between(
            2018,
            2025,
            inclusive="both",
        )
    ]

    if valor.empty:
        return figura_vacia(
            "No hay años completos 2018–2025 "
            "para los filtros seleccionados"
        )

    filas = []

    for anio, grupo in valor.groupby(
        "anio_firma"
    ):
        resumen = resumen_proveedores(
            grupo
        )

        filas.append(
            {
                "anio": int(anio),
                "CR5": calcular_cr(
                    resumen,
                    5,
                ),
                "CR10": calcular_cr(
                    resumen,
                    10,
                ),
            }
        )

    evolucion = (
        pd.DataFrame(filas)
        .sort_values("anio")
    )

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=evolucion["anio"],
            y=evolucion["CR10"],
            mode="lines+markers",
            name="CR10",
            line={
                "color": AZUL,
                "width": 2.5,
            },
            marker={
                "size": 7,
                "color": AZUL,
            },
            hovertemplate=(
                "Año %{x}<br>"
                "CR10: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.add_trace(
        go.Scatter(
            x=evolucion["anio"],
            y=evolucion["CR5"],
            mode="lines+markers",
            name="CR5",
            line={
                "color": AZUL_CLARO,
                "width": 2.5,
            },
            marker={
                "size": 7,
                "color": AZUL_CLARO,
            },
            hovertemplate=(
                "Año %{x}<br>"
                "CR5: %{y:.2f}%"
                "<extra></extra>"
            ),
        )
    )

    figura.update_layout(
        **DISENO_BASE,
        height=350,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            font=dict(size=10),
        ),
    )

    figura.update_xaxes(
        title="Año de firma",
        dtick=1,
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    figura.update_yaxes(
        title="Concentración (%)",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        gridcolor="#ecebe6",
        zeroline=False,
    )

    return figura


# ============================================================
# 13. CALLBACK TABLA DE PROVEEDORES
# ============================================================

@callback(
    Output(
        "conc-tabla",
        "data",
    ),
    Input(
        "conc-anios",
        "value",
    ),
    Input(
        "conc-tipo",
        "value",
    ),
    Input(
        "conc-modalidad",
        "value",
    ),
    Input(
        "conc-buscar",
        "value",
    ),
)
def actualizar_tabla(
    anios,
    tipo,
    modalidad,
    busqueda,
):
    valor = filtrar(
        df_valor,
        anios,
        tipo,
        modalidad,
    )

    resumen = resumen_proveedores(
        valor
    )

    if resumen.empty:
        return []

    if busqueda:
        resumen = resumen[
            resumen[
                "proveedor_etiqueta"
            ]
            .astype(str)
            .str.contains(
                busqueda,
                case=False,
                na=False,
            )
        ]

    tabla = resumen[
        [
            "proveedor_etiqueta",
            "numero_contratos",
            "valor_contratado",
            "participacion_pct",
            "participacion_acumulada_pct",
        ]
    ].copy()

    tabla = tabla.rename(
        columns={
            "proveedor_etiqueta": (
                "proveedor"
            ),
        }
    )

    tabla[
        "numero_contratos"
    ] = tabla[
        "numero_contratos"
    ].map(
        entero
    )

    tabla[
        "valor_contratado"
    ] = tabla[
        "valor_contratado"
    ].map(
        pesos
    )

    tabla[
        "participacion_pct"
    ] = tabla[
        "participacion_pct"
    ].map(
        porcentaje
    )

    tabla[
        "participacion_acumulada_pct"
    ] = tabla[
        "participacion_acumulada_pct"
    ].map(
        porcentaje
    )

    return tabla.to_dict(
        "records"
    )
