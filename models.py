from alembic import op
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Admin(db.Model, UserMixin):
    id_adm = db.Column(db.Integer, primary_key=True)
    nom_adm = db.Column(db.String(20))
    pren_adm = db.Column(db.String(20))
    cin_adm = db.Column(db.String(10))
    add_adm = db.Column(db.String(50))
    email_adm = db.Column(db.String(20), unique=True)
    user_adm = db.Column(db.String(30))
    passwd_adm = db.Column(db.String(30))

    def __init__(self, nom_adm, pren_adm, cin_adm, add_adm, email_adm, user_adm, passwd_adm):
        self.nom_adm = nom_adm
        self.pren_adm = pren_adm
        self.cin_adm = cin_adm
        self.add_adm = add_adm
        self.email_adm = email_adm
        self.user_adm = user_adm
        self.passwd_adm = passwd_adm


class Chercheur(db.Model, UserMixin):
    id_che = db.Column(db.Integer, primary_key=True)
    nom_che = db.Column(db.String(20))
    pren_che = db.Column(db.String(20))
    cin_che = db.Column(db.String(10))
    add_che = db.Column(db.String(50))
    tel_che = db.Column(db.String(10))
    email_che = db.Column(db.String(20))
    special_che = db.Column(db.String(30))
    affiliation_che = db.Column(db.String(30))
    techno_che = db.Column(db.String(30))
    user_che = db.Column(db.String(30))
    passwd_che = db.Column(db.String(30), unique=True)
    projets = db.relationship('Projet', backref='chercheur')

    def __init__(self, nom_che, pren_che, cin_che, add_che, tel_che, email_che,
                 special_che, affiliation_che, techno_che, user_che, passwd_che):
        self.nom_che = nom_che
        self.pren_che = pren_che
        self.cin_che = cin_che
        self.add_che = add_che
        self.tel_che = tel_che
        self.email_che = email_che
        self.special_che = special_che
        self.affiliation_che = affiliation_che
        self.techno_che = techno_che
        self.user_che = user_che
        self.passwd_che = passwd_che


class Projet(db.Model, UserMixin):
    id_prj = db.Column(db.Integer, primary_key=True)
    sujet = db.Column(db.String(100))
    description = db.Column(db.Text)
    filename = db.Column(db.String(100))
    filedata = db.Column(db.LargeBinary)
    grade = db.Column(db.Integer, nullable=False)
    cher_id = db.Column(db.Integer, db.ForeignKey('chercheur.id_che'), name='fk_projet_cher_id')

    def __init__(self, sujet, description, filename, filedata,grade, cher_id):
        self.sujet = sujet
        self.description = description
        self.filename = filename
        self.filedata = filedata
        self.grade = grade
        self.cher_id = cher_id



class Expert(db.Model, UserMixin):
    id_exp = db.Column(db.Integer, primary_key=True)
    nom_exp = db.Column(db.String(20))
    pren_exp = db.Column(db.String(20))
    cin_exp = db.Column(db.String(10))
    add_exp = db.Column(db.String(50))
    tel_exp = db.Column(db.String(10))
    email_exp = db.Column(db.String(20))
    dispo = db.Column(db.String(20))
    special_exp = db.Column(db.String(30))
    affiliation_exp = db.Column(db.String(30))
    user_exp = db.Column(db.String(30))
    passwd_exp = db.Column(db.String(30), unique=True)

    def __init__(self, nom_exp, pren_exp, cin_exp, add_exp, tel_exp, email_exp,dispo,
                 special_exp, affiliation_exp, user_exp, passwd_exp):
        self.nom_exp = nom_exp
        self.pren_exp = pren_exp
        self.cin_exp = cin_exp
        self.add_exp = add_exp
        self.tel_exp = tel_exp
        self.email_exp = email_exp
        self.dispo = dispo
        self.special_exp = special_exp
        self.affiliation_exp = affiliation_exp
        self.user_exp = user_exp
        self.passwd_exp = passwd_exp


