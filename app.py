import os
from flask import Flask, render_template, request, session, url_for, redirect, flash
from datetime import timedelta
from os import path
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from auth import auth_bp
from models import *

DB_NAME = "db.db"
app = Flask(__name__)
app.register_blueprint(auth_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
db.init_app(app)
app.secret_key = "helo"
app.permanent_session_lifetime = timedelta(hours=5)
migrate = Migrate(app, db)


@app.before_request
def create_tables():
    db.create_all()


def create_database(app):
    if not path.exists('project/' + DB_NAME):
        db.create_all(app=app)
        print('Creation de Base de donnée')


@app.route('/')
def home():  # put application's code here
    return render_template("header/index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['name']
        passwd = request.form['passwd']
        Cherch = Chercheur.query.filter_by(user_che=user, passwd_che=passwd).first()
        Exper = Expert.query.filter_by(user_exp=user, passwd_exp=passwd).first()
        if user == "admin" and passwd == "admin":
            session['user'] = user
            flash('Logged in successfully!', category='success')
            return redirect(url_for('home'))

        elif Cherch:
            session['id_che'] = Cherch.id_che
            session['che_user'] = user
            flash('Logged in successfully Chercheur!', category='success')
            return redirect(url_for('auth.index'))

        elif Exper:
            session['id_exp'] = Exper.id_exp
            session['exp_user'] = user
            flash('Logged in successfully Expert!', category='success')
            return redirect(url_for("auth.index"))

        else:
            flash('User et/ou Mot de passe est uncorrect !', category='error')
            return render_template("login.html")
    else:
        if "user" in session:
            return redirect(url_for("home"))

        return render_template("login.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        post = request.form['postl']
        nom = request.form['nom']
        pren = request.form['prenom']
        cin = request.form['cin']
        add = request.form['adresse']
        tel = request.form['tel']
        email = request.form['email']
        special = request.form['spec']
        affiliation = request.form['affil']
        techno = request.form['tech']
        user = request.form['user']
        passwd = request.form['pass']
        cpasswd = request.form['cpass']
        if passwd != cpasswd:
            flash('Passwords don\'t match.', category='error')
        elif len(passwd) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif post == "chercheur":
            if Chercheur.query.filter_by(cin_che=cin).first() or Chercheur.query.filter_by(email_che=email).first():
                return 'Le Chercheur existe déjà'
            new_chercheur = Chercheur(nom_che=nom, pren_che=pren, cin_che=cin, add_che=add, tel_che=tel,
                                  email_che=email, special_che=special, affiliation_che=affiliation,
                                  techno_che=techno, user_che=user, passwd_che=passwd)
            db.session.add(new_chercheur)
            db.session.commit()
            return redirect(url_for("login"))
        elif post == "expert":
            if Expert.query.filter_by(cin_exp=cin).first() or Expert.query.filter_by(email_exp=email).first():
                return 'L\'expert existe déjà'
            new_expert = Expert(nom_exp=nom, pren_exp=pren, cin_exp=cin, add_exp=add, tel_exp=tel,
                                email_exp=email, special_exp=special, affiliation_exp=affiliation,
                                dispo="True", user_exp=user, passwd_exp=passwd)
            db.session.add(new_expert)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/addCherch', methods=['GET', 'POST'])
def addcherch():
    if request.method == 'POST':
        session.permanent = True
        nom_che = request.form['nom']
        pren_che = request.form['prenom']
        cin_che = request.form['cin']
        add_che = request.form['adresse']
        tel_che = request.form['tel']
        email_che = request.form['email']
        special_che = request.form['spec']
        affiliation_che = request.form['affil']
        techno_che = request.form['tech']
        username = request.form['user']
        passwd_che = request.form['pass']
        if Chercheur.query.filter_by(cin_che=cin_che).first() or Chercheur.query.filter_by(email_che=email_che).first():
            return 'Le Chercheur existe déja'

        new_chercheur = Chercheur(nom_che=nom_che, pren_che=pren_che, cin_che=cin_che, add_che=add_che,tel_che=tel_che, email_che=email_che,special_che=special_che, affiliation_che=affiliation_che, techno_che=techno_che,user_che=username, passwd_che=passwd_che)
        db.session.add(new_chercheur)
        db.session.commit()
        return redirect(url_for("ChecheurList"))


@app.route('/addExpert', methods=['POST', 'GET'])
def addExpert():
    if request.method == 'POST':
        nom_exp = request.form['nom']
        pren_exp = request.form['prenom']
        cin_exp = request.form['cin']
        add_exp = request.form['adresse']
        tel_exp = request.form['tel']
        email_exp = request.form['email']
        special_exp = request.form['spec']
        affiliation_exp = request.form['affil']
        username = request.form['user']
        passwd_exp = request.form['pass']
        if Expert.query.filter_by(cin_exp=cin_exp).first() or Expert.query.filter_by(email_exp=email_exp).first():
            return 'Le expert existe déja'

        new_expert = Expert(nom_exp=nom_exp, pren_exp=pren_exp, cin_exp=cin_exp, add_exp=add_exp, tel_exp=tel_exp,
                            email_exp=email_exp, special_exp=special_exp, affiliation_exp=affiliation_exp,
                            dispo="True", user_exp=username, passwd_exp= passwd_exp)
        db.session.add(new_expert)
        db.session.commit()
        return redirect(url_for("ExpertList"))


@app.route('/DelCherch/<int:id_che>/delete')
def delete_che(id_che):
    che = Chercheur.query.get(id_che)
    if che:
        db.session.delete(che)
        db.session.commit()
        return redirect(url_for("ChecheurList"))
    else:
        return 'Chercheur non trouvé', 404


@app.route('/UptCherch/<int:id_che>/edit', methods=['GET', 'POST'])
def updateche(id_che):
    find_che = Chercheur.query.get_or_404(id_che)
    if request.method == 'POST':
        find_che.nom_che = request.form['nom']
        find_che.pren_che = request.form['prenom']
        find_che.cin_che = request.form['cin']
        find_che.add_che = request.form['adresse']
        find_che.tel_che = request.form['tel']
        find_che.email_che = request.form['email']
        find_che.special_che = request.form['spec']
        find_che.affiliation_che = request.form['affil']
        find_che.techno_che = request.form['tech']
        find_che.passwd_che = request.form['pass']
        find_che.user_che = request.form['nom']
        db.session.commit()
        return redirect(url_for("ChecheurList"))


@app.route('/DelExp/<int:id_exp>/delete')
def delete_exp(id_exp):
    exp = Expert.query.get(id_exp)
    if exp:
        db.session.delete(exp)
        db.session.commit()
        return redirect(url_for("ExpertList"))
    else:
        return 'Expert non trouvé', 404


@app.route('/UptExp/<int:id_exp>/edit' , methods=['GET', 'POST'])
def update_exp(id_exp):
    find_exp = Expert.query.get_or_404(id_exp)
    if request.method == 'POST':
        find_exp.nom_exp = request.form['nom']
        find_exp.pren_exp = request.form['prenom']
        find_exp.cin_exp = request.form['cin']
        find_exp.add_exp = request.form['adresse']
        find_exp.tel_exp = request.form['tel']
        find_exp.email_exp = request.form['email']
        find_exp.special_exp = request.form['spec']
        find_exp.affiliation_exp = request.form['affil']
        find_exp.passwd_exp = request.form['pass']
        find_exp.user_exp = request.form['nom']
        db.session.commit()
        return redirect(url_for("ExpertList"))


@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
        redirect(url_for('login'))
    elif "che_user" in session:
        session.pop("che_user", None)
        render_template("Client/index.html")
    elif "exp_user" in session:
        session.pop("exp_user", None)
        render_template("Client/index.html")
    return redirect(url_for("login"))


# ----------- Debut Les Pages de Application ---------
# ____________________________________________________
# -----------------------------------------------------


@app.route('/ProjetList')
def ProjetList():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("header/ProjetList.html", projets= Projet.query.all())


@app.route('/ExpertList')
def ExpertList():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("header/ExpertList.html", experts=Expert.query.all())


@app.route('/contact')
def contact():
    return render_template("header/contact.html")


@app.route('/ChercheurList')
def ChecheurList():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("Header/ChecheurList.html", chercheurs=Chercheur.query.all())


# ----------- Fin Les Pages de Application ---------


if __name__ == '__main__':
    if not os.path.exists('db.db'):
        db.create_all()
    app.run(port=5000)
    app.debug = True
