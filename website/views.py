#in views definiamo le routes

from flask import Blueprint, render_template, request, redirect, url_for, flash
import pandas as pd
from website import db
from website.models import Cliente, Valuta, Vendita, Consumo, Impiego, Risorsa
#from . import db


views = Blueprint('views', __name__)

@views.route('/s')
def fai():

    print("proviamo il distinct")
    lista = db.session.query(Vendita.nrArticolo).distinct().all()
    print(lista)
    print(" quanti articoli ho: " + str(len(lista)))
    #QUA SI DEVE FARE SIA A BUDGET CHE A CONSUNTIVO RIPETERE x2
    qtaBudget = 0 #qtaTOTALE RIGA D8 exe scostamenti
    listaPrezziBudget = []
    listaQuantitaBudget = []
    mixBudget = []
    for i in range(len(lista)) : #for con il distinct
        #
        qtasingola = 0
        prezzosingolo = 0.00
        prezzotot = 0.00
        volume = 0
        tipo = "BUDGET"
        arttocheck = lista[i].nrArticolo
        #
        print("TABELLA RICAVI => " + tipo + " => " + arttocheck)
        artB = Vendita.query.filter_by(nrArticolo=arttocheck, tipo=tipo).all()
        for j in range(len(artB)): #for con il group by
            qtasingola = qtasingola + artB[j].qta
            prezzosingolo = artB[j].importoVenditeVL
            prezzosingolo = conversioneValuta(prezzosingolo, artB[j].nrOrigine, tipo)
            prezzotot = prezzotot + prezzosingolo
        volume = qtasingola
        listaQuantitaBudget.append(volume)
        prezzotot = prezzotot/volume #questo sarebbe il prezzo unitario, non cambio variabile
        listaPrezziBudget.append(prezzotot)
        qtaBudget = qtaBudget + volume
        print(str(volume) + "  " + str(round(prezzotot, 2)))
    print("TOTALE QUANTITA' TUTTI ARTICOLI => " + str(qtaBudget))

    #QUA CALCOLIAMO IL MIX
    for i in range(len(lista)) : #for per trovare il mix
        mixBudget.append((listaQuantitaBudget[i] / qtaBudget)*100)
        print(str(round(mixBudget[i],3)) + " %" + "  |  " + lista[i].nrArticolo)

    #QUA CALCOLIAMO IL RICAVO TOTALE
    ricavoBudget = 0.00
    for i in range(len(lista)) :
        ricavoBudget = ricavoBudget + listaQuantitaBudget[i]*listaPrezziBudget[i]
    print(" RICAVI TOTALI: " + " a " + tipo + "  =>  " + str(round(ricavoBudget, 2)))

    print()
    print()
    #PARTE A CONSUNTIVO: QUARTA COLONNA DI EXCEL
    qtaCons = 0  # qtaTOTALE RIGA J8 exe scostamenti
    listaPrezziCons = []
    listaQuantitaCons = []
    mixCons = []
    for i in range(len(lista)):  # for con il distinct
        #
        qtasingola = 0
        prezzosingolo = 0.00
        prezzotot = 0.00
        volume = 0
        tipo = "Consuntivo"
        arttocheck = lista[i].nrArticolo
        #
        print("TABELLA RICAVI => " + tipo + " => " + arttocheck)
        artB = Vendita.query.filter_by(nrArticolo=arttocheck, tipo=tipo).all()
        for j in range(len(artB)):  # for con il group by
            qtasingola = qtasingola + artB[j].qta
            prezzosingolo = artB[j].importoVenditeVL
            prezzosingolo = conversioneValuta(prezzosingolo, artB[j].nrOrigine, tipo)
            prezzotot = prezzotot + prezzosingolo
        volume = qtasingola
        listaQuantitaCons.append(volume)
        prezzotot = prezzotot / volume  # questo sarebbe il prezzo unitario, non cambio variabile
        listaPrezziCons.append(prezzotot)
        qtaCons = qtaCons + volume
        print(str(volume) + "  " + str(round(prezzotot, 2)))
    print("TOTALE QUANTITA' TUTTI ARTICOLI => " + str(qtaCons))

    # QUA CALCOLIAMO IL MIX
    for i in range(len(lista)):  # for per trovare il mix
        mixCons.append((listaQuantitaCons[i] / qtaCons) * 100)
        print(str(round(mixCons[i], 3)) + " %" + "  |  " + lista[i].nrArticolo)

    # QUA CALCOLIAMO IL RICAVO TOTALE CONSUNTIVO
    ricavoCons = 0.00
    for i in range(len(lista)):
        ricavoCons = ricavoCons + listaQuantitaCons[i] * listaPrezziCons[i]
    print(" RICAVI TOTALI: " + " a " + tipo + "  =>  " + str(round(ricavoCons, 2)))


    # MIX STANDARD!!!
    qtaTotStandard = qtaCons
    listaQuantitaMixStd = []
    for i in range(len(lista)) :
        listaQuantitaMixStd.append((qtaTotStandard*mixBudget[i])/100)
        print(str(round(listaQuantitaMixStd[i])))
    ricaviMixStd = 0.00
    for i in range(len(lista)) :
        ricaviMixStd = ricaviMixStd + listaQuantitaMixStd[i] *listaPrezziBudget[i]
    print(" RICAVI TOTALI MIX STANDARD => " + str(round(ricaviMixStd,2)))


    #MIX EFFETTIVO!!!
    qtatotEffettiva = qtaCons
    mixMixEffettivo = []
    for i in range(len(lista)):
        mixMixEffettivo.append((listaQuantitaCons[i]/qtatotEffettiva)*100)
        print(str(round(mixMixEffettivo[i],3)) + " %" + "  |  " + lista[i].nrArticolo)
    ricaviMixEffettivo = 0.00
    for i in range(len(lista)):
        ricaviMixEffettivo = ricaviMixEffettivo + listaQuantitaCons[i] * listaPrezziBudget[i]
    print(" RICAVI TOTALI MIX EFFETTIVO => " + str(round(ricaviMixEffettivo)))
    print()
    print(" TABELLA RICAVI ")
    print(" ricavi budget => " + str(round(ricavoBudget)) + "  |  " + " ricavi mix std => " + str(round(ricaviMixStd)) + "  |  " +  " ricavi mix effettivo => " + str(round(ricaviMixEffettivo)) + "  |  " + " ricavi consuntivo => " + str(round(ricavoCons)))
    print()
    print()

    #COSTI VARIABILI --- PARTE BUDGET
    listaCostiUnitariMPBudget = []
    listaCostiUnitariLAVBudget = []
    listaCostiUnitariBudget = []
    for i in range(len(lista)):  #for con il distinct
        tipo = "BUDGET"
        arttocheck = lista[i].nrArticolo
        #cerco tutti i consumi dell'articolo che sto controllando => MATERIE PRIME
        artC = Consumo.query.filter_by(tipo=tipo,nrArticolo = arttocheck).all()
        costoUnitarioSomma = 0.00
        for j in range(len(artC)) : #TROVIAMO IL COSTO UNITARIO PER PRODOTTO DELLE MP facendo costo totale / quantita
            costoUnitarioSomma = costoUnitarioSomma + (artC[j].importoTotaleC/listaQuantitaBudget[i])
        listaCostiUnitariMPBudget.append(costoUnitarioSomma)

        #cerco gli impieghi dell'articolo => LAVORAZIONE
        costoOrarioSommaUnita = 0
        artCC = Impiego.query.filter_by(tipo=tipo, nrArticolo = arttocheck).all()
        for j in range(len(artCC)):#TROVIAMO COSTO UNITARIO DELLA LAVORAZIONE
            areaProdToCheck = artCC[j].areaProd
            risToCheck = artCC[j].risorsa
            #facciamo l'accesso alla tabella risorsa per la singola riga
            risorsaUsata = Risorsa.query.filter_by(codRisorsa=risToCheck, areaProd = areaProdToCheck).first()
            #siccome siamo a budget piglio la colonna euro a budget
            euroAllOra = risorsaUsata.costoOrarioBudget
            if artCC[j].qtaOutput != 0:
                costoOrarioSommaUnita = costoOrarioSommaUnita + ((euroAllOra*artCC[j].tempoRisorsa)/artCC[j].qtaOutput)
        listaCostiUnitariLAVBudget.append(costoOrarioSommaUnita)
        listaCostiUnitariBudget.append(listaCostiUnitariLAVBudget[i]+listaCostiUnitariMPBudget[i])
        print(arttocheck + "  |  " + "costo unitario MP => " + str(round(listaCostiUnitariMPBudget[i], 2)) + "  |  "  + " costo unitario LAV =>" + str(round(listaCostiUnitariLAVBudget[i],2)) + "  ==> COSTO UNITARIO PRODOTTO: "+ str(round(listaCostiUnitariBudget[i],2)))

    print()
    print()

    #COSTI VARIABILI --- PARTE CONSUNTIVO
    listaCostiUnitariMPCons = []
    listaCostiUnitariLAVCons = []
    listaCostiUnitariCons = []
    for i in range(len(lista)):  #for con il distinct
        tipo = "CONSUNTIVO"
        arttocheck = lista[i].nrArticolo
        #cerco tutti i consumi dell'articolo che sto controllando => MATERIE PRIME
        artC = Consumo.query.filter_by(tipo=tipo,nrArticolo = arttocheck).all()
        costoUnitarioSomma = 0.00
        for j in range(len(artC)) : #TROVIAMO IL COSTO UNITARIO PER PRODOTTO DELLE MP facendo costo totale / quantita
            costoUnitarioSomma = costoUnitarioSomma + (artC[j].importoTotaleC/listaQuantitaCons[i])
        listaCostiUnitariMPCons.append(costoUnitarioSomma)

        #cerco gli impieghi dell'articolo => LAVORAZIONE
        costoOrarioSommaUnita = 0
        artCC = Impiego.query.filter_by(tipo=tipo, nrArticolo = arttocheck).all()
        for j in range(len(artCC)):#TROVIAMO COSTO UNITARIO DELLA LAVORAZIONE
            areaProdToCheck = artCC[j].areaProd
            risToCheck = artCC[j].risorsa
            #facciamo l'accesso alla tabella risorsa per la singola riga
            risorsaUsata = Risorsa.query.filter_by(codRisorsa=risToCheck, areaProd = areaProdToCheck).first()
            #siccome siamo a consuntivo piglio la colonna euro a consuntivo
            euroAllOra = risorsaUsata.costoOrarioConsuntivo
            if artCC[j].qtaOutput != 0:
                costoOrarioSommaUnita = costoOrarioSommaUnita + ((euroAllOra*artCC[j].tempoRisorsa)/artCC[j].qtaOutput)
        listaCostiUnitariLAVCons.append(costoOrarioSommaUnita)
        listaCostiUnitariCons.append(listaCostiUnitariLAVCons[i]+listaCostiUnitariMPCons[i])
        print(arttocheck + "  |  " + "costo unitario MP => " + str(round(listaCostiUnitariMPCons[i], 2)) + "  |  "  + " costo unitario LAV =>" + str(round(listaCostiUnitariLAVCons[i],2)) + "  ==> COSTO UNITARIO PRODOTTO: "+ str(round(listaCostiUnitariCons[i],2)))


    #CVTot = costi variabili totali!!! => qta * costo unitario
    cvTotBudget = 0.00
    cvTotMixStd = 0.00
    cvTotMixEffettivo = 0.00
    cvTotConsuntivo = 0.00
    for i in range(len(lista)):
        cvTotBudget = cvTotBudget + listaQuantitaBudget[i]*listaCostiUnitariBudget[i]
        cvTotMixStd = cvTotMixStd + listaQuantitaMixStd[i]*listaCostiUnitariBudget[i]
        cvTotMixEffettivo = cvTotMixEffettivo + listaQuantitaCons[i]*listaCostiUnitariBudget[i]
        cvTotConsuntivo = cvTotConsuntivo + listaQuantitaCons[i]*listaCostiUnitariCons[i]
    #calcolo => MOL
    molBudget =ricavoBudget- cvTotBudget
    molMixStd =ricaviMixStd-cvTotMixStd
    molMixEff =ricaviMixEffettivo -cvTotMixEffettivo
    molCons = ricavoCons-cvTotConsuntivo
    #calcolo scostamenti ricavi
    sRBudgetMixStd = ricaviMixStd-ricavoBudget
    sRMixStdMixEff = ricaviMixEffettivo-ricaviMixStd
    sRMixEffCons = ricavoCons - ricaviMixEffettivo
    #calcolo scostamenti costi
    sCBudgetMixStd = cvTotMixStd - cvTotBudget
    sCMixStdMixEff = cvTotMixEffettivo - cvTotMixStd
    scMixEffCons = cvTotConsuntivo - cvTotMixEffettivo
    #calcolo scostamenti MOL
    sBudgetMixStd = molMixStd-molBudget
    sMixStdMixEff = molMixEff-molMixStd
    sMixEffCons = molCons - molMixEff
    print()
    print(" -------------------BUDGET -------------------------")
    print(" RICAVI TOTALI => " + str(round(ricavoBudget)))
    print(" COSTI VARIABILI TOTALI  ==> " + str(round(cvTotBudget)))
    print(" MARGINE OPERATIVO LORDO ==> " + str(round(molBudget)))
    print(" -----------------------------------------------------------")
    print(" SCOSTAMENTI TRA BUDGET / MIXSTD (R/C/MOL) ==> " + str(round(sRBudgetMixStd)) + " | "  + str(round(sCBudgetMixStd)) + " | "  + str(round(sBudgetMixStd)))
    print(" -----------------------------------------------------------")

    print()
    print(" ------------------- MIX STD -------------------------")
    print(" RICAVI TOTALI  => " + str(round(ricaviMixStd)))
    print(" COSTI VARIABILI TOTALI  ==> " + str(round(cvTotMixStd)))
    print(" MARGINE OPERATIVO LORDO ==> " + str(round(molMixStd)))
    print(" -----------------------------------------------------------")
    print(" SCOSTAMENTI TRA MIX STD / MIX EFF (R/C/MOL) ==> " + str(round(sRMixStdMixEff)) + " | " + str(round(sCMixStdMixEff)) + " | "+ str(round(sMixStdMixEff)))
    print(" -----------------------------------------------------------")

    print()
    print(" ------------------- MIX EFF -------------------------")
    print(" RICAVI TOTALI  => " + str(round(ricaviMixEffettivo)))
    print(" COSTI VARIABILI TOTALI  ==> " + str(round(cvTotMixEffettivo)))
    print(" MARGINE OPERATIVO LORDO ==> " + str(round(molMixEff)))
    print(" -----------------------------------------------------------")
    print(" SCOSTAMENTI TRA MIX EFF / CONSUNTIVO (R/C/MOL) ==> " + str(round(sRMixEffCons)) + " | " + str(round(scMixEffCons)) + " | " + str(round(sMixEffCons)))
    print(" -----------------------------------------------------------")

    print()
    print(" ------------------- CONSUNTIVO -------------------------")
    print(" RICAVI TOTALI  => " + str(round(ricavoCons)))
    print(" COSTI VARIABILI TOTALI  ==> " + str(round(cvTotConsuntivo)))
    print(" MARGINE OPERATIVO LORDO ==> " + str(round(molCons)))
    print(" -----------------------------------------------------------")

    return render_template("base.html")


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

    return render_template("scostamenticliente.html")

@views.route('/scostamentiArticolo', methods=['GET','POST'])
def produzione():
    if request.method == 'POST':
        print("")
        print()
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
            print( "TABELLA RICAVI => " + tipo)
            artB = Vendita.query.filter_by(nrArticolo=art, tipo=tipo).all()
            print(artB)  # mi mostra tutte le vendita a TIPO per un determinato articolo
            # ora voglio contare la quantità totale di articoli venduti per trovare il Volume(Budget o consuntivo)
            for i in range(len(artB)):
                qtaB = qtaB + artB[i].qta
            vBudget = qtaB
            print(str(vBudget) + " => " + art + " venduti")
            # ora invece voglio trovare il prezzo di un singolo articolo --> leggi la prima vendita a BUDGET dell'articolo, prendi il prezzo, qta e il codice del cliente(in caso l'utente non pagasse in euro, fai la funzione qua sopra)
            pBudget = artB[0].importoVenditeVL
            print(str(pBudget) + " => prezzo totale dei tot articoli, da sistemare ")
            qtaB = artB[0].qta
            pBudget = pBudget / qtaB
            print(str(pBudget) + " => prezzo unitario in valuta locale")
            pBudget = conversioneValuta(pBudget, artB[0].nrOrigine, tipo)
            print(str(pBudget) + " => prezzo unitario in euro")
            print()
            print()

            # -------------------TABELLA MP --- legata al file excel Consumi --------------------------#
            print(" TABELLA MP => " + tipo)
            artBB = Consumo.query.filter_by(nrArticolo=art, tipo=tipo).all()
            qtaB = 0
            for i in range(len(artBB)):
                qtaB = artBB[i].qtaC + qtaB
                costoMPB = artBB[i].importoTotaleC + costoMPB
            print(str(qtaB) + " => totale materie prime usate: non separato!! ")
            print(str(costoMPB) + " => costo totale materie prime: non separato!!" )
            print(artBB) #mi mostra tutti i consumi del determinato articolo
            print()
            print()

            #------------------TABELLA IMPIEGO + RISORSE?----- legata al file excel impiegoOrarioRisorse e CostoRisors---------#
            print(" TABELLA LAVORO => " + tipo)
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

@views.route('/modifica')
def modify():
    #modificare il tipo dell'art 841 e 814 a consuntivo basandoci sul nrMovimento
    tochange = 'Consuntivo'
    db.session.query(Vendita).filter(Vendita.nrMovimentoV == 35089).update({'tipo': tochange})
    db.session.commit()
    query = Vendita.query.filter_by(nrMovimentoV = 35089).first()
    print(query.tipo)

    #altro articolo

    db.session.query(Vendita).filter(Vendita.nrMovimentoV == 35550).update({'tipo': tochange})
    db.session.commit()
    query = Vendita.query.filter_by(nrMovimentoV = 35550).first()
    print(query.tipo)

    return render_template("base.html")

def conversioneValuta (prezzo, codiceCliente, tipo) :
    subtotaleInEuro = prezzo
    clien1 = Cliente.query.filter_by(codiceCliente=codiceCliente).first()
    valClien = clien1.valutaCliente
    #print(" CONVERSIONE VALUTA ----> " + codiceCliente + " codice valuta: " + str(valClien))
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

def CalcoloRisorsa (tempoImpiegato, tipo, ris, aProd) :
    return


