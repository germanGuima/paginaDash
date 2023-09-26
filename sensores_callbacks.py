
from dash import Output, Input, State, no_update,callback
import pandas as pd
import plotly.express as px
import json
from plotly import graph_objects as go
from dash import dcc
from dash import Patch
#from gdash2 import app
from glob import glob

def openJsonAsDf(Jdata):
    with open(str(Jdata),'r') as json_file:
     Jdata3 = json.load(json_file)
    return pd.DataFrame(Jdata3)


def get_data_files_names():

    dataList = glob('data/*.json')
    names = [d.split('/')[-1].split('.')[0]
                    for d in dataList]
    return dataList,names


#-------------------- levantar datos-----------------------
@callback(  
          Output('dropSensor','options'),
        Input('intervalo-actualizacion','n_intervals'),
)
def uptade_names(n_intervals):
    """Levanta nombre de las bases sensoras."""
    dl,names=get_data_files_names()
    namesS = [str(elemento) for elemento in names]
    op={'dl': dl, 'names': names, 'nombre': namesS}

    opciones=[ {'label': namesS, 'value': dl} for namesS, dl in zip(op['nombre'], op['dl']) ]  
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
    for elemento in valor:
        #print(elemento)
        df =openJsonAsDf(elemento)
        name = elemento.split('/')[-1].split('.')[0]
        dic[name]=df.to_dict()
    return dic# retorno diccionario
    

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
        #print(l0)
        l0.remove('tiempo')
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
