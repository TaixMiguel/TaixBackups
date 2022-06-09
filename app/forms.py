#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Descripción')
    server = SelectField('Servidor de almacenamiento', choices=[('LOCAL', 'Local'), ('MEGA', 'Mega')])
    source_dir = StringField('Ruta origen', validators=[DataRequired(), Length(max=256)])
    destination_dir = StringField('Ruta destino', validators=[DataRequired(), Length(max=256)])
    user = StringField('Usuario', validators=[Length(max=64)])
    password = PasswordField('Contraseña', validators=[Length(max=64)])
    submit = SubmitField('Crear')
