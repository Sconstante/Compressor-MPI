from mpi4py import MPI
import time
import math
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


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


def dividir(texto, n):
    sz = len(texto) / 2
    tam = math.ceil(sz / n)
    extra = sz % n
    if extra == 0:
        extra = n
    t = []
    i = 0
    while i < sz:
        if tam * extra - 1 < i:
            t.append(texto[i * 2 : (i + tam - 1) * 2])
            i += tam - 1
        else:
            t.append(texto[i * 2 : (i + tam) * 2])
            i += tam
    return t


if rank == 0:
    # Codigo del padre
    size = comm.Get_size()

    if len(sys.argv) < 2:
        print("Se requiere un archivo como argumento.")
        sys.exit()

    ruta = sys.argv[1]

    with open(ruta, "rb") as archivo:
        contenido = archivo.read()

    inicio = time.time()

    contenido_hex = contenido.hex()

    t = dividir(contenido_hex, size - 1)

    for i in range(size - 1):  # Manda los datos cortados a los trabajadores
        comm.send(t[i], dest=i + 1)

    tablas = []
    for i in range(size - 1):  # Recibe los datos de los trabajadores
        tablas.append(comm.recv(source=i + 1))

    hex_counts = tablas[0]
    for i in range(size - 2):
        for key, value in tablas[i + 1].items():
            hex_counts[key] = hex_counts.get(key, 0) + value

    hex_counts = dict(
        sorted(hex_counts.items(), key=lambda item: item[1], reverse=True)
    )

    for i in range(size - 1):  # Manda los datos cortados a los trabajadores
        comm.send(hex_counts, dest=i + 1)

    indice = format(len(hex_counts) - 1, "08b")
    indice = indice.zfill(8)
    tabla = "".join(hex_counts.keys())

    resultado = ""
    for i in range(size - 1):  # Recibe los datos de los trabajadores
        resultado += comm.recv(source=i + 1)

    ceros = 8 - (len(resultado) % 8)
    resultado = ("0" * ceros) + resultado
    ceros = bin(ceros)[2:].zfill(8)

    tablanueva = bin(int(tabla, 16))[2:].zfill(len(tabla) * 4)
    comprimido = indice + ceros + tablanueva + resultado

    fin = time.time()
    print(fin - inicio)

    with open("comprimidop.elmejorprofesor", "wb") as archivo:
        archivo.write(
            bytes(int(comprimido[i : i + 8], 2) for i in range(0, len(comprimido), 8))
        )
else:
    # Codigo del hijos
    contenido_hex = comm.recv(source=0)
    contenido = bytes.fromhex(contenido_hex)
    hex_counts = {
        hex(byte)[2:].zfill(2): contenido.count(byte) for byte in set(contenido)
    }
    comm.send(hex_counts, dest=0)

    hex_counts = comm.recv(source=0)
    n = bits_necesarios(len(hex_counts))

    binarioList_1 = binary_list((2 ** (n - 1)) - 1, n - 1)
    binarioList_2 = binary_list2(len(hex_counts) - (2 ** (n - 1)) + 1, n)

    cons = (2 ** (n - 1)) - 1
    hex_index = {v: k for k, v in enumerate(hex_counts.keys())}

    resultado = "".join(
        [
            binarioList_1[hex_index.get(contenido_hex[i : i + 2])]
            if hex_index.get(contenido_hex[i : i + 2]) < cons
            else binarioList_2[hex_index.get(contenido_hex[i : i + 2]) - cons]
            for i in range(0, len(contenido_hex), 2)
        ]
    )
    comm.send(resultado, dest=0)
