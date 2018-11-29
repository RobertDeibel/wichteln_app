
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_login import login_user, LoginManager, UserMixin, logout_user,\
login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
#script import
import utils

DEADLINE = datetime(2018, 12, 3)

deadline = datetime.now() + timedelta(seconds=30)
#flask stuff
app = Flask(__name__)
app.config['DEBUG'] = True
#database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="robertdeibel",
    password="wichteln18",
    hostname="robertdeibel.mysql.pythonanywhere-services.com",
    databasename="robertdeibel$wichteln",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'deibel.robert@gmail.com'
app.config['MAIL_PASSWORD'] = 'lqqwngfebmkgvtgh'
app.config['MAIL_PORT'] = 587
mail = Mail()
mail.init_app(app)

db = SQLAlchemy(app)

app.secret_key = 'mxckjhvudksjer283747ijfvds7czqwje347'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username


all_users = {'admin': User('admin', generate_password_hash('secret'))}

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)


class Wichtel(db.Model):

    __tablename__ = "wichtel"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    email = db.Column(db.String(4096))
    wichtel = db.Column(db.String(4096))


@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == "GET":
        result = []
        for wicht in utils.WICHTEL:
            result.append(utils.WICHTEL[wicht])
        return render_template("main_page.html", wichtel=Wichtel.query.all())

    if request.form['name'] != '' and request.form['email'] != ''\
        and request.form['email'] not in [email[0] for email in db.session.query(Wichtel.email).all()]:
        wichtel = Wichtel(name = request.form["name"], email = request.form['email'])
        db.session.add(wichtel)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_page.html', error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("login_page.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)

    login_user(user)
    return redirect(url_for('index'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def send_mails(message, emails):
    with mail.connect() as conn:
        for m, e in zip(message, emails):
            msg = Message('Wichteln',sender='wichtelbot@gmail.com', recipients = [e], body = m)
            conn.send(msg)

