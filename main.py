# Flask importieren
from flask import Flask
from flask import render_template
from flask import request

# JSON importieren
import json

# Plotly importieren
import plotly.express as px
from plotly.offline import plot

app = Flask("__name__")


# Startseite
@app.route('/', methods=["GET", "POST"])
def hello_home():
    # zwei leere Listen werden eröffnet. Diese werden auf der index.html Seite angezeigt
    module_pflicht = []
    module_wp = []

    # zwei leere Listen werden eröffnet.
    # Diese werden mit den absolvierten modulen gefüllt und unten auf der index.html unten Seite angezeigt
    module_pflicht_absolviert = []
    module_wp_absolviert = []

    # die module werden aus der Datei module.json geladen als datei_inhalt.
    # falls das nicht klappt, wird eine leere Liste eröffnet
    try:
        with open("data/module.json", encoding="utf8") as open_file:
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

    # Alle elemente welche aus module.json geladen wurden, werden per for Schleife iteriert.
    for element in datei_inhalt:
        # Falls das Modul die Modulgruppe "Pflicht" hat kommt es in die Liste "module_pflicht"
        # Dabei wird nur der Modulname in die Liste gespeichert, da später nur dieser auf der Startseite aufgegeben wird
        if element["Modulgruppe"] == "Pflicht":
            module_pflicht.append(element["Modul"])
        # Sonst kommt es in die Liste "module_wp". wp steht für Wahlpflicht
        else:
            module_wp.append(element["Modul"])

    # Die Gleiche for Schleife wird nochmals durchlaufen.
    for element in datei_inhalt:
        # Jetzt die absolvierten Module zusätzlich in die
        # Listen "module_pflicht_absolviert" und "module_wp_absolviert" gespeichert
        if element["Absolviert"]:
            if element["Modulgruppe"] == "Pflicht":
                module_pflicht_absolviert.append(element["Modul"])
            else:
                module_wp_absolviert.append(element["Modul"])

        # Wenn der "Zurücksetzen" Button geklickt wird, werden die Module alle auf false (nicht absolviert) gestellt
        if request.method == 'POST':
            if request.form.get("zuruecksetzen") == "zuruecksetzen":
                for element in datei_inhalt:
                    element["Absolviert"] = False
                # die ECTS aus ects.json werden zudem auf den Startwert zurückgesetzt
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
    with open("data/module.json", "w", encoding="utf8") as open_file:
        json.dump(datei_inhalt, open_file, indent=4, separators=(",", ":"), ensure_ascii=False)
    with open("data/ects.json", "w") as open_file:
        json.dump(ects_inhalt, open_file, indent=4, separators=(",", ":"), ensure_ascii=False)

    # return auf index.html und Übergabe der benötigten Werte
    return render_template('index.html', module_pflicht=module_pflicht, module_wp=module_wp,
                           module_pflicht_absolviert=module_pflicht_absolviert,
                           module_wp_absolviert=module_wp_absolviert)


# Seite "ECTS"
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
        for element in datei_inhalt:
            if request.form.get(element["Modul"]):

                # Durch diese if Abfrage wird verhindert, dass ein Modul mehrmals ausgewählt wird
                if not element["Absolviert"]:
                    element["Absolviert"] = True

                    # Der ECTS Wert des Moduls wird dem Wert "ECTS"
                    # und dem ECTS_Wert der jeweiligen Modulgruppe abgezogen
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
    return render_template('ects.html', ECTS=ects_inhalt["ECTS"], ECTS_UX_Gesamt=ects_inhalt["ECTS_UX_Gesamt"],
                           ECTS_IT_Gesamt=ects_inhalt["ECTS_IT_Gesamt"], ECTS_DI_Gesamt=ects_inhalt["ECTS_DI_Gesamt"],
                           ECTS_SM=ects_inhalt["ECTS_SM"], ECTS_UX_Major=ects_inhalt["ECTS_UX_Major"],
                           ECTS_IT_Major=ects_inhalt["ECTS_IT_Major"], ECTS_DI_Major=ects_inhalt["ECTS_DI_Major"])


# Seite "Auswertung"
@app.route('/auswertung.html')
def hello_auswertung():
    # "div" wird eröffnet. Dieses wird im return dann als viz_div übergeben
    div = viz()

    # return auf auswertung.html und Übergabe des Diagramms
    return render_template('auswertung.html', viz_div=div)


# Hier werden die Daten für das Diagramm aus Plotly definiert
def get_data():
    # die Modulgruppen werden hier definiert und sind fix, deshalb können sie hart codiert eingegeben werden
    modulgruppen = ["User Experience", "Information Technology", "Digital Innovation"]

    # Eine leere Liste wird eröffnet, in welche die ECTS-Werte aus "ects.json" dynamisch geladen werden
    absolvierte_ects = []

    # die ECTS Punkte werden aus der Datei ects.json geladen als ects_inhalt
    # falls das nicht klappt, wird ein leeres Dictionary eröffnet
    try:
        with open("data/ects.json") as open_file:
            ects_inhalt = json.load(open_file)
    except FileNotFoundError:
        ects_inhalt = {}

    # Damit nur die gewünschten Werte geladen werden, wird mit einer if Abfrage sichergestellt,
    # dass nur die Werte welche "_Gesamt" enthalten geladen werden
    for key, value in ects_inhalt.items():
        if "_Gesamt" in key:
            # Diese drei Werte werden umgerechnet, damit man sie in der Grafik richtig anzeigen kann
            # und in die Liste "absolvierte_ects" geladen
            absolvierte_ects.append(8 - value)
    return modulgruppen, absolvierte_ects


# Das Plotly Diagramm wird hier erstellt
def viz():
    modulgruppe, absolvierte_ects = get_data()

    # Die Modulgruppen bilden die x-Achse und die ECTS Punkte die y-Achse
    fig = px.bar(x=modulgruppe, y=absolvierte_ects)

    # Gestaltung des Diagramms. Roter (Minimum ECTS) und Grüner Bereich (Major) wird ins Diagramm hinzugefügt
    # Quellen für Diagrammgestaltung:
    # https://plotly.com/python/styling-plotly-express/ und https://plotly.com/python/figure-labels/
    fig.add_hrect(y0=0, y1=8, line_width=0, fillcolor="red", opacity=0.2, annotation_text="Minimum nicht erfüllt",
                  annotation_position="top right")
    fig.add_hrect(y0=20, y1=40, line_width=0, fillcolor="green", opacity=0.2, annotation_text="Major erreicht",
                  annotation_position="top right")
    fig.update_layout(
        xaxis_title="Modulgruppen",
        yaxis_title="ECTS-Punkte",
    )

    div = plot(fig, output_type="div")

    # Übergabe des Diagrams
    return div


if __name__ == "__main__":
    app.run(debug=True, port=5000)
