#in views definiamo le routes

from flask import Blueprint, render_template
import pandas as pd
from website import db
from website.models import Cliente, Valuta, Vendita, Consumo, Impiego, Risorsa
#from . import db

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

@views.route('/db')
def riempi():
            print(" procedura riempimento database: ")
            keytoinsert = 'a'
            key = input(" --> inserisci la password per riempire il database o resettarlo ai valori iniziali: ")
            if (key == keytoinsert):

                print("---------------------------CLIENTE----------------------------------")
                # leggo "Clienti" e riempio la tabella del database "Cliente"
                df = pd.read_excel('inputXLSX/clienti.xlsx', index_col=0)
                # righe del xls
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella CLIENTE ")
                for i in range(len(df)):
                    codiceCliente = df.iloc[i, 0]
                    fattureCumulative = df.iloc[i, 1]
                    valutaCliente = int(df.iloc[i, 2])
                    newCliente = Cliente(codiceCliente=codiceCliente, fattureCumulative=fattureCumulative,
                                         valutaCliente=valutaCliente)
                    db.session.add(newCliente)
                    db.session.commit()

                print("---------------------------VALUTA----------------------------------")
                # leggo "tassiDiCambio" e riempio la tabella del database "Valuta"
                df = pd.read_excel('inputXLSX/tassiDiCambio.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella VALUTA ")
                for i in range(len(df)):
                    codValuta = int(df.iloc[i, 0])
                    budOCons = df.iloc[i, 1]
                    tassoCambioMedio = str(df.iloc[i, 2])
                    tassoCambioMedio = tassoCambioMedio.replace(",",".")
                    tassoCambioMedio = float(tassoCambioMedio)
                    newValuta = Valuta(codValuta=codValuta, budOCons=budOCons, tassoCambioMedio=tassoCambioMedio)
                    db.session.add(newValuta)
                    db.session.commit()

                print("---------------------------VENDITA----------------------------------")
                # leggo "Vendite" e riempio la tabella del database "Vendita"
                df = pd.read_excel('inputXLSX/Vendite.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella VENDITE ")
                for i in range(len(df)):
                    nrMovimentoV = int(df.iloc[i, 0])
                    tipo = df.iloc[i, 1]
                    nrArticolo = df.iloc[i, 2]
                    nrOrigine = df.iloc[i, 3]
                    qta = int(df.iloc[i, 4])
                    importoVenditeVL = str(df.iloc[i, 5])
                    importoVenditeVL = importoVenditeVL.replace(",",".")
                    importoVenditeVL = float(importoVenditeVL)
                    newVendita = Vendita(nrMovimentoV=nrMovimentoV, tipo=tipo, nrArticolo=nrArticolo,
                                         nrOrigine=nrOrigine,
                                         qta=qta, importoVenditeVL=importoVenditeVL)
                    db.session.add(newVendita)
                    db.session.commit()

                print("---------------------------CONSUMO----------------------------------")
                # leggo "Consumi" e riempio la tabella del database "Consumo"
                df = pd.read_excel('inputXLSX/Consumi.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella CONSUMO ")
                for i in range(len(df)):
                    nrMovimentoC = int(df.iloc[i, 0])
                    tipo = df.iloc[i, 1]
                    codiceMP = df.iloc[i, 2]
                    nrArticolo = df.iloc[i, 3]
                    nrDocumentoODP = df.iloc[i, 4]
                    qta = int(df.iloc[i, 5])
                    importoTotaleC = str(df.iloc[i, 6])
                    importoTotaleC = importoTotaleC.replace(",",".")
                    importoTotaleC = float(importoTotaleC)
                    newConsumo = Consumo(nrMovimentoC=nrMovimentoC, tipo=tipo, codiceMP=codiceMP, nrArticolo=nrArticolo,
                                         nrDocumentoODP=nrDocumentoODP, qta=qta, importoTotaleC=importoTotaleC)
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
                    tempoRisorsa = str(df.iloc[i, 6])
                    tempoRisorsa = tempoRisorsa.replace(",", ".")
                    tempoRisorsa = float(tempoRisorsa)
                    qtaOutput = int(df.iloc[i, 7])
                    newImpiego = Impiego(nrArticolo=nrArticolo, tipo=tipo, nrODP=nrODP, descrizione=descrizione,
                                         areaProd=areaProd, risorsa=risorsa, tempoRisorsa=tempoRisorsa,
                                         qtaOutput=qtaOutput)
                    db.session.add(newImpiego)
                    db.session.commit()

                print("---------------------------RISORSA----------------------------------")
                # leggo "Risorse" e riempio la tabella del database "Risorsa"
                df = pd.read_excel('inputXLSX/costoOrario.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella RISORSA ")
                for i in range(len(df)):
                    codRisorsa = df.iloc[i, 0]
                    areaProd = df.iloc[i, 1]
                    costoOrarioBudget = str(df.iloc[i, 2])
                    costoOrarioBudget = costoOrarioBudget.replace(",",".")
                    costoOrarioBudget = float(costoOrarioBudget)
                    costoOrarioConsuntivo = str(df.iloc[i, 3])
                    costoOrarioConsuntivo = costoOrarioConsuntivo.replace(",",".")
                    costoOrarioConsuntivo = float(costoOrarioConsuntivo)
                    newRisorsa = Risorsa(codRisorsa=codRisorsa, areaProd=areaProd, costoOrarioBudget=costoOrarioBudget,
                                         costoOrarioConsuntivo=costoOrarioConsuntivo)
                    db.session.add(newRisorsa)
                    db.session.commit()

        # quelliCheUsanoDollaro = df[(df['Valuta'] == 2)]