import redis
import time

# Conexión
CHANNEL = 'NOMBRE DE CANAL'
usuario = 'HVAC_Lorenzo' # input('Ingrese su Usuario: ')
client = redis.StrictRedis(host='[DIRECCIÓN IP]',port='[PUERTO]',db=0, decode_responses=True)

Temperatura = 30
Objetivo = 15

def listen_redis():
    try:
        pubsub = client.pubsub()
        pubsub.subscribe('_____')
        client.publish(CHANNEL,f'{usuario}: Sistema HVAC en línea.')
        for message in pubsub.listen(): # Capturar mensajes
            if message['type'] == 'message':
                message_converter(message) # Enviar mensajes al convertidor

    except Exception as e:
        print(f"Error en la suscripción: {e}")

def message_converter(message):
    global Temperatura
    global Objetivo
    try:
        num = int(message['data'])
        Temperatura = num
        message = f"La temperatura ha cambiado a {Temperatura} Grados Celcius."
        client.publish(CHANNEL,f'{usuario}: {message}')
        if Temperatura > Objetivo:
            message = "Se ha detectado una temperatura elevada. Enfriando..."
            client.publish(CHANNEL,f'{usuario}: {message}')
        elif Temperatura < Objetivo:
            message = "Se ha detectado una temperatura reducida. Calentando..."
            client.publish(CHANNEL,f'{usuario}: {message}')

    except ValueError:
        message = "El mensaje no es una temperatura." 
        # client.publish(CHANNEL, f'{usuario}: {message}') # Comentar si repite mucho el mensaje

listen_redis()

# Reguladores
def AC():
    global Temperatura
    global Objetivo
    while Temperatura != Objetivo:
        if Temperatura < Objetivo:
            Temperatura += 5
        elif Temperatura > Objetivo:
            Temperatura -= 5
    time.sleep(3)

def Vent():
    global Temperatura
    global Objetivo
    while Temperatura != Objetivo:
        if Temperatura < Objetivo:
            Temperatura += 3
        elif Temperatura > Objetivo:
            Temperatura -= 3
    time.sleep(2)

def Pasivo():
    global Temperatura
    global Objetivo
    while Temperatura != Objetivo:
        if Temperatura < Objetivo:
            Temperatura += 1
        elif Temperatura > Objetivo:
            Temperatura -= 1
    time.sleep(1)

def Reporte():
    global Temperatura
    global Objetivo
    while Temperatura != Objetivo:
        message = f"El cuarto está a {Temperatura} Grados Celcius."
        client.publish(CHANNEL,f'{usuario}: {message}')
    time.sleep(3)

def Estable():
    global Temperatura
    global Objetivo
    while Temperatura == Objetivo:
        message = f"Temperatura estable a {Temperatura} Grados Celcius."
        client.publish(CHANNEL,f'{usuario}: {message}')
    time.sleep(30)

AC()
Vent()
Pasivo()
Reporte()
Estable()
