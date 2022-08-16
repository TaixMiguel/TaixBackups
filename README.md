# TaixBackups
Proyecto web para generar backups y almacenarlos en local o en la nube ([Mega](https://mega.io/))


## Para hacer:
- [x] Lanzar un backup de forma manual
  - [x] Invocar backup desde la línea de comandos
  - [x] Generar backups desde la aplicación web
- [ ] Programar el backup para ejecución diaria o por un cron
- [x] Almacenamiento del backup
  - [x] En local
  - [x] En la nube de [Mega](https://mega.io/)
- [ ] Montar sensores MQTT para informar de los backups
  - [x] Informar del último backup realizado (fecha-hora, nombre del backup ~~y estado~~)
  - [ ] Informar del estado del último backup realizado (de forma individual) (fecha-hora, nombre del backup y estado)
  - [ ] Informar del próximo backup (fecha-hora y nombre del backup)
- [ ] Montar la integración continua para el despliegue automático del proyecto
  - [ ] Definir un Dockerfile para poder generar una imagen con el proyecto web
    - [x] Definir un Dockerfile básico para ejecutar una app en modo dev
    - [ ] Definir un Dockerfile para ejecutar una app segura en un entorno de producción
  - [x] Generar una imagen docker (con etiqueta dev) para la rama dev
  - [x] Generar una imagen docker (con etiqueta latest) para la rama main
  - [x] Generar una imagen docker (con etiqueta versión) para la rama main


## Instalación de dependencias
En el proyecto se distribuye un fichero (requirements.txt) con todas las dependencias. Para instalarlas
basta con ejecutar:
> pip install -r requirements.txt


## Configuración personalizada
Se puede personalizar la configuración creando una carpeta hermana a `config` llamada `instance` y dentro
de ella crear un fichero llamado `config.py` con las variables de configuración que queremos sobreescribir.

Fichero de ejemplo:
```python
import logging

APP_ENV = 'development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database2.db'

# Logger
LOG_LEVEL = logging.DEBUG
LOG_FILE = 'taixBackups'
LOG_DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

# MQTT
MQTT_SERVER = ''
MQTT_USER = ''
MQTT_PASS = ''
```


## Licencia
[GNU General Public License v3.0](https://github.com/TaixMiguel/TaixBackups/blob/main/LICENSE)
