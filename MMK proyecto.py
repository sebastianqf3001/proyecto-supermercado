import numpy as np

class Supermercado:
    def __init__(self, horario, cajas):
        self.Abierto_hasta = horario
        self.Cantidad_de_cajas = cajas
        self.cajas = []
        self.Personas_totales = 0
        self.Personas_atendidas = 0
        self.Personas_que_quedan = 0
        

class Persona:
    def __init__(self, indice, llegada, compra, atencion):
        self.indice_de_persona = indice
        self.hora_de_llegada = llegada
        self.hora_de_compra = compra
        self.hora_de_atencion = atencion

class Caja:
    def __init__(self, indice):
        self.indice_de_caja = indice
        self.Ocupada = False
        self.Cola = 0

def ExponentialInstance(lambd):
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd

def Simulacion(Capacidad,a,b,c,Tfin):
    T = 0 # Reloj

    supermercado = Supermercado(Tfin,16)    #Creo supermercado

    for i in range(supermercado.Cantidad_de_cajas): #Creo cajas
        supermercado.cajas.append(Caja())

    TP1 = ExponentialInstance(a) # llegada de cliente 1
    TP2 = np.inf # compra de cliente 1
    TP3 = np.inf # atencion de cliente 1

    ESTOT=0 #Variable auxiliar guardadora de tiempos de espera


    while (T < Tfin): #condición de stop
        if 
    return(ESTOT/supermercado.Personas_totales) #Calculamos promedio de espera
