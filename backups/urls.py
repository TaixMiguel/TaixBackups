from django.urls import path, include

from app import kTaixBackups
from app.configApp import ConfigApp
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newBackup', views.create_new_backup, name='create-new-backup'),
    path('execBackup/<int:id_backup>', views.exec_backup, name='execute-backup'),
    path('updateBackup/<int:id_backup>', views.update_backup, name='update-backup'),
    path('deleteBackup/<int:id_backup>', views.delete_backup, name='delete-backup'),
]

configApp: ConfigApp = ConfigApp()
if configApp.get_value_boolean(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.DASHBOARD):
    urlpatterns += [
        path('django_rq/', include('django_rq.urls')),
    ]