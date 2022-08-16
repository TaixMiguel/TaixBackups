# Changelog
Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Sin versión]
### Añadido
- Archivo entrypoint.sh para actualizar la BBDD al inicio y levantar la app
- Histórico de backups
- Se añade la opción de incluir la fecha al nombre del archivo de log que se genera en el sistema
- Autoeliminación de backups
- Generación de sensores MQTT
- Alta del vigilante de demonios

### Cambiado
- Generación de un log nuevo cada día
- Cambio visual en la cabecera de backups

### Arreglado
- Actualización del algoritmo de duración del backup

## [0.0.1_alpha] - 13/06/2022
### Añadido
- Creación de backups local y en la nube del servidor Mega vía terminal.
- Creación básica de la aplicación web.
- Creación de backups local y en la nube del servidor Mega vía aplicación web.
- Uso del usuario y contraseña para la nube del backup configurado.
- Gestión de la BBDD con Flask-Migrate.
- Configuración de la aplicación desde un fichero externo.
- Salida de errores, mensajes y avisos a un log configurable.
