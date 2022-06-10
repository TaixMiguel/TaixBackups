# TaixBackups
Proyecto web para generar backups y almacenarlos en local o en la nube ([Mega](https://mega.io/))


## Para hacer:
- [x] Lanzar un backup de forma manual
  - [x] Invocar backup desde la línea de comandos
  - [x] Generar backups desde la aplicación web
- [ ] Programar el backup para ejecución diaria o por un cron
- [ ] Almacenamiento del backup
  - [x] En local
  - [ ] En la nube de [Mega](https://mega.io/)
- [ ] Montar sensores MQTT para informar de los backups
  - [ ] Informar del último backup realizado (fecha-hora, nombre del backup y estado)
  - [ ] Informar del próximo backup (fecha-hora y nombre del backup)
- [ ] Montar la integración continua para el despliegue automático del proyecto
  - [ ] Definir un Dockerfile para poder generar una imagen con el proyecto web
    - [x] Definir un Dockerfile básico para ejecutar una app en modo dev
    - [ ] Definir un Dockerfile para ejecutar una app segura en un entorno de producción
  - [x] Generar una imagen docker (con etiqueta dev) para la rama dev
  - [ ] Generar una imagen docker (con etiqueta latest) para la rama main
  - [ ] Generar una imagen docker (con etiqueta versión) para la rama main


## Instalación de dependencias
En el proyecto se distribuye un fichero (requirements.txt) con todas las dependencias. Para instalarlas
basta con ejecutar:
> pip install -r requirements.txt

## Licencia
[GNU General Public License v3.0](https://github.com/TaixMiguel/TaixBackups/blob/main/LICENSE)
