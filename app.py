import pandas
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from geopy.geocoders import ArcGIS
nom = ArcGIS()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success_table',  methods=['POST'])
def success_table():
    global file
    if request.method == 'POST':
        try:
            file = request.files['file']
            data = pandas.read_csv(file)
        except:
            return render_template("index.html", text = "There's something wrong with your file, please double check it")    
        if "Address" in data:
            data["Latitude"] =  data["Address"].apply(nom.geocode).apply(lambda x: x.latitude if x != None else None)
            data["Longitude"] =  data["Address"].apply(nom.geocode).apply(lambda x: x.longitude if x != None else None)
            data.to_csv("data.csv")
            return render_template("index.html", btn = "download.html", text = data.to_html())
        return render_template("index.html", text = "Please make sure you have an address column in your CSV file!")
        

@app.route('/download')
def download():
    return send_file("data.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()