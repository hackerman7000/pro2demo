from flask import Flask
from flask import render_template
from flask import request

import plotly.express as px
from plotly.offline import plot


app = Flask("__name__")

# dict wird erstellt, pro modul wird noch ein unter-dict eingebaut mit den Werten für die Berechung für die ECTS
#
faecher = {
    "englischb2": {"ects": 4, "gruppe": "pflicht"},
    "softskills1": {"ects": 4, "gruppe": "pflicht"},
    "wiar": {"ects": 4, "gruppe": "pflicht"},
    "math": {"ects": 4, "gruppe": "pflicht"},
    "bwl": {"ects": 4, "gruppe": "pflicht"},
    "designthinking": {"ects": 4, "gruppe": "pflicht"},
    "ebus": {"ects": 4, "gruppe": "pflicht"},
    "recht": {"ects": 4, "gruppe": "pflicht"},
    "statistik": {"ects": 4, "gruppe": "pflicht"},
    "prog1": {"ects": 4, "gruppe": "pflicht"},
    "prog2": {"ects": 4, "gruppe": "pflicht"},
    "aris": {"ects": 4, "gruppe": "pflicht"},
    "markom": {"ects": 4, "gruppe": "pflicht"},
    "prototyping": {"ects": 4, "gruppe": "pflicht"},
    "sgdu": {"ects": 4, "gruppe": "pflicht"},
    "softskills2": {"ects": 4, "gruppe": "pflicht"},
    "reque": {"ects": 4, "gruppe": "pflicht"},
    "dima": {"ects": 4, "gruppe": "pflicht"},
    "pro1": {"ects": 4, "gruppe": "pflicht"},
    "pro2": {"ects": 4, "gruppe": "pflicht"},
    "hci": {"ects": 4, "gruppe": "pflicht"},
    "masofo": {"ects": 4, "gruppe": "pflicht"},
    "ecommerce": {"ects": 4, "gruppe": "pflicht"},
    "bpe": {"ects": 4, "gruppe": "pflicht"},
    "unternehmensprojekt": {"ects": 4, "gruppe": "pflicht"},
    "thesis": {"ects": 4, "gruppe": "pflicht"},

           }

@app.route('/')
def hello_home():
    return render_template('index.html')

@app.route('/ects.html', methods=['get', 'post'])
def hello_ects():
    if request.method =='POST':

        # Liste L wird erstellt, Module werden falls angewählt in die Liste aufgenommen
        L = []
        ECTS = 180
        ECTS_UX = 8
        ECTS_UX_Major = 20
        ECTS_DI = 8
        ECTS_DI_Major = 20
        ECTS_IT = 8
        ECTS_IT_Major = 20
        ECTS_SM = 4


        for key, value in faecher.items():
            if request.form.get(key):
                print("TRUE")
                # Modul wird in die Liste L gespeichert
                L.append(key)
                ECTS = ECTS - faecher[key]["ects"]



    return render_template('ects.html', liste=L, ECTS = ECTS)

@app.route('/noten.html')
def hello_noten():
    return render_template('noten.html')


def get_data():
    modulgruppen = ["UX", "IT", "DI", "SM"]
    absolvierte_ects = [4, 0, 0, 0]
    return modulgruppen, absolvierte_ects

def viz():
    modulgruppe, absolvierte_ects = get_data()
    fig = px.bar(x=modulgruppe, y=absolvierte_ects)
    div = plot(fig, output_type="div")
    return div


@app.route('/auswertung.html')
def hello_auswertung():
    div = viz()
    return render_template('auswertung.html', viz_div=div)



if __name__ == "__main__":
    app.run(debug=True, port=5000)