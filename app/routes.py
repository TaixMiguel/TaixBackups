#!/usr/bin/python3

from flask import render_template, redirect, url_for
from app import app_bp
from app import consts
from app import forms
from app.backup.backup import Backup


@app_bp.route("/")
def index():
    backups = Backup.get_instances()
    return render_template("index.html", app_name=consts.APP_NAME, app_version=consts.APP_VERSION, backups=backups)


@app_bp.route("/execBackup/<int:id_backup>/")
def exec_backup(id_backup):
    backup = Backup.get_instance(id_backup)
    backup.create_backup()
    return "Ejecutando el backup {}".format(backup.name)


@app_bp.route("/newBackup", methods=["GET", "POST"])
def new_backup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        server = form.server.data
        source_dir = form.source_dir.data
        destination_dir = form.destination_dir.data
        user = form.user.data
        password = form.password.data

        backup = Backup(name=name, description=description, server=server, source_dir=source_dir,
                        destination_dir=destination_dir, user=user, password=password)
        backup.save()
        return redirect('/')
    return render_template("new_backup.html", app_name=consts.APP_NAME, app_version=consts.APP_VERSION, form=form)


@app_bp.route("/b/<string:slug>/")
def show_backup(slug):
    return "Mostrando el backup {}".format(slug)
