import django as django
from django.db import models

class StorageService(models.Model):

    id_storage_service = models.AutoField(primary_key=True)
    code = models.CharField(max_length=8, help_text='Código del servicio de almacenamiento')
    name = models.CharField(max_length=50, help_text='Nombre del servicio de almacenamiento')

class Backup(models.Model):

    id_backup = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, help_text='Código del backup')
    description = models.TextField(max_length=300, help_text="Descripción asociada al backup", null=True)
    id_storage_service_fK = models.ForeignKey(StorageService, help_text='Código del servicio de almacenamiento', on_delete=models.CASCADE)
    source_dir = models.CharField(max_length=256)
    destination_dir = models.CharField(max_length=256)
    user = models.CharField(max_length=64, help_text='Usuario del servicio de almacenamiento')
    password = models.CharField(max_length=64, help_text='Contraseña del servicio de almacenamiento')
    n_backups_max = models.IntegerField(max_length=3, help_text='Nº de backups disponibles', default=10)
    sw_sensor_mqtt = models.BooleanField(help_text='Avisar por MQTT de cambios', default=False)
    audit_time = models.DateTimeField('Fecha de creación',
                                      help_text='Indica la fecha de alta del backup',
                                      default=django.utils.timezone.now)

class BackupHistory(models.Model):

    id_backup_history = models.AutoField(primary_key=True)
    id_backup_fk = models.ForeignKey(Backup, help_text='Backup asociado', on_delete=models.CASCADE)

    backup_name = models.CharField(max_length=64, help_text='Nombre del fichero de backup')
    backup_size = models.IntegerField(help_text='Tamaño del backup', default=0)
    status = models.CharField(max_length=8, help_text='Estado del backup', default='PDTE')
    duration = models.FloatField(help_text='Duración de la creación del backup', default=0)
    audit_time = models.DateTimeField('Fecha de creación',
                                      help_text='Indica la fecha de creación del backup',
                                      default=django.utils.timezone.now)
