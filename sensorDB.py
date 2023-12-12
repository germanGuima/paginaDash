"""Este archivo se encarga SOLO de conectar el mqtt, leer y 
guardar en la base de mongo"""
#########################################################################
# #-----------------------Base-de-datos--------------------------------------------#
# import pymongo
# import pprint
# import datetime as dt
# from pymongo import MongoClient
# # Establish connection
# import time
# import pandas as pd

# conn = "mongodb://localhost:27017"
# mongo_client = pymongo.MongoClient(conn)

# # Create a database

# db = mongo_client.sensor#sensorsDB#classDB
# tabla = db.sensor
# tabla.find()

# #esto es lo que hay que hacer para recuperar los nombres unicos
# todos_nombres = [val['deviceId'] for val in tabla.find({},{'deviceId':1,'_id':0})]
# nombres_unicos = list(set(todos_nombres))

# todosLosDatosDelPrimerNombreUnico = list(tabla.find({'deviceId':nombres_unicos[0]}))


# from pymongo import MongoClient

#########################################################################
#----------------------Mqtt------------------------------------------------------------------
  
import BaseDatos
import json
import time

import paho.mqtt.client as mqtt 
#import the client1 
broker_address="4a98668d55074575a6e66b180cc7b6b2.s1.eu.hivemq.cloud" #use external broker
port=8883
usuario= {'username':'german',
             'password':'German1234'}

mqtt_client = mqtt.Client(userdata=usuario)#mqtt.Client("P1") #create new instance
#usar identificador para multiples clientes 
mqtt_client.username_pw_set("german","German1234")
mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
mqtt_client.connect(broker_address,port) #connect to broker
pub=mqtt_client.publish("a","PC:Estoy Viendo")
print(pub.is_published())

#TODO: tenemos que separar la parte de mqtt de la parte de mong
# el on_message tiene que llamar a la funcion de mongo que escriba
# y todo lo de mongo tiene que estar junto en un scrip

#####################funcion que se ejecuta cuando recibe un mensaje####################################################
diccSensores={}
dicc={}
def on_message(mqtt_client, userdata, message):
    #funcion que se ejecuta cuando recibe un mensaje
    msg = str(message.payload.decode("utf-8"))
    print("received message =",msg)
    #msg_json ... #json.loads(msg)
    Jmsg=json.loads(msg)
    Jmsg['tiempo'] = time.time()
    
    # db.sensor.insert_one(Jmsg)
    insertarBase(Jmsg) # Esto me esta creando una base de datos x cada mensaje
                        #deberia crear si no existe *arreglar en basedatos
    print('valor guardado---------------')

mqtt_client.on_message = on_message #Mensaje Recibido -Guardar en base de datos
mqtt_client.subscribe("a")

mqtt_client.loop_forever() 
# mqtt_client.loop_start()
#---------------------------------------------------
#Funciones para trabajar la informacion de la base de datos de mongo

