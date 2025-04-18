import time
import concurrent.futures
import threading
import datetime
import os

# VALORES
Temperatura = 15
Objetivo = 15
sistema = 'HVAC'
stop = threading.Event()
lock = threading.Lock()  # Se utiliza lock para no crear conflictos.

print(f'{sistema}: Sistema HVAC en línea.')

# INPUT
def Captura():
    global Temperatura
    while not stop.is_set():
        try:
            nueva_temp = input("Ingrese nueva temperatura (Enter para continuar): \n").strip()
            if nueva_temp:
                with lock:
                    Temperatura = int(nueva_temp)
                print(f'{sistema}: La temperatura ha cambiado a {Temperatura}°C.')
                if Temperatura > Objetivo:
                    print(f'{sistema}: Se ha detectado una temperatura elevada. Enfriando...')
                elif Temperatura < Objetivo:
                    print(f'{sistema}: Se ha detectado una temperatura reducida. Calentando...')
        except ValueError:
            print(f'{sistema}: Error. Ingrese un número válido.')
        except KeyboardInterrupt:
            stop.set()  # Solución para pagar todo.
            break
        time.sleep(0.5)
    print(f'{sistema}: Captura detenido.')

# REGULADORES
def AC():
    global Temperatura
    while not stop.is_set():
        try:
            with lock:
                if Temperatura < Objetivo - 4:
                    Temperatura += 3
                elif Temperatura > Objetivo + 4:
                    Temperatura -= 3
            time.sleep(2)
        except Exception as e:
            print(f'{sistema}: Error en AC: {e}')
            time.sleep(2)
    print(f'{sistema}: AC detenido.')

def Vent():
    global Temperatura
    while not stop.is_set():
        try:
            with lock:
                if Temperatura < Objetivo - 1:
                    Temperatura += 2
                elif Temperatura > Objetivo + 1:
                    Temperatura -= 2
            time.sleep(1)
        except Exception as e:
            print(f'{sistema}: Error en Vent: {e}')
            time.sleep(1)
    print(f'{sistema}: Ventilador detenido.')

def Reporte():
    while not stop.is_set():
        try:
            print(f'{sistema}: El cuarto está a {Temperatura} Grados Celcius.')
            time.sleep(1)
        except Exception as e:
            print(f'{sistema}: Error en Reporte: {e}')
            time.sleep(1)
    print(f'{sistema}: Reporte detenido.')

# SEMÁFORO
def Inercia(inercia_c=True):
    global Temperatura
    while not stop.is_set():
        try:
            with lock:
                if inercia_c:
                    Temperatura += 1
                    if Temperatura >= Objetivo:
                        inercia_c = False
                else:
                    Temperatura -= 1
                    if Temperatura <= Objetivo:
                        inercia_c = True
            time.sleep(2)
        except Exception as e:
            print(f'{sistema}: Error en Inercia: {e}')
            time.sleep(2)
    print(f'{sistema}: Inercia detenido.')

def LogTemperatura():
    log_file = "log.txt"
    while not stop.is_set():
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"{timestamp} - Temperatura: {Temperatura} Grados Celcius\n"
            with lock:  # Asegurarse de que solo esta función intente escribir al archivo.
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(log_message)
            time.sleep(10)
        except IOError as e:
            print(f'{sistema}: Error al escribir en log.txt: {e}')
            time.sleep(10)
        except Exception as e:
            print(f'{sistema}: Error en LogTemperatura: {e}')
            time.sleep(10)
    print(f'{sistema}: LogTemperatura detenido.')

# CONCURRENCIA
def main():
    try:
        # Crear archivo log.txt si no existe en el mismo folder.
        log_file = "log.txt"
        
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("HVAC System Log\n")
                
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(Captura),
                executor.submit(AC),
                executor.submit(Vent),
                executor.submit(Reporte),
                executor.submit(Inercia),
                executor.submit(LogTemperatura),
            ]
            try:
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f'{sistema}: Error en tarea: {e}')
            except KeyboardInterrupt:
                stop.set()
                print(f'{sistema}: Apagando sistema...')
    except Exception as e:
        print(f'{sistema}: Error crítico en main: {e}')
    finally:
        stop.set()
        print(f'{sistema}: Sistema apagado.')

if __name__ == "__main__":
    main()