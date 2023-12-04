
import numpy as np
import random
import time
#En esta sección definiré funciones auxiliares que me ayudarán en la simulación
def Infinitar_el_menor(lista_de_vectores):  #Esta función sirve para hacer infinito el menor número de una matriz
    min_valor = float('inf')  
    min_indice = None  
    
    for i, vector in enumerate(lista_de_vectores):
        for j, numero in enumerate(vector):
            if numero < min_valor:
                min_valor = numero
                min_indice = (i, j)  
    
    lista_de_vectores[i][j] = float('inf')

    if min_indice == None:
        min_indice=(0,0)
    return min_indice
def Vector_del_menor(lista_de_vectores):  #Esta función sirve para indicar el vector en el que se encuentra el menor numero de una matriz
    min_valor = float('inf')  
    min_indice = None  
    
    for i, vector in enumerate(lista_de_vectores):
        for j, numero in enumerate(vector):
            if numero < min_valor:
                min_valor = numero
                min_indice = (i, j)      

    if min_indice == None:
        min_indice=(0,0)
    return min_indice[0]

def indice_del_menor(lista_de_vectores):  #Esta función sirve para indicar el indice del vector en el que se encuentra el menor numero de una matriz
    min_valor = float('inf')  
    min_indice = None  
    
    for i, vector in enumerate(lista_de_vectores):
        for j, numero in enumerate(vector):
            if numero < min_valor:
                min_valor = numero
                min_indice = (i, j)  
    

    if min_indice == None:
        min_indice=(0,0)
    return min_indice[1]
#--------------------------------------------------------------------------------------------------------

def ExponentialInstance(lambd): #Definicion de instancia Exponencial
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd

a = 3 # parámetro de exponencial de llegada
b = 1/15 # parámetro exponencial de compra
c = 1/5 # parámetro exponencial de pago
Tfin = 840 # Tiempo de la simulación

initial_time = time.time()
sumaaa=0
for i in range(30):
    T = 0.0 # Reloj
    NLl = 0 # Total de clientes que han llegado a la tienda
    NClientes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Número de clientes atendido por caja
    STATUS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # si es que la caja esta ocupada, 0 en otro caso
    NCola = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # clientes en la cola en la caja
    NTot = 0 # Total de clientes atendidos en todas las cajas
    WTot = 0 # Espera total de todos los clientes que han sido atendidos
    TOcpTot = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #tiempo total de ocupación de todas las cajas2.83


    TP1 = [ExponentialInstance(a)] #Tiempo de llegada del cliente i a la tienda
    TP2 = [float('inf')]  #Tiempo de compra del cliente i
    TP3 = [[float('inf')],[float('inf')],[float('inf')],[float('inf')],
        [float('inf')],[float('inf')],[float('inf')],[float('inf')],
        [float('inf')],[float('inf')],[float('inf')],[float('inf')],
        [float('inf')],[float('inf')],[float('inf')],[float('inf')]]    #Tiempo de pago del cliente i en la caja k

    TCol = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #tiempo de llegada del cliente i a la cola de la caja k
    TOcp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Tiempo de ocupación del cliente i en la caja k

    finalizar=0 #Condición para finalizar la simulación

    while (finalizar==0):  
        if np.min(TP1) < np.min(TP2):   #Primera condición: ( TP1 < TP2 )
            if np.min(TP1) < TP3[Vector_del_menor(TP3)][indice_del_menor(TP3)]:  #Segunda condicion: ( TP1 < TP3 )
                minTP1=np.argmin(TP1)
                T = TP1[minTP1]
                TP1[minTP1] = float('inf')
                NLl = NLl+1
                
                TP1.append(float('inf'))
                if T <= Tfin:                                #Los clientes dejarán de llegar cuando cierre el super
                    TP1[minTP1+1] = T + ExponentialInstance(a)
                TP2[minTP1] = T + ExponentialInstance(b)
                TP2.append(float('inf'))

            else:   #( TP1 > TP3 )
                
                TP3H = [num for vector in TP3 for num in vector]    #Buscamos el menor número de la matriz TP3
                T = min(TP3H)
                
                minVecTP3=Vector_del_menor(TP3)
                minIndTP3=indice_del_menor(TP3)

                TP3[minVecTP3][minIndTP3]=float('inf')

                if NCola[minVecTP3]>0:          #Condición 3 NCOl[K_i]>0
                    NCola[minVecTP3]=NCola[minVecTP3] - 1
                    D = T - TCol[minVecTP3]
                    WTot = WTot + D


                    NClientes[minVecTP3] = NClientes[minVecTP3] + 1
                    TP3[minVecTP3].append(float('inf'))
                    TP3[minVecTP3][minIndTP3 + 1] = T + ExponentialInstance(c)
                    

                else:           #NCOl[K_i]>0
                    STATUS[minVecTP3]=0
                    M = T -TOcp[minVecTP3]
                    TOcpTot[minVecTP3] = TOcpTot[minVecTP3] + M
                
        else:               #TP1>TP2
            
            if np.min(TP2) < TP3[Vector_del_menor(TP3)][indice_del_menor(TP3)]:     #Condicion 4 TP2 < TP3
                
                minTP2=np.argmin(TP2)
                T = TP2[minTP2]

                if STATUS != [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:      #Condición 5 STATUS != vector(1), hay una o más cajas desocupadas
                    lista_de_cajas_desocupadas=[]
                    for i in range(0,(len(STATUS))):    #Se ven todas las cajas que están desocupadas
                        if STATUS[i] == 0:
                            lista_de_cajas_desocupadas.append(i)
                    k = random.choice(lista_de_cajas_desocupadas)   #Se elije una de todas las cajas que están desocupadas

                    STATUS[k] = 1
                    NClientes[k] = NClientes[k] + 1
                    TP3[k][len(TP3[k])-1] = T + ExponentialInstance(c)
                    TP3[k].append(float('inf'))
                    TOcp[k] = T
                    
                else:           #STATUS = vector(1), todas las cajas están ocupadas
                    lista_de_cajas_menor_fila=[]
                    Ncola_menor = np.min(NCola)
                    for i in range(0,(len(NCola))): #Se ven todas las cajas que tengan la menor fila
                        if NCola[i] == Ncola_menor:
                            lista_de_cajas_menor_fila.append(i) #Se elije una caja entre todas las que tengan menor fila

                    Cola_menor = random.choice(lista_de_cajas_menor_fila)
                    NCola[Cola_menor] = NCola[Cola_menor] + 1
                    TCol[Cola_menor] = T
                TP2[minTP2]=float('inf')

            else:       #TP2 > TP3
                TP3H = [num for vector in TP3 for num in vector]    #Buscamos el menor número de la matriz TP3
                T = min(TP3H)
                
                minVecTP3=Vector_del_menor(TP3)
                minIndTP3=indice_del_menor(TP3)
                
                if NCola[minVecTP3]>0:      #Condición 6 NCOl[K_i]>0
                    NCola[minVecTP3]=NCola[minVecTP3] - 1
                    D = T - TCol[minVecTP3]
                    WTot = WTot + D

                    NClientes[minVecTP3] = NClientes[minVecTP3] + 1
                    TP3[minVecTP3].append(float('inf'))
                    TP3[minVecTP3][indice_del_menor(TP3) + 1] = T + ExponentialInstance(c)
                
                
                else:   #NCOl[K_i]<0
                    STATUS[minVecTP3]=0
                    M = T -TOcp[minVecTP3]
                    TOcpTot[minVecTP3] = TOcpTot[minVecTP3] + M

                TP3[minVecTP3][minIndTP3]=float('inf')

        NTot = 0
        NTot=sum(NClientes)
        if T > Tfin and NLl==NTot:  #Condición para finalizar, que todos los clientes hayan sido atendidos y que haya cerrado el super
            #print("Porcentaje de ocupación por caja: ",TOcpTot[0]*100/T,TOcpTot[1]*100/T,TOcpTot[2]*100/T,TOcpTot[3]*100/T,
            #TOcpTot[4]*100/T,TOcpTot[5]*100/T,TOcpTot[6]*100/T,TOcpTot[7]*100/T,
            #TOcpTot[8]*100/T,TOcpTot[9]*100/T,TOcpTot[10]*100/T,TOcpTot[11]*100/T,
            #TOcpTot[12]*100/T,TOcpTot[13]*100/T,TOcpTot[14]*100/T,TOcpTot[15]*100/T )
            sumaaa+=WTot/NLl
            print("Terminó en: ",T)
            finalizar=1

final_time = time.time()

print(sumaaa/30)
print(final_time - initial_time)