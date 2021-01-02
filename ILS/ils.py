import tsplib95
import matplotlib.pyplot as plt
import random
import time
from visualizar import animacion


fuente= open('instancias.txt','r')
lista_total = fuente.readlines()

global total_ciudades
global costo_optimo_total
global costo_minimo_total
global error_minimo_total
global costo_promedio_total
global error_promedio_total
global tiempo_promedio_total


for instancia in lista_total:
    
    b = instancia.split()
    id_instancia = b[0]
    nombre_instancia = b[1]
    costo_optimo = int(b[2])
    
    
    
    graficar_ruta = False
    coord_x = []
    coord_y = []
    problem = tsplib95.load('instancias/'+ nombre_instancia + '.tsp') #para cargar instancias
    info = dict()   
    #variables a utilizar    
    tiempo_total=0
    costo_total=0
    ejecuciones = 3
    costo_minimo = 99999999
    error_total = 0

    total_ciudades=0
    costo_optimo_total = 0
    costo_minimo_total=0
    error_minimo_total=0
    costo_promedio_total=0
    error_promedio_total=0
    tiempo_promedio_total = 0
    # distancia entre la ciudad i y j
    # def distancia(i, j):
    #     if info['EDGE_WEIGHT_TYPE']== 'EUC_2D' or info['EDGE_WEIGHT_TYPE']== 'GEO' or info['EDGE_WEIGHT_TYPE']== 'ATT' or info['EDGE_WEIGHT_TYPE']== 'EXPLICIT':
    #         u = i+1, j+1
    #     else:
    #         u = i, j
    #     return problem.get_weight(*u)

    def distancia(i, j):
        u = i+tipo_var, j+tipo_var
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
            
            
    
    def nueva_distancia_propuesta(x1,x2,y1,y2,z1,z2,ciudad):
        actual = distancia(ciudad[x1], ciudad[x2]) + distancia(ciudad[y1], ciudad[y2]) + distancia(ciudad[z1], ciudad[z2]) 
        nueva = distancia(ciudad[x1], ciudad[y2]) + distancia(ciudad[x2], ciudad[z1]) + distancia(ciudad[y1], ciudad[z2])
        resultado = actual - nueva
        return resultado
    
    #OR-opt (http://tsp-basics.blogspot.com/2017/03/or-opt.html)
        #la diferencia de or-opt es que OR considera la distancia entre dos de los tres tipos de cambio casi adyacentes, lo que reduce hacer un tercer for mas
    def OrOpt(ciudad):
        n = len(ciudad)
        min_change= 0
        for adyacencia in range(3,1,-1): #dejar en maximo de 4 o 3?????????????????????
            for i in range(n - adyacencia - 1): 
                x1= i
                x2= i+1
                
                j = i + adyacencia
                y1 = j
                y2= j+1
                
                for k in range(j+1,n-1):
                    z1= k
                    z2= k+1
                    evaluar = nueva_distancia_propuesta(x1,x2,y1,y2,z1,z2,ciudad)
                    if evaluar > min_change:
                        min_change = evaluar
                        ciudad[x1 + 1 : y1 + 1] = ciudad[x1 + 1 : y1 + 1][::-1]
                
                        ciudad[y1 + 1 : z1 + 1] =ciudad[y1 + 1 : z1 + 1][::-1]
                
                        ciudad[x1+ 1 : z1 + 1] = ciudad[x1+ 1 : z1 + 1][::-1]
                        
                        break
                        
                                                                             
    # Búsqueda local 3-opt (http://matejgazda.com/tsp-algorithms-2-opt-3-opt-in-python/)
    #VERSION 2: entra el que tenga el mayor beneficio para el cambio
    def TresOpt(ciudad):
        n = len(ciudad)
        flag = True
        contar = 0
        min_change=0
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range ( j + 1, n - 1):
                    
                    lista_1= []
                    nuevoCosto_1 = 0 #sin cambio de nada ciudades
                    lista_1.append(nuevoCosto_1)
                    nuevoCosto_2 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[i], ciudad[k]) + distancia(ciudad[i + 1], ciudad[k + 1]))
                    lista_1.append(nuevoCosto_2)
                    nuevoCosto_3 = distancia(ciudad[j], ciudad[j + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[j], ciudad[k]) + distancia(ciudad[j + 1], ciudad[k + 1]))
                    lista_1.append(nuevoCosto_3)
                    nuevoCosto_4 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[j], ciudad[j + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[i], ciudad[j + 1]) + distancia(ciudad[i + 1], ciudad[k + 1]) + distancia(ciudad[j], ciudad[k]))
                    lista_1.append(nuevoCosto_4)
                    nuevoCosto_5 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[j], ciudad[j + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[j], ciudad[k + 1]) + distancia(ciudad[i + 1], ciudad[j + 1]) + distancia(ciudad[i], ciudad[k]))
                    lista_1.append(nuevoCosto_5)
                    nuevoCosto_6 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[j], ciudad[j + 1]) - (distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]))
                    lista_1.append(nuevoCosto_6)
                    nuevoCosto_7 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[j], ciudad[j + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[i + 1], ciudad[k]) + distancia(ciudad[j + 1], ciudad[k + 1]) + distancia(ciudad[i], ciudad[j]))
                    lista_1.append(nuevoCosto_7)
                    nuevoCosto_8 = distancia(ciudad[i], ciudad[i + 1]) + distancia(ciudad[j], ciudad[j + 1]) + distancia(ciudad[k], ciudad[k + 1]) - (distancia(ciudad[i], ciudad[j + 1]) + distancia(ciudad[j], ciudad[k + 1]) + distancia(ciudad[i + 1], ciudad[k]))
                    lista_1.append(nuevoCosto_8)
                    # min_i, min_j, min_k = i, j, k
                    nuevoCosto=max(lista_1)
                    
                    if nuevoCosto > min_change: #si el calculo es mejor se acepta, sino no se acepta
                        min_change = nuevoCosto
                        min_i, min_j, min_k = i, j, k 
                        contar += 1
                        if contar == 1:
                            flag = False
        
                if flag == False:
                    break
    
        if contar > 0: #si se enconetro una solucion mejor contar se igualaba a 1, entonces se acepta el cambio y se realiza
            primer_seg = ciudad[min_i + 1 : min_k + 1] 
            segundo_seg = ciudad[min_j + 1 : min_k + 1]
            tercer_seg = ciudad[min_i + 1 : min_j + 1]
            #Case 2
            if nuevoCosto_2 == nuevoCosto:
                ciudad[min_i + 1 : min_k + 1] = reversed(primer_seg) 
        
            #Case 3
            elif nuevoCosto_3 == nuevoCosto:
                ciudad[min_j + 1 : min_k + 1] =reversed(segundo_seg)
            #Case 4
            elif nuevoCosto_4 == nuevoCosto :
                ciudad[min_i + 1 : min_k + 1] = reversed(primer_seg)
                        
                ciudad[min_j + 1 : min_k + 1] =reversed(segundo_seg)
            #Case 5
            elif nuevoCosto_5 == nuevoCosto :
                ciudad[min_i + 1 : min_k + 1] = reversed(primer_seg)
            
                ciudad[min_i + 1 : min_j + 1] = reversed(tercer_seg)   
            #Case 6
            elif nuevoCosto_6 == nuevoCosto:
                ciudad[min_i + 1 : min_j + 1] = reversed(tercer_seg)   
            #Case 7
            elif nuevoCosto_7 == nuevoCosto:
                ciudad[min_i + 1 : min_j + 1] = reversed(tercer_seg)   
                        
                ciudad[min_j + 1 : min_k + 1] =reversed(segundo_seg)
            #Case 8
            elif nuevoCosto_8 == nuevoCosto:
                ciudad[min_i + 1 : min_j + 1] = reversed(tercer_seg)
                
                ciudad[min_j + 1 : min_k + 1] =reversed(segundo_seg)
                
                ciudad[min_i + 1 : min_k + 1] = reversed(primer_seg)
            
    
    
    
    
    # VERSION 1: entra al cambio el primero que cumpla con la condicion
    # def TresOpt(ciudad):
    #     n = len(ciudad)
    #     flag = True
    #     contar = 0
    #     min_change=0
    #     for i in range(n - 2):
    #         for j in range(i + 1, n - 1):
    #             for k in range ( j + 1, n - 1):
                    
    #                 nuevoCosto_1 = 0 #sin cambio de nada ciudades
    #                 nuevoCosto_2 = distancia(ciudad[i], ciudad[k]) + distancia(ciudad[i + 1], ciudad[k + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[k], ciudad[k + 1])
    #                 nuevoCosto_3 = distancia(ciudad[j], ciudad[k]) + distancia(ciudad[j + 1], ciudad[k + 1]) - distancia(ciudad[j], ciudad[j + 1]) - distancia(ciudad[k], ciudad[k + 1])
    #                 nuevoCosto_4 = distancia(ciudad[i], ciudad[j + 1]) + distancia(ciudad[i + 1], ciudad[k + 1]) + distancia(ciudad[j], ciudad[k]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1]) - distancia(ciudad[k], ciudad[k + 1])
    #                 nuevoCosto_5 = distancia(ciudad[j], ciudad[k + 1]) + distancia(ciudad[i + 1], ciudad[j + 1]) + distancia(ciudad[i], ciudad[k]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1]) - distancia(ciudad[k], ciudad[k + 1])
    #                 nuevoCosto_6 = distancia(ciudad[i], ciudad[j]) + distancia(ciudad[i + 1], ciudad[j + 1]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1])
    #                 nuevoCosto_7 = distancia(ciudad[i + 1], ciudad[k]) + distancia(ciudad[j + 1], ciudad[k + 1]) + distancia(ciudad[i], ciudad[j]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1]) - distancia(ciudad[k], ciudad[k + 1])
    #                 nuevoCosto_8 = distancia(ciudad[i], ciudad[j + 1]) + distancia(ciudad[j], ciudad[k + 1]) + distancia(ciudad[i + 1], ciudad[k]) - distancia(ciudad[i], ciudad[i + 1]) - distancia(ciudad[j], ciudad[j + 1]) - distancia(ciudad[k], ciudad[k + 1])
                    
    #                 min_i, min_j, min_k = i, j, k
    
            
    #                 #Case 2
    #                 if nuevoCosto_2 < 0:
    #                       ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
    #                       flag = False
            
    #                 #Case 3
    #                 elif nuevoCosto_3 < 0:
    #                     ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
    #                     flag = False
    #                 #Case 4
    #                 if nuevoCosto_4 < 0:
    #                     ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                        
    #                     ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
    #                     flag = False
    #                 #Case 5
    #                 elif nuevoCosto_5 < 0:
    #                     ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
            
    #                     ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]     
    #                     flag = False
    #                 #Case 6
    #                 elif nuevoCosto_6 < 0:
    #                     ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1] 
    #                     flag = False
    #                 #Case 7
    #                 elif nuevoCosto_7 < 0:
    #                     ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
                        
    #                     ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
    #                     flag = False
    #                 #Case 8
    #                 if nuevoCosto_8 < 0:
    #                     ciudad[min_i + 1 : min_k + 1] = ciudad[min_i + 1 : min_k + 1][::-1]
            
    #                     ciudad[min_j + 1 : min_k + 1] = ciudad[min_j + 1 : min_k + 1][::-1]
            
    #                     ciudad[min_i + 1 : min_j + 1] = ciudad[min_i + 1 : min_j + 1][::-1]
    #                     flag = False
                   
    #         if flag == False:
    #             break            
            
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
        
    def s_mixto(ciudad):
        x= random.randint(0,1)
        if x < 0.8:
            DosOpt(ciudad)
        else:
            TresOpt(ciudad)
            
    def per_mixto(ciudad):
        x= random.randint(0,1)
        if x < 0.5:
            perturbation2(ciudad)
        elif 0.5 < x < 0.8:
            perturbation3(ciudad)
        else:
            perturbation(ciudad)
    
    def mejor_vecino(n):
        mejor = 9999999999
        for l in range(n): #aplicamos esto dado que dependiendo de que ciudad comience el resultado tambien cambia
            s_1 = vecinoMasCercano(n,l)
            costo = costoTotal(s_1)
            if costo < mejor:
                mejor=costo
                partida = s_1
        return partida
        
    
    def ILS(ciudad,semilla):
        random.seed(semilla) #se define una semilla random 
        inicioTiempo = time.time() #tiempo inicial
        n = len(ciudad)
        
        # Solución inicial
        s = mejor_vecino(n) #punto de partida desde mejor resultado de NN


        #s = vecinoMasCercano(n,0)
        # for l in range(n): #aplicamos esto dado que dependiendo de que ciudad comience el resultado tambien cambia
        #     s_1 = vecinoMasCercano(n,l)
        #     if s_1 < s:
        #         s = s_1
    
        DosOpt(s)
        OrOpt(s)
        #TresOpt(s)   #es la primera busqueda local (3-opt)
        #DosOpt(s)
    
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
            #per_mixto(s)
            perturbation2(s)
            #perturbation3(s)
            #perturbation2(s)
            # Búsqueda local
            #s_mixto(s)
            # DosOpt(s)
            # DosOpt(s)
            #DosOpt(s)
            # TresOpt(s)
            #s_mixto(s)
            DosOpt(s)
            OrOpt(s)
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
            if costo_optimo == costoMejor: #si encuentra el optimo lo saca del ciclo
                break
    
        finTiempo = time.time()
        tiempo = finTiempo - inicioTiempo
        
        global tiempo_total
        tiempo_total= tiempo_total + tiempo #para obtener el tiempo total de ejecucion
        global costo_total
        costo_total = costo_total + costoMejor # para obtener el costo total 
        global costo_minimo
        if costo_minimo > costoMejor:
            costo_minimo = costoMejor
        global error_total
        error_instancia = ((costoMejor - costo_optimo)/costo_optimo)*100
        error_total = error_total + error_instancia
        global cantidad_ciudades
        cantidad_ciudades = n 
 
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
        #ciudad = [i-1 for i in list(problem.get_nodes())]
        numero = len(list(problem.get_nodes()))
        ciudad = [i for i in range(numero)]
        global info
        info = problem.as_keyword_dict()
        if info['EDGE_WEIGHT_TYPE'] == 'EUC_2D': # se puede graficar la ruta
            global graficar_ruta
            graficar_ruta = True
            for i in range(1, len(ciudad) + 1):
                x, y = info['NODE_COORD_SECTION'][i]
                coord_x.append(x)
                coord_y.append(y)
        global tipo_var
        if info['EDGE_WEIGHT_TYPE']== 'EUC_2D' or info['EDGE_WEIGHT_TYPE']== 'GEO' or info['EDGE_WEIGHT_TYPE']== 'ATT' or info['EDGE_WEIGHT_TYPE']== 'EXPLICIT':
            tipo_var = 1
        else:
            tipo_var = 0   
    
        for semilla in range(ejecuciones):
            print('------------- Semilla ', semilla,'------------')
            ILS(ciudad,semilla)
    
    if __name__ == "__main__":
        main()
        
#PARTES O DATOS SOLICITADOS
#1 : ID INSTANCIA
    print('ID: ', id_instancia)
        
#2 : NOMBRE INSTANCIA 
    print('Nombre: ',nombre_instancia)
        
#3 : NUMERO DE VERTICES INSTANCIA
    print('N° Vertices: ',cantidad_ciudades)
    total_ciudades= total_ciudades + cantidad_ciudades
        
#4 :  NUMERO DE ARISTAS INSTANCIA
        
#5 : COSTOS OPTIMOS INSTANCIA
    print('Costo optimo: ',costo_optimo)
    costo_optimo_total = costo_optimo_total + costo_optimo
        
#6 : COSTO MINIMO DE LAS 10 INSTANCIAS
    print('Costo mínimo de ejecuciones: ',costo_minimo) 
    costo_minimo_total = costo_minimo_total + costo_minimo
        
#7 : ERROR RELATIVO MINIMO
    error_minimo = ((costo_minimo - costo_optimo)/costo_optimo) * 100
    print('ERM: ',error_minimo) 
    error_minimo_total = error_minimo_total + error_minimo
        
#8 : COSTO PROMEDIO 10 EJECUCIONES
    costo_promedio = (costo_total) / ejecuciones
    print('Costo promedio ejecuciones:', costo_promedio)
    costo_promedio_total = costo_promedio_total + costo_promedio
        
#9 : ERROR RELATIVO PROMEDIO 10 EJECUCIONES
    error_promedio = error_total / ejecuciones
    print('ERP: ',error_promedio)
    error_promedio_total = error_promedio_total + error_promedio
#10 : TIEMPO PROMEDIO EJECUCIONES
    tiempo_promedio = (tiempo_total)/ejecuciones
    print('Tiempo promedio de ejecución:', tiempo_promedio)
    tiempo_promedio_total = tiempo_promedio_total + tiempo_promedio
 
    
#GENERAL
print("\n")
print("\n")
print("------------- GENERAL-------------")
        
#3 : NUMERO DE VERTICES INSTANCIA
total_ciudades_promedio= total_ciudades/40
print('Promedio n° Vertices: ',total_ciudades_promedio)

        
#4 :  NUMERO DE ARISTAS INSTANCIA
        
#5 : COSTOS OPTIMOS INSTANCIA
costo_optimo_total_promedio = costo_optimo_total/40
print('Costo optimo promedio: ',costo_optimo_total_promedio)
        
#6 : COSTO MINIMO DE LAS 10 INSTANCIAS
costo_minimo_total_promedio = costo_minimo_total/40
print('Costo mínimo promedio de ejecuciones: ',costo_minimo_total_promedio) 
        
#7 : ERROR RELATIVO MINIMO
error_minimo_total_promedio = error_minimo_total/40
print('ERM promedio: ',error_minimo_total_promedio)
        
#8 : COSTO PROMEDIO 10 EJECUCIONES
costo_promedio_total_promedio = costo_promedio_total/40
print('Costo promedio ejecuciones:', costo_promedio_total_promedio)
        
#9 : ERROR RELATIVO PROMEDIO 10 EJECUCIONES
error_promedio_total_promedio = error_promedio_total / 40
print('ERP promedio: ',error_promedio_total_promedio)
        
#10 : TIEMPO PROMEDIO EJECUCIONES
tiempo_promedio_total_promedio = tiempo_promedio_total/40
print('Tiempo promedio de ejecución:', tiempo_promedio_total_promedio)