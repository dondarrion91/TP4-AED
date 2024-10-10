import os
import pickle
from envios import Envio

def crear_envios(nombre_archivo, nombre_binario):
    if not os.path.exists(nombre_archivo):
        print('El archivo', nombre_archivo, 'no existe...')
        print('Revise, y reinicie el programa...')
        exit(1)

    csv_file_object = open(nombre_archivo, 'rt')
    linea = 0

    binary_file_object = open(nombre_binario, "wb")

    while True:
        line = csv_file_object.readline()

        if line == '':
            break

        if linea >= 2:
            cp = line.split(",")[0]
            direccion = line.split(",")[1]
            tipo = int(line.split(",")[2])
            pago = int(line.split(",")[3])

            envio = Envio(cp, direccion, tipo, pago)
            pickle.dump(envio, binary_file_object)

        linea += 1

    csv_file_object.close()
    binary_file_object.close()

def mostrar_envios_archivo(nombre_binario):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)
        print(envio)

    binary_file_object.close()

def cargar_envio_archivo(nombre_binario):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    binary_file_object = open(nombre_binario, "a+b")

    print("\nNuevo envio:")
    cp = input("Ingresar código postal:")
    direccion = input("Ingresar dirección:")
    tipo = validar_tipo("Ingresar tipo de envio (valor del 0 al 6):")
    pago = validar_pago("Ingresar forma de pago (1 en efectivo y 2 en tarjeta de credito):")

    envio = Envio(cp, direccion, tipo, pago)

    pickle.dump(envio, binary_file_object)

    binary_file_object.close()

def validar_mayor_igual(mayor, mensaje):
    valor = int(input(mensaje))
    while valor < mayor:
        valor = int(input(mensaje))
    return valor

def validar_tipo(mensaje="Ingrese un valor:"):
    nvo_tipo = int(input(mensaje))
    while nvo_tipo < 0 or nvo_tipo > 6:
        print("Error, debe ingresar un valor entre 0 y 6!")
        nvo_tipo = int(input(mensaje))
    return nvo_tipo

def validar_pago(mensaje="Ingrese un valor:"):
    nvo_pago = int(input(mensaje))
    while nvo_pago not in (1, 2):
        print("Error, debe ingresar un valor igual a 1 o un valor igual a 2!")
        nvo_pago = int(input(mensaje))
    return nvo_pago

def main():
    nombre_archivo = "envios-tp4.csv"
    nombre_binario = "envios.dat"
                
    menu = '\nMenú de Opciones - TP4 G038\n' \
    '1. Crear binario con envios desde csv.\n' \
    '2. Cargar nuevo envio por teclado\n' \
    '3. Mostrar todos los envios guardados en el archivo binario.\n' \
    '0. SALIR\n' \
    'Ingrese su opción: '

    opcion = -1

    while opcion != 0:
        opcion = validar_mayor_igual(0, menu)
        
        if opcion == 1:
            verysure = input(
                "\nEsta acción sobreescribira los archivos previamente cargardos\n" \
                "Esta seguro de realizar esta acción? (y/n)\n"
            )
            
            if verysure.lower() == "y":
                crear_envios(nombre_archivo, nombre_binario)
                print("Archivo binario creado con exito!")
        elif opcion == 2:
            cargar_envio_archivo(nombre_binario)
            print("Envio cargado con exito")
        elif opcion == 3:
            mostrar_envios_archivo(nombre_binario)

if __name__ == "__main__":
    main()