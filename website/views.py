#in views definiamo le routes

from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/scostamentiVendite')
def vendite():
    return "<h1> Pagina Vendite </h1>"

@views.route('/scostamentiProduzione')
def produzione():
    return "<h1> Pagina Produzione </h1>"

#