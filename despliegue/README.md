# Tablero — Analítica de contratación pública del INVIAS

Tablero en Dash que responde las tres preguntas de negocio del proyecto sobre la
contratación del Instituto Nacional de Vías (INVIAS), a partir de los datos de
SECOP II.

## Estructura

```
despliegue/
├── app.py                  Aplicación Dash
├── preparar_datos.py       Genera los agregados que consume el tablero
├── requirements.txt
├── assets/
│   └── estilos.css         Hoja de estilos (Dash la carga automáticamente)
└── data/
    ├── departamentos.csv
    ├── evolucion_departamento.csv
    ├── trazabilidad_anual.csv
    ├── resumen_trazabilidad.csv
    ├── departamento_por_tipo.csv
    ├── departamento_por_modalidad.csv
    └── departamentos_colombia.geojson
```

## Por qué datos agregados y no la base completa

La base analítica tiene 25.605 registros y pesa 11 MB. Todas las vistas del
tablero son agregadas, así que cargarla completa solo encarece el arranque y la
memoria en una instancia pequeña de EC2. `preparar_datos.py` genera los archivos
que el tablero necesita, que juntos pesan menos de 250 KB.

Para regenerarlos después de cambiar la base analítica:

```bash
python preparar_datos.py
```

## Ejecución local

```bash
pip install -r requirements.txt
python app.py
```

Queda disponible en http://127.0.0.1:8050

## Despliegue en AWS EC2

```bash
# En la instancia
sudo apt update && sudo apt install -y python3-pip
git clone https://github.com/caldeeh/proyecto1-analitica-contratacion.git
cd proyecto1-analitica-contratacion/despliegue
pip3 install -r requirements.txt

# Servidor de producción
gunicorn --bind 0.0.0.0:8050 --workers 2 app:server
```

El security group de la instancia debe permitir tráfico entrante en el puerto
8050.

Para que el tablero siga corriendo al cerrar la sesión SSH:

```bash
nohup gunicorn --bind 0.0.0.0:8050 --workers 2 app:server > tablero.log 2>&1 &
```
