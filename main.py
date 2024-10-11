import os
import pickle
from envios import Envio, get_tipo, get_pago

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

def buscar_en_binario(nombre_binario, valor):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return
    
    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)

        if envio.direccion == valor:
            binary_file_object.close()
            return envio

    binary_file_object.close()
    return None

def crear_matriz_envios_pagos(nombre_binario):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    matriz = [2 * [0] for i in range(7)]

    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)

        matriz[envio.tipo][envio.pago - 1] += 1

    binary_file_object.close()

    return matriz

def mostrar_envios_archivo(nombre_binario, filter = None):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    cantidad = 0
    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)

        # Si no paso un filtro muestro todos los envios.
        # Si coincide el valor con el filtro muestro el envio.
        if filter is None or envio.cp == filter:
            print(envio)
            cantidad += 1

    binary_file_object.close()

    return cantidad

def contar_matriz_envios(matriz):
    total_tipos = 7 * [0]
    total_envios = 2 * [0]

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            total_tipos[i] += matriz[i][j]
            total_envios[j] += matriz[i][j]

    return total_tipos, total_envios

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

def calcular_promedio_arch(nombre_binario):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    total_importe = 0
    cantidad_envios = 0

    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)

        importe_final = envio.calcular_importe_final()

        total_importe += importe_final
        cantidad_envios += 1

    binary_file_object.close()

    if cantidad_envios == 0:
        return 0

    return total_importe // cantidad_envios

def generar_vector_envios(nombre_binario, promedio):
    if not os.path.exists(nombre_binario):
        print('\nEl archivo', nombre_binario, 'no existe...')
        print('Ingrese la opción 1!')
        return

    vec_envios = []

    binary_file_object = open(nombre_binario, "rb")
    tamanio = os.path.getsize(nombre_binario)

    while binary_file_object.tell() < tamanio:
        envio = pickle.load(binary_file_object)

        if envio.calcular_importe_final() > promedio:
            vec_envios.append(envio)

    binary_file_object.close()

    return vec_envios

def shell_sort(v):
    n = len(v)
    h = 1
    while h <= n // 9:
        h = 3*h + 1

    while h > 0:
        for j in range(h, n):
            y = v[j]
            k = j - h

            while k >= 0 and y.cp < v[k].cp:
                v[k+h] = v[k]
                k -= h
            v[k+h] = y
        h //= 3

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
    '4. Mostrar todos los envios por código postal.\n' \
    '5. Buscar envio por dirección.\n' \
    '6. Cantidad de envíos de cada combinación posible entre tipo de envío y forma de pago.\n' \
    '7. Cantidad total de envíos por tipo y por forma de pago.\n' \
    '8. Calcular el importe promedio pagado entre todos los envíos que figuran en el archivo.\n' \
    '0. SALIR\n' \
    'Ingrese su opción: '

    opcion = -1
    matriz_envios_pagos = None

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
        elif opcion == 4:
            cp = input("Ingresar código postal:")
            cantidad = mostrar_envios_archivo(nombre_binario, cp)
            print("\nCantidad de envios mostrados: ", cantidad)
        elif opcion == 5:
            direccion = input("Ingresar dirección a buscar:")
            envio = buscar_en_binario(nombre_binario, direccion)

            if envio is None:
                print("No se encontro envio que coincida con la dirección ingresada!")
            else:
                print(envio)
        elif opcion == 6:
            matriz_envios_pagos = crear_matriz_envios_pagos(nombre_binario)

            for i in range(len(matriz_envios_pagos)):
                print("Para" , "{0} (tipo {1})".format(get_tipo(i), i))

                for j in range(len(matriz_envios_pagos[i])):
                    cantidad_envios_pagos = matriz_envios_pagos[i][j]
                    if cantidad_envios_pagos > 0:
                        print("Cantidad de envios en {0}: {1}".format(get_pago(j + 1), cantidad_envios_pagos))

                print("\n")
        elif opcion == 7:
            if matriz_envios_pagos is None:
                print('\nPara este punto es necesario generar la matriz de contadores.')
                print('Ingrese la opción 6!')
            else:
                total_tipos, total_pagos = contar_matriz_envios(matriz_envios_pagos)

                print("\nTotal por tipo de envio....")
                for i in range(len(total_tipos)):
                    print("Total para envios {0}({1}): {2}".format(get_tipo(i), i, total_tipos[i]))

                print("\nTotal por forma de pago....")
                for i in range(len(total_pagos)):
                    print("Total para envios {0}({1}): {2}".format(get_pago(i + 1), i + 1, total_pagos[i]))
        elif opcion == 8:
            promedio = calcular_promedio_arch(nombre_binario)
            print("Promedio", promedio)

            vec_envios = generar_vector_envios(nombre_binario, promedio)
            shell_sort(vec_envios)

            for i in range(len(vec_envios)):
                print(vec_envios[i])

if __name__ == "__main__":
    main()