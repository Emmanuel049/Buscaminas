#Asignación de las constantes para el juego

FILAS = 11
COLUMNAS = 11
MINAS = 20

#Asignar una cadena que represente a cada elemento del juego (si se quisiese)

ELEMENTO_TABLERO = "."
ELEMENTO_MINA = "X"
ELEMENTO_BANDERA = "*"

#No modificar, asignaciones necesarias para el correcto funcionamiento

from random import randint
ABECEDARIO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main():
    """Función principal, llama a las demás funciones
    paso a paso para la ejecución del juego"""
    imprimir_bienvenida()
    jugar = True
    while jugar:
        jugadas = []
        banderas = []            
        derrota = False
        victoria = False
        tablero = crear_tablero()
        interfaz = crear_interfaz()
        lista_minas = generar_minas()
        while not derrota and not victoria:
            imprimir_tablero(interfaz, tablero)
            jugada = pedir_jugada()
            derrota = procesar_jugada(tablero, jugada, lista_minas, banderas, jugadas)
            victoria = hay_victoria(jugadas)
            if victoria:
                imprimir_tablero(interfaz, tablero)
                print()
                print ("Felicidades! encontró todas las casillas vacías!")
                print()
            if derrota:
                imprimir_tablero(interfaz, tablero)
                print()
                print ("Pisó una mina, fin del juego!")  
                print()              
        jugar = seguir_jugando()

def crear_tablero():
    """Crea la matriz utilizada para el tablero
    de dimensiones establecidas al incio y le
    asigna sus valores iniciales y lo devuelve"""
#CREACION DE LA MATRIZ
    tablero = []
    for i in range (FILAS):
        tablero.append([])
        for j in range (COLUMNAS):
#ASIGNACION DE VALORES INICIALES
            tablero[i].append(ELEMENTO_TABLERO)
    return tablero
    
def crear_interfaz():
    """Crea la interfaz utilizada para mostrarle
    al usuario en que coordenada se encuentra cada
    valor y la devuelve"""
    interfaz = []
    for i in range (FILAS+1):
        interfaz.append([])
        if i != 0:
            interfaz[i] = ABECEDARIO[i-1]
    for j in range (COLUMNAS+1):
        interfaz[0].append([])
        if j != 0:
            interfaz[0][j] = str(j)
    return interfaz        
        
def imprimir_tablero(interfaz,tablero):
    """Imprime el tablero cuando sea necesario mostrarle
    nueva información al usuario"""
    print ()
    for i in range (len(interfaz)):
        for j in range (len(interfaz[0])):
            if i == 0 and j == 0:
                print ("  ", "", end="")
            elif j == 0:
                print ("{:3}".format(interfaz[i][0]), end="")
            elif i == 0:
                print ("{:3}".format(interfaz[0][j]), end="")
            if i != 0 and j != 0:
                print ("{:3}".format(tablero [i-1][j-1]), end="")
        print()
    print()

def generar_minas():
    """Genera las minas en base a la cantidad de minas
    establecidas al inicio del programa, devuelve una 
    lista de posiciones donde estarán las minas."""
    lista_minas = []
    for i in range (MINAS):
        if MINAS > len(lista_minas):
            lista_minas.append([])
            while True:
                mina_generada = [ABECEDARIO[randint(1,FILAS)-1],str(randint(1, COLUMNAS))]
                if mina_generada not in lista_minas:
                    break
            lista_minas[i] = mina_generada
    return lista_minas
  
def pedir_jugada():
    """Le pide al usuario que ingrese una posición y
    determina si es una posición válida o una puesta
    de bandera, si es válida devuelve la jugada."""
    n = input("Ingrese una posición (Ejemplo: a,3 ó b,2,"+ELEMENTO_BANDERA+"): ")
    while True:
        jugada=n.split(",")
        jugada_verificada = verificar_jugada(jugada)
        if jugada_verificada != False:
            break
        n = input ("Ingrese una jugada válida (Ejemplo: a,3 ó b,2,"+ELEMENTO_BANDERA+"): ")
    return jugada_verificada
          
def verificar_jugada(jugada):
    """Verifica que el usuario haya hecho una jugada válida
    y en ese caso la devuelve."""
    if len(jugada) < 2 or len(jugada) > 3:
        return False
    if jugada[1].isdigit() and jugada[0].upper() in ABECEDARIO[:FILAS:] and int(jugada[1]) <= COLUMNAS and int(jugada[1]) > 0:
        if len(jugada) == 3 and jugada[2] == ELEMENTO_BANDERA:
            jugada[0]=jugada[0].upper()
            return jugada
        jugada[0]=jugada[0].upper()
        return jugada
    return False
                 
def procesar_jugada(tablero, jugada, lista_minas, banderas, jugadas):
    """Recibe la jugada del usuario y dependiendo del tipo de
    jugada que se haya hecho, realiza una acción diferente, 
    también devuelve False si no pisó una mina y True si la pisó
    (derrota)"""
    if len(jugada) == 3:
        if [jugada[0],str(int(jugada[1]))] not in jugadas:
            if [jugada[0],str(int(jugada[1]))] in banderas: 
                tablero [ABECEDARIO.index(jugada[0])][int(jugada[1])-1] = ELEMENTO_TABLERO
                banderas.remove([jugada[0],str(int(jugada[1]))])
            else:
                tablero [ABECEDARIO.index(jugada[0])][int(jugada[1])-1] = ELEMENTO_BANDERA
                banderas.append([jugada[0],str(int(jugada[1]))])
        else:
            print("No puede poner una bandera en una casilla revisada")
    elif len(jugada) == 2 and jugada not in lista_minas:
        if jugada not in banderas:
            if jugada not in jugadas:
                a = ABECEDARIO.index(jugada[0])    #a sería la fila de la jugada y la represento así para abreviar luego
                b = int(jugada [1])-1    #b representa la columna y abrevia para llamar a la función contar_minas
                contador = contar_minas(jugada, a, b, tablero, lista_minas)
                tablero [a][b] = contador
                jugadas.append(jugada)
            else:
                print("No puede revisar una posición ya revisada, ingrese otra")
        else:
            print("No puede revisar una casilla ocupada por una bandera, primero saque la bandera")
    elif jugada in lista_minas:
        if jugada not in banderas:
            a = ABECEDARIO.index(jugada[0])
            b = int(jugada [1])-1
            if tablero [a][b] == ELEMENTO_TABLERO:
                tablero [a][b] = ELEMENTO_MINA
                return True
        else:
            print("No puede revisar una casilla ocupada por una bandera, primero saque la bandera")
    return False
        
def contar_minas(jugada, a, b, tablero, lista_minas):
    """Recibe una jugada y cuenta la cantidad de minas que haya alrededor
    de la casilla seleccionada para devolver el número que indicará al
    usuario la información necesaria para seguir jugando"""
    contador = 0
    for i in range (-1,2):
        for j in range (-1,2):
            if a+i >= 0 and b+j >= 0 and a+i < FILAS and b+j < COLUMNAS and [ABECEDARIO[a+i],str(b+j+1)] in lista_minas:
                contador += 1
    return str(contador)
     
def hay_victoria(jugadas):
    """Determina si el número de minas y el número de jugadas son
    iguales a la cantidad de posiciones totales para determinar si
    ganó"""
    if MINAS+len(jugadas) == FILAS*COLUMNAS:
        return True
    return False
        
def seguir_jugando():
    """Pide al usuario si se quiere seguir jugando o
    se corta el programa"""
    n = input("Quiere volver a jugar? (s/n): ")
    while True:
        if n == "s":
            return True
        if n == "n":
            return False
        print ()
        n = input("Ingrese una opción válida: ")        
        
def imprimir_bienvenida():
    """Imprime una bienvenida para el usuario y le pregunta
    si quiere conocer las reglas o quiere jugar"""
    print ()
    print ("##############################")
    print ("$$$$$$$$$$BUSCAMINAS$$$$$$$$$$")
    print ("##############################")
    print ("###***Versión BETA 2.015***###")
    print ("##############################")
    print ()
    print ("Para empezar seleccione una opción:")
    print ()
    print ("1. Empezar a jugar")
    print ("2. Como jugar")
    print ()
    while True:
        s = input("Ingrese una opción: ")
        if s != "1" and s != "2":
            print()
            print("Ingrese un comando válido!")
            print()
        elif s == "2":
            print()
            print ("Al empezar contará con un tablero con coordenadas alfabéticas y numéricas de",FILAS,"filas y",COLUMNAS,"columnas. Para ganar deberá encontrar todos los puntos en los que no haya minas, el tablero comenzará oculto y las",MINAS,"minas se generarán aleatoriamente. Al ingresar una posición donde no haya una mina aparecerá un número que indicará la cantidad de minas alrededor de la posición. Para jugar deberá ingresar una letra seguida de una coma y un número, y si se quisiese poner una bandera: otra coma y un asterisco, por ejemplo si quisiese marcar la posición de la tercera fila y la cuarta columna ingresará: c,4 y si quisiera poner o sacar una bandera ya puesta en esa posición ingresaría: c,4," + ELEMENTO_BANDERA + " mucha suerte!")
            print()
        elif s == "1":
            print ()
            return
            
main()