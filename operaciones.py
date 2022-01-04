import datetime
import os
import random


def limpiar():      #cosa rara en ANSI que limpia la consola
    os.system('cls')


def crearIdentificador(tipo,tarj,num,ide):      #relacionar un numero de tarjeta con un usuario

    if tipo == 'f':     #cambiar minusculas por mayusculas, por las dudas
        t = 'F'
    if tipo == 'j':
        t = 'J'
    with open('usuarios/identificador.txt','a') as iden:    #abrir un archivo
        iden.write(t+" "+str(tarj)+" "+str(num)+" "+str(ide)+"\n")    #definir su tipo, numero e id


def loginUsuario():

    limpiar()   #limpiar la consola

    print(" Si desea ingresar como persona fisica, ingrese [F]\n Si desea ingresar como persona juridica, ingrese [J]\n\n Ingrese [-1] para cancelar.")    #pedir tipo de usuario
    tipo = input()

    while tipo not in ['J','F','f','j','-1']:  #asegurarse de que lo ingresado sea valido
        tipo = input("Tipo no valido, vuelva a intentarlo: ")

    logeoF,logeoJ = False,False     #variables auxiliares

    if tipo == '-1':        #en caso de que se quiera cancelar
        return None 
    elif tipo in ['F','f'] :        #dependiendo la opcion pedida, llamar a la funcion de logeo
        logeoF = loginPersona('F')  #con el tipo de usuario pedido como argumento
        return logeoF
    elif tipo in ['j','J']:
        logeoJ = loginPersona('J')
        return logeoJ


def listaPosiblesLogin(tipo):   #evaluar cada posible usuario dependiendo de su tipo

    with open('usuarios/identificador.txt') as iden:    #abrir archivo
        
        listaIden = [(lis.strip('\n')) for lis in iden.readlines()]     #remover salto de linea
        listaIden = [lis.split() for lis in listaIden]                  #separar en distintos elementos
        listaIden = [lis for lis in listaIden if lis[0] == tipo]        #devolver solo los que coincidan en tipo de persona
    
    return listaIden


def loginPersona(tipo):

    if tipo == 'F':     #identificar tipo de persona
        archivo = 'fisicos'
    elif tipo == 'J':
        archivo = 'juridicos'
    
    limpiar()
    print("Seleccione la forma en la que desea ingresar...\n")      #pedir opcion
    print(" Ingrese [1] si desea iniciar sesion con su numero de Tarjeta y su PIN")
    print(" Ingrese [2] si desea iniciar sesion con su numero de DNI/CUIT y su PIN\n")
    opcion = input()

    while opcion not in ['1','2']:      #asegurarse de que no se ingrese cualquier cosa
        opcion = input("Opcion invalida. Vuelva a intentarlo: ")
    opcion = int(opcion)

    if opcion == 1:
        numero = input("Ingrese su numero de tarjeta: ")     #pedir tarjeta
    if opcion == 2:
        numero = input("Ingrese su numero de DNI/CUIT: ")     #pedir dni/cuit

    pin = input("Ingrese su PIN: ")     #pedir pin

    Liden = listaPosiblesLogin(tipo)    #aislar usuarios que puedan coincidir para el login
    
    intentos = 3    #intentos para ingresar bien el pin
    ide = None      #ID sel usuario si es que existe

    for i in Liden:         #buscar en la lista de usuarios posibles
        if i[opcion] == numero:   #la primer coincidancia del dato ingresada
            ide = i[3]      #guardar la id correspondiente a esa tarjeta
            break       

    while ide == None:  #en caso de no haberla encontrado, la tarjeta fue ingresada mal o no existe

        numero = input("\nERROR: Numero de cuenta no encontrado o inexistente,\nvuelva a intentarlo.\n\nIngrese [-1] para cancelar.\n")       #volver a pedir la tarjeta
        if numero == '-1':   #en caso de que se desee cancelar
            print("\nOperacion cancelada.")
            return None

        for i in Liden:         #mismo metodo de busqueda que antes
            if i[opcion] == numero:
                ide = i[3]
                break
                
    with open('usuarios/%s/%s.txt' % (archivo,ide)) as usu:     #abrir archivo con los datos del usuario segun su ID
        lineas = usu.read().split('\n')     #cargar datos a una lista

    while intentos >0:  #mientras que no se exceda el maximo de intentos
        
        if lineas[2] == pin and lineas[0] == ':(':      #si la tarjeta y el pin coinciden pero el usuario esta bloqueado 
            limpiar()   #limpiar la consola
            print("La cuenta a la cual esta tratando de ingresar esta suspendida.")
            print("Contactese con un administrador del sistema para rehabilitarla.")
            return False    #avisar que no se pudo iniciar sesion

        elif lineas[2] == pin and not detectarVencimiento(lineas[4]):
            limpiar()   #limpiar la consola
            print("La cuenta a la cual esta tratando de acceder ha caducado.")
            print("Contactese con un administrador para renovarla.")
            return False    #avisar que la cuenta/tarjeta esta vencida
        
        elif lineas[2] == pin:  #pin coincidente y usuario habilitado
            print("Acceso concedido. Bienvenido.")
            return [tipo,ide]
        
        else:       #pin incorrecto
            intentos -=1    #disminucion al numero de intentos
            print("\nEl PIN ingresado no es valido, intentelo nuevamente\n ["+str(intentos)+"] intento(s) restante(s)")

            pin = input()   #volver a pedir el pin

    bloquearUsuario(tipo,ide,"Excesivos intentos de inicio de sesion")    #suspender al usuario si se excedio el numero de intentos
    return False
    

def bloquearUsuario(tipo,aidi,razon):

    if tipo == 'F':     #identificar tipo de persona
        archivo = 'fisicos'
    elif tipo == 'J':
        archivo = 'juridicos'

    with open('usuarios/%s/%s.txt' % (archivo,aidi)) as usu:     #abrir archivo con los datos del usuario segun su ID
        lista = usu.read().split('\n')     #cargar datos a una lista

    if tipo == 'F':     #identificar tipo de persona
        archivo = 'fisicos'
    elif tipo == 'J':
        archivo = 'juridicos'
    
    limpiar()
    print("\nNumero maximo de intentos excedido.")     #avisar circumstancias
    print("Por motivos de seguridad, la cuenta ha sido suspendida.")
    print("Contactese con un administrador del sistema para rehabilitarla.")

    fechahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

    with open('usuarios/%s/%s.txt' % (archivo,aidi),'w+') as usu:   #abrir archivo de datos
        lista[0] = ':('     #la ':(' significa 'cuenta suspendida'

        lista[-2],lista[-3],lista[-4],lista[-5] = lista[-1],lista[-2],lista[-3],lista[-4]
        lista[-1] = fechahora + " - Usuario bloqueado por el sistema. Razon: " + razon

        usu.write('\n'.join(str(line) for line in lista))   #reescribir el .txt con la linea cambiada


def detectarVencimiento(fven):  #declaro la funcion

    hoy = [int(datetime.datetime.now().strftime("%d")),int(datetime.datetime.now().strftime("%m")),int(datetime.datetime.now().strftime("%Y"))]     #paso la fecha de hoy a una lista de enteros

    fvenUsuario = fven.split('/')   #separo el string de la fecha de vencimiento del usuario
    fvenUsuario = [int(n) for n in fvenUsuario]     #paso cada numero a int

    return (hoy[2] < fvenUsuario[2]) or ( (hoy[2] == fvenUsuario[2]) and (hoy[1] < fvenUsuario[1]) ) or ( (hoy[2] == fvenUsuario[2]) and (hoy[1] == fvenUsuario[1]) and (hoy[0] <= fvenUsuario[0]) )   #comparar las fechas y devolver True o False



def leerBilletes(tipoMoneda):
  
    with open('billetes/%s.txt' % tipoMoneda) as file:  #abrir archivo con la lista de cantidades
        billetes = file.readlines()             #crear lista de lineas de tipo str
        billetes = [int(b) for b in billetes]   #pasar la lista a enteros

    return billetes     #devolver dicha lista


def listaBilletesPosibles(tipoMoneda):  #esta funcion es simplemente un selector

    if tipoMoneda == 'ARS':         #en caso de pedir la lista de billetes de pesos
        return [10,20,50,100,200,500,1000]
    elif tipoMoneda == 'USD':       #en caso de pedir la lista de billetes de dolares
        return [1,2,5,10,20,50,100]
    else:
        print("ERROR: Moneda invalida.")    #avisar en caso de error
        return None


def totalBilletes(tipoMoneda):  #declaro la funcion para contar la plata total adentro del cajero

    tipos = listaBilletesPosibles(tipoMoneda)   #valores admitidos de los billetes
    stock = leerBilletes(tipoMoneda)            #cantidad de cada billete

    total = 0   #total de plata
    for i in range(len(stock)):         #iterar por cada tipo de billete
        total += stock[i] * tipos[i]    #sumar la cantidad de plata por tipo al total

    return total    #devolver la suma


def reemplazarBilletes(lista,tipoMoneda):

    if not len(lista) == 7:     #asegurarse de que solo haya 7 tipos de billetes
        print("ERROR: Lista de billetes invalida")
        return None

    with open('billetes/%s.txt' % tipoMoneda,'w') as file:  #abrir archivo de stock
        for num in lista:
            file.write(str(num)+"\n")   #reemplazar cantidades


def numEnBilletes(num,tipoMoneda):  #funcion para convertir un entero a cantidad en billetes

    if tipoMoneda == 'ARS' and not num % 10 == 0:   #asegurarse de que la conversion se pueda hacer
        print("\nERROR: No es posible realizar una transaccion en ARS con valores menores a $10")
        return None

    tipos = listaBilletesPosibles(tipoMoneda)   #lista de valores de los billetes dependiendo la moneda
    indice = 6      #variables auxiliares
    grupo = []

    while indice >= 0:      #empezar desde el billete mas grande
        cant = 0

        while num >= 0:     #restar sucesivamente ese valor hasta superar el monto pedido
            num -= tipos[indice]    
            cant += 1

        num += tipos[indice]    #sumar una vez dicho valor para volver a un numero positivo
        cant -= 1
        indice -= 1     #disminuir el indice en la lista de tipos de billetes
        grupo.insert(0,cant)    #guardar la cantidad a la que se llego en una lista

    return grupo    #devolver la lista con la cantidad de cada billete ordenada

