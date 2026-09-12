"""Tablero de analítica de la contratación pública del INVIAS.

Producto de analítica del Proyecto 1 del curso Analítica Computacional para la
Toma de Decisiones. Responde las tres preguntas de negocio definidas por el
equipo a partir de los datos de SECOP II.

Usuario final: alta Dirección del INVIAS y organismos de control interno.

Cada pregunta vive en su propio módulo bajo `modulos/`, de modo que cada
integrante trabaje sobre el suyo sin bloquear a los demás.

Ejecución local:
    python app.py

Despliegue:
    gunicorn --bind 0.0.0.0:8050 --workers 2 app:server
"""

import dash
from dash import dcc, html

from modulos import ejecucion, territorial

# --------------------------------------------------------------------------
# Definición de las pestañas
# --------------------------------------------------------------------------

PREGUNTAS = [
    {
        "id": "concentracion",
        "etiqueta": "Concentración de la contratación",
        "responsable": "Jhoiner Javier Ramos Ramírez",
        "descripcion": "En qué proveedores, modalidades y tipos de contrato se "
                       "concentra la contratación del INVIAS.",
        "contenido": None,
    },
    {
        "id": "territorial",
        "etiqueta": "Distribución territorial",
        "responsable": "Cristian Camilo Rodríguez Cagueñas",
        "descripcion": "Dónde ejecuta INVIAS sus recursos.",
        "contenido": territorial.layout,
    },
    {
        "id": "ejecucion",
        "etiqueta": "Ejecución financiera",
        "responsable": "Edwin H. Calderón García",
        "descripcion": "Cómo se comporta la ejecución financiera de los contratos "
                       "y cuáles requieren seguimiento.",
        "contenido": ejecucion.layout,
    },
]


# --------------------------------------------------------------------------
# Secciones comunes
# --------------------------------------------------------------------------

def encabezado():
    return html.Div(className="encabezado", children=[
        html.Div(className="contenedor", children=[
            html.H1("Contratación pública del INVIAS"),
            html.P(
                "Instituto Nacional de Vías · Datos de SECOP II con corte al "
                "24 de agosto de 2026",
                className="entidad",
            ),
        ])
    ])


def modulo_pendiente(pregunta):
    """Marcador para las pestañas cuyo módulo aún no se ha integrado."""
    return html.Div(className="pendiente", children=[
        html.Strong(pregunta["etiqueta"]),
        html.Br(), html.Br(),
        pregunta["descripcion"],
        html.Br(), html.Br(),
        html.Span(f"Responsable: {pregunta['responsable']}", style={"fontSize": "13px"}),
    ])


def pestana(pregunta):
    contenido = pregunta["contenido"]
    if contenido is None:
        contenido = modulo_pendiente(pregunta)
    return dcc.Tab(
        label=pregunta["etiqueta"],
        value=pregunta["id"],
        className="pestana",
        selected_className="pestana--activa",
        children=html.Div(style={"paddingTop": "22px"}, children=[contenido]),
    )


def pie_pagina():
    return html.Div(className="contenedor", children=[
        html.Div(className="pie", children=[
            "Proyecto 1 — Analítica Computacional para la Toma de Decisiones · "
            "Universidad de los Andes",
            html.Br(),
            "Fuente: SECOP II — Contratos Electrónicos, Datos Abiertos de Colombia.",
        ])
    ])


# --------------------------------------------------------------------------
# Aplicación
# --------------------------------------------------------------------------

app = dash.Dash(__name__, title="Contratación INVIAS", suppress_callback_exceptions=True)
server = app.server   # requerido por gunicorn en el despliegue

app.layout = html.Div([
    encabezado(),
    html.Div(className="contenedor", children=[
        dcc.Tabs(
            value="territorial",
            children=[pestana(p) for p in PREGUNTAS],
        ),
    ]),
    pie_pagina(),
])


if __name__ == "__main__":
    app.run(debug=True)
