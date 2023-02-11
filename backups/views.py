from django.shortcuts import render

from app import kTaixBackups
from backups.models import Backup
from backups.task import execute_backup_task

def create_context(custom: dict=None) -> dict:
    context = {'app_name':kTaixBackups.APP_NAME, 'app_version':kTaixBackups.APP_VERSION}
    if custom:
        context.update(custom)
    return context

def index(request):
    backups = Backup.objects.all()

    return render(
        request,
        'index.html',
        context=create_context({'backup_list': backups}),
    )

def exec_backup(request, id_backup: int):
    backups: Backup = Backup.objects.filter(id_backup=id_backup)
    if backups:
        backup: Backup = backups[0]
        execute_backup_task.delay(backup)

        return render(
            request,
            'execute_backup.html',
            context=create_context({'backup': backup}),
        )
    return None