"""Pregunta 2 — Distribución territorial de los recursos.

Autor: Cristian Camilo Rodríguez Cagueñas

¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el lugar de
ejecución del contrato, ¿qué proporción de la contratación es territorialmente
identificable a partir del objeto contractual, y cómo se distribuyen y
evolucionan en el territorio los recursos que sí lo son?
"""

from pathlib import Path

from dash import html
import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "data"


# --------------------------------------------------------------------------
# Datos
# --------------------------------------------------------------------------

resumen = pd.read_csv(DATOS / "resumen_trazabilidad.csv")
departamentos = pd.read_csv(DATOS / "departamentos.csv")
evolucion = pd.read_csv(DATOS / "evolucion_departamento.csv")
trazabilidad = pd.read_csv(DATOS / "trazabilidad_anual.csv")


# --------------------------------------------------------------------------
# Formato
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


# --------------------------------------------------------------------------
# Componentes
# --------------------------------------------------------------------------

def _indicador(valor, etiqueta):
    return html.Div(className="kpi", children=[
        html.Div(valor, className="valor"),
        html.Div(etiqueta, className="etiqueta"),
    ])


def _indicadores():
    """Cobertura territorial de la contratación."""
    total_contratos = resumen["contratos"].sum()
    total_valor = resumen["valor"].sum()

    trazables = resumen[resumen["trazabilidad_territorial"] != "No territorializable"]
    pct_valor_trazable = 100 * trazables["valor"].sum() / total_valor

    return html.Div(className="fila-kpi", children=[
        _indicador(formato_entero(total_contratos), "Contratos con valor registrado"),
        _indicador(formato_pesos(total_valor), "Valor total contratado"),
        _indicador(f"{pct_valor_trazable:.1f} %", "Del valor puede ubicarse en el territorio"),
        _indicador(formato_entero(departamentos["departamento"].nunique()),
                   "Departamentos con contratación identificada"),
    ])


# --------------------------------------------------------------------------
# Contenido de la pestaña
# --------------------------------------------------------------------------

layout = html.Div([
    html.Div(className="pregunta-negocio", children=[
        html.Strong("Pregunta de negocio. "),
        "¿Dónde ejecuta INVIAS sus recursos? Dado que el SECOP II no registra el "
        "lugar de ejecución del contrato, ¿qué proporción de la contratación es "
        "territorialmente identificable a partir del objeto contractual, y cómo se "
        "distribuyen y evolucionan en el territorio los recursos que sí lo son?",
    ]),
    _indicadores(),
    html.Div(className="pendiente", children=[
        html.Strong("Mapa, ranking y evolución territorial"),
        html.Br(),
        "En construcción.",
    ]),
])
