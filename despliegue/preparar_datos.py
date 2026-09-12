"""Prepara los datos agregados que consume el tablero.

El tablero no lee la base analítica completa (25.605 registros, 11 MB): en una
instancia pequeña de EC2 eso encarece el arranque y el uso de memoria sin
aportar nada, porque todas las vistas son agregadas.

Este script parte de la base analítica de la Pregunta 2 y genera archivos
livianos que el tablero carga una sola vez al iniciar.

Uso:
    python preparar_datos.py
"""

from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
ORIGEN = BASE.parent / "Tarea 2" / "Pregunta 2" / "df_analitico_p2.csv"
DESTINO = BASE / "data"

# Los contratos con valores superiores a un billón de pesos fueron identificados
# durante la auditoría como registros que requieren validación de calidad de
# datos. Se excluyen de las agregaciones y la decisión queda documentada aquí.
UMBRAL_VALOR_ATIPICO = 1e12

# El geojson nombra los departamentos en mayúsculas y sin tildes, y usa una
# forma distinta para San Andrés y para Bogotá.
EQUIVALENCIA_GEOJSON = {
    "Amazonas": "AMAZONAS", "Antioquia": "ANTIOQUIA", "Arauca": "ARAUCA",
    "Atlántico": "ATLANTICO", "Bolívar": "BOLIVAR", "Boyacá": "BOYACA",
    "Caldas": "CALDAS", "Caquetá": "CAQUETA", "Casanare": "CASANARE",
    "Cauca": "CAUCA", "Cesar": "CESAR", "Chocó": "CHOCO", "Córdoba": "CORDOBA",
    "Cundinamarca": "CUNDINAMARCA", "Guainía": "GUAINIA", "Guaviare": "GUAVIARE",
    "Huila": "HUILA", "La Guajira": "LA GUAJIRA", "Magdalena": "MAGDALENA",
    "Meta": "META", "Nariño": "NARIÑO", "Norte de Santander": "NORTE DE SANTANDER",
    "Putumayo": "PUTUMAYO", "Quindío": "QUINDIO", "Risaralda": "RISARALDA",
    "San Andrés y Providencia": "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA",
    "Santander": "SANTANDER", "Sucre": "SUCRE", "Tolima": "TOLIMA",
    "Valle del Cauca": "VALLE DEL CAUCA", "Vaupés": "VAUPES", "Vichada": "VICHADA",
    "Bogotá D.C.": "SANTAFE DE BOGOTA D.C",
}


def cargar_base():
    df = pd.read_csv(ORIGEN, low_memory=False)
    df["fecha_de_firma"] = pd.to_datetime(df["fecha_de_firma"], errors="coerce", utc=True)
    df["anio_firma"] = df["fecha_de_firma"].dt.year
    return df[
        df["valor_del_contrato"].notna()
        & (df["valor_del_contrato"] > 0)
        & (df["valor_del_contrato"] < UMBRAL_VALOR_ATIPICO)
    ].copy()


def main():
    DESTINO.mkdir(exist_ok=True)
    df = cargar_base()
    print(f"Contratos con valor válido: {len(df):,}")

    # 1. Resumen de trazabilidad territorial
    resumen = df.groupby("trazabilidad_territorial").agg(
        contratos=("id_contrato", "size"), valor=("valor_del_contrato", "sum")
    ).reset_index()
    resumen["pct_contratos"] = (100 * resumen["contratos"] / resumen["contratos"].sum()).round(1)
    resumen["pct_valor"] = (100 * resumen["valor"] / resumen["valor"].sum()).round(1)
    resumen.to_csv(DESTINO / "resumen_trazabilidad.csv", index=False)

    # 2. Agregado por departamento (solo atribución inequívoca)
    unico = df[df["trazabilidad_territorial"] == "Departamento único"]
    deptos = unico.groupby("departamento_inferido").agg(
        contratos=("id_contrato", "size"),
        valor=("valor_del_contrato", "sum"),
        valor_mediano=("valor_del_contrato", "median"),
    ).reset_index().rename(columns={"departamento_inferido": "departamento"})
    deptos["pct_valor"] = (100 * deptos["valor"] / deptos["valor"].sum()).round(2)
    deptos["nombre_geojson"] = deptos["departamento"].map(EQUIVALENCIA_GEOJSON)
    sin_equivalencia = deptos[deptos["nombre_geojson"].isna()]["departamento"].tolist()
    if sin_equivalencia:
        raise ValueError(f"Departamentos sin equivalencia en el geojson: {sin_equivalencia}")
    deptos.sort_values("valor", ascending=False).to_csv(
        DESTINO / "departamentos.csv", index=False)

    # 3. Evolución anual por departamento
    evolucion = unico.groupby(["departamento_inferido", "anio_firma"]).agg(
        contratos=("id_contrato", "size"), valor=("valor_del_contrato", "sum")
    ).reset_index().rename(columns={"departamento_inferido": "departamento", "anio_firma": "anio"})
    evolucion.to_csv(DESTINO / "evolucion_departamento.csv", index=False)

    # 4. Trazabilidad territorial por año
    traza = df.groupby("anio_firma").apply(
        lambda g: pd.Series({
            "contratos": len(g),
            "valor": g["valor_del_contrato"].sum(),
            "pct_contratos_trazables": round(100 * g["es_territorializable"].mean(), 1),
            "pct_valor_trazable": round(
                100 * g.loc[g["es_territorializable"], "valor_del_contrato"].sum()
                / g["valor_del_contrato"].sum(), 1),
        }), include_groups=False
    ).reset_index().rename(columns={"anio_firma": "anio"})
    traza.to_csv(DESTINO / "trazabilidad_anual.csv", index=False)

    # 5. Departamento por tipo de contrato y por modalidad
    for columna, salida in [("tipo_de_contrato", "departamento_por_tipo.csv"),
                            ("modalidad_de_contratacion", "departamento_por_modalidad.csv")]:
        (unico.groupby(["departamento_inferido", columna])
              .agg(contratos=("id_contrato", "size"), valor=("valor_del_contrato", "sum"))
              .reset_index()
              .rename(columns={"departamento_inferido": "departamento"})
              .to_csv(DESTINO / salida, index=False))

    for archivo in sorted(DESTINO.glob("*.csv")):
        print(f"  {archivo.name:<34} {archivo.stat().st_size/1024:>7.1f} KB")


if __name__ == "__main__":
    main()
