"""Tablero de analítica de la contratación pública del INVIAS.

Producto de analítica del Proyecto 1 del curso Analítica Computacional para la
Toma de Decisiones. Responde las tres preguntas de negocio definidas por el
equipo a partir de los datos de SECOP II.

Usuario final: alta Dirección del INVIAS y organismos de control interno.

Ejecución local:
    python app.py
"""

from pathlib import Path

import dash
from dash import dcc, html
import pandas as pd

DATOS = Path(__file__).parent / "data"


# --------------------------------------------------------------------------
# Carga de datos
# --------------------------------------------------------------------------

def cargar_datos():
    """Carga los agregados que genera preparar_datos.py."""
    return {
        "resumen": pd.read_csv(DATOS / "resumen_trazabilidad.csv"),
        "departamentos": pd.read_csv(DATOS / "departamentos.csv"),
        "evolucion": pd.read_csv(DATOS / "evolucion_departamento.csv"),
        "trazabilidad": pd.read_csv(DATOS / "trazabilidad_anual.csv"),
    }


datos = cargar_datos()


# --------------------------------------------------------------------------
# Utilidades de formato
# --------------------------------------------------------------------------

def _separadores_es(texto):
    """Pasa un número con formato en inglés (1,234.5) a español (1.234,5)."""
    return texto.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def formato_pesos(valor):
    """Convierte un valor en pesos a una escala legible."""
    if valor >= 1e12:
        return "$" + _separadores_es(f"{valor / 1e12:,.1f}") + " billones"
    if valor >= 1e9:
        return "$" + _separadores_es(f"{valor / 1e9:,.0f}") + " mil millones"
    return "$" + _separadores_es(f"{valor / 1e6:,.0f}") + " millones"


def formato_entero(valor):
    return _separadores_es(f"{valor:,.0f}")


def indicador(valor, etiqueta):
    return html.Div(className="kpi", children=[
        html.Div(valor, className="valor"),
        html.Div(etiqueta, className="etiqueta"),
    ])


# --------------------------------------------------------------------------
# Secciones del tablero
# --------------------------------------------------------------------------

def encabezado():
    return html.Div(className="encabezado", children=[
        html.Div(className="contenedor", children=[
            html.H1("Contratación pública del INVIAS"),
            html.P(
                "Instituto Nacional de Vías · Datos de SECOP II con corte al 24 de agosto de 2026",
                className="entidad",
            ),
        ])
    ])


def indicadores_territoriales():
    """Indicadores de la Pregunta 2: cobertura territorial de la contratación."""
    resumen = datos["resumen"]
    total_contratos = resumen["contratos"].sum()
    total_valor = resumen["valor"].sum()

    trazables = resumen[resumen["trazabilidad_territorial"] != "No territorializable"]
    pct_valor_trazable = 100 * trazables["valor"].sum() / total_valor

    n_departamentos = datos["departamentos"]["departamento"].nunique()

    return html.Div(className="fila-kpi", children=[
        indicador(formato_entero(total_contratos), "Contratos con valor registrado"),
        indicador(formato_pesos(total_valor), "Valor total contratado"),
        indicador(f"{pct_valor_trazable:.1f} %", "Del valor puede ubicarse en el territorio"),
        indicador(formato_entero(n_departamentos), "Departamentos con contratación identificada"),
    ])


def modulo_territorial():
    """Pregunta 2 — Distribución territorial de los recursos."""
    return html.Div([
        html.Div(className="pregunta-negocio", children=[
            html.Strong("Pregunta de negocio. "),
            "¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el "
            "lugar de ejecución del contrato, ¿qué proporción de la contratación es "
            "territorialmente identificable a partir del objeto contractual, y cómo se "
            "distribuyen y evolucionan en el territorio los recursos que sí lo son?",
        ]),
        indicadores_territoriales(),
        html.Div(className="pendiente", children=[
            html.Strong("Mapa, ranking y evolución territorial"),
            html.Br(),
            "En construcción.",
        ]),
    ])


def modulo_pendiente(titulo, responsable, descripcion):
    return html.Div(className="pendiente", children=[
        html.Strong(titulo),
        html.Br(), html.Br(),
        descripcion,
        html.Br(), html.Br(),
        html.Span(f"Responsable: {responsable}", style={"fontSize": "13px"}),
    ])


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

app = dash.Dash(__name__, title="Contratación INVIAS")
server = app.server   # requerido por gunicorn en el despliegue

app.layout = html.Div([
    encabezado(),
    html.Div(className="contenedor", children=[
        dcc.Tabs(
            value="territorial",
            className="fila-pestanas",
            children=[
                dcc.Tab(
                    label="Concentración de la contratación",
                    value="concentracion",
                    className="pestana",
                    selected_className="pestana--activa",
                    children=html.Div(style={"paddingTop": "22px"}, children=[
                        modulo_pendiente(
                            "Concentración por proveedor, modalidad y tipo de contrato",
                            "Jhoiner Javier Ramos Ramírez",
                            "En qué proveedores, modalidades y tipos de contrato se concentra "
                            "la contratación del INVIAS.",
                        )
                    ]),
                ),
                dcc.Tab(
                    label="Distribución territorial",
                    value="territorial",
                    className="pestana",
                    selected_className="pestana--activa",
                    children=html.Div(style={"paddingTop": "22px"}, children=[
                        modulo_territorial()
                    ]),
                ),
                dcc.Tab(
                    label="Ejecución financiera",
                    value="ejecucion",
                    className="pestana",
                    selected_className="pestana--activa",
                    children=html.Div(style={"paddingTop": "22px"}, children=[
                        modulo_pendiente(
                            "Ejecución financiera y modificaciones contractuales",
                            "Edwin H. Calderón García",
                            "Cómo se comporta la ejecución financiera de los contratos y "
                            "cuáles requieren seguimiento.",
                        )
                    ]),
                ),
            ],
        ),
    ]),
    pie_pagina(),
])


if __name__ == "__main__":
    app.run(debug=True)
