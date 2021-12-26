#in views definiamo le routes

from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
from website import db
from website.models import Cliente, Valuta, Vendita, Consumo, Impiego, Risorsa
#from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def home():
    #----ESEMPIO DI QUERY con SQLALCHEMY (NO JOIN QUI) -------------------
    #newCliente1 = Cliente.query.filter_by(codiceCliente='C00140')
    newCliente = Cliente.query.filter_by(valutaCliente=2).all()#trova tutti i clienti che usano l'euro
    vend = Vendita.query.filter_by(tipo="BUDGET", qta=5).all()#trova tutte le vendite a budget con quantità 5
    quantinehannovenduti5 = len(vend) #contare le entry del risultato della query vend
    vend2 = Vendita.query.filter_by(tipo="BUDGET").all() #trova tutte le vendite a budget
    # voglio trovare tutte le vendite a budget del cliente dato e fare la somma dell'importo totale



    #----------------------------------------------- LO RIPETE DUE VOLTE.
    #print(vend3)
    #print(str(len(vend3)) + " totale vendite del cliente: " + cc)
    print(str(len(vend2)) + " vendite totali a budget")
    print(str(quantinehannovenduti5) + " vendite a budget con quantita 5")
    print(newCliente)
    print(vend)
    #print(newCliente1)
    print("sono DOPO la query")
    return render_template("home.html")

@views.route('/scostamentiCliente', methods=['GET','POST'])
def vendite():

    # PROVO A RENDERE INTERATTIVA LA NOSTRA WEB APP
    if request.method == 'POST':
        subtotaleVL = 0
        tipo = request.form.get('tipo')
        cc = request.form.get('codiceCliente')
        x = Cliente.query.filter_by(codiceCliente = cc).first()
        if x:
            # alternativa più compatta:2 (ORA FUNZIONANTE)
            vend4 = Vendita.query.filter_by(tipo=tipo, nrOrigine=cc).all()
            for i in range(len(vend4)):
                venditaa = vend4[
                    i].importoVenditeVL  # vend4[i] dovrebbe essere una singola vendita delle condizioni soddisfatte sopra
                print(venditaa)
                subtotaleVL = subtotaleVL + venditaa
            # ----parte che non c'è nella versione 1. che valuta ha il cliente x?
            print(subtotaleVL)
            subtotaleInEuro = subtotaleVL
            clien1 = Cliente.query.filter_by(codiceCliente=cc).first()
            valClien = clien1.valutaCliente
            print(valClien)
            if valClien == 2:  # caso in cui il cliente paga in dollari
                if tipo == "BUDGET":
                    subtotaleInEuro = subtotaleInEuro * 0.94868  # conversione dollaro/euro a budget
                else:
                    subtotaleInEuro = subtotaleInEuro * 0.8338  # conversione dollaro/euro a consuntivo
            elif valClien == 3:  # caso in cui il cliente paga in yen
                if tipo == "BUDGET":
                    subtotaleInEuro = subtotaleInEuro * 0.0081300813  # conversione yen/euro a budget
                else:
                    subtotaleInEuro = subtotaleInEuro * 0.00740685875  # conversione yen/euro a consuntivo
            print(
                str(subtotaleInEuro) + " questo è il totale pagato a " + tipo + " dal cliente: " + str(cc) + " in Euro")
        else :
            flash('Inserisci un CODICE CLIENTE valido', category='error')
    """
    #versione funzionante: 1 (più lenta e lunga da scrivere) 
    vend3 = Vendita.query.filter_by(tipo=tipo, nrOrigine=cc).all()
    for i in range(len(vend3)):
        burner = str(vend3[i]) #trasformo il singolo elemento in stringa
        burnersplit = burner.split(" ")
        burner2 = burnersplit[1]
        burnersplit2 = burner2.split(">")
        codiceVenditaToSearch = burnersplit2[0]
        print(codiceVenditaToSearch)
        vendita = Vendita.query.filter_by(nrMovimentoV=codiceVenditaToSearch).first()
        vendz = vendita.importoVenditeVL
        subtotaleVL = subtotaleVL + vendz
        print(burner + " " + str(subtotaleVL))  #qua mi serve a capire se sta venendo aggiornato o meno!!!
    print(str(subtotaleVL) + " questo è il totale pagato a " + tipo + " dal cliente: " + str(cc))
    """


    return render_template("scostamenticliente.html")

@views.route('/scostamentiArticolo', methods=['GET','POST'])
def produzione():
    if request.method == 'POST':
        #definisco le variabili che mi servono per creare la tabella degli scostamenti
        vBudget = 0 #definisce il volume di tale prodotto a budget
        pBudget = 0.00
        vConsuntivo = 0
        pConsuntivo = 0.00
        qtaB = 0 #usata come sommatore e come variabile della seconda tabella dello scostamento
        costoMPB = 0.00
        qtaC = 0
        costoMPC = 0.00
        hpzB = 0.00
        hpzC = 0.00

        #creazione tabelle - prima fase leggere per l'articolo le cose da fare
        art = request.form.get('nrArticolo') #l'utente mi inserisce l'articolo e lo ho qua
        tipo = request.form.get('tipo') #questa verrà rimossa
        x = Vendita.query.filter_by(nrArticolo=art).first()
        if x:
            #-------------------TABELLA RICAVI --- legata al file excel Vendite --------------------------#
            artB = Vendita.query.filter_by(nrArticolo=art, tipo=tipo).all()
            print(artB)  # mi mostra tutte le vendita a TIPO per un determinato articolo
            # ora voglio contare la quantità totale di articoli venduti per trovare il Volume(Budget o consuntivo)
            for i in range(len(artB)):
                qtaB = qtaB + artB[i].qta
            vBudget = qtaB
            print(vBudget)
            # ora invece voglio trovare il prezzo di un singolo articolo --> leggi la prima vendita a BUDGET dell'articolo, prendi il prezzo, qta e il codice del cliente(in caso l'utente non pagasse in euro, fai la funzione qua sopra)
            pBudget = artB[0].importoVenditeVL
            print(str(pBudget) + " questo è il prezzo totale dei tot articoli, da sistemare ")
            qtaB = artB[0].qta
            pBudget = pBudget / qtaB
            print(str(pBudget) + "prezzo unitario in valuta locale")
            pBudget = conversioneValuta(pBudget, artB[0].nrOrigine, tipo)
            print(str(pBudget) + "prezzo unitario in euro")

            # -------------------TABELLA MP --- legata al file excel Consumi --------------------------#
            print("sono alla tabella mp, vediamo se ci sono dei records")
            artBB = Consumo.query.filter_by(nrArticolo=art, tipo=tipo).all()
            qtaB = 0
            for i in range(len(artBB)):
                qtaB = artBB[i].qtaC + qtaB
                costoMPB = artBB[i].importoTotaleC + costoMPB
            print(qtaB)
            print(costoMPB)
            print(artBB) #mi mostra tutti i consumi del determinato articolo

            #------------------TABELLA IMPIEGO ----- legata al file excel impiegoOrarioRisorse ---------#
            artBBB = Impiego.query.filter_by(nrArticolo=art, tipo=tipo).all()
            print(artBBB)
            #controllo per quante sezioni di produzione passa l'articolo
            odp = artBBB[0].nrODP
            artDipartimenti = Impiego.query.filter_by(nrArticolo=art,nrODP = odp, tipo = tipo).all()
            print(str(len(artDipartimenti)) + " numero dipartimenti per " + art)
            for i in range (len(artDipartimenti)) :
                print(artDipartimenti[i].descrizione +  " " + str(artDipartimenti[i].qtaOutput) + " " + str(artDipartimenti[i].tempoRisorsa))
            print(artDipartimenti)


            # -----------------TABELLA RISORSE ---- legata al file excel Risore ------------------------#
            print("prova per vedere se la tabella risorse funziona")
            queryy = Risorsa.query.all()
            print(queryy)

        else:
            flash('INSERIRE UN CODICE VALIDO!', category='error')

    return render_template("scostamentiArticolo.html")

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
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")

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
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")

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
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")

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
                                         nrDocumentoODP=nrDocumentoODP, qtaC=qta, importoTotaleC=importoTotaleC)
                    db.session.add(newConsumo)
                    db.session.commit()
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")

                print("---------------------------IMPIEGO----------------------------------")
                # leggo "impiegoOrarioRisorse" e riempio la tabella del database "Impiego"
                df = pd.read_excel('inputXLSX/impiegoOrarioRisorse.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella IMPIEGO ")
                for i in range(len(df)):
                    idImpiego = i
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
                    newImpiego = Impiego(idImpiego=idImpiego, nrArticolo=nrArticolo, tipo=tipo, nrODP=nrODP, descrizione=descrizione,
                                         areaProd=areaProd, risorsa=risorsa, tempoRisorsa=tempoRisorsa,
                                         qtaOutput=qtaOutput)
                    db.session.add(newImpiego)
                    db.session.commit()
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")

                print("---------------------------RISORSA----------------------------------")
                # leggo "Risorse" e riempio la tabella del database "Risorsa"
                df = pd.read_excel('inputXLSX/costoOrario.xlsx', index_col=0)
                print(" | " + str(len(df)) + " | " + " entries trovate per la tabella RISORSA ")
                for i in range(len(df)):
                    idRisorsa = i
                    codRisorsa = df.iloc[i, 0]
                    areaProd = df.iloc[i, 1]
                    costoOrarioBudget = str(df.iloc[i, 2])
                    costoOrarioBudget = costoOrarioBudget.replace(",", ".")
                    costoOrarioBudget = float(costoOrarioBudget)
                    costoOrarioConsuntivo = str(df.iloc[i, 3])
                    costoOrarioConsuntivo = costoOrarioConsuntivo.replace(",", ".")
                    costoOrarioConsuntivo = float(costoOrarioConsuntivo)
                    newRisorsa = Risorsa(idRisorsa=idRisorsa, codRisorsa=codRisorsa, areaProd=areaProd, costoOrarioBudget=costoOrarioBudget,
                                         costoOrarioConsuntivo=costoOrarioConsuntivo)
                    db.session.add(newRisorsa)
                    db.session.commit()
                print(" ----------> TABELLA RIEMPITA <-------------")
                print(" ")
            return
def conversioneValuta (prezzo, codiceCliente, tipo) :
    subtotaleInEuro = prezzo
    clien1 = Cliente.query.filter_by(codiceCliente=codiceCliente).first()
    valClien = clien1.valutaCliente
    print(" CONVERSIONE VALUTA ----> " + codiceCliente + " codice valuta: " + str(valClien))
    if valClien == 2:  # caso in cui il cliente paga in dollari
        if tipo == "BUDGET":
            subtotaleInEuro = subtotaleInEuro * 0.94868  # conversione dollaro/euro a budget
        else:
            subtotaleInEuro = subtotaleInEuro * 0.8338  # conversione dollaro/euro a consuntivo
    elif valClien == 3:  # caso in cui il cliente paga in yen
        if tipo == "BUDGET":
            subtotaleInEuro = subtotaleInEuro * 0.0081300813  # conversione yen/euro a budget
        else:
            subtotaleInEuro = subtotaleInEuro * 0.00740685875  # conversione yen/euro a consuntivo
    return subtotaleInEuro