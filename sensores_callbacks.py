
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
        dic[name]=df.to_dict()
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
    Output('figures-container', 'children' ),
    Input('dropVar','value'),
    State('data-store','data'),
    #State('figures-container', 'children' ),
    prevent_initial_call=True
)
# crea graficos si no hay variables
def create_graph(selected_column,datos):#,fig):

    figs=[]
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
                fig.add_trace(this_line)
                fig.update_layout(title=f'{yy}')
        g=dcc.Graph(figure=fig ,id={'type':'graph',
                                  'id':sel})
        figs.append(g)
    return figs


from dash import MATCH,ALL, callback_context

@callback(Output({'type':'graph','id':MATCH},'figure'),
          Input('data-store','data'),
          State({'type':'graph','id':MATCH},'figure'),
          prevent_initial_callback=True
)
#actualiza graficos si ya existen
def update(data,fig):
    print("")
    print("")
    print("cb context")
    print(len(callback_context.states_list))
    print(callback_context.states_list[0]['id']['id'])
    return no_update#fig


# #------------------grafico  -----------------
# @callback(
#     Output('figures-container', 'children' ),
#     Input('dropVar','value'),
#     Input('data-store','data'),
#     State('figures-container', 'children' ),
#     prevent_initial_call=True
# )

# #esta funcion hay que corregir
# def update_graph(selected_column,datos,fig):
#     figuras = {}
#     this_line= {}
#     lines={}

#     if selected_column is None:
#         return no_update
#     if fig is None:
#         fig = go.Figure()
#     for datos_key,datos_val in datos.items():
#         df = pd.DataFrame(datos_val)
#         for col_sel in selected_column:
#             if col_sel in df.columns:
#                 xx= 'tiempo'
#                 yy= col_sel

#                      #no existe variable
#                 if yy not in figuras:

#                     fig=go.Figure()

#                     this_line[yy] = go.Scatter(
#                         x=df[xx],
#                         y=df[yy],
#                         name=f'{datos_key}'         
#                     )
              
#                     fig=go.Figure()
#                     fig.add_trace(this_line[yy])
#                     fig.update_layout(title=f'{yy}')
#                     lines[datos_key]=this_line[yy]
#                     figuras[yy]=(dcc.Graph(figure=fig))
#                     #


#                 else:    #ya existe variable
#                     fig=go.Figure()
#                     for item in lines:
#                         linea=lines[item]
#                         fig.add_trace(linea)

#                     this_line[yy] = go.Scatter(x=df[xx],
#                             y=df[yy],
#                             name=f'{yy} - {datos_key}' 
#                     )   

#                     fig.add_trace(this_line[yy])
#                     figuras[yy] =(dcc.Graph(figure=fig))  
#                     fig.update_layout(title=f'{yy}')
   

#     return  [ figu[1]    for figu in list(figuras.items())  ] # dict to list



