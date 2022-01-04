from operaciones import *
from clases import *

def cargarUsuarioAclase(tipo,ide):      #funcion para leer un .txt y pasar los datos a un objeto

    global loginActual      #declarar variables globales
    global tipoActual
    global idActual
    tipoActual = str(tipo)
    idActual = str(ide)

    if tipo in ['F','f']:       #en caso de ser un usuario fisico

        with open('usuarios/fisicos/%d.txt' % ide) as userf:    #abrir el .txt con sus datos
            lineas = userf.read().split('\n')

        loginActual = persona_F(lineas[7],lineas[8],lineas[9],lineas[10],lineas[11],lineas[12],lineas[1],lineas[4],lineas[3],lineas[2],lineas[5],lineas[6],lineas[-5:])     #cargar atributos

    elif tipo in ['J','j']:     #en caso de ser un usuario fisico
        
        with open('usuarios/juridicos/%d.txt' % ide) as userj:  #abrir el .txt con sus datos
            lineas = userj.read().split('\n')

        loginActual = persona_J(lineas[7],lineas[8],lineas[9],lineas[10],lineas[1],lineas[4],lineas[3],lineas[2],lineas[5],lineas[6],lineas[-5:])       #cargar atributos


def guardarCambios():   #lo opuesto a la funcion anterior, pasar los datos de la clase a un .txt

    if tipoActual == 'F':     #identificar tipo de persona
        archivo = 'fisicos'
    elif tipoActual == 'J':
        archivo = 'juridicos'

    with open('usuarios/%s/%s.txt' % (archivo,idActual)) as usu:    #leer archivo con datos
        lineas = usu.read().split('\n')     #copiar cada linea como elementos de una lista

    lineas[2] = loginActual.pin         #cambiar los datos no constantes por los atrubitos
    lineas[5] = loginActual.saldoARS    #de la clase
    lineas[6] = loginActual.saldoUSD
    
    lineas[-1] = loginActual.historial[-1]      #y actualizar el historial
    lineas[-2] = loginActual.historial[-2]
    lineas[-3] = loginActual.historial[-3]
    lineas[-4] = loginActual.historial[-4]
    lineas[-5] = loginActual.historial[-5]
        
    with open('usuarios/%s/%s.txt' % (archivo,idActual),'w+') as usu:
        usu.write('\n'.join(str(line) for line in lineas))   #reescribir el .txt


while True:

    limpiar()   #limpiar la consola
    print(" Bienvenido a")
    print("                                                     ▄▄                    ")
    print("   ▄██▀▀▀█▄█                                       ▀███                    ")
    print(" ▄██▀     ▀█                                         ██                    ")
    print(" ██▀       ▀ ▀███▄██▄  ▄█▀██▄  █▀██▀▀▀██▄   ▄▄█▀█▄   ██   ▄██▀█▄   ▄██▀██▄ ")
    print(" ██            ██  ▀▀ ██   ██    ██    ██  ▄█▀   ██  ██  ██▀  ▄█  ██▀   ▀██")
    print(" ██▄    ▀████  ██      ▄▄████    ██    ██  ██▀▀▀▀▀▀  ██  ██       ██     ██")
    print(" ▀██▄     ██   ██     ██   ██    ██    ██  ██▄    ▄  ██  ██▄    ▄ ██▄   ▄██")
    print("   ▀▀██████▀  ▄██▄    ▀████▀█▄  ▄██▄  ▄██▄  ▀████▀ ▄████▄ ▀████▀   ▀█████▀ ")
    print("   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄            ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄  ")
    print(" █▀ ▄▄                         ▀▀▀▀██▄▄▄▄██▀▀▀▀                       ▄▄ ▀█")
    print(" ▀█▄▄▀                               ▀██▀                             ▀▄▄█▀")
    print("                                      ██                                   ")
    print("\n ¿Que desea hacer?\n")

    print(" Ingrese [1] si desea ingresar con una cuenta Granelco.")    #imprimir opciones
    print(" Ingrese [2] si desea ingresar como administrador.")
    print("\n Ingrese [-1] si desea salir.\n")
    opcionInicio = input()

    while opcionInicio not in ['1','2','-1']:   #asegurarse de que se ingrese una opcion valida
        opcionInicio = input("Opcion invalida. Vuelva a intentarlo: ")

    if opcionInicio == '-1':    #salir del loop principal y finalizar programa
        break

    elif opcionInicio == '1':   #iniciar sesion con cuenta Granelco
        aux = loginUsuario()    #llamar a la funcion y guardar el resultado en una variable (T o F)

        if not aux:     #en caso de que haya fallado el login, por cualquier razon
            print("\nIntento de inicio de sesion fallido.")
            input("\n\nPresione ENTER para continuar...")
        else:
            cargarUsuarioAclase(aux[0],int(aux[1]))     #crear un nuevo objeto con los datos del usuario
                                                        #como atributos
            while True:     
                limpiar()   #limpiar la consola
                if tipoActual in ['f','F']:     #en caso de usuario fisico
                    print(" Bienvenido, "+str(loginActual.nombre)+" "+str(loginActual.apellido))
                if tipoActual in ['j','J']:     #en caso de usuario juridico
                    print(" Bienvenido, "+str(loginActual.rasoc))   #dar la bienvenida al usuario

                print("\n\nIngrese [1] si desea ver los datos del usuario.")    #imprimir opciones
                print("Ingrese [2] si desea depositar billetes.")
                print("Ingrese [3] si desea retirar billetes.")
                print("Ingrese [4] si desea modificar su PIN.")
                print("\nIngrese [-1] si desea cerrar sesion.")
                opcionLogin = input()

                while opcionLogin not in ['1','2','3','4','-1']:    #asegurarse de que se ingrese una opcion valida
                    opcionLogin = input("Opcion invalida. Vuelva a intentarlo: ")
                
                if opcionLogin == '-1':     #cerrar sesion del usuario actual

                    print("\nCerrando sesion...")
                    guardarCambios()        #guardar los datos actualizados del usuario
                    input("\n\nPresione ENTER para continuar...")
                    break

                if opcionLogin == '1':          #ejecutar una funcion en base a la opcion elegida
                    loginActual.imprimirDatos()         #mostrar datos del usuario

                if opcionLogin == '2':
                    loginActual.depositarBilletes()     #depositar billetes en el cajero
                    
                if opcionLogin == '3':
                    loginActual.retirarBilletes()       #extraer billetes del cajero

                if opcionLogin == '4':
                    auxPin = loginActual.cambiarPin()   #modificar pin de la cuenta
                    guardarCambios()

                    if not auxPin:
                        bloquearUsuario(tipoActual,idActual,"Excesivos intentos de modificacion de PIN")
                        
                        limpiar()   #limpiar la consola
                        print("\nNumero maximo de intentos excedido.")     #avisar circunstancias
                        print("Por motivos de seguridad, la cuenta ha sido suspendida.")
                        print("Contactese con un administrador del sistema para rehabilitarla.")
                        input("\n\nPresione ENTER para continuar...")

                    break

                guardarCambios()    #guardar datos del usuario despues de cada accion

    elif opcionInicio == '2':   #si se desea iniciar sesion en modo administrador
        
        OA = Administrador()        #crear objeto de la clase administrador
        OA.loginAdministrador()     #llamado al metodo principal de la clase (ahi esta todo)


limpiar()   #limpiar la consola
print("\n Hasta luego.")    #mensaje final