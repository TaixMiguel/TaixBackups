from django.contrib import admin

from backups.models import StorageService, Backup, BackupHistory

admin.site.register(StorageService)
admin.site.register(Backup)
admin.site.register(BackupHistory)
