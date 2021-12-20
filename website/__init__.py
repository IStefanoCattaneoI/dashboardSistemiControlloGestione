#moduli installati: flask, pandas, openpyxl

#imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
from os import path

#creo il database per muovermi più facilmente tra le tabelle

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() :
    app = Flask(__name__)

    #creo chiave segreta
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    # configura database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    #engine = db.create_engine(f'sqlite:///{DB_NAME}')
    #connection = engine.connect()



    # registra il blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    #controlla se db esiste già
    #from .models import .....
    create_database(app)
    return app

#creo database se non esiste
def create_database(app) :
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        db.session.commit()
        print('Created Database')
    else:
        print('database esiste già')

