from flask import Flask
from flask import render_template

app = Flask("__name__")


@app.route('/')
def hello_home():
    return render_template('index.html')

@app.route('/ects.html')
def hello_ects():
    return render_template('ects.html')

@app.route('/noten.html')
def hello_noten():
    return render_template('noten.html')

@app.route('/auswertung.html')
def hello_auswertung():
    return render_template('auswertung.html')



if __name__ == "__main__":
    app.run(debug=True, port=5000)