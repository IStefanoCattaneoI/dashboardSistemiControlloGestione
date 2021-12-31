from website import create_app

#quando inserisco i dati nel database disattivo la app sennò me le fa due volte
app = create_app()

if __name__ == '__main__':
    print("ciao")
    app.run(debug=True)  #ogni volta che salvo una modifica resetta il server