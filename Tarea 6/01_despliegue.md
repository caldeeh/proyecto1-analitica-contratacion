# Tarea 6. Despliegue y mantenimiento

**Rol involucrado:** Despliegue y mantenimiento.
**Responsable:** Jhoiner Javier Ramos Ramírez

Esta carpeta es el soporte del despliegue: el procedimiento seguido, la URL del tablero en ejecución y las evidencias que pide el enunciado (**Soporte 5**).

El código del tablero no va aquí. Vive en la carpeta `despliegue/` en la raíz del repositorio, que es la que se clona en la instancia.

---

## 1. URL del tablero en ejecución

> PENDIENTE — Javier: reemplazar por la URL real.

```
http://<IP-PUBLICA-EC2>:8050
```

## 2. Configuración de la instancia

> PENDIENTE — Javier: completar con los valores reales del despliegue.

| Elemento | Valor |
|---|---|
| Región | |
| Tipo de instancia | |
| AMI / sistema operativo | |
| Almacenamiento | |
| Security group | |
| Puerto expuesto | 8050 |
| IP pública | |

## 3. Procedimiento de despliegue

Los pasos están probados en local y documentados en `despliegue/README.md`. Este es el resumen de lo que se ejecuta en la instancia:

```bash
# 1. Dependencias del sistema
sudo apt update && sudo apt install -y python3-pip git

# 2. Clonar el repositorio
git clone https://github.com/caldeeh/proyecto1-analitica-contratacion.git
cd proyecto1-analitica-contratacion/despliegue

# 3. Dependencias de Python
pip3 install -r requirements.txt

# 4. Levantar el tablero con gunicorn
gunicorn --bind 0.0.0.0:8050 --workers 2 app:server
```

Para que siga corriendo al cerrar la sesión SSH:

```bash
nohup gunicorn --bind 0.0.0.0:8050 --workers 2 app:server > tablero.log 2>&1 &
```

El security group debe permitir tráfico entrante TCP en el puerto 8050.

## 4. Verificación

Antes de dar el despliegue por terminado:

- [ ] El tablero abre desde un navegador fuera de la instancia, con la IP pública.
- [ ] Las tres pestañas cargan (Pregunta 1, Pregunta 2, Pregunta 3).
- [ ] Los filtros de cada pestaña responden y los gráficos se actualizan.
- [ ] El mapa de la Pregunta 2 se dibuja. Si aparece en blanco, es que está intentando descargar geometría de internet: se usa `Choroplethmapbox` con fondo plano justamente para evitarlo.
- [ ] El proceso sobrevive al cierre de la sesión SSH.
- [ ] La URL sigue respondiendo al día siguiente.

## 5. Mantenimiento

Para publicar cambios en el tablero:

```bash
cd ~/proyecto1-analitica-contratacion
git pull
cd despliegue
# si cambiaron los datos base
python3 preparar_datos.py
# reiniciar
pkill gunicorn
nohup gunicorn --bind 0.0.0.0:8050 --workers 2 app:server > tablero.log 2>&1 &
```

Si el tablero deja de responder, `tablero.log` tiene la traza del error.

## 6. Evidencias

Las capturas van en la subcarpeta `capturas/`. Ver el archivo `capturas/README.md` para la lista de las que pide el enunciado.
