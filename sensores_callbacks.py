import dash
from dash import Output, Input, State, no_update,callback
import pandas as pd
import plotly.express as px
import json 
from plotly import graph_objects as go

#from gdash2 import app

def openJsonAsDf(Jdata):
    with open(str(Jdata),'r') as json_file:
     Jdata3 = json.load(json_file)
    return pd.DataFrame(Jdata3)
  
#--------------------Elegir Sensor-----------------------
@callback(
    Output('data-store','data'),
    Input('dropSensor','value'),
)
def update_output(valor):
    # valor ahora es lista=[sensor1.json,sensor2.json]
    if valor is None:
        return no_update
    dic={}#diccionario
    #print(valor)
    for elemento in valor:
        #print(elemento)
        df =openJsonAsDf(elemento)
        name = elemento.split('/')[-1].split('.')[0]
        #print(df)
        dic[name]=df.to_dict()
    #print(dic)
    return dic# retorno diccionario
 
    #--------------------Elegir variable-----------------------
@callback(
    Output('dropVar', 'options') ,  # Actualizar las opciones del dropdown
    Input('data-store','data')
)
def actualizar_opciones(datos):
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
    Output('my-graph', 'figure' ),
    Input('dropVar','value'),
    Input('data-store','data'),
    State('my-graph', 'figure' ),
    prevent_initial_call=True
)

#esta funcion hay que corregir
def update_graph(selected_column,datos,fig):
    if selected_column is None:
        return no_update
    if fig is None:
        fig = go.Figure()
    else:
        fig = go.Figure(**fig)
        fig.data =[]
    #print(fig)
    
    for datos_key,datos_val in datos.items():
        df = pd.DataFrame(datos_val)
        for col_sel in selected_column:
            if col_sel in df.columns:
                xx= 'tiempo'
                yy= col_sel
                

                this_line = go.Scatter(x=df[xx],
                                       y=df[yy])
                #agregar legend correspondiente
                fig.add_trace(this_line)
    return fig
    # df3=pd.DataFrame(datos)
    # if selected_column is None:
    #     return no_update
    # if any(column not in df3.columns for column in selected_column):
    #     #filtro seleccionadas.
    #     selected=[column for column in selected_column if column in df3.columns]
    #     fig=px.line(df3, x='tiempo', y=selected, title='Valores Medidos')
    #     return fig
    # else:
    #     fig=px.line(df3, x='tiempo', y=selected_column, title='Valores Medidos')
    #     return fig 