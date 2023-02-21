from django import forms
from django.core.exceptions import ValidationError

from backups.models import StorageService


class CreateBackupForm(forms.Form):

    backup_code = forms.CharField(min_length=4, max_length=64, required=True)
    description = forms.CharField(max_length=300, required=False)
    storage_service = forms.ModelChoiceField(StorageService.objects.all(), required=True)
    source_dir = forms.CharField(required=True, max_length=256)
    destination_dir = forms.CharField(required=True, max_length=256)
    user = forms.CharField(max_length=64, required=False)
    password = forms.CharField(max_length=64, required=False)
    num_backups = forms.IntegerField(min_value=1, max_value=99, required=True)
    sensor_mqtt = forms.BooleanField(required=False)

    def clean(self):
        server: StorageService = self.cleaned_data['storage_service']
        if server.code != 'LOCAL':
            user = self.cleaned_data['user']
            if not user:
                raise ValidationError('El usuario es obligatorio para servidores que no sean locales', code='invalid')
            password = self.cleaned_data['password']
            if not password:
                raise ValidationError('La contraseña es obligatoria para servidores que no sean locales', code='invalid')
        return self.cleaned_data
