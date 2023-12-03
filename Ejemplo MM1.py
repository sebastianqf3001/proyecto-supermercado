import numpy as np

def t(alpha):
    if alpha == 90:
        return 1.699
    elif alpha == 95:
        return 2.045

def Error(varianza,muestras,alpha):
    a = (t(alpha) * varianza)/np.sqrt(muestras)
    return a

def ExponentialInstance(lambd):
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd
def Simulacion(Capacidad,a,b,Nfin):
    T = 0 # Reloj

    NCOL=0  #Largo fila
    STATUS=0    #Si esta ocupada la caja
    NCLIENTES=0 #Numero de clientes que han sido atendidos

    TP1 = ExponentialInstance(a) # llegada de cliente
    TP2 = np.inf # atencion de cliente

    TLLEG=[] #Lista almacenadora tiempos de llegada de clientes
    ESTOT=0 #Variable auxiliar guardadora de tiempos de espera


    while (NCLIENTES < Nfin): #condición de stop
        
        if TP1 < TP2:   #llegada < atención
            T = TP1
            TP1 = T + ExponentialInstance(a)    #Actualizamos tiempo llegada
            if STATUS == 0:  #Revisamos status de caja
                NCLIENTES=NCLIENTES+1
                STATUS=1
                TP2 = T + ExponentialInstance(b) #Actualizamos tiempo atencion

            else:
                if NCOL<Capacidad:
                    NCOL=NCOL+1
                    TLLEG.append(T)

        else:   #TP1>TP2
            T = TP2
            if NCOL>0:  #Revisamos si hay fila
                NCOL=NCOL-1 #Quitamos cliente de fila
                D=T-TLLEG[0]
                ESTOT=ESTOT+D   #Calculamos tiempo de espera del cliente
                NCLIENTES=NCLIENTES+1
                TP2 = T + ExponentialInstance(b) #Actualizamos tiempo atencion
                Expulso=TLLEG.pop(0) #Quitamos tiempo de llegada del cliente que salió

                

            else:   #En caso de que no haya fila
                STATUS=0 #caja desocupada
                TP2 = np.inf
    return(ESTOT/NCLIENTES) #Calculamos promedio de espera
print(Simulacion(35,6,9,1000))