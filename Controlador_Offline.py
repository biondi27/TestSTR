import time
import threading

# VALORES
Temperatura = 15
Objetivo = 15
sistema = 'HVAC'
stop = False

print(f'{sistema}: Sistema HVAC en línea.')

def Captura():
    global Temperatura
    while not stop:
        try:
            nueva_temp = input("Ingrese nueva temperatura (Enter para continuar): \n").strip()
            if nueva_temp:  # Solo procesa si el usuario ingresó algo
                Temperatura = int(nueva_temp)
                print(f'{sistema}: La temperatura ha cambiado a {Temperatura}°C.')
                if Temperatura > Objetivo:
                    print(f'{sistema}: Se ha detectado una temperatura elevada. Enfriando...')
                elif Temperatura < Objetivo:
                    print(f'{sistema}: Se ha detectado una temperatura reducida. Calentando...')
        except ValueError:
            print(f'{sistema}: Error. Ingrese un número válido.')

# REGULADORES
def AC():
    global Temperatura
    while not stop:
        if Temperatura < Objetivo:
            Temperatura += 5
        elif Temperatura > Objetivo:
            Temperatura -= 5
        time.sleep(3)

def Vent():
    global Temperatura
    while not stop:
        if Temperatura < Objetivo:
            Temperatura += 3
        elif Temperatura > Objetivo:
            Temperatura -= 3
        time.sleep(2)

def Reporte():
    while not stop:
        print(f'{sistema}: El cuarto está a {Temperatura} Grados Celcius.')
        time.sleep(1)

# SEMÁFORO
def Inercia():
    global Temperatura
    inercia_c = True
    while not stop:
        if inercia_c:
            Temperatura += 1
            if Temperatura <= Objetivo:
                inercia_c = False
        else:
            Temperatura -= 1
            if Temperatura >= Objetivo:
                inercia_c = True
        #print(f'{sistema}: {Temperatura} Grados Celcius')
        time.sleep(1)

def Estable():
    while not stop:
        if Temperatura == Objetivo:
            print(f'{sistema}: Temperatura estable a {Temperatura} Grados Celcius.')
        time.sleep(30)

def main():
    global stop
    funciones = [
        threading.Thread(target=Captura,  daemon=True),
        threading.Thread(target=AC,       daemon=True),
        threading.Thread(target=Vent,     daemon=True),
        threading.Thread(target=Reporte,  daemon=True),
        threading.Thread(target=Inercia,  daemon=True),
        threading.Thread(target=Estable,  daemon=True)
    ]

    for funcion in funciones:
        funcion.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop = True
        print(f'{sistema}: Apagando sistema...')

if __name__ == "__main__":
    main()