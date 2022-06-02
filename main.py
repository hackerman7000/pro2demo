from flask import Flask
from flask import render_template
from flask import request

import json

import plotly.express as px
from plotly.offline import plot

app = Flask("__name__")


@app.route('/', methods=["GET", "POST"])
def hello_home():
    # zwei leere Listen werden eröffnet. Diese werden auf der index.html Seite angezeigt
    module_pflicht = []
    module_wp = []

    # zwei leere Listen werden eröffnet. Diese werden mit den absolvierten modulen gefüllt und unten auf der index.html Seite angezeigt
    module_pflicht_absolviert = []
    module_wp_absolviert = []

    # die module werden aus der Datei module.json geladen als datei_inhalt.
    # falls das nicht klappt, wird eine leere Liste eröffnet
    try:
        with open("data/module.json", encoding="utf-8") as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    # die ECTS Punkte werden aus der Datei ects.json geladen als ects_inhalt
    # falls das nicht klappt, wird ein leeres Dictionary eröffnet
    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}

    # Alle elemente welche aus module.json geladen wurden, werden per for Schleife durchlaufen.
    # Falls das Modul die Modulgruppe "Pflicht" hat kommt es in die Liste "module_pflicht"
        # Sonst kommt es in die Liste "module_wp". wp steht für Wahlpflicht
    for element in datei_inhalt:
        if element["Modulgruppe"] == "Pflicht":
            module_pflicht.append(element["Modul"])
        else:
            module_wp.append(element["Modul"])

    for element in datei_inhalt:
        if element["Absolviert"] == True:
            if element["Modulgruppe"] == "Pflicht":
                module_pflicht_absolviert.append(element["Modul"])
            else:
                module_wp_absolviert.append(element["Modul"])

            # alt: module_wp.append([element["Modul"], element["Modulgruppe"]])

    # Wenn der "Zurücksetzen" Button geklickt wird, werden die Module alle auf false (nicht absolviert) gestellt
    # Zudem werden die ECTS aus ects.json auf den Startwert zurückgesetzt
    if request.method == 'POST':
        if request.form.get("zuruecksetzen") == "zuruecksetzen":
            for element in datei_inhalt:
                element["Absolviert"] = False
            ects_inhalt["ECTS"] = 180
            ects_inhalt["ECTS_UX_Gesamt"] = 8
            ects_inhalt["ECTS_UX_Major"] = 20
            ects_inhalt["ECTS_DI_Gesamt"] = 8
            ects_inhalt["ECTS_DI_Major"] = 20
            ects_inhalt["ECTS_IT_Gesamt"] = 8
            ects_inhalt["ECTS_IT_Major"] = 20
            ects_inhalt["ECTS_SM"] = 4


    # Die bearbeiteten Daten werden zurück in die json Files geladen
    # Somit speichert man die Module & ECTS Punkte auch, wenn das Programm geschlossen wird
    # mithilfe indent und seperators werden die Daten übersichtlich im json dargestellt
    with open("data/module.json", "w") as open_file:
        json.dump(datei_inhalt, open_file, indent=4, separators=(",", ":"))
    with open("data/ects.json", "w") as open_file:
        json.dump(ects_inhalt, open_file, indent=4, separators=(",", ":"))

    # return auf index.html und Übergabe der benötigten Werte
    return render_template('index.html', module_pflicht=module_pflicht, module_wp=module_wp, module_pflicht_absolviert=module_pflicht_absolviert, module_wp_absolviert=module_wp_absolviert)




@app.route('/ects.html', methods=['get', 'post'])
def hello_ects():
    # die module werden aus der Datei module.json geladen als datei_inhalt.
    # falls das nicht klappt, wird eine leere Liste eröffnet
    try:
        with open("data/module.json") as open_file:
            datei_inhalt = json.load(open_file)
    except FileNotFoundError:
        datei_inhalt = []

    # die ECTS Punkte werden aus der Datei ects.json geladen als ects_inhalt
    # falls das nicht klappt, wird ein leeres Dictionary eröffnet
    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}


    if request.method == 'POST':

        # Wenn ein Modul ausgewähl wurde wird der Wert (falls er noch False ist) von "Absolviert" auf True gesetzt
        # Zusätzlich wird der ECTS Wert des Moduls dem Gesamtwert der ECTS abgezogen
        for element in datei_inhalt:
            if request.form.get(element["Modul"]):
                if element["Absolviert"] == False:
                    element["Absolviert"] = True
                    ects_inhalt["ECTS"] = ects_inhalt["ECTS"] - element["ECTS"]
                    if element["Modulgruppe"] == "User Experience":
                        ects_inhalt["ECTS_UX_Gesamt"] = ects_inhalt["ECTS_UX_Gesamt"] - element["ECTS"]
                        ects_inhalt["ECTS_UX_Major"] = ects_inhalt["ECTS_UX_Major"] - element["ECTS"]
                    elif element["Modulgruppe"] == "Information Technology":
                        ects_inhalt["ECTS_IT_Gesamt"] = ects_inhalt["ECTS_IT_Gesamt"] - element["ECTS"]
                        ects_inhalt["ECTS_IT_Major"] = ects_inhalt["ECTS_IT_Major"] - element["ECTS"]
                    elif element["Modulgruppe"] == "Digital Innovation":
                        ects_inhalt["ECTS_DI_Gesamt"] = ects_inhalt["ECTS_DI_Gesamt"] - element["ECTS"]
                        ects_inhalt["ECTS_DI_Major"] = ects_inhalt["ECTS_DI_Major"] - element["ECTS"]
                    elif element["Modulgruppe"] == "Sozial- und Methodenkompetenz":
                        ects_inhalt["ECTS_SM"] = ects_inhalt["ECTS_SM"] - element["ECTS"]


        # Die bearbeiteten Daten werden zurück in die json Files geladen
        # Somit speichert man die Module & ECTS Punkte auch, wenn das Programm geschlossen wird
        # mithilfe indent und seperators werden die Daten übersichtlich im json dargestellt
        with open("data/module.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4, separators=(",", ":"))
        with open("data/ects.json", "w") as open_file:
            json.dump(ects_inhalt, open_file, indent=4, separators=(",", ":"))

    # return auf ects.html und Übergabe der benötigten Werte
    return render_template('ects.html', ECTS=ects_inhalt["ECTS"], ECTS_UX_Gesamt=ects_inhalt["ECTS_UX_Gesamt"], ECTS_IT_Gesamt=ects_inhalt["ECTS_IT_Gesamt"], ECTS_DI_Gesamt=ects_inhalt["ECTS_DI_Gesamt"], ECTS_SM=ects_inhalt["ECTS_SM"], ECTS_UX_Major=ects_inhalt["ECTS_UX_Major"], ECTS_IT_Major=ects_inhalt["ECTS_IT_Major"], ECTS_DI_Major=ects_inhalt["ECTS_DI_Major"])



@app.route('/auswertung.html')
def hello_auswertung():
    div = viz()

    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}

    return render_template('auswertung.html', viz_div=div)


def get_data():
    modulgruppen = ["User Experience", "Information Technology", "Digital Innovation"]
    absolvierte_ects = []
    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}

    for key, value in ects_inhalt.items():
        if "_Gesamt" in key:
            absolvierte_ects.append(8 - value)
    return modulgruppen, absolvierte_ects


def viz():
    modulgruppe, absolvierte_ects = get_data()
    fig = px.bar(x=modulgruppe, y=absolvierte_ects)
    fig.add_hrect(y0=0, y1=8, line_width=0, fillcolor="red", opacity=0.2, annotation_text="Minimum nicht erfüllt", annotation_position="top right")
    fig.add_hrect(y0=20, y1=40, line_width=0, fillcolor="green", opacity=0.2, annotation_text="Major erreicht", annotation_position="top right")
    div = plot(fig, output_type="div")

    return div


if __name__ == "__main__":
    app.run(debug=True, port=5000)
