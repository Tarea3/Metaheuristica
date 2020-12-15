import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion

graficar_ruta = False
coord_x = []
coord_y = []
problem = tsplib95.load('instancias/st70.tsp') #para cargar instancias

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
    actual = desde         #se manda la ciudad que queremos que parta, ciudad de 'origen' 
    ciudad = []
    ciudad.append(desde)
    seleccionada = [False] * n
    seleccionada[actual] = True   #se crea una lista con las ciudades ya visitadas para no pasar por ellas nuevamente

    while len(ciudad) < n:  #aca se crean las conexiones. se agrega la ciudad que tenga la menor distancia con la actual y asi susecivamente
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

    return ciudad   #finalmente se retorna la lista de ciudades

# Búsqueda local 2-opt
def DosOpt(ciudad):
    n = len(ciudad)
    flag = True
    contar = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < 0: #si el calculo es mejor se acepta, sino no se acepta
                min_i, min_j = i, j
                contar += 1
                if contar == 1:
                    flag = False

        if flag == False:
            break

    if contar > 0: #si se enconetro una solucion mejor contar se igualaba a 1, entonces se acepta el cambio y se realiza
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1] #se invierten rutas

# perturbación: se escogen dos ciudades aleatorias y las intercambia
def perturbation(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
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

    if i == n - 1:
        j = 0
    else:
        j = i + 1
    # intercambio
    temp = ciudad[i]
    ciudad[i] = ciudad[j]
    ciudad[j] = temp


def perturbation2(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i >= j:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
    ciudad[i : j] = ciudad[i : j][::-1]

def ILS(ciudad):
    random.seed(1) #se define una semilla random 
    inicioTiempo = time.time() #tiempo inicial
    n = len(ciudad)
    # Solución inicial
    s = vecinoMasCercano(n, 0)#random.randint(0, n))    #heuristica constructiva, solucion inicial
    DosOpt(s)   #es la primera busqueda local (2-opt)

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

def main(): #para leer la instancia 
    G = problem.get_graph()
    ciudad = [i-1 for i in list(problem.get_nodes())]
    info = problem.as_keyword_dict()

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
