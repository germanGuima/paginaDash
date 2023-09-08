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



def get_data_files_names():

    dataList = glob('data/*.json')
    names = [d.split('/')[-1].split('.')[0]
                    for d in dataList]
    return dataList,names

# def openJsonAsDf(Jdata):
#     with open(str(Jdata),'r') as json_file:
#      Jdata3 = json.load(json_file)
#     return pd.DataFrame(Jdata3)

dl,names=get_data_files_names()
namesS = [str(elemento) for elemento in names]
# df = pd.DataFrame()


app.layout = html.Div(
[

     # ---------------------Imagen-------------------------------
    html.Img(src='https://ddhh.unq.edu.ar/wp-content/uploads/2017/04/Logo-UNQ-RGB.png', alt='Imagen de ejemplo',style={'width': '25%', 'height': 'auto'}),
# --------------------Titulo--------------------------------
    html.H1(""" SiCoBioNa """, style={'color': 'white','text-align': 'center'}),
    # ---------------------Subtitulo-------------------------------
    html.H1("Sensores Ambientales", style={'color': 'white','text-align': 'center'}),

 #-------------------Selector de Sensores-Variables-------------------
        
        dcc.Store(id='data-store'),
        dcc.Dropdown( id='dropSensor',
                     options=[{'label': namesS, 'value': dl} for namesS, dl in zip(namesS, dl)],multi=True),
        dcc.Dropdown( id='dropVar',options=[],multi=True,style={"width": 800}),
     # --------------------------Registro--------------------------
        html.H1("Registro Histórico", style={'color': 'white','text-align': 'center'}),
        dcc.Graph(id='my-graph')

] ,style={'backgroundColor': '#411023', 'padding': '50px'})

# from callbacks import * 
# #--------------------Elegir Sensor-----------------------
# @app.callback(
#     Output('data-store','data'),
#     Input('dropSensor','value'),
# )
# def update_output(Valor):
#     if Valor!=None:
#         df=openJsonAsDf(Valor)
#         return df.to_dict()
#     else:
#         no_update

#     #--------------------Elegir variable-----------------------
# @app.callback(
#     Output('dropVar', 'options') ,  # Actualizar las opciones del dropdown
#     Input('data-store','data')
# )
# def actualizar_opciones(datos):
#     if datos:

#         df3=pd.DataFrame(datos)
#         del df3['tiempo']
#         opciones=[{'label': col , 'value':col} for col in df3.columns]
#     else:
#         opciones=[]
#     return opciones
# #------------------grafico  -----------------
# @app.callback(
#     Output('my-graph', 'figure' ),
#     [Input('dropVar','value'),
#     Input('data-store','data')],
#     prevent_initial_call=True
# )
# def update_graph(selected_column,datos):
  
#     df3=pd.DataFrame(datos)
#     if selected_column is None:
#         return no_update
#     if any(column not in df3.columns for column in selected_column):
#         #filtro seleccionadas.
#         selected=[column for column in selected_column if column in df3.columns]
#         fig=px.line(df3, x='tiempo', y=selected, title='Valores Medidos')
#         return fig
#     else:
#         fig=px.line(df3, x='tiempo', y=selected_column, title='Valores Medidos')
#         return fig 


if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port=8050,debug=True,)

#http://127.0.0.1:8050/

