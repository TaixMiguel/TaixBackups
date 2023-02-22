import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

from app import kTaixBackups
from backups.forms import CreateBackupForm
from backups.models import Backup
from backups.task import execute_backup_task

logger = logging.getLogger(__name__)

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

    return render(request, 'create_new_backup.html', create_context({'form':form, 'sw_create':True}))

def exec_backup(request, id_backup: int):
    backups: Backup = Backup.objects.filter(id_backup=id_backup)
    if backups:
        backup: Backup = backups[0]
        execute_backup_task.delay(backup)

        return render(request, 'execute_backup.html', context=create_context({'backup': backup}))
    return None

def update_backup(request, id_backup: int):
    backups: Backup = Backup.objects.filter(id_backup=id_backup)
    if backups:
        backup: Backup = backups[0]

        if request.method == 'POST':
            form = CreateBackupForm(request.POST)
            if form.is_valid():
                backup.name = form.cleaned_data['backup_code']
                backup.description = form.cleaned_data['description']
                backup.id_storage_service_fK = form.cleaned_data['storage_service']
                backup.source_dir = form.cleaned_data['source_dir']
                backup.destination_dir = form.cleaned_data['destination_dir']
                backup.user = form.cleaned_data['user']
                backup.password = form.cleaned_data['password']
                backup.n_backups_max = form.cleaned_data['num_backups']
                backup.sw_sensor_mqtt = form.cleaned_data['sensor_mqtt']
                backup.save()
                return HttpResponseRedirect('/')
        else:
            initial = {
                'backup_code': backup.name,
                'description': backup.description,
                'storage_service': backup.id_storage_service_fK,
                'source_dir': backup.source_dir,
                'destination_dir': backup.destination_dir,
                'user': backup.user,
                'password': backup.password,
                'num_backups': backup.n_backups_max,
                'sensor_mqtt': backup.sw_sensor_mqtt
            }
            form: CreateBackupForm = CreateBackupForm(initial=initial)

        return render(request, 'create_new_backup.html', create_context({'form': form, 'sw_create':False}))
    return HttpResponseRedirect('/')

def delete_backup(request, id_backup: int):
    backups: Backup = Backup.objects.filter(id_backup=id_backup)
    if backups:
        logger.info(f'Se ha pedido la eliminación del backup {backups[0]}')
        Backup.objects.filter(id_backup=id_backup).delete()
    return HttpResponseRedirect('/')