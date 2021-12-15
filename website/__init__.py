#moduli installati: flask, pandas, openpyxl

#imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
from os import path
import pandas as pd
from .models import Cliente, Valuta, Vendita, Consumo, Impiego, Risorsa



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

    # registra il blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    #controlla se db esiste già
    #from .models import .....
    create_database(app)
    print(" procedura riempimento database: ")
    keytoinsert = 'sicksUniverse'
    key = input(" --> inserisci la password per riempire il database o resettarlo ai valori iniziali: ")
    if (key == keytoinsert):
        riempiDatabase()
    return app

#creo database se non esiste
def create_database(app) :
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')
    else:
        print('database esiste già')

def riempiDatabase():


    print("---------------------------CLIENTE----------------------------------")
    #leggo "Clienti" e riempio la tabella del database "Cliente"
    df = pd.read_excel('inputXLSX/clienti.xlsx', index_col=0)
    #righe del xls
    print(" | " + str(len(df)) + " | " +" entries trovate per la tabella CLIENTE ")
    for i in range(len(df)):
        codiceCliente = df.iloc[i, 0]
        fattureCumulative = df.iloc[i, 1]
        valutaCliente = df.iloc[i, 2]
        print(str(codiceCliente) + " " + str(fattureCumulative) + " " + str(valutaCliente) + " ")
        newCliente = Cliente(codCliente=codiceCliente, fattureCumulative=fattureCumulative, valutaCliente = valutaCliente)
        db.session.add(newCliente)
        db.session.commit()


    print("---------------------------VALUTA----------------------------------")
    #leggo "tassiDiCambio" e riempio la tabella del database "Valuta"
    df = pd.read_excel('inputXLSX/tassiDiCambio.xlsx', index_col=0)
    print(" | " + str(len(df)) + " | " + " entries trovate per la tabella VALUTA ")
    for i in range(len(df)):
        codValuta = df.iloc[i, 0]
        budOCons = df.iloc[i, 1]
        tassoCambioMedio = df.iloc[i, 2]
        print(str(codValuta) + " " + str(budOCons) + " " + str(tassoCambioMedio) + " ")
        newValuta = Valuta(codValuta=codValuta, budOCons=budOCons, tassoCambioMedio=tassoCambioMedio)
        db.session.add(newValuta)
        db.session.commit()

    print("---------------------------VENDITA----------------------------------")
    # leggo "Vendite" e riempio la tabella del database "Vendita"
    df = pd.read_excel('inputXLSX/Vendite.xlsx', index_col=0)
    print(" | " + str(len(df)) + " | " + " entries trovate per la tabella VENDITE ")
    for i in range(len(df)):
        nrMovimentoV = df.iloc[i, 0]
        tipo = df.iloc[i, 1]
        nrArticolo = df.iloc[i, 2]
        nrOrigine = df.iloc[i, 3]
        qta = df.iloc[i, 4]
        importoVenditeVL = df.iloc[i, 5]
        print(str(nrMovimentoV) + " " + tipo + " " + str(nrArticolo) + " " + str(nrOrigine) + " " + str(qta) + " " + str(importoVenditeVL) + " ")
        newVendita = Vendita(nrMovimentoV=nrMovimentoV, tipo=tipo, nrArticolo=nrArticolo, nrOrigine=nrOrigine, qta=qta,importoVenditeVL=importoVenditeVL)
        db.session.add(newVendita)
        db.session.commit()

    print("---------------------------CONSUMO----------------------------------")
    # leggo "Consumi" e riempio la tabella del database "Consumo"
    df = pd.read_excel('inputXLSX/Consumi.xlsx', index_col=0)
    print(" | " + str(len(df)) + " | " + " entries trovate per la tabella CONSUMO ")
    for i in range(len(df)):
        nrMovimentoC = df.iloc[i, 0]
        tipo = df.iloc[i, 1]
        codiceMP = df.iloc[i, 2]
        nrArticolo = df.iloc[i, 3]
        nrDocumentoODP = df.iloc[i, 4]
        qta = df.iloc[i, 5]
        importoTotaleC = df.iloc[i, 6]
        print(str(nrMovimentoC) + " " + tipo + " " + str(codiceMP) + " " + str(nrArticolo) + " " + str(nrDocumentoODP) + " " + str(qta) + " " + str(importoTotaleC) + " ")
        newConsumo = Consumo(nrMovimentoC=nrMovimentoC, tipo=tipo, codiceMP=codiceMP, nrArticolo=nrArticolo, nrDocumentoODP=nrDocumentoODP, qta=qta, importoTotaleC=importoTotaleC)
        db.session.add(newConsumo)
        db.session.commit()

    print("---------------------------IMPIEGO----------------------------------")
    # leggo "impiegoOrarioRisorse" e riempio la tabella del database "Impiego"
    df = pd.read_excel('inputXLSX/impiegoOrarioRisorse.xlsx', index_col=0)
    print(" | " + str(len(df)) + " | " + " entries trovate per la tabella IMPIEGO ")
    for i in range(len(df)):
        nrArticolo = df.iloc[i, 0]
        tipo = df.iloc[i, 1]
        nrODP = df.iloc[i, 2]
        descrizione = df.iloc[i, 3]
        areaProd = df.iloc[i, 4]
        risorsa = df.iloc[i, 5]
        tempoRisorsa = df.iloc[i, 6]
        qtaOutput = df.iloc[i, 7]
        print(str(nrArticolo) + " " + tipo + " " + str(nrODP) + " " + str(descrizione) + " " + str(areaProd) + " " + str(risorsa) + " " + str(tempoRisorsa) + " " + str(qtaOutput))
        newImpiego = Impiego(nrArticolo=nrArticolo,tipo=tipo,nrODP=nrODP,descrizione=descrizione,areaProd=areaProd,risorsa=risorsa,tempoRisorsa=tempoRisorsa,qtaOutput=qtaOutput)
        db.session.add(newImpiego)
        db.session.commit()

    print("---------------------------RISORSA----------------------------------")
    # leggo "Risorse" e riempio la tabella del database "Risorsa"
    df = pd.read_excel('inputXLSX/costoOrario.xlsx', index_col=0)
    print(" | " + str(len(df)) + " | " + " entries trovate per la tabella RISORSA ")
    for i in range(len(df)):
        codRisorsa = df.iloc[i, 0]
        areaProd = df.iloc[i, 1]
        costoOrarioBudget = df.iloc[i, 2]
        costoOrarioConsuntivo = df.iloc[i, 3]
        print(
            str(codRisorsa) + " " + str(areaProd) + " " + str(costoOrarioBudget) + " " + str(costoOrarioConsuntivo) + " ")
        newRisorsa = Risorsa(codRisorsa=codRisorsa,areaProd=areaProd,costoOrarioBudget=costoOrarioBudget,costoOrarioConsuntivo=costoOrarioConsuntivo)
        db.session.add(newRisorsa)
        db.session.commit()

    #quelliCheUsanoDollaro = df[(df['Valuta'] == 2)]