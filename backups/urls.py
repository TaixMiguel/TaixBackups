from django.urls import path, include

from app import kTaixBackups
from app.configApp import ConfigApp
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('execBackup/<int:id_backup>', views.exec_backup, name='execute-backup'),
]

configApp: ConfigApp = ConfigApp()
if configApp.get_value_boolean(kTaixBackups.Config.DjangoRQ.ROOT, kTaixBackups.Config.DjangoRQ.DASHBOARD):
    urlpatterns += [
        path('django_rq/', include('django_rq.urls')),
    ]