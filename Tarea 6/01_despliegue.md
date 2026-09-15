# Tarea 6. Despliegue y mantenimiento

**Rol involucrado:** Despliegue y mantenimiento.  
**Responsable:** Jhoiner Javier Ramos Ramírez

Esta carpeta contiene el soporte del despliegue del tablero, incluyendo la configuración de la instancia EC2, el procedimiento seguido, la URL pública de acceso y las evidencias solicitadas.

El código del tablero se encuentra en la carpeta `despliegue/` ubicada en la raíz del repositorio.

---

## 1. URL del tablero en ejecución

El tablero se encuentra desplegado en una instancia de Amazon EC2 y puede consultarse en:

```text
http://13.219.17.0:8050/
```

---

## 2. Configuración de la instancia

| Elemento | Valor |
|---|---|
| Proveedor de nube | AWS Academy Learner Lab |
| Servicio | Amazon EC2 |
| Nombre de la instancia | `tableroproyecto` |
| Instance ID | `i-0fc1ed24b69b25996` |
| Región | `us-east-1` — US East (N. Virginia) |
| Tipo de instancia | `t3.micro` |
| AMI / sistema operativo | Amazon Linux 2023 |
| Plataforma | Linux/UNIX |
| IP pública / Elastic IP | `13.219.17.0` |
| IP privada | `172.31.19.220` |
| Public DNS | `ec2-13-219-17-0.compute-1.amazonaws.com` |
| Key pair | `tablero` |
| Puerto del tablero | `8050` |

---

## 3. Procedimiento de despliegue

### 3.1. Preparación de la instancia

La instancia utilizada corresponde a Amazon Linux 2023.

Se actualizan los paquetes del sistema:

```bash
sudo yum update -y
```

En caso de ser necesario, se instalan Python, `pip` y Git:

```bash
sudo yum install -y python3-pip git
```

Se verifican las instalaciones:

```bash
python3 --version
pip3 --version
git --version
```

### 3.2. Clonación del repositorio

Se clona el repositorio del proyecto desde GitHub:

```bash
git clone https://github.com/caldeeh/proyecto1-analitica-contratacion.git
```

Posteriormente se ingresa al proyecto:

```bash
cd proyecto1-analitica-contratacion
```

### 3.3. Instalación de dependencias

Se instalan las dependencias definidas para el despliegue:

```bash
pip3 install -r despliegue/requirements.txt
```

La aplicación integra los tres módulos correspondientes a las preguntas de negocio:

```text
concentracion.py
territorial.py
ejecucion.py
```

### 3.4. Ejecución del tablero

Se ingresa a la carpeta de despliegue:

```bash
cd despliegue
```

El tablero puede ejecutarse mediante Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8050 app:server
```

Para mantenerlo ejecutándose después de cerrar la sesión SSH:

```bash
nohup gunicorn --bind 0.0.0.0:8050 app:server > tablero.log 2>&1 &
```

El Security Group de la instancia debe permitir tráfico entrante TCP por el puerto `8050`.

---

## 4. Verificación

Para verificar que Gunicorn se encuentre activo:

```bash
ps aux | grep gunicorn
```

También se puede comprobar la respuesta de la aplicación directamente desde la instancia:

```bash
curl -I http://127.0.0.1:8050
```

Una respuesta correcta debe incluir:

```text
HTTP/1.1 200 OK
```

El tablero debe poder abrirse desde un navegador externo mediante:

```text
http://13.219.17.0:8050/
```

Antes de dar por finalizado el despliegue se verifica:

- [x] La instancia EC2 se encuentra en estado `Running`.
- [x] La instancia cuenta con una IP pública asociada.
- [x] El tablero es accesible mediante la IP pública y el puerto `8050`.
- [ ] Las tres pestañas del tablero cargan correctamente.
- [ ] Los filtros de cada pestaña responden.
- [ ] Las visualizaciones se actualizan correctamente.
- [ ] El proceso continúa funcionando después de cerrar la sesión SSH.

---

## 5. Mantenimiento

Para actualizar el tablero después de realizar cambios en el repositorio:

```bash
cd ~/proyecto1-analitica-contratacion
git pull origin main
```

Si se modificaron las dependencias:

```bash
pip3 install -r despliegue/requirements.txt
```

Posteriormente se reinicia Gunicorn:

```bash
pkill -f gunicorn
cd despliegue
nohup gunicorn --bind 0.0.0.0:8050 app:server > tablero.log 2>&1 &
```

Para revisar posibles errores:

```bash
tail -n 50 tablero.log
```

---

## 6. Evidencias

Las capturas correspondientes al despliegue deben almacenarse en la subcarpeta `capturas/`.

Se recomienda incluir:

1. Instancia EC2 `tableroproyecto` en estado **Running**.
2. Región `us-east-1` — N. Virginia.
3. Tipo de instancia `t3.micro`.
4. IP pública / Elastic IP `13.219.17.0`.
5. Configuración del Security Group y puerto `8050`.
6. Terminal con Gunicorn en ejecución.
7. Respuesta `HTTP/1.1 200 OK`.
8. Tablero abierto desde `http://13.219.17.0:8050/`.
9. Evidencia de las tres pestañas del tablero.