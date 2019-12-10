import os
import io
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug import secure_filename
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import numpy as np


# instancia del objeto Flask
app = Flask(__name__)
# Carpeta de subida
app.config['UPLOAD_FOLDER'] = './'

@app.route('/')
def index(): 
    return render_template('index.html')
    
@app.route('/obtener_csv',methods=['POST'])
def csv():
    if request.method == 'POST':
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        global df
        df = pd.read_csv(filename)
        global titulos
        titulos = list(df)
    return redirect(url_for('graficar'))

@app.route('/graficar')
def graficar():
    return render_template('graficar.html',titles=titulos )

@app.route('/graficar/seleccion',methods=['POST'])
def graficar_seleccion():
    global plot_url
    plt.clf()
    columna = request.form['columna']
    tipo = request.form['tipo']
    nombre = request.form['nombre']
    df_sub=df.iloc[0:10]
    if(tipo == 'Puntos'):
        img = io.BytesIO()
        plt.title("Gráfica: "+tipo+" Columna: "+columna)
        plt.plot(df_sub[columna],'--')
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
    if(tipo == 'Lineas'):
        img = io.BytesIO()
        plt.plot(df_sub[columna])
        plt.title("Gráfica: "+tipo+" Columna: "+columna)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
    if(tipo == 'Pastel'):
        img = io.BytesIO()
        plt.pie(df_sub[columna], labels=df_sub[columna], autopct="%0.1f %%")
        plt.title("Gráfica: "+tipo+" Columna: "+columna)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
    if(tipo == 'Barras'):
        img = io.BytesIO()
        plt.bar(df_sub['Rank'],df_sub[columna],align="center")
        plt.title("Gráfica: "+tipo+" Columna: "+columna)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
    return redirect(url_for('mostrar'))

@app.route('/mostrar')
def mostrar():
    imagen = os.path.join(app.config['UPLOAD_FOLDER'], 'grafica.png')
    return render_template('mostrar.html', imagen={ 'imagen': plot_url })

if __name__ == "__main__":
    app.run(debug=True)