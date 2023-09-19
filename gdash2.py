import dash
from dash import dcc,html
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

#from dash import Input , Output ,State, no_update
#import plotly.graph_objs as go
#import pandas as pd
#from datetime import datetime, timedelta
#from dash import dash_table
#import json
# import plotly.express as px
 
load_figure_template('slate')

app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.SLATE])

#SOLAR
#Veo los .json
from glob import glob

import sensores_callbacks



# def get_data_files_names():

#     dataList = glob('data/*.json')
#     names = [d.split('\\')[-1].split('.')[0]
#                     for d in dataList]
#     return dataList,names

# dl,names=get_data_files_names()
# namesS = [str(elemento) for elemento in names]


app.layout = html.Div(
[
    dcc.Interval(
        id='intervalo-actualizacion',
        interval=20*1000,  # Intervalo en milisegundos (en este caso, cada segundo)
        n_intervals=0  # Valor inicial de n_intervals
    ),
    
    dcc.Store(id='storeJ'),
     # ---------------------Imagen-------------------------------
    html.Img(src='https://ddhh.unq.edu.ar/wp-content/uploads/2017/04/Logo-UNQ-RGB.png', alt='Imagen de ejemplo',style={'width': '25%', 'height': 'auto'}),
# --------------------Titulo--------------------------------
    html.H1(""" SiCoBioNa """, style={'color': 'white','text-align': 'center'}),
    # ---------------------Subtitulo-------------------------------
    html.H1("Sensores Ambientales", style={'color': 'white','text-align': 'center'}),

 #-------------------Selector de Sensores-Variables-------------------
        
    dcc.Store(id='data-store'),
    dcc.Dropdown( id='dropSensor',options=[],multi=True),
    dcc.Dropdown( id='dropVar'   ,options=[],multi=True,style={"width": 800}),
     # --------------------------Registro--------------------------
    html.H1("Registro Histórico", style={'color': 'white','text-align': 'center'}),
        #dcc.Graph(id='my-graph')
    html.Div(id='figures-container')

] ,style={'backgroundColor': '#411023', 'padding': '50px'})




if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port=8050,debug=True,)

#http://127.0.0.1:8050/

