import os
from io import BytesIO

from flask import Blueprint, render_template, redirect, url_for, session, request, flash, send_file, make_response
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from models import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/index')
def index():
    if "che_user" in session:
        cher_id = session['id_che']
        projets = Projet.query.filter_by(cher_id=cher_id).all()
        if projets:
            return render_template("Client/indexC.html", projets=projets)
        else:
            return render_template("Client/indexC.html" )
    elif "exp_user" in session:
        expert_id = session['id_exp']
        expert = Expert.query.get(expert_id)
        chercheur = (
            Chercheur.query
            .join(Projet, Projet.cher_id == Chercheur.id_che)
            .filter(Chercheur.special_che == expert.special_exp)
            .options(joinedload(Chercheur.projets))
            .all()
        )
        if chercheur:
            return render_template("Client/indexE.html", chercheur=chercheur)
        else:
            return render_template("Client/indexE.html")
    else:
        return render_template("Client/index.html")


@auth_bp.route('/addProjet/<int:id_che_prj>', methods=['GET', 'POST'])
def addProjet(id_che_prj):
    if request.method == 'POST':
        session.permanent = True
        sujet = request.form['sujet']
        desc = request.form['desc']
        if 'file' not in request.files:
            # No file uploaded
            return 'No file uploaded', 400
        file = request.files['file']
        filename = file.filename
        filedata = file.read()
        file.save('static/sauvegarde/' + file.filename)
        if id_che_prj == session['id_che']:
            new_prj = Projet(sujet=sujet, description=desc, filename=filename, filedata=filedata, grade="NULL",
                         cher_id=id_che_prj)
            db.session.add(new_prj)
            db.session.commit()
            return redirect(url_for('auth.index'))
        else:
            return "errreur en ID session"
    else:
        return "erreur dans reqyest"


@auth_bp.route('/DelProjet/<int:id_prj>/delete')
def delete_prj(id_prj):
    prj = Projet.query.get(id_prj)
    if prj:
        db.session.delete(prj)
        db.session.commit()
        if "user" in session:
            return redirect(url_for("ProjetList"))
        else:
            return redirect(url_for('auth.index'))
    else:
        return 'Projet non trouvé', 404


@auth_bp.route('/UptProjet/<int:id_prj>/update')
def updateprj(id_prj):
    find_prj = Projet.query.get_or_404(id_prj)
    if request.method == 'POST':
        find_prj.sujet = request.form['sujet']
        find_prj.description = request.form['desc']
        find_prj.filename = request.form['file']
        db.session.commit()
        return redirect(url_for("index"))


@auth_bp.route('/testprojet/<int:id>')
def testprojet(id):
    chercheur = (
        Chercheur.query
        .join(Projet, Projet.cher_id == Chercheur.id_che)
        .filter(Chercheur.id_che == id)
        .options(joinedload(Chercheur.projets))
        .first()
    )
    if chercheur:
        return render_template("Client/testProjet.html", chercheur = chercheur)
    else:
        return render_template("Client/testProjet.html")


@auth_bp.route('/addgrade/<int:id>', methods=['POST'])
def addgrade(id):
    che = Chercheur.query.get(id)
    if request.method == 'POST':
        for prj in che.projets:
            prj.grade = request.form['grade']
            db.session.commit()
            return redirect(url_for('auth.index'))
    else:
        return "erreur en requete POST"

@auth_bp.route('/uploadfile/<int:id_upl>')
def uploadfile(id_upl):
    projet = Projet.query.filter_by(id_prj=id_upl).first()
    response = make_response(projet.filedata)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename=projet.filename)
    return response

@auth_bp.route('/logout_client')
def clt_logout():
    return render_template("client/index.html")
