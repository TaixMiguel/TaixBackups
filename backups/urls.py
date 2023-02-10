from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('execBackup/<int:id_backup>', views.exec_backup, name='execute-backup'),
]
