from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, dcc, html, dash_table
from plotly import graph_objects as go


# ============================================================
# 1. CARGA DE DATOS
# ============================================================

RAIZ = Path(__file__).resolve().parents[2]
RUTA_DATOS = RAIZ / "Tarea 2" / "Pregunta 1" / "df_analitico_p1.csv"

df = pd.read_csv(RUTA_DATOS, low_memory=False)

# Universo para frecuencia/conteo y universo para análisis monetario.
df_conteo = df[df["apto_conteo_p1"]].copy()
df_valor = df[df["apto_valor_p1"]].copy()

ANIO_MIN = int(df_conteo["anio_firma"].min())
ANIO_MAX = int(df_conteo["anio_firma"].max())

TIPOS = sorted(df_conteo["tipo_de_contrato"].dropna().astype(str).unique())
MODALIDADES = sorted(
    df_conteo["modalidad_de_contratacion"].dropna().astype(str).unique()
)


# ============================================================
# 2. APLICACIÓN DASH
# ============================================================

app = Dash(__name__, title="INVIAS | Concentración")


# ============================================================
# 3. PALETA Y ESTILOS
# ============================================================

FONDO = "#F4F7FB"
BLANCO = "#FFFFFF"
TINTA = "#1E293B"
TINTA_2 = "#64748B"
BORDE = "#D9E2EC"
AZUL = "#2F6FED"
AZUL_2 = "#5D8FF0"
AZUL_CLARO = "#A9C8FA"
AZUL_MUY_CLARO = "#EEF4FF"
ROJO_SUAVE = "#F08080"
GRIS_BARRA = "#E9EEF5"

ESTILO_TARJETA = {
    "backgroundColor": BLANCO,
    "border": f"1px solid {BORDE}",
    "borderRadius": "12px",
    "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.04)",
}

ESTILO_TITULO_GRAFICO = {
    "fontSize": "18px",
    "fontWeight": "700",
    "color": TINTA,
    "margin": "0 0 3px 0",
}

ESTILO_SUBTITULO = {
    "fontSize": "12px",
    "color": TINTA_2,
    "margin": "0 0 8px 0",
}


# ============================================================
# 4. FUNCIONES AUXILIARES
# ============================================================

def formato_entero(valor):
    return f"{int(valor):,}".replace(",", ".")


def formato_porcentaje(valor):
    return f"{valor:.2f} %".replace(".", ",")


def formato_monetario(valor):
    if pd.isna(valor) or valor == 0:
        return "$ 0"

    if abs(valor) >= 1_000_000_000_000:
        texto = f"$ {valor / 1_000_000_000_000:,.2f} billones"
    elif abs(valor) >= 1_000_000_000:
        texto = f"$ {valor / 1_000_000_000:,.1f} mil millones"
    elif abs(valor) >= 1_000_000:
        texto = f"$ {valor / 1_000_000:,.1f} millones"
    else:
        texto = f"$ {valor:,.0f}"

    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def abreviar_texto(texto, maximo=38):
    texto = str(texto)
    return texto if len(texto) <= maximo else texto[: maximo - 1] + "…"


def aplicar_filtros(base, anios, tipo, modalidad):
    datos = base.copy()

    if anios and len(anios) == 2:
        datos = datos[
            datos["anio_firma"].between(anios[0], anios[1], inclusive="both")
        ]

    if tipo:
        datos = datos[datos["tipo_de_contrato"] == tipo]

    if modalidad:
        datos = datos[datos["modalidad_de_contratacion"] == modalidad]

    return datos


def construir_resumen_proveedores(datos):
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
    if resumen.empty:
        return 0.0
    return float(resumen.head(n)["participacion_pct"].sum())


def configurar_figura(figura, altura=390):
    figura.update_layout(
        template="plotly_white",
        paper_bgcolor=BLANCO,
        plot_bgcolor=BLANCO,
        font={"family": "Arial, sans-serif", "color": TINTA},
        height=altura,
        margin={"l": 50, "r": 25, "t": 25, "b": 45},
        hoverlabel={"font": {"family": "Arial, sans-serif"}},
    )
    figura.update_xaxes(
        showgrid=True,
        gridcolor="#E9EEF5",
        zeroline=False,
        linecolor="#D5DDE7",
    )
    figura.update_yaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#D5DDE7",
    )
    return figura


def figura_vacia(mensaje="Sin datos para los filtros seleccionados"):
    figura = go.Figure()
    figura.add_annotation(
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        text=mensaje,
        showarrow=False,
        font={"size": 14, "color": TINTA_2},
    )
    figura.update_layout(
        template="plotly_white",
        paper_bgcolor=BLANCO,
        plot_bgcolor=BLANCO,
        height=390,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        xaxis={"visible": False},
        yaxis={"visible": False},
    )
    return figura


def resumen_categoria(conteo, valor, columna, max_categorias=7):
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

    resumen = tabla_conteo.merge(tabla_valor, on=columna, how="outer").fillna(0)

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

    # Selecciona las categorías más relevantes sin perder la mirada
    # conjunta entre frecuencia y valor.
    resumen["relevancia"] = resumen[["pct_contratos", "pct_valor"]].max(axis=1)
    resumen = resumen.nlargest(max_categorias, "relevancia").copy()
    resumen = resumen.sort_values("relevancia", ascending=True)

    return resumen


def tarjeta_kpi(titulo, id_valor, subtitulo, simbolo):
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        titulo,
                        style={
                            "fontSize": "14px",
                            "fontWeight": "700",
                            "color": TINTA,
                        },
                    ),
                    html.Div(
                        simbolo,
                        style={
                            "fontSize": "14px",
                            "color": AZUL,
                            "fontWeight": "700",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "marginBottom": "8px",
                },
            ),
            html.Div(
                id=id_valor,
                style={
                    "fontSize": "27px",
                    "fontWeight": "700",
                    "color": TINTA,
                    "lineHeight": "1.1",
                    "marginBottom": "7px",
                },
            ),
            html.Div(
                subtitulo,
                style={
                    "fontSize": "11px",
                    "lineHeight": "1.45",
                    "color": TINTA_2,
                },
            ),
        ],
        style={
            **ESTILO_TARJETA,
            "padding": "16px 16px",
            "flex": "1 1 170px",
            "minHeight": "105px",
        },
    )


# ============================================================
# 5. DISEÑO DEL TABLERO
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
                            "Contratación pública del INVIAS",
                            style={
                                "margin": "0",
                                "fontSize": "30px",
                                "fontWeight": "700",
                                "color": TINTA,
                            },
                        ),
                        html.P(
                            "Instituto Nacional de Vías · SECOP II, corte 24-ago-2026",
                            style={
                                "margin": "5px 0 0 0",
                                "fontSize": "12px",
                                "color": TINTA_2,
                            },
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            "Tablero de análisis",
                            style={
                                "fontSize": "11px",
                                "color": TINTA_2,
                                "textAlign": "center",
                            },
                        ),
                        html.Div(
                            "Concentración",
                            style={
                                "fontSize": "14px",
                                "fontWeight": "700",
                                "color": AZUL,
                                "textAlign": "center",
                                "marginTop": "2px",
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": "#E8F0FF",
                        "border": "1px solid #BED2FA",
                        "borderRadius": "9px",
                        "padding": "9px 24px",
                        "minWidth": "150px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "flex-start",
                "gap": "20px",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # NAVEGACIÓN VISUAL
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    "Concentración",
                    style={
                        "fontWeight": "700",
                        "color": TINTA,
                        "paddingBottom": "10px",
                        "borderBottom": f"3px solid {AZUL}",
                    },
                ),
                html.Div(
                    "Distribución territorial",
                    style={
                        "color": TINTA_2,
                        "paddingBottom": "10px",
                    },
                ),
                html.Div(
                    "Ejecución financiera",
                    style={
                        "color": TINTA_2,
                        "paddingBottom": "10px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "34px",
                "fontSize": "13px",
                "borderBottom": f"1px solid {BORDE}",
                "marginBottom": "17px",
            },
        ),

        # ----------------------------------------------------
        # PREGUNTA DE NEGOCIO
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    "Pregunta de negocio",
                    style={
                        "fontSize": "14px",
                        "fontWeight": "700",
                        "marginBottom": "5px",
                    },
                ),
                html.Div(
                    "¿En qué proveedores, modalidades y tipos de contrato se concentra "
                    "la contratación de INVIAS, y existen patrones de concentración que "
                    "requieran seguimiento por parte de la Dirección y los organismos de control?",
                    style={
                        "fontSize": "12px",
                        "lineHeight": "1.5",
                        "color": "#475569",
                    },
                ),
            ],
            style={
                "backgroundColor": AZUL_MUY_CLARO,
                "borderLeft": f"4px solid {AZUL}",
                "borderRadius": "8px",
                "padding": "14px 16px",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------
        html.Div(
            [
                tarjeta_kpi(
                    "Contratos",
                    "conc-kpi-contratos",
                    "contratos formalizados / aptos para conteo",
                    "▧",
                ),
                tarjeta_kpi(
                    "Valor total",
                    "conc-kpi-valor",
                    "valor de contratos con valor positivo",
                    "●",
                ),
                tarjeta_kpi(
                    "Proveedores",
                    "conc-kpi-proveedores",
                    "proveedores únicos en contratos formalizados",
                    "■",
                ),
                tarjeta_kpi(
                    "CR5",
                    "conc-kpi-cr5",
                    "participación de los top 5 proveedores",
                    "▥",
                ),
                tarjeta_kpi(
                    "CR10",
                    "conc-kpi-cr10",
                    "participación de los top 10 proveedores",
                    "▥",
                ),
            ],
            style={
                "display": "flex",
                "gap": "10px",
                "flexWrap": "wrap",
                "marginBottom": "18px",
            },
        ),

        html.Div(
            id="conc-nota-universo",
            style={
                "fontSize": "11px",
                "color": TINTA_2,
                "margin": "-10px 0 18px 2px",
            },
        ),

        # ----------------------------------------------------
        # FILTROS
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    "FILTROS",
                    style={
                        "fontSize": "13px",
                        "fontWeight": "700",
                        "color": "#475569",
                        "letterSpacing": "0.4px",
                        "marginBottom": "16px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "Año de firma",
                                    style={
                                        "fontSize": "12px",
                                        "fontWeight": "600",
                                        "color": "#475569",
                                    },
                                ),
                                dcc.RangeSlider(
                                    id="conc-filtro-anios",
                                    min=ANIO_MIN,
                                    max=ANIO_MAX,
                                    step=1,
                                    value=[ANIO_MIN, ANIO_MAX],
                                    marks={
                                        anio: str(anio)
                                        for anio in range(ANIO_MIN, ANIO_MAX + 1)
                                    },
                                    tooltip={"placement": "bottom"},
                                ),
                            ],
                            style={"flex": "1.4 1 370px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Tipo de contrato",
                                    style={
                                        "fontSize": "12px",
                                        "fontWeight": "600",
                                        "color": "#475569",
                                        "display": "block",
                                        "marginBottom": "6px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="conc-filtro-tipo",
                                    options=[
                                        {"label": valor, "value": valor}
                                        for valor in TIPOS
                                    ],
                                    placeholder="Todos",
                                    clearable=True,
                                    style={"fontSize": "12px"},
                                ),
                            ],
                            style={"flex": "1 1 250px"},
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "Modalidad",
                                    style={
                                        "fontSize": "12px",
                                        "fontWeight": "600",
                                        "color": "#475569",
                                        "display": "block",
                                        "marginBottom": "6px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="conc-filtro-modalidad",
                                    options=[
                                        {"label": valor, "value": valor}
                                        for valor in MODALIDADES
                                    ],
                                    placeholder="Todas",
                                    clearable=True,
                                    style={"fontSize": "12px"},
                                ),
                            ],
                            style={"flex": "1 1 250px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "18px",
                        "alignItems": "flex-end",
                        "flexWrap": "wrap",
                    },
                ),
                html.Div(
                    "Nota: 2017 y 2026 son periodos parciales. La evolución anual se compara "
                    "principalmente sobre años completos 2018–2025.",
                    style={
                        "fontSize": "10.5px",
                        "color": TINTA_2,
                        "marginTop": "12px",
                    },
                ),
            ],
            style={
                **ESTILO_TARJETA,
                "padding": "15px 18px",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # FILA 1 DE GRÁFICOS
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "Top 10 proveedores",
                            style=ESTILO_TITULO_GRAFICO,
                        ),
                        html.Div(
                            "Por valor contratado",
                            style=ESTILO_SUBTITULO,
                        ),
                        dcc.Graph(
                            id="conc-grafico-top10",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={
                        **ESTILO_TARJETA,
                        "padding": "14px 16px",
                        "flex": "1 1 520px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            "Concentración acumulada",
                            style=ESTILO_TITULO_GRAFICO,
                        ),
                        html.Div(
                            "Eje X: % acumulado de proveedores · Eje Y: % acumulado del valor contratado",
                            style=ESTILO_SUBTITULO,
                        ),
                        dcc.Graph(
                            id="conc-grafico-pareto",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={
                        **ESTILO_TARJETA,
                        "padding": "14px 16px",
                        "flex": "1 1 520px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "12px",
                "flexWrap": "wrap",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # FILA 2 DE GRÁFICOS
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "Contratos vs. valor por modalidad",
                            style=ESTILO_TITULO_GRAFICO,
                        ),
                        html.Div(
                            "% del número de contratos vs. % del valor contratado",
                            style=ESTILO_SUBTITULO,
                        ),
                        dcc.Graph(
                            id="conc-grafico-modalidad",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={
                        **ESTILO_TARJETA,
                        "padding": "14px 16px",
                        "flex": "1 1 520px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            "Contratos vs. valor por tipo de contrato",
                            style=ESTILO_TITULO_GRAFICO,
                        ),
                        html.Div(
                            "% del número de contratos vs. % del valor contratado",
                            style=ESTILO_SUBTITULO,
                        ),
                        dcc.Graph(
                            id="conc-grafico-tipo",
                            config={"displayModeBar": False},
                        ),
                    ],
                    style={
                        **ESTILO_TARJETA,
                        "padding": "14px 16px",
                        "flex": "1 1 520px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "gap": "12px",
                "flexWrap": "wrap",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # EVOLUCIÓN
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    "Evolución de la concentración",
                    style=ESTILO_TITULO_GRAFICO,
                ),
                html.Div(
                    "CR5 y CR10 por año de firma",
                    style=ESTILO_SUBTITULO,
                ),
                dcc.Graph(
                    id="conc-grafico-evolucion",
                    config={"displayModeBar": False},
                ),
            ],
            style={
                **ESTILO_TARJETA,
                "padding": "14px 16px",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # DETALLE DE PROVEEDORES
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    "Detalle de proveedores",
                                    style=ESTILO_TITULO_GRAFICO,
                                ),
                                html.Div(
                                    "Vista de datos con los filtros aplicados",
                                    style=ESTILO_SUBTITULO,
                                ),
                            ]
                        ),
                        dcc.Input(
                            id="conc-buscar-proveedor",
                            type="text",
                            placeholder="Buscar proveedor...",
                            debounce=True,
                            style={
                                "width": "220px",
                                "height": "34px",
                                "border": f"1px solid {BORDE}",
                                "borderRadius": "7px",
                                "padding": "0 10px",
                                "fontSize": "12px",
                                "outline": "none",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "flex-start",
                        "gap": "15px",
                        "flexWrap": "wrap",
                        "marginBottom": "10px",
                    },
                ),
                dash_table.DataTable(
                    id="conc-tabla-proveedores",
                    columns=[
                        {"name": "Proveedor", "id": "proveedor"},
                        {"name": "Nº contratos", "id": "numero_contratos"},
                        {"name": "Valor contratado", "id": "valor_contratado"},
                        {"name": "% del valor total", "id": "participacion_pct"},
                        {"name": "% acumulado", "id": "participacion_acumulada_pct"},
                    ],
                    data=[],
                    page_size=10,
                    sort_action="native",
                    style_table={
                        "overflowX": "auto",
                        "border": f"1px solid {BORDE}",
                        "borderRadius": "7px",
                    },
                    style_cell={
                        "fontFamily": "Arial, sans-serif",
                        "fontSize": "11px",
                        "padding": "9px 10px",
                        "textAlign": "left",
                        "border": "none",
                        "borderBottom": "1px solid #E8EDF3",
                        "color": "#475569",
                    },
                    style_header={
                        "backgroundColor": "#EEF2F7",
                        "color": "#475569",
                        "fontWeight": "700",
                        "fontSize": "11px",
                        "border": "none",
                        "borderBottom": f"1px solid {BORDE}",
                    },
                    style_cell_conditional=[
                        {"if": {"column_id": "proveedor"}, "width": "36%"},
                        {"if": {"column_id": "numero_contratos"}, "textAlign": "right"},
                        {"if": {"column_id": "valor_contratado"}, "textAlign": "right"},
                        {"if": {"column_id": "participacion_pct"}, "textAlign": "right"},
                        {
                            "if": {"column_id": "participacion_acumulada_pct"},
                            "textAlign": "right",
                        },
                    ],
                    page_action="native",
                ),
            ],
            style={
                **ESTILO_TARJETA,
                "padding": "15px 16px",
                "marginBottom": "18px",
            },
        ),

        # ----------------------------------------------------
        # PIE
        # ----------------------------------------------------
        html.Div(
            [
                html.Div(
                    "Pregunta 1 — Concentración de proveedores, modalidades y tipos de contrato"
                ),
                html.Div("Contratación pública del INVIAS"),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "gap": "15px",
                "fontSize": "10px",
                "color": "#94A3B8",
                "borderTop": f"1px solid {BORDE}",
                "paddingTop": "12px",
            },
        ),
    ],
    style={
        "maxWidth": "1380px",
        "margin": "0 auto",
        "padding": "24px 26px 30px 26px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": FONDO,
        "minHeight": "100vh",
        "boxSizing": "border-box",
    },
)


# ============================================================
# 6. CALLBACK DE KPI
# ============================================================

@app.callback(
    Output("conc-kpi-contratos", "children"),
    Output("conc-kpi-valor", "children"),
    Output("conc-kpi-proveedores", "children"),
    Output("conc-kpi-cr5", "children"),
    Output("conc-kpi-cr10", "children"),
    Output("conc-nota-universo", "children"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_kpi(anios, tipo, modalidad):
    conteo = aplicar_filtros(df_conteo, anios, tipo, modalidad)
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)

    resumen = construir_resumen_proveedores(valor)

    contratos = len(conteo)
    contratos_valor = len(valor)
    valor_total = valor["valor_del_contrato"].sum()
    proveedores_conteo = conteo["proveedor_id"].nunique()
    proveedores_valor = valor["proveedor_id"].nunique()

    cr5 = calcular_cr(resumen, 5)
    cr10 = calcular_cr(resumen, 10)

    nota = (
        f"{formato_entero(contratos_valor)} contratos con valor positivo y "
        f"{formato_entero(proveedores_valor)} proveedores se usan en los análisis "
        f"monetarios de concentración."
    )

    return (
        formato_entero(contratos),
        formato_monetario(valor_total),
        formato_entero(proveedores_conteo),
        formato_porcentaje(cr5),
        formato_porcentaje(cr10),
        nota,
    )


# ============================================================
# 7. CALLBACK TOP 10 PROVEEDORES
# ============================================================

@app.callback(
    Output("conc-grafico-top10", "figure"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_top10(anios, tipo, modalidad):
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)
    resumen = construir_resumen_proveedores(valor)

    if resumen.empty:
        return figura_vacia()

    top10 = resumen.head(10).copy()
    top10["proveedor_corto"] = top10["proveedor_etiqueta"].map(abreviar_texto)
    top10 = top10.sort_values("valor_contratado", ascending=True)

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=top10["valor_contratado"] / 1e9,
            y=top10["proveedor_corto"],
            orientation="h",
            marker={"color": AZUL_CLARO},
            customdata=top10[
                ["proveedor_etiqueta", "numero_contratos", "participacion_pct"]
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

    configurar_figura(figura, altura=395)
    figura.update_layout(
        margin={"l": 10, "r": 20, "t": 10, "b": 45},
        showlegend=False,
    )
    figura.update_xaxes(title="Valor contratado (miles de millones COP)")
    figura.update_yaxes(title=None)

    return figura


# ============================================================
# 8. CALLBACK CONCENTRACIÓN ACUMULADA
# ============================================================

@app.callback(
    Output("conc-grafico-pareto", "figure"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_pareto(anios, tipo, modalidad):
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)
    resumen = construir_resumen_proveedores(valor)

    if resumen.empty:
        return figura_vacia()

    resumen = resumen.copy()
    resumen["porcentaje_proveedores"] = (
        100 * (resumen.index + 1) / len(resumen)
    )

    candidatos = resumen[
        resumen["participacion_acumulada_pct"] >= 80
    ]

    if candidatos.empty:
        n_80 = len(resumen)
        pct_80 = 100.0
    else:
        posicion = int(candidatos.index[0])
        n_80 = posicion + 1
        pct_80 = float(resumen.loc[posicion, "porcentaje_proveedores"])

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=resumen["porcentaje_proveedores"],
            y=resumen["participacion_acumulada_pct"],
            mode="lines",
            line={"color": AZUL, "width": 2.5},
            name="% acumulado del valor",
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
            marker={"size": 8, "color": ROJO_SUAVE},
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
        line_width=1.3,
    )
    figura.add_vline(
        x=pct_80,
        line_dash="dash",
        line_color=ROJO_SUAVE,
        line_width=1.3,
    )

    figura.add_annotation(
        x=pct_80,
        y=80,
        text=(
            f"<b>{n_80} proveedores</b><br>"
            f"{pct_80:.2f}% concentran el 80% del valor"
        ),
        showarrow=True,
        arrowhead=2,
        ax=95,
        ay=-38,
        font={"size": 10, "color": TINTA},
        bgcolor="rgba(255,255,255,0.90)",
        bordercolor=BORDE,
        borderpad=5,
    )

    configurar_figura(figura, altura=395)
    figura.update_layout(
        margin={"l": 55, "r": 25, "t": 10, "b": 50},
        showlegend=False,
    )
    figura.update_xaxes(
        title="% acumulado de proveedores",
        range=[0, 100],
        ticksuffix="%",
    )
    figura.update_yaxes(
        title="% acumulado del valor",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        gridcolor="#E9EEF5",
    )

    return figura


# ============================================================
# 9. CALLBACK MODALIDAD
# ============================================================

@app.callback(
    Output("conc-grafico-modalidad", "figure"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_modalidad(anios, tipo, modalidad):
    conteo = aplicar_filtros(df_conteo, anios, tipo, modalidad)
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)

    if conteo.empty:
        return figura_vacia()

    resumen = resumen_categoria(
        conteo,
        valor,
        "modalidad_de_contratacion",
        max_categorias=7,
    )

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen["pct_contratos"],
            y=resumen["modalidad_de_contratacion"].map(
                lambda x: abreviar_texto(x, 31)
            ),
            orientation="h",
            name="% Nº contratos",
            marker={"color": AZUL},
            hovertemplate="%{y}<br>% contratos: %{x:.2f}%<extra></extra>",
        )
    )

    figura.add_trace(
        go.Bar(
            x=resumen["pct_valor"],
            y=resumen["modalidad_de_contratacion"].map(
                lambda x: abreviar_texto(x, 31)
            ),
            orientation="h",
            name="% Valor contratado",
            marker={"color": AZUL_CLARO},
            hovertemplate="%{y}<br>% valor: %{x:.2f}%<extra></extra>",
        )
    )

    configurar_figura(figura, altura=420)
    figura.update_layout(
        barmode="group",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "font": {"size": 10},
        },
        margin={"l": 10, "r": 20, "t": 35, "b": 45},
    )
    figura.update_xaxes(title="Participación (%)", ticksuffix="%")
    figura.update_yaxes(title=None)

    return figura


# ============================================================
# 10. CALLBACK TIPO DE CONTRATO
# ============================================================

@app.callback(
    Output("conc-grafico-tipo", "figure"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_tipo(anios, tipo, modalidad):
    conteo = aplicar_filtros(df_conteo, anios, tipo, modalidad)
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)

    if conteo.empty:
        return figura_vacia()

    resumen = resumen_categoria(
        conteo,
        valor,
        "tipo_de_contrato",
        max_categorias=7,
    )

    figura = go.Figure()

    figura.add_trace(
        go.Bar(
            x=resumen["pct_contratos"],
            y=resumen["tipo_de_contrato"].map(
                lambda x: abreviar_texto(x, 31)
            ),
            orientation="h",
            name="% Nº contratos",
            marker={"color": AZUL},
            hovertemplate="%{y}<br>% contratos: %{x:.2f}%<extra></extra>",
        )
    )

    figura.add_trace(
        go.Bar(
            x=resumen["pct_valor"],
            y=resumen["tipo_de_contrato"].map(
                lambda x: abreviar_texto(x, 31)
            ),
            orientation="h",
            name="% Valor contratado",
            marker={"color": AZUL_CLARO},
            hovertemplate="%{y}<br>% valor: %{x:.2f}%<extra></extra>",
        )
    )

    configurar_figura(figura, altura=420)
    figura.update_layout(
        barmode="group",
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "font": {"size": 10},
        },
        margin={"l": 10, "r": 20, "t": 35, "b": 45},
    )
    figura.update_xaxes(title="Participación (%)", ticksuffix="%")
    figura.update_yaxes(title=None)

    return figura


# ============================================================
# 11. CALLBACK EVOLUCIÓN CR5 Y CR10
# ============================================================

@app.callback(
    Output("conc-grafico-evolucion", "figure"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
)
def actualizar_evolucion(anios, tipo, modalidad):
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)

    # La comparación temporal principal utiliza años completos.
    valor = valor[
        valor["anio_firma"].between(2018, 2025, inclusive="both")
    ]

    if valor.empty:
        return figura_vacia(
            "No hay años completos 2018–2025 para los filtros seleccionados"
        )

    filas = []

    for anio, grupo in valor.groupby("anio_firma"):
        resumen = construir_resumen_proveedores(grupo)

        filas.append(
            {
                "anio": int(anio),
                "CR5": calcular_cr(resumen, 5),
                "CR10": calcular_cr(resumen, 10),
            }
        )

    evolucion = pd.DataFrame(filas).sort_values("anio")

    figura = go.Figure()

    figura.add_trace(
        go.Scatter(
            x=evolucion["anio"],
            y=evolucion["CR10"],
            mode="lines+markers",
            name="CR10",
            line={"color": AZUL, "width": 2.5},
            marker={"size": 7, "color": AZUL},
            hovertemplate="Año %{x}<br>CR10: %{y:.2f}%<extra></extra>",
        )
    )

    figura.add_trace(
        go.Scatter(
            x=evolucion["anio"],
            y=evolucion["CR5"],
            mode="lines+markers",
            name="CR5",
            line={"color": AZUL_CLARO, "width": 2.5},
            marker={"size": 7, "color": AZUL_CLARO},
            hovertemplate="Año %{x}<br>CR5: %{y:.2f}%<extra></extra>",
        )
    )

    configurar_figura(figura, altura=370)
    figura.update_layout(
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "x": 0,
            "font": {"size": 10},
        },
        hovermode="x unified",
        margin={"l": 55, "r": 25, "t": 30, "b": 45},
    )
    figura.update_xaxes(title="Año de firma", dtick=1)
    figura.update_yaxes(
        title="Concentración (%)",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        gridcolor="#E9EEF5",
    )

    return figura


# ============================================================
# 12. CALLBACK TABLA DE PROVEEDORES
# ============================================================

@app.callback(
    Output("conc-tabla-proveedores", "data"),
    Input("conc-filtro-anios", "value"),
    Input("conc-filtro-tipo", "value"),
    Input("conc-filtro-modalidad", "value"),
    Input("conc-buscar-proveedor", "value"),
)
def actualizar_tabla(anios, tipo, modalidad, busqueda):
    valor = aplicar_filtros(df_valor, anios, tipo, modalidad)
    resumen = construir_resumen_proveedores(valor)

    if resumen.empty:
        return []

    if busqueda:
        resumen = resumen[
            resumen["proveedor_etiqueta"]
            .astype(str)
            .str.contains(busqueda, case=False, na=False)
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
        columns={"proveedor_etiqueta": "proveedor"}
    )

    tabla["numero_contratos"] = tabla["numero_contratos"].map(formato_entero)
    tabla["valor_contratado"] = tabla["valor_contratado"].map(formato_monetario)
    tabla["participacion_pct"] = tabla["participacion_pct"].map(
        formato_porcentaje
    )
    tabla["participacion_acumulada_pct"] = tabla[
        "participacion_acumulada_pct"
    ].map(formato_porcentaje)

    return tabla.to_dict("records")


# ============================================================
# 13. EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
