import time
import concurrent.futures
import threading

# VALORES
Temperatura = 15
Objetivo = 15
sistema = 'HVAC'
stop = threading.Event()

print(f'{sistema}: Sistema HVAC en línea.')

# INPUT
# Procesamiento del input del usuario para ajustar la temperatura.
def Captura():
    global Temperatura
    if stop.is_set():
        return
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
    time.sleep(0.5)
    Captura()
       

# REGULADORES
def AC(): # Aire Acondicionado
    global Temperatura
    if stop.is_set():
        return
    if Temperatura < Objetivo - 4:
        Temperatura += 3
    elif Temperatura > Objetivo + 4:
        Temperatura -= 3
    time.sleep(2)
    AC()

def Vent(): #
    global Temperatura
    if stop.is_set():
        return
    if Temperatura < Objetivo - 1:
        Temperatura += 2
    elif Temperatura > Objetivo + 1:
        Temperatura -= 2
    time.sleep(1)
    Vent()

def Reporte():
    if stop.is_set():
        return
    print(f'{sistema}: El cuarto está a {Temperatura} Grados Celcius.')
    time.sleep(1)
    Reporte()

# SEMÁFORO
def Inercia(inercia_c = True):
    global Temperatura
    if stop.is_set():
        return
    if inercia_c:
        Temperatura += 1
        if Temperatura <= Objetivo:
            inercia_c = False
    else:
        Temperatura -= 1
        if Temperatura >= Objetivo:
            inercia_c = True
    time.sleep(2)
    Inercia(inercia_c)

def Estable():
    if stop.is_set():
        return
    if Temperatura == Objetivo:
        print(f'{sistema}: Temperatura estable a {Temperatura} Grados Celcius.')
    time.sleep(30)
    Estable()

# NOTA: Todas las funciones anterirores utilizan recursión para mantenerse activas

# CONCURRENCIA
# Uso de CONCURRENCIA para correr todas las funciones simultaneamente.
def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(Captura),
            executor.submit(AC),
            executor.submit(Vent),
            executor.submit(Reporte),
            executor.submit(Inercia),
            executor.submit(Estable),
        ]
        try:
            for future in concurrent.futures.as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            stop.set()
            print(f'{sistema}: Apagando sistema...')

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()