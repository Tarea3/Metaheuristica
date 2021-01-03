#import random

def DosOptChange(ciudad,min_i,min_j,min_k):
    min_i= i
    min_j= j
    min_k= k
    
    opcion_1=distancia(ciudad[j], ciudad[j+1]) + distancia(ciudad[k], ciudad[k+1]) - (distancia(ciudad[j+1], ciudad[k+1]) + distancia(ciudad[j], ciudad[k])) #i no cambia con nadie
    
    opcion_2= distancia(ciudad[i], ciudad[i+1]) + distancia(ciudad[k], ciudad[k+1]) -(distancia(ciudad[i+1], ciudad[k+1]) + distancia(ciudad[i], ciudad[k])) #j no cambia con nadie

    opcion_3=distancia(ciudad[i], ciudad[i+1]) + distancia(ciudad[j], ciudad[j+1]) - ( distancia(ciudad[i+1], ciudad[j+1]) + distancia(ciudad[i], ciudad[j]))  #k no cambia con nadie
    
    mejor=max(opcion_1,opcion_2,opcion_3)

    if mejor == opcion_1:
        ciudad[j + 1 : k + 1] = ciudad[j + 1 : k + 1][::-1]
    elif mejor == opcion_2:
        ciudad[i + 1 : k + 1] = ciudad[i + 1 : k + 1][::-1]
    elif mejor == opcion_3:
        ciudad[i + 1 : j + 1] = ciudad[i + 1 : j + 1][::-1]
    return ciudad


def TresChange(ciudad):

    n = len(ciudad)
    var=0
    i = random.randint(0,round(n/3)-1)
    j = random.randint(round(n/3),round(2*n/3)-1)
    k = random.randint(round(2*n/3), n-1)
    
    min_i,min_j,min_k = i,j,k
    ciudad[i + 1 : j + 1] = ciudad[i + 1 : j + 1][::-1]

    ciudad[j + 1 : k + 1] =ciudad[j + 1 : k + 1][::-1]
                
    ciudad[i + 1 : k + 1] = ciudad[i + 1 : k + 1][::-1]
    
    ciudad_final = DosOptChange(ciudad,min_i,min_j,min_k)
    return ciudad_final


