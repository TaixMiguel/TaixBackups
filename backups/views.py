from django.shortcuts import render
from backups.models import Backup

def create_context(custom: dict=None) -> dict:
    context = {'app_name':'Generador de Backups', 'app_version':'0.0.3_alpha'}
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
        backup.create_backup()

        return render(
            request,
            'execute_backup.html',
            context=create_context({'backup': backup}),
        )
    return None