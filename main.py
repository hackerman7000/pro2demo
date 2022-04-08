from flask import Flask
from flask import render_template
from flask import request

# nur funktion berechnungm mit dem . kommt man auf nächste ebene im ordner
from rechnen.steuern import berechnen

from rechnen.steuern import abgaben

from datetime import datetime

app = Flask(__name__)

# das Fragezeichen wird in der URL später eingegeben, das <eingabe> in der URL ist dynamisch
@app.route("/noten/<eingabe>")
def noten_eingabe(eingabe):
    print(eingabe)
    print(eingabe.split("WW"))
    teile = eingabe.split("WW")
    print(teile)
    student = teile[0]
    note = teile[1]
    daten.speichern("noten.json", student, note)
    return student + " " + note


@app.route("/about")
def about():
    return "about test"

@app.route("/")
def hello():
    if request.method.lower() == "get":
        return render_template("index.html", name="Fabian")
    if request.method.lower() == "post":
        name = request.form['vorname']
        return name

@app.route('/form', methods=["get", "post"])
def form():
    return render_template('formular.html')

@app.route("/list")
def auflistung():
    elemente = ["Bla", "Hallo", "heloo"]
    return render_template("liste.html", html_elemente=elemente)

@app.route("/table")
def tabelle():
    biere = [
    {
        "name": "Glatsch",
        "herkunft": "Chur",
        "vol": 4.0,
        "brauerei": "Calanda",
        "preis": 1.00
    },
    {
        "name": "Retro",
        "herkunft": "Luzern",
        "vol": 4.2,
        "brauerei": "Eichhof",
        "preis": 2.00
    }
    ]
    for bier in biere:
        preis = bier["preis"]
        tax = berechnen(preis)
        # da funktion steuern in datei steuern
        bier["steuern"] = tax

    table_header = ["Name", "Herkunft", "Vol%", "Brauerei", "Preis", "Steuern"]
    return render_template("beer.html", beers=biere, header=table_header)

@app.route("/abgaben", methods=["get", "post"])
# funktion abgaben wurde oben importiert aus steuern
def egal():
    if request.method.lower() == "get":
        return render_template("preis.html")
    if request.method.lower() == "post":
        preis = request.form['preis']
        preis = float(preis)
        abgaben_betrag = abgaben(preis)

        now = datetime.now()
        with open("jail_free_card.txt", "a", encoding="utf-8") as offene_datei:
            offene_datei.write(f"{now},{preis},{abgaben_betrag}\n")
        return render_template("preis.html", abgabe=abgaben_betrag)


    abgaben_betrag = abgaben(preis)
    return render_template("preis.html", abgabe=abgaben_betrag)

@app.route("/datum")
def datum_anzeigen():
    with open("jail_free_card.txt", encoding="utf-8") as open_file:
        inhalt = open_file.read()
    return inhalt.replace("\n", "<br>")


if __name__ == "__main__":
    app.run(debug=True, port=5000)


