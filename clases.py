import operaciones

class Granelco:     #clase Granelco

    t = 'placeholder'       #atributos constantes
    tipo = 'placeholder'

    def __init__(self,ntar,fven,cseg,pin,saldoARS,saldoUSD,historial):        #atributos de la clase

        self.saldoARS = str(saldoARS)
        self.saldoUSD = str(saldoUSD)
        self.ntar = str(ntar)
        self.fven = str(fven)
        self.cseg = str(cseg)
        self.pin = str(pin)
        self.historial = historial


    def depositarBilletes(self):     #definir metodo de clase para ingresar billetes

        operaciones.limpiar()
        tipoMoneda = input("Ingrese el tipo de moneda con el que desea operar (ARS o USD): ")

        while tipoMoneda not in ['ARS','USD']:
            tipoMoneda = input("Tipo invalido, vuelva a intentarlo (se deben repetar las mayusculas): ")

        tipos = operaciones.listaBilletesPosibles(tipoMoneda)   #creacion de variables a usar
        stock = operaciones.leerBilletes(tipoMoneda)

        fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

        print("\nIngrese la cantidad de billetes de cada tipo que desea depositar...\n")

        total = 0       #monto total ingresado
        ingresado = []  #lista de billetes ingresados
        auxiliar = -1

        for i in range(len(tipos)):
            ingresado.append(int(input(" Billetes de "+str(tipos[i])+" : ")))   #pedir biletes de cada tipo

            while ingresado[i] <0:  #comprobar que no se ingrese un numero negativo
                auxiliar = int(input("ERROR: Numero ingresado no admitido, vuelva a intentarlo: "))
                ingresado.pop(-1)
                ingresado.append(auxiliar)

            total += tipos[i] * ingresado[i]    #sumar lo ingresado al total

        if tipoMoneda == 'ARS':     #pedir confirmacion
            confirmar = input("\nEl total ingresado es de AR$ "+str(total)+"\nSu nuevo balance sera de: AR$ "+str(int(self.saldoARS)+total)+"\n ¿Desea proceder? (S/N): ")     
        elif tipoMoneda == 'USD':
            confirmar = input("\nEl total ingresado es de U$D "+str(total)+"\nSu nuevo balance sera de: U$D "+str(int(self.saldoUSD)+total)+"\n ¿Desea proceder? (S/N): ")

        while confirmar not in ['S','s','N','n']:
            confirmar = input("Opcion invalida. Vuaelva a intentarlo: ")

        if confirmar in ['N','n']:    #en caso de querer cancelar
            print("Operacion cancelada.")
            input("\n\nPresione ENTER para continuar...")
            return None

        elif confirmar in ['S','s']:  #confirmado

            for i in range(len(stock)):     #sumar lo el stock del cajero a lo ingresado
                stock[i] += ingresado[i]

            operaciones.reemplazarBilletes(stock,tipoMoneda)    #actualizar stock

            if tipoMoneda == 'ARS': #cambiar el atributo de saldo en la clase dependiendo de la moneda
                self.saldoARS = str(int(self.saldoARS) + total)
                paraRegistro = self.saldoARS
            elif tipoMoneda == 'USD':
                self.saldoUSD = str(int(self.saldoUSD) + total)
                paraRegistro = self.saldoUSD

            hist = self.historial.copy()    #copiar historial
            for i in range(4):              #ciclar todos los elementos
                hist[i] = hist[i+1]

            hist[4] = fechahora + " - Depositados " + tipoMoneda + " " + str(total) + ". Balance actual de " + tipoMoneda +" "+ paraRegistro  #crear nuevo registro
            self.historial = hist       #guargar regisro en atributo de la clase

            print("\nOperacion realizada exitosamente.")
            input("\n\nPresione ENTER para continuar...")
            return True     #terminar la funcion


    def retirarBilletes(self):     #lo mismo que lo de arriba pero para retirar billetes

        operaciones.limpiar()
        tipoMoneda = input("Ingrese el tipo de moneda con el que desea operar (ARS o USD): ")

        while tipoMoneda not in ['ARS','USD']:
            tipoMoneda = input("Tipo invalido, vuelva a intentarlo (se deben repetar las mayusculas): ")

        tipos = operaciones.listaBilletesPosibles(tipoMoneda)   #creacion de variables a usar
        stock = operaciones.leerBilletes(tipoMoneda)

        fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

        print("\nIngrese la cantidad de billetes de cada tipo que desea retirar...\n")

        total = 0       #monto total ingresado
        pedido = []     #lista de billetes ingresados
        auxiliar = -1

        for i in range(len(tipos)):
            pedido.append(int(input(" Billetes de "+str(tipos[i])+" : ")))   #pedir biletes de cada tipo

            while pedido[i] <0:  #comprobar que no se ingrese un numero negativo
                auxiliar = int(input("ERROR: Numero ingresado no admitido, vuelva a intentarlo: "))
                pedido.pop(-1)
                pedido.append(auxiliar)

            total += tipos[i] * pedido[i]    #sumar lo ingresado al total

        if (tipoMoneda == 'ARS' and total > int(self.saldoARS)) or (tipoMoneda == 'USD' and total > int(self.saldoUSD)):    #en caso de que el saldo no alcance
            print("\nEl balance actual de la cuenta en la moneda especificada NO es suficiente\ncomo para completar la accion.")
            input("\n\nPresione ENTER para continuar...")
            return None

        if tipoMoneda == 'ARS':     #pedir confirmacion
            confirmar = input("\nEl total pedido es de "+ tipoMoneda +" "+str(total)+"\nSu nuevo balance sera de: AR$ "+str(int(self.saldoARS)-total)+"\n ¿Desea proceder? (S/N): ")     
        elif tipoMoneda == 'USD':
            confirmar = input("\nEl total pedido es de "+ tipoMoneda +" "+str(total)+"\nSu nuevo balance sera de: U$D "+str(int(self.saldoUSD)-total)+"\n ¿Desea proceder? (S/N): ")

        while confirmar not in ['S','s','N','n']:   #asegurarse de que no se ingrese cualquier cosa
            confirmar = input("Opcion invalida. Vuaelva a intentarlo: ")

        if confirmar in ['N','n']:    #en caso de querer cancelar
            print("Operacion cancelada.")
            input("\n\nPresione ENTER para continuar...")
            return None

        elif confirmar in ['S','s']:  #confirmado

            for i in range(len(stock)):     #restar lo ingresado al stock interno del cajero
                stock[i] -= pedido[i]

                if stock[i] <0:     #en caso de que el cajero no pueda completar la accion
                    operaciones.limpiar()
                    print("\nLa operacion no puede completarse debido a que el deposito del cajero\nno cuenta con un stock de billetes suficiente para cubrir lo solicitado.")
                    print("\nPor favor presentese en caja y solicite ahi el monto que necesite.")
                    print("Disculpe las molestias.")
                    input("\n\nPresione ENTER para continuar...")
                    return False
             
            operaciones.reemplazarBilletes(stock,tipoMoneda)    #actualizar stock

            if tipoMoneda == 'ARS': #cambiar el atributo de saldo en la clase dependiendo de la moneda
                self.saldoARS = str(int(self.saldoARS) - total)
                paraRegistro = self.saldoARS
            elif tipoMoneda == 'USD':
                self.saldoUSD = str(int(self.saldoUSD) - total)
                paraRegistro = self.saldoUSD

            hist = self.historial.copy()    #copiar historial
            for i in range(4):              #correr todos los elementos
                hist[i] = hist[i+1]

            hist[4] = fechahora + " - Retirados " + tipoMoneda + " " + str(total) + ". Balance actual de " + tipoMoneda +" "+ paraRegistro  #crear nuevo registro
            self.historial = hist       #guargar regisro en atributo de la clase

            print("\nOperacion realizada exitosamente.")
            input("\n\nPresione ENTER para continuar...")
            return True     #terminar la funcion


    def cambiarPin(self):

        operaciones.limpiar()
        fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

        print("Cambiar PIN...")
        intentos = 3
        pinActual = input("Ingrese su PIN actual: ")

        while intentos >0:

            if pinActual == self.pin:
                nuevoPin = input("\nIngrese su nuevo PIN: ")
                nuevoPin2 = input("Vuelva a ingresar su nuevo PIN para confirmar: ")

                if nuevoPin == nuevoPin2:
                    self.pin = nuevoPin

                    print("\nSu PIN ha sido cambiado exitosamente.")
                    print("Su sesion se cerrara para guardar los cambios.")

                    hist = self.historial.copy()    #copiar historial
                    for i in range(4):              #correr todos los elementos
                        hist[i] = hist[i+1]

                    hist[4] = fechahora + " - Pin de la cuenta modificado. Pin obsoleto: "+ pinActual
                    self.historial = hist       #guargar registro en atributo de la clase
                    
                    input("\n\nPresione ENTER para continuar...")
                    return True

                else:
                    print("\nLos pines ingresados no coinciden. Vuelva a intentarlo.")

            else:       #pin incorrecto
                intentos -=1    #disminucion al numero de intentos
                print("El PIN ingresado no es valido, intentelo nuevamente\n ["+str(intentos)+"] intento(s) restante(s)")

                pinActual = input()   #volver a pedir el pin

        return False







class persona_F(Granelco):  #clase Persona Fisica que hereda de Granelco

    t = 'F'
    tipo = "fisicos"

    def __init__(self, nombre,apellido,dni,fnac,prof,genero, *args,**kwargs):   #atributos nuevos + los de Granelco

        self.nombre = str(nombre)
        self.apellido = str(apellido)
        self.dni = str(dni)
        self.fnac = str(fnac)
        self.prof = str(prof)
        self.genero = str(genero)

        super().__init__(*args,**kwargs)    #pedir atributos de Granelco


    def imprimirDatos(self):

        operaciones.limpiar()   #limpiar la consola
        print("\nDatos de usuario:")

        print("\n Nombre: "+self.nombre)    #datos personales
        print(" Apellido: "+self.apellido)
        print(" DNI: "+self.dni)
        print(" Fecha de nacimiento: "+self.fnac)
        print(" Profesion: "+self.prof)
        print(" Genero: "+self.genero)

        print("\n Saldo en pesos argentinos: "+str(self.saldoARS)+ " AR$")      #saldo
        print(" Saldo en dolares estadounidenses: "+str(self.saldoUSD)+ " U$D")

        print("\nHistorial de acciones del usuario:\n")
        for i in range (-5,0):
            print(self.historial[i])

        input("\n\nPresione ENTER para continuar...")



class persona_J(Granelco):  #clase Persona juridica que hereda de Granelco

    t = 'J'
    tipo = 'juridicos'

    def __init__(self, rasoc,cuit,iniact,rubro, *args,**kwargs):    #atributos nuevos + los de Granelco

        self.rasoc = str(rasoc)
        self.cuit = str(cuit)
        self.iniact = str(iniact)
        self.rubro = str(rubro)

        super().__init__(*args,**kwargs)    #pedir atributos de Granelco

    def imprimirDatos(self):

        operaciones.limpiar()   #limpiar la consola
        print("\nDatos de usuario:")

        print("\n Razon social: "+self.rasoc)    #datos personales
        print(" CUIT: "+self.cuit)
        print(" Fecha de inicio de actividades: "+self.iniact)
        print(" Rubro : "+self.rubro)

        print("\n Saldo en pesos argentinos: "+str(self.saldoARS)+ " AR$")      #saldo
        print(" Saldo en dolares estadounidenses: "+str(self.saldoUSD)+ " U$D")

        print("\nHistorial de acciones del usuario:\n")
        for i in range (-5,0):
            print(self.historial[i])

        input("\n\nPresione ENTER para continuar...")

class Administrador:

    nombre = "Admin"            #atributos constantes de la clase
    password = "314159265"

    def loginAdministrador(self):   #declarar la funcion para el login

        operaciones.limpiar()   #limpiar la consola

        print(" Ingreso al sistema en modo administrador...\n")
        nom = input("Ingrese su Nombre: ")      #pedir datos
        pw = input("Ingrese su contraseña de administrador: ")

        if not self.nombre == nom or not self.password == pw:       #en caso de que los atributos no coincidan con lo ingresado
            print("\n ERROR: Alguno de los datos ingresados es incorrecto.")
            input("\n\nPresione ENTER para continuar...")                  
            return False
        
        print("\nAcceso concedido. Bienvenido.\n")
        input("\n\nPresione ENTER para continuar...")

        while True:
            operaciones.limpiar()   #limpiar la consola

            print("¿Que desea hacer?\n")    #imprimir opciones
            print(" Ingrese [1] si desea registrar a una nueva persona.")
            print(" Ingrese [2] si desea desbloquear a un usuario.")
            print(" Ingrese [3] si desea realizar un arquedo de la caja.")
            print("\n Ingrese [-1] para cerrar sesion.")

            opcion =input()   

            while opcion not in ['-1','1','2','3']:     #asegurarse de que no se ingrese cualquier cosa
                opcion =input("Opcion invalida. Vuelva a intentarlo: ")

            opcion = int(opcion)
            operaciones.limpiar()   #limpiar la consola

            if opcion == 1:     #opcion 1
                t = input(" Ingrese [F] si desea registrar a una persona fisica\n Ingrese [J] si desea registrar a una persona juridica\n")   #pedir tipo de usuario

                while t not in ['f','F','j','J']:  #asegurarse de que no se ingrese cualquier cosa
                    t =input("Opcion invalida. Vuelva a intentarlo: ")

                self.registrarPersona(t)   #llamar al metodo de clase

            elif opcion == 2:   #opcion 2
                self.desbloquearUsuario()  #llamar al metodo de clase

            elif opcion == 3:   #opcion 3
                self.arqueoCaja()      #llamar al metodo de clase
            
            elif opcion == -1:  #carrar sesion
                print("La sesion en modo administrador ha sido cerrada, adios.")
                input("\n\nPresione ENTER para continuar...")
                return None


    def registrarPersona(self,tipo):     #registrar nueva persona fisica o juridica (solo admin)

        operaciones.limpiar()
        rtarj = int(operaciones.random.randint(1000000000000000,9999999999999999))  #definir datos de granelco
        rpin = int(operaciones.random.randint(1000,9999))
        rcseg = int(operaciones.random.randint(100,999))
        fven = operaciones.datetime.datetime.now().strftime("%d/%m/%Y")     #viva python y sus puntitos

        fven = fven.split('/')      #formateo de la fecha de vencimiento
        fven[2] = str(int(fven[2])+5)
        fven = '/'.join(fven)

        if tipo == 'F' or tipo == 'f':     #creacion de persona fisica

            nombre = str(input("Ingrese su nombre: "))      #pedir datos
            apellido = str(input("Ingrese su apellido: "))
            dni = str(input("Ingrese su DNI (sin puntos ni espacios): "))
            fn = str(input("Ingrese su fecha de nacimiento [dd/mm/yyyy] : "))
            prof = str(input("Ingrese su profesion: "))
            genero = str(input("Ingrese su genero [M,F,X]: "))

            canTXT = len(operaciones.os.listdir('usuarios/fisicos'))    #definicion de ID a base de cantidad de usuarios fisicos
            numero = dni
            fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

            with open('usuarios/fisicos/%d.txt' % canTXT,'w') as userf:     #crear .txt con los datos
                userf.write(":)\n"+str(rtarj)+"\n"+str(rpin)+"\n"+str(rcseg)+"\n"+str(fven)+"\n0\n0\n"+str(nombre)+"\n"+str(apellido)+"\n"+str(dni)+"\n"+str(fn)+"\n"+str(prof)+"\n"+str(genero)+"\n\nNone\nNone\nNone\nNone\n"+fechahora +" - Usuario fisico creado")

        elif tipo == 'J' or tipo == 'j':   #creacion de persona juridica

            rs = str(input("Ingrese su razon social: "))    #pedir datos
            cuit = str(input("Ingrese su CUIT (sin puntos ni espacios): "))
            inac = str(input("Ingrese su fecha de inicio de actividades [dd/mm/yyyy]: "))
            rubro = str(input("Ingrese su rubro: "))

            canTXT = len(operaciones.os.listdir('usuarios/juridicos'))  #definicion de id a base de cantidad de usuarios juridicos
            numero = cuit
            fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

            with open('usuarios/juridicos/%d.txt' % canTXT,'w') as userj:   #crear .txt con los datos
                userj.write(":)\n"+str(rtarj)+"\n"+str(rpin)+"\n"+str(rcseg)+"\n"+str(fven)+"\n0\n0\n"+str(rs)+"\n"+str(cuit)+"\n"+str(inac)+"\n"+str(rubro)+"\n\nNone\nNone\nNone\nNone\n"+ fechahora +" - Usuario juridico creado")

        print("\nRegistro exitoso.\n Su numero de tarjeta es: "+str(rtarj)+"\n Su PIN es: "+str(rpin)+"\n Su codigo de seguridad es: "+str(rcseg)+"\n Su fecha de vencimiento es: "+str(fven))
        #imprimir datos de usuario Granelco generados

        operaciones.crearIdentificador(tipo,rtarj,numero,canTXT)   #linkear id con numero de tarjeta

        input("\n\nPresione ENTER para continuar...")


    def desbloquearUsuario(self):       #declaro la funcion 

        bloqueadosF =[]     #listas para cargar usuarios bloqueados
        bloqueadosJ =[]     #de cada tipo
        hayUsuarios = False

        print("Lista de usuarios suspendidos: ")
        print("\nFisicos:")

        for i in range(len(operaciones.os.listdir('usuarios/fisicos'))):    #iterar en la carpeta de usuarios fisicos

            with open('usuarios/fisicos/%d.txt' % i) as usuf:   #abrir el .txt
                lineas = usuf.read().split('\n')                # y pasar las lineas a una lista

            if lineas[0] == ':(':       #detectar que es un usuario bloqueado
                hayUsuarios = True
                bloqueadosF.append(i)               #añadirlo a la lista
                print(" ",i,":",lineas[7],lineas[8])    #imprimir nombre y apellido correspondientes

        print("\nJuridicos:")

        for i in range(len(operaciones.os.listdir('usuarios/juridicos'))):  #iterar en la carpeta de usuarios juridicos

            with open('usuarios/juridicos/%d.txt' % i) as usuj:     #abrir el .txt
                lineas = usuj.read().split('\n')                    #y pasar las lineas a una lista

            if lineas[0] == ':(':       #detectar que es un usuario bloqueado
                hayUsuarios = True
                bloqueadosJ.append(i)               #añadirlo a la lista
                print(" ",i,":",lineas[7])              #imprimir rubro correspondiente

        if not hayUsuarios:     #en caso de que no haya usuarios bloqueados
            print("\nNo hay usuarios para desbloquear.")
            input("\n\nPresione ENTER para continuar...")
            return None

        tipoOper = input("\n Ingrese [F] para desbloquear un usuario fisico.\n Ingrese [J] para desbloquear un usuario juridico.\n Ingrese [-1] para cancelar.\n")    #pedir operacion

        while tipoOper not in ['F','f','J','j','-1']:   #comprobar que sea valida
            tipoOper = input("Opcion invalida. Vuelva a intentarlo: ")

        if tipoOper == '-1':        #en caso de querer calcelar
            print("Operacion cancelada.")
            return None

        else :
            selector = input("Ingrese la ID del usuario a desbloquear: ")   #pedir ID

            if tipoOper == 'F' or tipoOper == 'f':      #selector de carpeta
                archivo = 'fisicos'                     #de usuarios correspondiente
            elif tipoOper == 'J' or tipoOper == 'j':
                archivo = 'juridicos'

            with open('usuarios/%s/%s.txt' % (archivo,selector)) as usu:    #abrir el .txt del usuario
                lineas = usu.read().split('\n')                             #y pasar las lineas a una lista

            fechahora = operaciones.datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")   #fecha y hora de la accion

            with open('usuarios/%s/%s.txt' % (archivo,selector),'w+') as usu:   #volver a abrirlo
                lineas[0] = ':)'    #y reescribir la primer linea
                lineas[-2],lineas[-3],lineas[-4],lineas[-5] = lineas[-1],lineas[-2],lineas[-3],lineas[-4]
                lineas[-1] = fechahora + " - Usuario desbloqueado por el Administrador"

                usu.write('\n'.join(str(line) for line in lineas))

            print("\nUsuario rehabilitado.")    #feedback
            input("\n\nPresione ENTER para continuar...")
            return True


    def arqueoCaja(self):       #Defino la funcion para el arqueo de caja

        print("Contando stock de billetes...")  #feedback

        listaPesos = operaciones.listaBilletesPosibles('ARS')       #declaracion de variables
        listaDolares = operaciones.listaBilletesPosibles('USD')
        listaCantPesos = operaciones.leerBilletes('ARS')
        listaCantDolares = operaciones.leerBilletes('USD')
        totalPesos = operaciones.totalBilletes('ARS')
        totalDolares = operaciones.totalBilletes('USD')

        modPesos = []   #listas para cargar desbalances de billetes
        modDolares = []

        print("\nHay en total:\n\n "+str(totalPesos)+" ARS, compuestos por:")   #imprimir total ARS

        for i in range(7):  #iterar por cada tipo de billete

            if listaCantPesos[i] > 10:            #si hay mas de 10
                num = listaCantPesos[i] - 10     #calcular cuantos sobran
                modPesos.append(num)            #guardarlo
                print("\t"+str(listaCantPesos[i])+"\tbilletes de AR$ "+str(listaPesos[i])+" -> Sobra(n) "+str(num))     #imprimir ambas cosas

            elif listaCantPesos[i] < 10:          #si hay menos de 10
                num = listaCantPesos[i] - 10     #calcular cuantos faltan
                modPesos.append(num)            #guardarlo
                print("\t"+str(listaCantPesos[i])+"\tbilletes de AR$ "+str(listaPesos[i])+" -> Falta(n) "+str(10- listaCantPesos[i]))   #imprimir ambas cosas

            else:
                modPesos.append(0)      #si no faltan ni sobran, no hay desbalance
                print("\t"+str(listaCantPesos[i])+"\tbilletes de AR$ "+str(listaPesos[i]))

        print("\n "+str(totalDolares)+" USD, compuestos por:")  #imprimir total USD

        for i in range(7):  #iterar por cada tipo de billete

            if listaCantDolares[i] > 10:          #si hay mas de 10
                num = listaCantDolares[i] - 10   #calcular cuantos sobran
                modDolares.append(num)          #guardarlo
                print("\t"+str(listaCantDolares[i])+"\tbilletes de U$D "+str(listaDolares[i])+" -> Sobra(n) "+str(num))     #imprimir ambas cosas

            elif listaCantDolares[i] < 10:        #si hay menos de 10
                num = listaCantDolares[i] - 10   #calcular cuantos faltan
                modDolares.append(num)          #guardarlo
                print("\t"+str(listaCantDolares[i])+"\tbilletes de U$D "+str(listaDolares[i])+" -> Falta(n) "+str(10- listaCantDolares[i]))     #imprimir ambas cosas

            else:
                modDolares.append(0)    #si no faltan ni sobran, no hay desbalance
                print("\t"+str(listaCantDolares[i])+"\tbilletes de U$D "+str(listaDolares[i]))

        if totalPesos > 18800 or totalDolares > 1880:   #si algun valor es mayor al stock default

            extraPesos = totalPesos - 18800         #calcular extra
            extraDolares = totalDolares - 1880 

            print("\n¿Desea extraer...")        #imprimir extra(s)
            if totalPesos > 18800:
                print("\t"+str(extraPesos)+" ARS")
            if totalDolares > 1880:
                print("\t"+str(extraDolares)+" USD")

            confirmar = input("\ny resetear el stock de billetes? (S/N): ") #confirmar accion

        elif listaCantPesos == [10,10,10,10,10,10,10] and listaCantDolares == [10,10,10,10,10,10,10]:  #en caso de no necesitar arqueo
            print("\nNo faltan ni sobran billetes.")
            input("\n\nPresione ENTER para continuar...")
            return None

        else:   #en caso de que falten billetes en ambas monedas
            confirmar = input("\n¿Desea reponer el stock de billetes faltantes? (S/N): ")

        while confirmar not in ['S','s','N','n']:   #asegurarse de que la opcion ingresada exista
            confirmar = input("Opcion invalida, vuelva a intentarlo: ")

        if confirmar == 'S' or confirmar == 's':    #resetear billetes
            operaciones.reemplazarBilletes([10,10,10,10,10,10,10],'ARS')
            operaciones.reemplazarBilletes([10,10,10,10,10,10,10],'USD')
            print("\nStock de billetes restablecido.")
            input("\n\nPresione ENTER para continuar...")
            return True
        elif confirmar == 'N' or confirmar == 'n':  #cancelar operacion
            print("\nOperacion cancelada.")
            input("\n\nPresione ENTER para continuar...")
            return False
            
