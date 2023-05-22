from mpi4py import MPI
import time
import math
import sys


def printt(*info):
    print(str(rank) + ">> ", end="")
    for arg in info:
        print(arg, end="")
        print(" ", end="")
    print()


def bits_necesarios(numero):
    numero = numero - 1
    if numero == 0:
        return 1
    else:
        bits = 0
        while numero > 0:
            numero = numero // 2
            bits += 1
        return bits


def buscar_posicion(diccionario, texto):
    return list(diccionario.keys()).index(texto)


def binary_list(m, n):
    result = []
    for i in range(m):
        bin_num = bin(i)[2:].zfill(n)
        result.append(bin_num)
    return result


def binary_list2(m, n):
    result = []
    for i in range(m):
        bin_num = bin(i)[2:].zfill(n)
        result.append("1" * (n - 1) + bin_num)
    return result


def dividir(texto, n, unos, bits):
    aver = len(texto) / n
    t = []
    i = 0
    l = 1
    last = 0
    while i < len(texto):
        if texto[i : i + bits] == unos:
            i += 2 * bits + 1
            # print(texto[i:i+2*bits+1])
        else:
            i += bits
            # print(texto[i:i+bits])
        if i > aver * l:
            l += 1
            t.append(texto[last:i])
            last = i
    t.append(texto[last:])
    return t


def bin_to_hex(bin_str):
    decimal = int(bin_str, 2)  # Convertir el str binario a decimal
    hex_str = hex(decimal)[2:]  # Convertir el decimal a str hexadecimal
    return hex_str


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
if rank == 0:
    if len(sys.argv) < 2:
        print("Se requiere un archivo como argumento.")
        sys.exit()

    ruta = sys.argv[1]

    with open(ruta, "rb") as archivo:
        contenido = archivo.read()

    inicio = time.time()

    contenido_hex = contenido.hex()

    indice_hex = contenido_hex[0:2]
    indice = int(indice_hex, 16) + 1

    contenido_bin = bin(int(contenido_hex, 16))[2:].zfill(len(contenido_hex) * 4)

    tabla = contenido_hex[4 : (indice + 2) * 2]

    n = bits_necesarios(indice)

    lista_tabla = [tabla[i : i + 2] for i in range(0, len(tabla), 2)]

    resultado = contenido_bin[8 * (indice + 2) :]

    ceros = int(contenido_hex[2:4], 16)

    resultado = resultado[ceros:]

    n = n - 1
    unos = "1" * n

    t = dividir(resultado, size - 1, unos, n)

    for i in range(size - 1):  # Manda los datos cortados a los trabajadores
        comm.send([lista_tabla, t[i], n], dest=i + 1)

    descomprimido = ""
    for i in range(size - 1):  # Recibe los datos de los trabajadores
        descomprimido += comm.recv(source=i + 1)

    bytes_data = bytes.fromhex(descomprimido)

    fin = time.time()
    printt(fin - inicio)

    # Escribir los bytes en el archivo binario
    with open("descomprimidop-elmejorprofesor.txt", "wb") as file:
        file.write(bytes_data)


else:
    recibido = comm.recv(source=0)
    desco = ""
    bits = recibido[2]
    texto = recibido[1]
    tabla = recibido[0]
    unos = "1" * bits
    i = 0
    while i < len(texto):
        if texto[i : i + bits] == unos:
            pos = int(texto[i + bits : i + 2 * bits + 1], 2) + 2 ** (bits) - 1
            i += 2 * bits + 1
        else:
            pos = bits_int = int(texto[i : i + bits], 2)
            i += bits
        desco += tabla[pos]

    comm.send(desco, dest=0)
