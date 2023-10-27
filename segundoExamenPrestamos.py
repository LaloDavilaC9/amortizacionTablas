from datetime import datetime
from prettytable import PrettyTable
import os
import re

class Cliente:
    def __init__(self):
        pass
    def __init__(self, nombre_completo="", rfc="", edad=0, fecha_alta="", telefono="", correo=""):
        self.nombre_completo = nombre_completo
        self.rfc = rfc
        self.edad = edad
        self.fecha_alta = fecha_alta
        self.telefono = telefono
        self.correo = correo
        self.prestamo = Prestamo(0,0,0)

    def solicitar_prestamo(self, monto, plazo, interes):
        self.prestamo = Prestamo(monto, plazo, interes)

    def __str__(self):
        return f"{self.nombre_completo},{self.rfc},{self.edad},{self.fecha_alta},{self.telefono},{self.correo},{self.prestamo}"

 # Setters
    def set_nombre_completo(self, nombre_completo):
        self.nombre_completo = nombre_completo

    def set_rfc(self, rfc):
        self.rfc = rfc

    def set_edad(self, edad):
        self.edad = edad

    def set_fecha_alta(self, fecha_alta):
        self.fecha_alta = fecha_alta

    def set_telefono(self, telefono):
        self.telefono = telefono

    def set_correo(self, correo):
        self.correo = correo

    def solicitar_prestamo(self, monto, plazo, interes):
        self.prestamo = Prestamo(monto, plazo, interes)

class Prestamo:
    def __init__(self, monto, plazo, interes):
        self.monto = monto
        self.plazo = plazo
        self.interes = interes

    def __str__(self):
        return f"{self.monto},{self.plazo},{self.interes}"


def cargarLista(listaClientes):
    #Se carga todo el archivo a una lista en memoria
    if(os.path.exists("clientes.txt")):
        with open('clientes.txt', 'r') as archivo:
            # Leer cada línea del archivo
            for linea in archivo:
                partes = linea.strip().split(',')
                cliente = Cliente(partes[0], partes[1], int(partes[2]), partes[3], partes[4],partes[5])
                cliente.prestamo.monto = float(partes[6])
                cliente.prestamo.plazo = int(partes[7])
                cliente.prestamo.interes = float(partes[8])
                listaClientes.append(cliente)


def menu():
    listaClientes = []
    cargarLista(listaClientes)
    opcion = 0
    print("1. Dar de alta un cliente")
    print("2. Solicitar un prestamo")
    print("3. Ver tabla de un amortización de un préstamo de un cliente")
    print("4. Salir")
    while (opcion < 1 or opcion > 4):
        opcion = int(input("Ingrese una opción: "))

    while(opcion!=4):
        if (opcion == 1):
            alta(listaClientes)
        elif (opcion == 2):
            prestamo(listaClientes)
        elif(opcion==3):
            mostrarAmortizacion(listaClientes)
        elif (opcion == 4):
            print("BYE")

        opcion=0
        print("1. Dar de alta un cliente")
        print("2. Solicitar un prestamo")
        print("3. Ver tabla de un amortización de un préstamo de un cliente")
        print("4. Salir")
        while (opcion < 1 or opcion > 4):
            opcion = int(input("Ingrese una opción: "))

def prestamo(listaClientes):
    mostrarClientes(listaClientes)
    numCliente = 0
    while (numCliente <= 0 or numCliente > len(listaClientes)):
        try:
            numCliente = int(input("Ingrese el número de cliente que desea solicitar un prestamo: "))
        except ValueError:
            numCliente = 0
            print("Error: Por favor, ingrese un número de cliente válido.")

    numCliente = numCliente - 1

    monto = -1
    while(monto < 0):
        try:
            monto = float(input("Ingrese el monto del prestamo: "))
        except ValueError:
            monto = -1
            print("Error: Por favor, ingrese un número válido.")

    plazo = 0

    while (plazo <= 0):
        try:
            plazo = int(input("Ingrese el plazo del prestamo: "))
        except ValueError:
            monto = 0
            print("Error: Por favor, ingrese un número entero válido.")

    interes = -1

    while (interes < 0):
        try:
            interes = float(input("Ingrese el porcentaje de interes: "))
        except ValueError:
            interes = 0
            print("Error: Por favor, ingrese un número válido.")

    listaClientes[numCliente].solicitar_prestamo(monto, plazo, interes)
    #Se borra el archivo y se carga uno nuevo
    archivo = open("clientes.txt", "w")
    for i in listaClientes:
        archivo.write(f"{i}\n")
    archivo.close()


def alta(listaClientes):
    nuevoCliente = Cliente()
    nuevoCliente.nombre_completo = input("Ingrese el nombre del cliente: ")

    while (not(validarRFC(nuevoCliente.rfc))):
        nuevoCliente.rfc = input("Ingrese el RFC del cliente: ")

    edadValida = False
    while(not(edadValida)):
        try:
            nuevoCliente.edad = int(input("Ingrese la edad del cliente: "))
            if(nuevoCliente.edad <= 0):
                raise ValueError()
            edadValida = True
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

    while(not(validarTelefono(nuevoCliente.telefono))):
        nuevoCliente.telefono = input("Ingrese el telefono del cliente: ")

    while(not(validarCorreo(nuevoCliente.correo))):
        nuevoCliente.correo = input("Ingrese el correo del cliente: ")

    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y")
    nuevoCliente.fecha_alta = fecha_formateada


    listaClientes.append(nuevoCliente)
    archivo = open("clientes.txt", "a")
    archivo.write(f"{nuevoCliente}\n")
    archivo.close()

def validarTelefono(telefono):
    patron = r'^\d{10}$'
    return bool(re.match(patron, telefono))

def validarRFC(rfc):
    #ABCD123456XYZ
    patron_rfc = r'^[A-Z&Ña-z]{4}\d{6}[A-Z&Ñ\d]{3}$'
    return re.match(patron_rfc, rfc)

def validarCorreo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if (re.match(patron, correo) is not None):
        return True
    return False

def mostrarAmortizacion(listaClientes):

    mostrarClientes(listaClientes)
    numCliente = 0
    while (numCliente <= 0 or numCliente > len(listaClientes)):
        try:
            numCliente = int(input("Ingrese el número de cliente que desea ver la tabla de amortización de su préstamo: "))
        except ValueError:
            numCliente = 0
            print("Error: Por favor, ingrese un número de cliente válido.")

    numCliente = numCliente - 1
    cliente = listaClientes[numCliente]
    if(cliente.prestamo.monto != 0):

        print(f"Titular del préstamo: {cliente.nombre_completo}")
        print(f"Monto del prestamo: ${cliente.prestamo.monto}")
        print(f"Plazo del prestamo (meses): {cliente.prestamo.plazo}")
        print(f"Tasa de interes del prestamo: {cliente.prestamo.interes}%")
        total = cliente.prestamo.monto * (1 + cliente.prestamo.interes / 100)
        print(f"Total a pagar del prestamo: ${total}")
        imprimirTabla(cliente,total)
    else:
        print(f"El cliente {cliente.nombre_completo} no ha solicitado ningún préstamo")


def imprimirTabla(cliente,total):
    tabla = PrettyTable()
    tabla.field_names = ["Periodo", "Cuota", "Interes", "Capital", "Saldo"]
    saldo = total
    for i in range(1, cliente.prestamo.plazo + 1):
        renglon = []
        renglon.append(i)
        # Cuota [1]
        cuota = total / cliente.prestamo.plazo
        renglon.append(f"${cuota:.2f}")
        # Interes [2]
        interes = (total - cliente.prestamo.monto) / cliente.prestamo.plazo
        renglon.append(f"${interes:.2f}")
        # Capital [3]
        capital = float(renglon[1].replace('$', '')) - float(renglon[2].replace('$', ''))
        renglon.append(f"${capital:.2f}")
        # Saldo [4]
        saldo = saldo - float(renglon[1].replace('$', ''))
        renglon.append(f"${saldo:.2f}")
        tabla.add_row(renglon)
    print(tabla)


def mostrarClientes(listaClientes):
    num = 1
    for i in listaClientes:
        print(f"Cliente numero: {num}\nNombre: {i.nombre_completo}\tRFC: {i.rfc}\tEdad: {i.edad}\tFecha de Alta: {i.fecha_alta}\tTeléfono: {i.telefono}\tCorreo: {i.correo}")
        num = num + 1



def main():
    menu()

# Llamar a la función main para iniciar la ejecución del programa
if __name__ == "__main__":
    main()