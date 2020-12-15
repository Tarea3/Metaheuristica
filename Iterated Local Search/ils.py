# -*- coding: utf-8 -*-
import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion # Codigo que sirve para hacer la animacion

graficar_ruta = False
coord_x = []
coord_y = []
problem = tsplib95.load('instancias/st70.tsp')

# distancia entre la ciudad i y j
def distancia(i, j):
    u = i+1, j+1
    return problem.get_weight(*u)

# Costo de la ruta
def costoTotal(ciudad):
    suma = 0
    i = 0
    while i < len(ciudad) - 1:
        # print(ciudad[i], ciudad[i +1])
        suma += distancia(ciudad[i], ciudad[i + 1])
        i += 1
    suma += distancia(ciudad[-1], ciudad[0])
    return suma

# heurística del vecino más cercano
def vecinoMasCercano(n, desde):
    actual = desde
    ciudad = []
    ciudad.append(desde)
    seleccionada = [False] * n
    seleccionada[actual] = True # Lista donde se van guardando las ciudades que ya se visitaron

    # Aqui se va construyendo la solucion
    while len(ciudad) < n:
        min = 9999999
        for candidata in range(n):
            if seleccionada[candidata] == False and candidata != actual:
                costo = distancia(actual, candidata)
                if costo < min:
                    min = costo
                    siguiente = candidata

        ciudad.append(siguiente)
        seleccionada[siguiente] = True
        actual = siguiente

    return ciudad

# Búsqueda local 2-opt
    # Esto significa que se estan considerando dos aristas.
    # Entre mas aristas se consideren deberia ser mejor, lo que implica mas for anidados (Las combinaciones suben n!)
def DosOpt(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    # Esto luego comienza a demorarse porque se esta ejecutando completo. Al principio como la solucion inicial no es tan buena se mejora facilmente.
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < 0:
                min_i, min_j = i, j
                contar += 1
                # Si se encuentra una mejora se sale del algoritmo
                if contar == 1:
                    flag = False

        if flag == False:
            break
    # Aqui se hace el cambio e invierte la ruta, en las busquedas locales hay que intentar de ahorrar la mayor cantidad de tiempo posible, por eso es mejor sacarlo altiro.
    if contar > 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]

# perturbación: se escogen dos ciudades aleatorias y las intercambia
def perturbation(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    # Es lo mismo que la de abajo, pero en vez de hacer el intercambio con el siguiente lo hace aleatorio
    while i == j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

# perturbación: se escoge una ciudad aleatoria y se intercambia con la ciudad siguiente en la ruta
def perturbation3(ciudad):
    j = 0
    n = len(ciudad)
    i = random.randint(0, n - 1)
    
    # Esto esta porque puede pasar que justo la ultima ciudad que se escoge es la ultima, y la que se sigue de la ultima es la primera
    if i == n - 1:
        j = 0
    else:
        j = i + 1
    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp

# Esta perturbacion es una poco mas sofisticada y lo que hace es invertir. Por ej:
    # 1 8 2 4 6 7 3 5 9 10
    # 1 8 7 6 4 2 3 5 9 10
def perturbation2(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    ciudad[i : j] = ciudad[i : j][::-1]

# Lo unico que no tiene sentido es aplicar una perturbacion despues de otra.
def ILS(ciudad):
    random.seed(1) # Le tengo que cambiar el valor si quero ocupar otra semilla
    inicioTiempo = time.time()
    n = len(ciudad)
    # Solución inicial
    s = vecinoMasCercano(n, 0)#random.randint(0, n))
    DosOpt(s)

    s_mejor = s[:]
    costoMejor = costoTotal(s_mejor)
    lista_soluciones = []
    lista_costos = []
    lista_costosMejores = []
    lista_costos.append(costoMejor)
    lista_costosMejores.append(costoMejor)
    lista_soluciones.append(s_mejor)
    print("inicial %d" % costoMejor)
    iterMax = 500
    for iter in range(iterMax):
        # Se pueden usar las perturbaciones que yo quiera. Con un if, que se produzca una perturbacion en algunos monentos y otra en otros. Con numeros de manera aleatoria por ejemplo.
        # Perturbación
        perturbation3(s)
        # Búsqueda local
        DosOpt(s)
        costo_candidato = costoTotal(s)
        # Actualizar mejor solución
        if costoMejor > costo_candidato:
            s_mejor = s[:]
            costoMejor = costo_candidato
            print("%d\t%d" % (iter, costoMejor))

        # Guardando las soluciones para despues hacer un grafico
        lista_costos.append(costo_candidato)
        lista_costosMejores.append(costoMejor)
        lista_soluciones.append(s)
        # criterio de aceptación de la solución actual
        if abs(costoMejor - costo_candidato) / costoMejor > 0.05:
            s = s_mejor[:]

    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo
    print("Costo  : %d" % costoMejor)
    print("Tiempo : %f" % tiempo)
    print(s_mejor)

    if graficar_ruta:
        lista_soluciones.append(s_mejor)
        lista_costos.append(costoMejor)
        ver = animacion(lista_soluciones, coord_x, coord_y, lista_costos)
        ver.animacionRutas()
        graficar_soluciones(lista_costosMejores)

def graficar_soluciones(soluciones):
    plt.plot([i for i in range(len(soluciones))], soluciones)
    plt.ylabel("Costo")
    plt.xlabel("Iteraciones")
    plt.title("Iteraciones vs Costo - TSP")
    plt.xlim((0, len(soluciones)))
    plt.show()

# Para hacer un grafico en una ruta nomas
def graficar(coord_x, coord_y, solucion):
    plt.figure(figsize = (20,20))
    plt.scatter(coord_x, coord_y, color = 'blue')
    s = []
    for n in range(len(coord_x)):
        s_temp = []
        s_temp.append("%.1f" % coord_x[n])
        s_temp.append("%.1f" % coord_y[n])
        s.append(s_temp)

        plt.xlabel("Distancia X")
        plt.ylabel("Distancia Y")
        plt.title("Ubicacion de las ciudades - TSP")

    ruta = list(solucion)
    if len(ruta) != 0:
        for i in range(len(ruta))[:-1]:
            plt.plot([coord_x[ruta[i]], coord_x[ruta[i+1]]],[coord_y[ruta[i]], coord_y[ruta[i+1]]], color='b', alpha=0.4, zorder=0)
            plt.scatter(x = coord_x, y = coord_y, color='blue', zorder=1)
        plt.plot([coord_x[ruta[-1]], coord_x[ruta[0]]],[coord_y[ruta[-1]], coord_y[ruta[0]]], color='b', alpha=0.4, zorder=0)

    for n in range(len(coord_x)):
        plt.annotate(str(n), xy=(coord_x[n], coord_y[n] ), xytext=(coord_x[n]+0.5, coord_y[n]+1),color='red')

def main():
    G = problem.get_graph()
    ciudad = [i-1 for i in list(problem.get_nodes())]
    info = problem.as_keyword_dict() # Aqui guardo la info

    if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D': # se puede graficar la ruta
        global graficar_ruta
        graficar_ruta = True
        for i in range(1, len(ciudad) + 1):
            x, y = info['NODE_COORD_SECTION'][i]
            coord_x.append(x)
            coord_y.append(y)

    ILS(ciudad)

if __name__ == "__main__":
    main()
