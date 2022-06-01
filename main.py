from flask import Flask
from flask import render_template
from flask import request

import json

import plotly.express as px
from plotly.offline import plot

app = Flask("__name__")

# dict wird erstellt, pro modul wird noch ein unter-dict eingebaut mit den Werten für die Berechung für die ECTS
#
faecher = {
    "englischb2": {"ects": 4, "gruppe": "pflicht"},
}


@app.route('/', methods=["GET", "POST"])
def hello_home():
    module_pflicht = []
    module_wp = []
    try:
        with open("data/module.json") as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}

    for element in datei_inhalt:
        if element["Modulgruppe"] == "Pflicht":
            module_pflicht.append(element["Modul"])
        else:
            module_wp.append([element["Modul"], element["Modulgruppe"]])

    if request.method == 'POST':
        if request.form.get("zuruecksetzen") == "zuruecksetzen":
            for element in datei_inhalt:
                element["Absolviert"] = False
            ects_inhalt["ECTS"] = 180

    with open("data/module.json", "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4, separators=(",", ":"))
    with open("data/ects.json", "w") as open_file:
        json.dump(ects_inhalt, open_file, indent=4, separators=(",", ":"))


    return render_template('index.html', module_pflicht=module_pflicht, module_wp=module_wp)




@app.route('/ects.html', methods=['get', 'post'])
def hello_ects():
    try:
        with open("data/module.json") as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}


    global L
    global ECTS

    if request.method == 'POST':
        print("Weiter wurde RICHTIG gedrückt")
        # Liste L wird erstellt, Module werden falls angewählt in die Liste aufgenommen
        L = []

        # ECTS-Punke fürs Studium und die einzelnen Module, um damit den Fortschritt berechnen zu können
       # ECTS = 180
       #  ECTS_UX = 8
       #  ECTS_UX_Major = 20
       #  ECTS_DI = 8
       #  ECTS_DI_Major = 20
       #  ECTS_IT = 8
       #  ECTS_IT_Major = 20
       #  ECTS_SM = 4

        for element in datei_inhalt:
            if request.form.get(element["Modul"]):
                if element["Absolviert"] == False:
                    print("element erkannt: " + element["Modul"])
                    element["Absolviert"] = True
                    ects_inhalt["ECTS"] = ects_inhalt["ECTS"] - element["ECTS"]


        with open("data/module.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4, separators=(",", ":"))
        with open("data/ects.json", "w") as open_file:
            json.dump(ects_inhalt, open_file, indent=4, separators=(",", ":"))

    return render_template('ects.html', ECTS=ects_inhalt["ECTS"])

@app.route('/noten.html')
def hello_noten():
    return render_template('noten.html')


@app.route('/auswertung.html')
def hello_auswertung():
    div = viz()
    return render_template('auswertung.html', viz_div=div)


def get_data():
    modulgruppen = ["UX", "IT", "DI", "SM"]
    absolvierte_ects = [4, 0, 0, 0]
    return modulgruppen, absolvierte_ects


def viz():
    modulgruppe, absolvierte_ects = get_data()
    fig = px.bar(x=modulgruppe, y=absolvierte_ects)
    div = plot(fig, output_type="div")
    return div


if __name__ == "__main__":
    app.run(debug=True, port=5000)
