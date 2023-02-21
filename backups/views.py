from django.http import HttpResponseRedirect
from django.shortcuts import render

from app import kTaixBackups
from backups.forms import CreateBackupForm
from backups.models import Backup
from backups.task import execute_backup_task

def create_context(custom: dict=None) -> dict:
    context = {'app_name':kTaixBackups.APP_NAME, 'app_version':kTaixBackups.APP_VERSION}
    if custom:
        context.update(custom)
    return context

def index(request):
    backups = Backup.objects.all()
    return render(request, 'index.html', context=create_context({'backup_list': backups}))

def create_new_backup(request):
    form: CreateBackupForm = CreateBackupForm()
    if request.method == 'POST':
        form = CreateBackupForm(request.POST)
        if form.is_valid():
            aux_backup: Backup = Backup()
            aux_backup.name = form.cleaned_data['backup_code']
            aux_backup.description = form.cleaned_data['description']
            aux_backup.id_storage_service_fK = form.cleaned_data['storage_service']
            aux_backup.source_dir = form.cleaned_data['source_dir']
            aux_backup.destination_dir = form.cleaned_data['destination_dir']
            aux_backup.user = form.cleaned_data['user']
            aux_backup.password = form.cleaned_data['password']
            aux_backup.n_backups_max = form.cleaned_data['num_backups']
            aux_backup.sw_sensor_mqtt = form.cleaned_data['sensor_mqtt']
            aux_backup.save()
            return HttpResponseRedirect(f'/execBackup/{aux_backup.id_backup}')

    return render(request, 'create_new_backup.html', create_context({'form':form}))

def exec_backup(request, id_backup: int):
    backups: Backup = Backup.objects.filter(id_backup=id_backup)
    if backups:
        backup: Backup = backups[0]
        execute_backup_task.delay(backup)

        return render(request, 'execute_backup.html', context=create_context({'backup': backup}))
    return None