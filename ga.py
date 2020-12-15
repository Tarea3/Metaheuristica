import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion

import array
import numpy
# Biblioteca que nos provee varias heuristicas
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# Tips: A algun individuo se le puede aplicar la busqueda local o arreglar una solucion infactible

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
    return suma,

# heurística del vecino más cercano
def vecinoMasCercano(n):
    desde = random.randrange(0, n)
    if random.uniform(0, 1) < 0.3:
        actual = desde
        ciudad = []
        ciudad.append(desde)
        seleccionada = [False] * n
        seleccionada[actual] = True
        # print(seleccionada)
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
        # print(ciudad)
        # print(costoTotal(ciudad))
    else:
        ciudad = [i for i in range(0, n)]
        random.shuffle(ciudad)
    return ciudad

def DosOpt(ciudad):

    actual = 0
    n = len(ciudad)
    flag = True
    contar = 0
    k = random.randint(0, len(ciudad) - 1)
    ciudad = ciudad[k:] + ciudad[:k]
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            nuevoCosto = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
            if nuevoCosto < actual:
                actual = nuevoCosto
                min_i, min_j = i, j
                # Al primer cambio se sale
                contar += 1
                if contar == 1 :
                    flag = False

        if flag == False:
            break

    # Actualiza la subruta se encontró
    if actual < 0:
        ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]

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

def perturbation3(ciudad):
    i = 0
    j = 0
    n = len(ciudad)
    while i == j:
        i = random.randint(0, n - 2)
        # j = random.randint(0, n - 1)
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
    # Esta pertubacion lo que hace es seleccionar dos individuos e invertir

def mutSet(ciudad):
    #perturbation(ciudad)
    # value = random.uniform(0, 1)
    # if value < 0.3:
    #     perturbation(ciudad)
    # elif value >= 0.3 and value < 0.6:
    #     perturbation2(ciudad)
    # elif value >= 0.6 and value < 0.85:
    perturbation2(ciudad)
    # else:
    #     DosOpt(ciudad) # Las busquedas locales hacen la presion de la seleccion, por lo general no aparecen, pero podriamos agregarlas como mutacion.
    # Generalmente se ocupan como mutacion, sabemos que son costosas, por eso se aplica en porcentajes bajos. Tips para ver que cosas probar en la mutacion

    return ciudad,

# Forma sencilla que no tenemos que ocupar mucho, porque ocupamos una biblioteca donde ya tienen definidas las funciones
def GA(ciudad):
    n = len(ciudad)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) # Definir al individuo (solucion). Hay que poner el tipo de fitness (para minimizar)
    creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin) # Se puede ocupar una lista una matriz o un arbol o la estructura que nosotros estimemos conveniente
    toolbox = base.Toolbox()

    # Attribute generator
    #toolbox.register("indices", random.sample, range(n), n)

    # Le decimos que llame a la funcion del vecino mas cercano
    # n es la cantidad de parametros que necesita la funcion que definimos 
    toolbox.register("indices", vecinoMasCercano, n) # Cuando se dice indices le estamos diciendo como ese individuo se va a generar inicialmente, es decir, estamos entrando a la poblacion inicial

    # Structure initializers
    # Como van a funcionar los individuos. Aqui los estamos registrando y diciendo que son iterables
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    # Como estan conformadas las poblaciones. Estan conformadas por los individuos y van a ser listas, es decir le estamos diciendo que sera una lista de lista
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Función objetivo
    toolbox.register("evaluate", costoTotal)
    # Selección
    toolbox.register("select", tools.selTournament, tournsize=4)
    # Cruzamiento, la biblioteca trae varios cruzamientos implantadas. Todos estos son de permutacion porque asi es el TSP. No se puede poner uno de binario a una de permutacion.
    #toolbox.register("mate", tools.cxPartialyMatched)
    #toolbox.register("mate", tools.cxUniformPartialyMatched)
    toolbox.register("mate", tools.cxOrdered)
    # Mutación
    #toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05) # Esta toma el 5% de la lista y la cambia aleatoriamente. Pero en este caso no queremos verla asi, porque como es un problema de permutacion no queremos que sea asi tan al azar
    toolbox.register("mutate", mutSet) # Llama a la funcion mutSet

    random.seed(1)
    pop = toolbox.population(n=100) # Tamaño de la poblacion
    # Lo que podriamos hacer es ir regristrando los individuos que se van generando de generacion en generacion

    hof = tools.HallOfFame(1) # Guarda el mejor individuo por generacion. Si ponemos 10 guardara los 10 mejores

    # Definicion de estadistica para ir guardando valores.
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean) # Palabra clave y funcion que ocuparemos
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

# El unico incoveniente es que no nos permite ver el detalle de las rutas, porque no hay acceso al algoritmo que esta adentro
    iterMax = 500
    inicioTiempo = time.time()
    result, log = algorithms.eaSimple(pop, toolbox, 0.9, 0.1, iterMax, stats=stats, halloffame=hof) # El algoritmo hace la pega
    # result, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=400, verbose=False)
    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo

    minimo, promedio = log.select("min", "avg") # Aqui se rescata la info en una lista

    best_individual = tools.selBest(result, k=1)[0] # Aqui rescatamos el mejor individuo de todo el proceso
    print('Costo  : %d' % costoTotal(best_individual)[0])
    print("Tiempo : %f" % tiempo)

    # print(best_individual)

    lala = tools.selBest(result, 500)
    for i in lala:
        print(costoTotal(i))

    plt.figure(figsize=(12, 8))
    plt.xlim((0, iterMax))


    # Permite graficar
    plots = plt.plot(minimo,'c-', promedio, 'b-')
    #print( log.select('mean'))
    plt.legend(plots, ('Costo Mínimo', 'Costo Promedio'), frameon=True)
    plt.ylabel('Costo')
    plt.xlabel('Iteraciones')
    plt.show()


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

    for n in range(len(coord_x)):
        plt.annotate(str(n), xy=(coord_x[n], coord_y[n] ), xytext=(coord_x[n]+0.5, coord_y[n]+1),color='red')

def GA2(ciudad):
    n = len(ciudad)
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, typecode='i', fitness=creator.FitnessMin)
    toolbox = base.Toolbox()

    # Attribute generator
    #toolbox.register("indices", random.sample, range(n), n)
    #depot = random.randrange(0, n)
    toolbox.register("indices", vecinoMasCercano, n)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # toolbox.register("mate", tools.cxPartialyMatched)
    #toolbox.register("mate", tools.cxUniformPartialyMatched)
    toolbox.register("mate", tools.cxOrdered)
    #toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("mutate", mutSet)
    toolbox.register("select", tools.selTournament, tournsize=4)
    toolbox.register("evaluate", costoTotal)


    random.seed(1)
    pop = toolbox.population(n=100)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    log = tools.Logbook()
    log.header = "gen", "evals", "std", "min", "avg", "max"
    CXPB, MUTPB = 0.9, 0.1
    print("Start of evolution")
    inicioTiempo = time.time()
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print("Evaluated %i individuals" % len(pop))
    g = 0
    lista_soluciones = []
    lista_costos = []
    iterMax = 500
    record = stats.compile(pop)
    log.record(gen=g, evals=len(pop), **record)
    print(log[-1]["gen"], log[-1]["avg"], log[-1]["min"])
    # Pseudocodigo del algoritmo, este podremos editar entremedio
    while g < iterMax:
        g = g + 1
        # print ("-- Generation %i --" % g)
        # Selección
        offspring = toolbox.select(pop, len(pop))
        # Cruzamiento
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        # Mutación
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
                
    # Los algoritmos geneticos tienen una extension que se llaman algoritmos memeticos
    # Estos consideran la busqueda local como un operador, agregandole luego de cruzar y mutar la busqueda local
        # # Memetic
        # for i in offspring:
        #     DosOpt(i)
        #     del i.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Reemplazamiento
        pop[:] = offspring
        #fits = [ind.fitness.values[0] for ind in pop]
        #print( "fitness-- ", max(fits))
    # Aqui fue registrando los individuos para luego ir graficandolos
        hof.update(offspring)
        record = stats.compile(offspring)
        log.record(gen=g, evals=len(offspring), **record)
        print(log[-1]["gen"], log[-1]["avg"], log[-1]["min"])

        top = tools.selBest(offspring, k=1)
        # print(top[0])
        #s = top[0]
        #costo = costoTotal(top[0])
        # print(g, costo[0])
        lista_costos.append(int(log[-1]["min"])) # Aqui guarda los menores en una lista
        lista_soluciones.append(top[0]) # Aqui guarda el costo de la no solucion

    finTiempo = time.time()
    tiempo = finTiempo - inicioTiempo
    minimo, promedio = log.select("min", "avg")

    print('Costo  : %d' % min(lista_costos))
    print("Tiempo : %f" % tiempo)

    # animacion.animateTSP(lista_soluciones, coord_x, coord_y, lista_costos)
    ver = animacion(lista_soluciones, coord_x, coord_y, lista_costos)
    ver.animacionRutas()

    plt.figure(figsize=(12, 8))
    plt.xlim((0, iterMax))


    plots = plt.plot(minimo,'c-', promedio, 'b-')
    #print( log.select('mean'))
    plt.legend(plots, ('Costo Mínimo', 'Costo Promedio'), frameon=True)
    plt.ylabel('Costo')
    plt.xlabel('Iteraciones')
    plt.show()


def main():
    G = problem.get_graph()
    ciudad = list(problem.get_nodes())
    info = problem.as_keyword_dict()

    if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D': # se puede graficar la ruta
        global graficar_ruta
        graficar_ruta = True
        for i in range(1, len(ciudad) + 1):
            x, y = info['NODE_COORD_SECTION'][i]
            coord_x.append(x)
            coord_y.append(y)

    #graficar(coord_x, coord_y, [])
    GA2(ciudad)
    #GA(ciudad)

if __name__ == "__main__":
    main()
