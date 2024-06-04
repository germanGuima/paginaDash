""" Este archivo tiene los callbacs de dash, adicionalmente tiene la 
lógica de lectura y filtrado de la base de datos de mongo. 
Optimamente hablando, la parte de mongo deberia estar aparte, meh"""

from dash import Output, Input, State, no_update,callback
import pandas as pd
import plotly.express as px
import json
from plotly import graph_objects as go
from dash import dcc
from dash import Patch
#from gdash2 import app
from glob import glob

#TODO: agregar base de mongo y tabla
import pymongo

#conn = "mongodb://localhost:27017"
conn="mongodb+srv://ger:iaci2023@cluster0.vxyuxqk.mongodb.net/"

mongo_client = pymongo.MongoClient(conn)

db = mongo_client.sensor#sensorsDB#classDB
tabla = db.sensor
tabla.find()


def openJsonAsDf(Jdata):
    with open(str(Jdata),'r') as json_file:
     Jdata3 = json.load(json_file)
    Jdata3.pop('deviceId')
    for k,v in Jdata3.items():
        print(f"{k}: {len(v)}")
    return pd.DataFrame(Jdata3)

from BaseDatos import (
                    get_dic_from_selected_val,
                    get_data_files_names
                    )

# def parse_dic_from_elems(lista_elems):
#     df = pd.DataFrame(lista_elems)
#     df.drop('_id',axis=1, inplace=True)
#     df.drop('deviceId',axis=1,inplace=True)
#     return df.to_dict(orient='list')
# def get_data_files_names():
#     dataList = glob('data/*.json')
#     names = [d.split('/')[-1].split('.')[0]
#                     for d in dataList]
#     return dataList,names
# def get_data_files_names(): #tiene que leer la db de mongo y 
#     #obtener los nombres distintos
#     #o sea, hacer un query de todos los device_id

#     #TODO: tengo que tener conectada la db de mongo y definida la tabla

#     todos_nombres = [val['deviceId'] for val in tabla.find({},{'deviceId':1,'_id':0})]
#     nombres_unicos = list(set(todos_nombres))
#     return nombres_unicos
#     # dataList = glob('data/*.json')
#     # names = [d.split('/')[-1].split('.')[0]
#     #                 for d in dataList]
#     # return dataList,names

#-------------------- levantar datos-----------------------
@callback(  
          Output('dropSensor','options'),
        Input('intervalo-actualizacion','n_intervals'),
)
def uptade_names(n_intervals):
    """Levanta nombre de las bases sensoras."""
    #TODO: modificar porque ahora solo devuelve names \check
    #print("funcion update_names")
    names = get_data_files_names()
    opciones = [ {'label': n, 'value':n} for n in names]
    # dl,names=get_data_files_names()
    # namesS = [str(elemento) for elemento in names]
    # op={'dl': dl, 'names': names, 'nombre': namesS}

    # opciones=[ {'label': namesS, 'value': dl} for namesS, dl in zip(op['nombre'], op['dl']) ]  
    #print(opciones)    
    return opciones


#--------------------Elegir Sensor-----------------------


@callback(
    Output('data-store','data'),
    Input('dropSensor','value'),
    Input('intervalo-actualizacion','n_intervals'),
)
def update_output(valor,n_interval):
    #print('actualizando data store')
    # valor ahora es lista=[sensor1.json,sensor2.json]
    if valor is None:
        return no_update
    dic={}#diccionario
    #print(valor)

    #TODO: obtener de la base de datos todos los elementos con deviceId==valor

    dic = get_dic_from_selected_val(valor)
    
    return dic
    # for elemento in valor:
    #     #print(elemento)
    #     df =openJsonAsDf(elemento)
    #     name = elemento.split('/')[-1].split('.')[0]
    #     dic[name]=df.to_dict()
    # return dic# retorno diccionario



    #--------------------Elegir variable-----------------------
@callback(
    Output('dropVar', 'options') ,  # Actualizar las opciones del dropdown
    Input('data-store','data')
)
def actualizar_opciones(datos):
    """Actualiza las opciones en el dropdown"""
    if datos:
        l0 =[]
        for k,v in datos.items():
            l0 = l0+ list(v.keys())
        l0 = set(l0)
        print(l0)
        # l0.remove('tiempo')
        opciones=[{'label': col , 'value':col} for col in l0]
    else:
        opciones=[]
    return opciones 

#------------------grafico  -----------------
@callback(
    Output('figures-container', 'children' ),
    Input('dropVar','value'),
    Input('data-store','data'), # en input porque asi puedo usar sensores para actualizar
    #State('figures-container', 'children' ),
    prevent_initial_call=True
)
# crea graficos si no hay variables
def create_graph(selected_column,datos):#,fig):
    """Crea los graficos con los valores de variables seleccionadas
    (si existen) en las figuras"""
    figs=[]
    if datos=={}:
        return None
    
    if selected_column is None :
        return no_update 
    for sel in selected_column:
        fig = go.Figure()
        for datos_key,datos_val in datos.items():
            df = pd.DataFrame(datos_val)
            if sel in df.columns:
                xx= 'tiempo'
                yy= sel
                this_line = go.Scatter(
                        x=df[xx],
                        y=df[yy],
                        name=f'{datos_key}'         
                )
                if yy is not None:
                    fig.add_trace(this_line)
                    fig.update_layout(title=f'{yy}',title_font=dict(size=24, color='white'),  # Estilo del título: tamaño y color
                    title_x=0.5)
                    fig.update_layout(template='plotly_dark')

        g=dcc.Graph(figure=fig ,id={'type':'graph',
                                  'id':sel
                                })
        figs.append(g)
        #dg#
    return figs
