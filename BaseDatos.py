#base de datos

"""Este archivo se encarga SOLO leer y 
guardar en la base de mongo"""
#########################################################################
#-----------------------Base-de-datos--------------------------------------------#
import pymongo
import pprint
import datetime as dt
from pymongo import MongoClient
# Establish connection
import time
import pandas as pd

conn = "mongodb://localhost:27017"
mongo_client = pymongo.MongoClient(conn)

# Create a database

db = mongo_client.sensor#sensorsDB#classDB
tabla = db.sensor
tabla.find()
# db.sensor.deleteOne('':'')  
#esto es lo que hay que hacer para recuperar los nombres unicos

# todos_nombres = [val['deviceId'] for val in tabla.find({},{'deviceId':1,'_id':0})]
# nombres_unicos = list(set(todos_nombres))

# todosLosDatosDelPrimerNombreUnico = list(tabla.find({'deviceId':nombres_unicos[0]}))


from pymongo import MongoClient
import json
# Esto me esta creando una base de datos x cada mensaje
                        #deberia crear si no existe *arreglar en basedatos
def insertarBase(mens):
    if(db.sensor.find() ): #si no existe en la base de datos
        return db.sensor.insert_one(mens) # chekear inser one como funciona
    else:  # si ya existe en la base de datos
        return db
def parse_dic_from_elems(lista_elems):
    """Nos devuelve un diccionario de listas de los datos 
    de una lista de elementos"""
    df = pd.DataFrame(lista_elems)#convierto a dataframe
    if '_id' in df:
        df.drop('_id',axis=1, inplace=True) #saco id 
    if 'deviceId' in df:    
        df.drop('deviceId',axis=1,inplace=True) #saco deviceId
    df.dropna(axis=1, how='all')       #borro columnas vacias
    
    return df.to_dict(orient='list')#diccionario



def get_data_files_names():
    #tiene que leer la db de mongo y 
    #obtener los nombres distintos
    #o sea, hacer un query de todos los device_id
    #TODO: tengo que tener conectada la db de mongo y definida la tabla

    todos_nombres = [val['deviceId'] for val in tabla.find({},{'deviceId':1,'_id':0})]
    nombres_unicos = list(set(todos_nombres))
    return nombres_unicos
    
    # dataList = glob('data/*.json')
    # names = [d.split('/')[-1].split('.')[0]
    #                 for d in dataList]
    # return dataList,names

def get_dic_from_selected_val(valor):
    dic={}
    for elemento in valor:
        lista_elems = list(tabla.find({'deviceId':elemento})) 
        dic[elemento] = parse_dic_from_elems(lista_elems)   
    # print(lista_elems)
    # print(valor)
    # print(dic)
    return dic
