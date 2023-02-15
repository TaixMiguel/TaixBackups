# TaixBackups
Proyecto web para generar backups y almacenarlos en local o en la nube ([Mega](https://mega.io/))

Ejemplo de docker-compose:
```dockerfile
version: "2"

services:
  taix-backups:
    image: omikel8/taix_backups:latest
    container_name: TaixBackups
    hostname: taix-backups
    restart: always
    network_mode: bridge
    ports:
      - 8000:8000
    environment:
      - 'CONFIG_FILE_TAIXBACKUP=/taixBackup/config/configApp.json'

  redis:
    image: redis:alpine
    container_name: Redis
    hostname: redis
    restart: always
    network_mode: bridge
    ports:
      - 6379:6379
```

Ejemplo de fichero de configuración:
```json
{
  "app": {
    "debugMode": false,
    "secretKey": "xxx"
  },
  "bbdd": {
    "engine": "django.db.backends.sqlite3",
    "name": "/taixBackup/db.sqlite3"
  },
  "djangoRQ": {
    "dashboard": false,
    "db": 0,
    "host": "localhost",
    "port": 6379,
    "timeout": 360
  },
  "log": {
    "numberOfLogsFile": 7,
    "levelLog": "INFO",
    "path": "xxx"
  },
  "mqtt": {
    "enabled": false,
    "password": "xxx",
    "server": "xxx",
    "username": "xxx"
  }
}
```

### RQ Dashboard
Para visualizar el cuadro RQ, necesitaremos entrar en la url `http://xxxxxxx:8000/django_rq/`

## Licencia
[GNU General Public License v3.0](https://github.com/TaixMiguel/TaixBackups/blob/main/LICENSE)
