# Capturas del despliegue (Soporte 5)

El enunciado pide *"snapshots de los recursos lanzados para el despliegue (AWS y terminal), y URL del tablero en ejecución"*. Estas son las que hay que dejar en esta carpeta.

| Archivo | Qué debe mostrar |
|---|---|
| `01_instancia_ec2.png` | Consola de EC2 con la instancia en estado *running*: tipo, región, IP pública. |
| `02_security_group.png` | Reglas de entrada del security group, con el puerto 8050 abierto. |
| `03_terminal_clone.png` | Terminal SSH con el `git clone` y la instalación de dependencias. |
| `04_terminal_gunicorn.png` | Terminal con gunicorn levantado y escuchando en 0.0.0.0:8050. |
| `05_tablero_navegador.png` | El tablero abierto en el navegador, con la **URL pública visible en la barra de direcciones**. |
| `06_tablero_pestanas.png` | Las tres pestañas del tablero funcionando en la instancia desplegada. |

La captura 05 es la que vale doble: es a la vez la evidencia del despliegue y la URL del tablero en ejecución, así que la barra de direcciones tiene que leerse.
