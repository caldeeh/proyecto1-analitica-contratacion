"""Pregunta 2 — Distribución territorial de los recursos.

Autor: Cristian Camilo Rodríguez Cagueñas

¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el lugar de
ejecución del contrato, ¿qué proporción de la contratación es territorialmente
identificable a partir del objeto contractual, y cómo se distribuyen y
evolucionan en el territorio los recursos que sí lo son?

El módulo lee `data/territorial_detalle.csv`, una tabla agregada por año,
trazabilidad, departamento, tipo y modalidad. Los filtros recalculan sobre esa
tabla en memoria, sin tocar la base analítica completa.

Todos los identificadores llevan el prefijo `terr-` para no chocar con los de
los demás módulos del tablero.
"""

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dcc, html

DATOS = Path(__file__).resolve().parent.parent / "data"

# Paleta validada para daltonismo; los colores se usan siempre en este orden.
AZUL = "#2a78d6"
NARANJA = "#eb6834"
GRIS = "#898781"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
LINEA = "#e1e0d9"
ESCALA_AZUL = [
    [0.0, "#e8f1fc"], [0.25, "#9ec5f4"], [0.5, "#5598e7"],
    [0.75, "#256abf"], [1.0, "#104281"],
]


# --------------------------------------------------------------------------
# Datos
# --------------------------------------------------------------------------

detalle = pd.read_csv(DATOS / "territorial_detalle.csv")

# 2.374 contratos no tienen fecha de firma registrada. No se descartan: aportan
# $5,87 billones y su exclusión desplazaría los indicadores respecto de las
# cifras del informe. No pueden ubicarse en el tiempo, así que quedan fuera de
# las series anuales y el usuario decide si entran en el resto mediante un
# control explícito.
CON_FECHA = detalle["anio"].notna()
SIN_FECHA_CONTRATOS = int(detalle.loc[~CON_FECHA, "contratos"].sum())

with open(DATOS / "departamentos_colombia.geojson", encoding="utf-8") as f:
    GEOJSON = json.load(f)

ANIO_MIN, ANIO_MAX = int(detalle["anio"].min()), int(detalle["anio"].max())
TIPOS = sorted(detalle["tipo"].dropna().unique())
MODALIDADES = sorted(detalle["modalidad"].dropna().unique())


# --------------------------------------------------------------------------
# Formato
# --------------------------------------------------------------------------

def _es(texto):
    """Pasa un número con formato en inglés (1,234.5) a español (1.234,5)."""
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def pesos(valor):
    if valor >= 1e12:
        return "$" + _es(f"{valor / 1e12:,.1f}") + " billones"
    if valor >= 1e9:
        return "$" + _es(f"{valor / 1e9:,.0f}") + " mil millones"
    return "$" + _es(f"{valor / 1e6:,.0f}") + " millones"


def entero(valor):
    return _es(f"{valor:,.0f}")


def filtrar(anios, tipos, modalidades, sin_fecha=None, solo_con_fecha=False):
    """Aplica los filtros del usuario sobre la tabla de detalle.

    `sin_fecha` es el valor del control que decide si los contratos sin fecha
    de firma entran en el cálculo. `solo_con_fecha` lo usan las series anuales,
    que por definición no pueden incluirlos.
    """
    en_rango = detalle["anio"].between(anios[0], anios[1])
    if solo_con_fecha:
        d = detalle[en_rango]
    else:
        incluir = bool(sin_fecha)
        d = detalle[en_rango | (~CON_FECHA & incluir)]
    if tipos:
        d = d[d["tipo"].isin(tipos)]
    if modalidades:
        d = d[d["modalidad"].isin(modalidades)]
    return d


def _figura_vacia(mensaje="Sin datos para los filtros seleccionados"):
    figura = go.Figure()
    figura.add_annotation(text=mensaje, showarrow=False,
                          font=dict(size=13, color=GRIS))
    figura.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False),
                         plot_bgcolor="white", paper_bgcolor="white",
                         margin=dict(l=10, r=10, t=10, b=10))
    return figura


DISENO_BASE = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="-apple-system, Segoe UI, Roboto, sans-serif",
              size=12, color=TINTA_2),
    margin=dict(l=10, r=10, t=30, b=10),
    hoverlabel=dict(bgcolor="white", font_size=12, bordercolor=LINEA),
)


# --------------------------------------------------------------------------
# Componentes
# --------------------------------------------------------------------------

def _indicador(id_valor, etiqueta):
    return html.Div(className="kpi", children=[
        html.Div(id=id_valor, className="valor"),
        html.Div(etiqueta, className="etiqueta"),
    ])


def _filtros():
    return html.Div(className="tarjeta", children=[
        html.H2("Filtros"),
        html.Div(style={"display": "flex", "gap": "22px", "flexWrap": "wrap",
                        "alignItems": "flex-end"}, children=[
            html.Div(style={"flex": "2 1 340px"}, children=[
                html.Label("Año de firma", style={"fontSize": "12px", "color": TINTA_2}),
                dcc.RangeSlider(
                    # Por defecto todo el periodo, para que los indicadores
                    # coincidan con las cifras del informe.
                    id="terr-anios", min=ANIO_MIN, max=ANIO_MAX, step=1,
                    value=[ANIO_MIN, ANIO_MAX],
                    marks={a: str(a) for a in range(ANIO_MIN, ANIO_MAX + 1)},
                    tooltip={"placement": "bottom"},
                ),
            ]),
            html.Div(style={"flex": "1 1 240px"}, children=[
                html.Label("Tipo de contrato", style={"fontSize": "12px", "color": TINTA_2}),
                dcc.Dropdown(id="terr-tipo", options=TIPOS, multi=True,
                             placeholder="Todos"),
            ]),
            html.Div(style={"flex": "1 1 240px"}, children=[
                html.Label("Modalidad", style={"fontSize": "12px", "color": TINTA_2}),
                dcc.Dropdown(id="terr-modalidad", options=MODALIDADES, multi=True,
                             placeholder="Todas"),
            ]),
        ]),
        dcc.Checklist(
            id="terr-sin-fecha",
            options=[{"label": f"  Incluir los {SIN_FECHA_CONTRATOS:,} contratos sin fecha "
                               "de firma registrada".replace(",", "."),
                      "value": "si"}],
            value=["si"],
            style={"marginTop": "14px", "fontSize": "12.5px", "color": TINTA_2},
        ),
    ])


layout = html.Div([
    html.Div(className="pregunta-negocio", children=[
        html.Strong("Pregunta de negocio. "),
        "¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el "
        "lugar de ejecución del contrato, ¿qué proporción de la contratación es "
        "territorialmente identificable a partir del objeto contractual, y cómo se "
        "distribuyen y evolucionan en el territorio los recursos que sí lo son?",
    ]),

    html.Div(className="fila-kpi", children=[
        _indicador("terr-kpi-contratos", "Contratos con valor registrado"),
        _indicador("terr-kpi-valor", "Valor total contratado"),
        _indicador("terr-kpi-trazable", "Del valor puede ubicarse en el territorio"),
        _indicador("terr-kpi-deptos", "Departamentos con contratación identificada"),
    ]),

    _filtros(),

    html.Div(className="rejilla-dos", children=[
        html.Div(className="tarjeta", children=[
            html.H2("Dónde se ejecutan los recursos"),
            html.P("Valor contratado por departamento inferido del objeto contractual. "
                   "Solo contratos con un departamento identificable.", className="nota"),
            dcc.Graph(id="terr-mapa", config={"displayModeBar": False},
                      style={"height": "460px"}),
        ]),
        html.Div(className="tarjeta", children=[
            html.H2("Departamentos por valor contratado"),
            html.P("Los quince con mayor valor. Pase el cursor para ver el número de "
                   "contratos.", className="nota"),
            dcc.Graph(id="terr-ranking", config={"displayModeBar": False},
                      style={"height": "460px"}),
        ]),
    ]),

    html.Div(className="tarjeta", children=[
        html.H2("Trazabilidad territorial en el tiempo"),
        html.P("Proporción de la contratación que puede ubicarse en el territorio, "
               "por año de firma. La brecha entre las dos líneas muestra que los "
               "contratos sin territorio son numerosos pero de bajo monto. Excluye los contratos sin fecha de firma, que no pueden ubicarse en el tiempo.",
               className="nota"),
        dcc.Graph(id="terr-trazabilidad", config={"displayModeBar": False},
                  style={"height": "330px"}),
    ]),

    html.Div(className="tarjeta", children=[
        html.H2("Evolución por departamento"),
        html.P("Valor contratado por año en los seis departamentos principales del "
               "periodo seleccionado.", className="nota"),
        dcc.Graph(id="terr-evolucion", config={"displayModeBar": False},
                  style={"height": "360px"}),
    ]),
])


# --------------------------------------------------------------------------
# Callbacks
# --------------------------------------------------------------------------

ENTRADAS = [Input("terr-anios", "value"), Input("terr-tipo", "value"),
            Input("terr-modalidad", "value"), Input("terr-sin-fecha", "value")]


@callback(
    Output("terr-kpi-contratos", "children"),
    Output("terr-kpi-valor", "children"),
    Output("terr-kpi-trazable", "children"),
    Output("terr-kpi-deptos", "children"),
    *ENTRADAS,
)
def actualizar_indicadores(anios, tipos, modalidades, sin_fecha):
    d = filtrar(anios, tipos, modalidades, sin_fecha)
    if d.empty:
        return "—", "—", "—", "—"

    total_valor = d["valor"].sum()
    trazable = d[d["trazabilidad"] != "No territorializable"]["valor"].sum()
    pct = 100 * trazable / total_valor if total_valor else 0
    n_deptos = d.loc[d["trazabilidad"] == "Departamento único", "departamento"].nunique()

    return entero(d["contratos"].sum()), pesos(total_valor), f"{pct:.1f} %", entero(n_deptos)


def _por_departamento(d):
    unico = d[d["trazabilidad"] == "Departamento único"]
    if unico.empty:
        return pd.DataFrame(columns=["departamento", "contratos", "valor", "nombre_geojson"])
    return (unico.groupby(["departamento", "nombre_geojson"], as_index=False)
                 .agg(contratos=("contratos", "sum"), valor=("valor", "sum"))
                 .sort_values("valor", ascending=False))


@callback(Output("terr-mapa", "figure"), *ENTRADAS)
def actualizar_mapa(anios, tipos, modalidades, sin_fecha):
    deptos = _por_departamento(filtrar(anios, tipos, modalidades, sin_fecha))
    if deptos.empty:
        return _figura_vacia()

    # Se usa Choroplethmapbox con estilo "white-bg" y sin capas de teselas: el
    # mapa se dibuja solo con el geojson local. Choropleth (el de proyección
    # geográfica) descarga un topojson de cdn.plot.ly al renderizar, y eso
    # rompería el mapa en una instancia de EC2 sin salida a internet.
    figura = go.Figure(go.Choroplethmapbox(
        geojson=GEOJSON,
        locations=deptos["nombre_geojson"],
        z=deptos["valor"] / 1e9,
        featureidkey="properties.NOMBRE_DPT",
        colorscale=ESCALA_AZUL,
        marker_line_color="white",
        marker_line_width=0.6,
        colorbar=dict(title=dict(text="Miles de<br>millones", font=dict(size=11)),
                      thickness=12, len=0.7, outlinewidth=0),
        customdata=deptos[["departamento", "contratos"]],
        hovertemplate="<b>%{customdata[0]}</b><br>"
                      "$%{z:,.0f} mil millones<br>"
                      "%{customdata[1]:,.0f} contratos<extra></extra>",
    ))
    figura.update_layout(
        **DISENO_BASE,
        mapbox=dict(style="white-bg", center=dict(lat=4.3, lon=-73.5), zoom=3.9),
    )
    return figura


@callback(Output("terr-ranking", "figure"), *ENTRADAS)
def actualizar_ranking(anios, tipos, modalidades, sin_fecha):
    deptos = _por_departamento(filtrar(anios, tipos, modalidades, sin_fecha))
    if deptos.empty:
        return _figura_vacia()

    top = deptos.head(15).iloc[::-1]
    figura = go.Figure(go.Bar(
        x=top["valor"] / 1e9, y=top["departamento"], orientation="h",
        marker=dict(color=AZUL, line=dict(width=0)),
        customdata=top[["contratos"]],
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f} mil millones<br>"
                      "%{customdata[0]:,.0f} contratos<extra></extra>",
    ))
    figura.update_layout(
        **DISENO_BASE,
        xaxis=dict(title="Miles de millones de pesos", gridcolor=LINEA,
                   zeroline=False),
        yaxis=dict(title=None, tickfont=dict(size=11)),
        bargap=0.32,
    )
    return figura


@callback(Output("terr-trazabilidad", "figure"), *ENTRADAS)
def actualizar_trazabilidad(anios, tipos, modalidades, sin_fecha):
    d = filtrar(anios, tipos, modalidades, solo_con_fecha=True)
    if d.empty:
        return _figura_vacia()

    d = d.assign(trazable=d["trazabilidad"] != "No territorializable")
    serie = d.groupby("anio").apply(
        lambda g: pd.Series({
            "pct_valor": 100 * g.loc[g["trazable"], "valor"].sum() / g["valor"].sum()
            if g["valor"].sum() else 0,
            "pct_contratos": 100 * g.loc[g["trazable"], "contratos"].sum()
            / g["contratos"].sum() if g["contratos"].sum() else 0,
        }), include_groups=False
    ).reset_index()

    figura = go.Figure()
    for columna, color, nombre in [("pct_valor", AZUL, "% del valor"),
                                   ("pct_contratos", NARANJA, "% de contratos")]:
        figura.add_trace(go.Scatter(
            x=serie["anio"], y=serie[columna], name=nombre, mode="lines+markers",
            line=dict(color=color, width=2), marker=dict(size=7),
            hovertemplate=f"<b>%{{x}}</b><br>{nombre}: %{{y:.1f}} %<extra></extra>",
        ))

    figura.update_layout(
        **DISENO_BASE,
        xaxis=dict(title="Año de firma", gridcolor=LINEA, dtick=1),
        yaxis=dict(title="Territorialmente identificable (%)", gridcolor=LINEA,
                   range=[0, 100]),
        legend=dict(orientation="h", y=1.13, x=0, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    return figura


@callback(Output("terr-evolucion", "figure"), *ENTRADAS)
def actualizar_evolucion(anios, tipos, modalidades, sin_fecha):
    d = filtrar(anios, tipos, modalidades, solo_con_fecha=True)
    unico = d[d["trazabilidad"] == "Departamento único"]
    if unico.empty:
        return _figura_vacia()

    principales = (unico.groupby("departamento")["valor"].sum()
                        .nlargest(6).index.tolist())
    serie = (unico[unico["departamento"].isin(principales)]
             .groupby(["anio", "departamento"])["valor"].sum()
             .unstack(fill_value=0) / 1e9)

    colores = [AZUL, NARANJA, "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"]
    figura = go.Figure()
    for departamento, color in zip(principales, colores):
        if departamento not in serie.columns:
            continue
        figura.add_trace(go.Scatter(
            x=serie.index, y=serie[departamento], name=departamento,
            mode="lines", stackgroup="uno", line=dict(width=0.5, color=color),
            fillcolor=color,
            hovertemplate=f"<b>{departamento}</b><br>%{{x}}: "
                          "$%{y:,.0f} mil millones<extra></extra>",
        ))

    figura.update_layout(
        **DISENO_BASE,
        xaxis=dict(title="Año de firma", gridcolor=LINEA, dtick=1),
        yaxis=dict(title="Miles de millones de pesos", gridcolor=LINEA),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    )
    return figura
