import numpy as np

class Supermercado:
    def __init__(self, horario, cajas):
        self.Hora_de_cierre = horario
        self.Cantidad_de_cajas = cajas
        self.cajas = []
        self.personas = []  #Lista que irá guardando personas que irán llegando
        self.Personas_totales = 0
        self.Personas_atendidas = 0
        self.Personas_que_quedan = 0
        

class Persona:
    def __init__(self, indice, llegada):
        self.indice_de_persona = indice
        self.hora_de_llegada = llegada
        self.hora_de_compra = np.inf
        self.hora_de_atencion = np.inf

class Caja:
    def __init__(self, indice):
        self.indice_de_caja = indice
        self.Ocupada = False
        self.Cola = 0
        self.orden_de_clientes_en_cola=[] #Aquí va el índice de la persona

def ExponentialInstance(lambd):
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd

def Simulacion(Capacidad,a,b,c,Tfin):
    T = 0 # Reloj
    Stop=False

    supermercado = Supermercado(Tfin,16)    #Creo supermercado

    for i in range(supermercado.Cantidad_de_cajas): #Creo cajas
        supermercado.cajas.append(Caja(i))

    TP1 = ExponentialInstance(a) # llegada de cliente 1
    TP2 = np.inf # compra de cliente 1
    TP3 = np.inf # atencion de cliente 1

    ESTOT=0 #Variable auxiliar guardadora de tiempos de espera


    while (Stop==False): #condición de stop
        if TP1<TP2 and TP1<TP3: #Si es que el tiempo de llegada va antes que una compra y atención:
            T=TP1   #Tiempo se actualiza a tiempo de llegada del cliente.
            persona=Persona(supermercado.Personas_totales,T)   #Se crea la persona que llega con el índice de las personas que hay en el super y el tiempo de llegada TP1 
            persona.hora_de_compra = T + ExponentialInstance(b) #Se crea un tiempo de compra para la persona que llegó
            supermercado.personas.append(persona)    #Se agrega esa persona al supermercado
            supermercado.Personas_totales+=1    #Se cuenta esa persona
            TP1 = T + ExponentialInstance(a) #Se actualiza la llegada del siguiente cliente
        
        elif TP2 < TP1 and TP2 < TP3:
            T = TP2

            for i in cajas


        

















        if supermercado.Hora_de_cierre > T and supermercado.Personas_que_quedan==0: #Condición de stop
            Stop=True
    return(ESTOT/supermercado.Personas_totales) #Calculamos promedio de espera
