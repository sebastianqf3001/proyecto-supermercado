import numpy as np
import random as rd
import time

class Supermercado:
    def __init__(self, horario, numb_cajas, numb_cajas_rapidas):
        self.Hora_de_cierre = horario
        self.Cantidad_de_cajas = numb_cajas
        self.cajas = self.create_cajas_normales(numb_cajas)
        self.cajas_rapidas = self.create_cajas_normales(numb_cajas_rapidas)
        self.fila_cajas_rapidas = [] #Aquí van en orden los indices de las personas
        self.Cola_rapida =0

        self.personas = []  #Lista que irá guardando personas que irán llegando
        self.Personas_totales = 0
        self.Personas_atendidas = 0
        self.Personas_que_quedan = 0
    
    def create_cajas_normales(self, numb_cajas):
        cajas = []
        for i in range(numb_cajas): #Creo cajas normales
            caja=Caja(i,False)
            cajas.append(caja)
        return cajas
    def create_cajas_rapidas(self, numb_cajas_rapidas):
        cajas = []
        for i in range(numb_cajas_rapidas): #Creo cajas rapidas
            caja=Caja(i,True)
            cajas.append(caja)
        return cajas
    



class Intervalo:
    
    def __init__(self,tiempo_inicio,tiempo_final):
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_final = tiempo_final
        self.tiempos_de_espera = []
        self.tiempos_de_ocupacion = []

        self.ya_se_reviso=False
        self.cajas_abiertas = 0

class Apertura_de_cajas_clase:
        
        def __init__(self,tiempo_apertura,cantidad):
            self.tiempo_apertura = tiempo_apertura
            self.cantidad = cantidad
            self.ya_se_utilizo = False

class Cierre_de_cajas_clase:
        
        def __init__(self,tiempo_cierre,cantidad):
            self.tiempo_cierre = tiempo_cierre
            self.cantidad = cantidad
            self.ya_se_utilizo = False

class Persona:
    
    def __init__(self, llegada, indice):
        self.hora_de_llegada = llegada
        self.hora_de_compra = np.inf
        self.hora_de_atencion = np.inf
        self.hora_que_entra_en_cola = np.inf
        self.tiempo_total_en_cola = 0
        
        self.ya_compro=False
        self.ya_fue_atendido=False
        self.escoge_caja_rapida = False
        self.indice_de_persona = indice  #Asignamos indice a persona
        self.se_atiende_en_caja_cerrada=False
        

class Caja:
    def __init__(self, indice, tipo):
        self.indice_de_caja = indice
        self.Ocupada = False
        self.Cerrada = False
        self.persona_siendo_atendida = -1   #Aquí va el índice de la persona
        self.Cola = 0
        self.orden_de_clientes_en_cola=[] #Aquí va el índice de la persona
        self.tiempo_de_uso = 0
        self.caja_rapida = tipo
        
def ExponentialInstance(lambd):
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd


def taylor_serie(x):  #Taylor Día completo
    y = 4.833468511100568e-61 * (x - 368.0)**25 + 1.104321097541718e-59 * (x - 368.0)**24 + -6.764502240882454e-55 * (x - 368.0)**23 + -1.164401773589306e-53 * (x - 368.0)**22 + 4.1460818454159185e-49 * (x - 368.0)**21 + 4.667870353711148e-48 * (x - 368.0)**20 + -1.4659596525009974e-43 * (x - 368.0)**19 + -7.746370031433263e-43 * (x - 368.0)**18 + 3.3167058552077726e-38 * (x - 368.0)**17 + -5.671961723527083e-39 * (x - 368.0)**16 + -5.037697259426038e-33 * (x - 368.0)**15 + 2.1449400770960893e-32 * (x - 368.0)**14 + 5.246041343119162e-28 * (x - 368.0)**13 + -3.0614021619992635e-27 * (x - 368.0)**12 + -3.758438093424414e-23 * (x - 368.0)**11 + 1.4169551592324059e-22 * (x - 368.0)**10 + 1.8287770822228958e-18 * (x - 368.0)**9 + 4.140212800064939e-18 * (x - 368.0)**8 + -5.834669245448097e-14 * (x - 368.0)**7 + -6.155984615892722e-13 * (x - 368.0)**6 + 1.1341045785547847e-09 * (x - 368.0)**5 + 1.884961111267024e-08 * (x - 368.0)**4 + -1.1601179506002755e-05 * (x - 368.0)**3 + -0.00019698650221112288 * (x - 368.0)**2 + 0.04565345572605308 * (x - 368.0)**1 + 6.0506699555558985 * (x - 368.0)**0
    return y

#6.992949261062695 #Tasa max Día completo

# def taylor_serie(x):    #Taylor de 12:50 a 15:00
#    y = -3.34267085727602e-45 * (x - 80.0)**20 + -4.727990917833113e-43 * (x - 80.0)**19 + -4.2704433777491045e-41 * (x - 80.0)**18 + 4.1753429940496695e-39 * (x - 80.0)**17 + 3.7561341628322776e-36 * (x - 80.0)**16 + 1.3288722397325895e-33 * (x - 80.0)**15 + 3.6840529067170416e-31 * (x - 80.0)**14 + 7.889973681646902e-29 * (x - 80.0)**13 + 1.4689389679892442e-26 * (x - 80.0)**12 + 3.9789138231363445e-25 * (x - 80.0)**11 + -2.027573561703069e-22 * (x - 80.0)**10 + -3.9564563442411497e-19 * (x - 80.0)**9 + -1.8482742459819104e-17 * (x - 80.0)**8 + -3.619950589177593e-14 * (x - 80.0)**7 + 1.2220916373902645e-11 * (x - 80.0)**6 + -2.339826711713704e-10 * (x - 80.0)**5 + -1.558435416662692e-07 * (x - 80.0)**4 + 9.367602290200922e-06 * (x - 80.0)**3 + 0.0004350372911088983 * (x - 80.0)**2 + -0.03606546014209252 * (x - 80.0)**1 + 4.872580760736155 * (x - 80.0)**0
#    return y

# 6.099 #Tasa 12:50 a 15:00

def generar_llegada(T):
    aceptar=False
    tasa_maxima= 6.992949261062695  #Poner tasa de día completo o de 12:50 a 15:00
    while aceptar == False:
        tiempo_llegada_persona= ExponentialInstance(tasa_maxima) + T
        prob_rechazar = 1 - (taylor_serie(tiempo_llegada_persona)/tasa_maxima)
        num_cero_uno= rd.random()

        if num_cero_uno >= prob_rechazar:
            aceptar = True

        return tiempo_llegada_persona - T

def simular_tiempo_compra():

    prob_tiempo_compra= rd.random()

    if prob_tiempo_compra <= 0.15:
        tiempo_compra = rd.normalvariate(51.23 , 4.8)

    elif prob_tiempo_compra >0.15:
        tiempo_compra = rd.normalvariate(14.68, 7.86)
    
    if tiempo_compra < 0:
        tiempo_compra=np.abs(tiempo_compra)

    return tiempo_compra

def escoge_caja_rapida_o_normal():
    prob_eleccion = rd.random()
    if prob_eleccion <= 0.4:
        eleccion = "caja_rapida"
    elif prob_eleccion > 0.4:
        eleccion = "caja_normal"
    return eleccion

def create_intervalos_temporales(numb_intervalos,lista_intervalos_inicio,lista_intervalos_final):
    intervalos=[]
    for i in range(numb_intervalos):
        inicio=lista_intervalos_inicio[i]
        final=lista_intervalos_final[i]
        intervalo=Intervalo(inicio,final)
        intervalos.append(intervalo)

    return intervalos

def create_veces_que_se_abren_cajas(numb_abren_cajas):
    apertura_de_cajas=[]
    for i in range(numb_abren_cajas):
        Hora_apertura=hora_apertura_de_cajas[i]
        cuantas=cuantas_cajas_abre[i]
        apertura=Apertura_de_cajas_clase(Hora_apertura,cuantas)
        apertura_de_cajas.append(apertura)

    return apertura_de_cajas

def create_veces_que_se_cierran_cajas(numb_cierran_cajas):
    cierre_de_cajas=[]
    for i in range(numb_cierran_cajas):
        Hora_cierre=hora_que_cierra_cajas[i]
        cuantas=cuantas_cajas_cierra[i]
        cierre=Cierre_de_cajas_clase(Hora_cierre,cuantas)
        cierre_de_cajas.append(cierre)
    
    return cierre_de_cajas

def Simulacion(Tfin,cantidad_de_cajas_normales, cantidad_de_cajas_rapidas,cantidad_intervalos_temporales, veces_que_se_abre_cajas, veces_que_se_cierra_cajas):
    T = 0 # Reloj
    Stop=False

    for i in range(len(intervalos)):
        intervalos[i].tiempos_de_espera=[] #Reseteo a vacío las listas que guardan los tiempos de espera por intervalos
        intervalos[i].tiempos_de_ocupacion=[]
        intervalos[i].ya_se_reviso=False 
        
    for i in range(len(apertura_de_cajas)):
        apertura_de_cajas[i].ya_se_utilizo=False    #Reseteo a que aun no se abre ninguna caja extra
    
    for i in range(len(cierre_de_cajas)):
        cierre_de_cajas[i].ya_se_utilizo=False    #Reseteo a que aun no se abre ninguna caja extra

    supermercado = Supermercado(Tfin,cantidad_de_cajas_normales,cantidad_de_cajas_rapidas)    #Creo supermercado
    indice_persona=0
    
    TP1 = generar_llegada(T) # llegada de cliente 1
    TP2 = np.inf # compra de cliente 1
    TP3 = np.inf # atencion de cliente 1

    ESTOT=0 #Variable auxiliar guardadora de tiempos de espera
    Porcentaje_sumado_cajas_normales=0 #Variable auxiliar guardadora de porcentajes de ocupación cajas normales
    Porcentaje_sumado_cajas_rapidas=0   #Variable auxiliar guardadora de porcentajes de ocupación cajas rápidas
    Promedios_por_intervalos=[] #Lista que guarda promedios de espera de cada intervalo
    Promedios_por_intervalo_cajas_normales=[] #Lista que guarda promedios de ocupacion cajas normales de cada intervalo


    while (Stop==False): #condición de stop

                
        for i in range(veces_que_se_abre_cajas):    #Revisamos si es hora de abrir cajas
            if T>=apertura_de_cajas[i].tiempo_apertura and apertura_de_cajas[i].ya_se_utilizo==False:
                
                Hay_alguna_caja_cerrada=False   #Reviso si hay alguna caja existente cerrada
                for a in range(len(supermercado.cajas)):
                    if supermercado.cajas[a].Cerrada==True:
                        Hay_alguna_caja_cerrada=True

                if Hay_alguna_caja_cerrada==False:  #Si es que no hay, creo cajas
                    for a in range(apertura_de_cajas[i].cantidad):
                        supermercado.cajas.append(Caja(len(supermercado.cajas),False))
                    apertura_de_cajas[i].ya_se_utilizo=True

                elif Hay_alguna_caja_cerrada==True: #Si es que hay, abro cajas existentes
                    
                    for a in range(apertura_de_cajas[i].cantidad):
                        if Hay_alguna_caja_cerrada==True:
                            caja_menor_indice = 0
                            while supermercado.cajas[caja_menor_indice].Cerrada == False:
                                caja_menor_indice+=1
                            supermercado.cajas[caja_menor_indice].Cerrada = False

                        elif Hay_alguna_caja_cerrada==False:
                            supermercado.cajas.append(Caja(len(supermercado.cajas),False))

                        Hay_alguna_caja_cerrada=False 
                        for b in range(len(supermercado.cajas)):
                            if supermercado.cajas[b].Cerrada==True:
                                Hay_alguna_caja_cerrada=True
                        


                    apertura_de_cajas[i].ya_se_utilizo=True
        
        for i in range(veces_que_se_cierra_cajas):    #Revisamos si es hora de cerrar cajas
            if T>=cierre_de_cajas[i].tiempo_cierre and cierre_de_cajas[i].ya_se_utilizo==False:
                for a in range(cierre_de_cajas[i].cantidad):
                    caja_mayor_indice = supermercado.cajas[-(a+1)].indice_de_caja
                    while supermercado.cajas[caja_mayor_indice].Cerrada == True:
                        caja_mayor_indice -=1

                    supermercado.cajas[caja_mayor_indice].Cerrada = True
                
                cierre_de_cajas[i].ya_se_utilizo=True

        for i in range(len(intervalos)):   #Revisamos cuantas cajas hay por intervalos
            if T>=intervalos[i].tiempo_inicio and intervalos[i].ya_se_reviso==False:
                cantidad_de_cajas_normales_en_intervalo=0
                for a in range(len(supermercado.cajas)):
                    if supermercado.cajas[a].Cerrada==False:
                        cantidad_de_cajas_normales_en_intervalo+=1
                intervalos[i].cajas_abiertas=cantidad_de_cajas_normales_en_intervalo
                intervalos[i].ya_se_reviso=True
                
        Horas_de_compras_totales=[]
        Horas_de_atencion_totales=[]
        

        if TP1 < TP2 and TP1 < TP3 and supermercado.Hora_de_cierre > T: #Si es que el tiempo de llegada va antes que uno compra y atención:
            T=TP1   #Tiempo se actualiza a tiempo de llegada del cliente.
            persona=Persona(T, indice_persona)   #Se crea la persona que llega con el índice correspondiente
            indice_persona+=1
            persona.hora_de_compra = T + simular_tiempo_compra() #Se crea un tiempo de compra para la persona que llegó
            supermercado.personas.append(persona)    #Se agrega esa persona al supermercado
            supermercado.Personas_totales += 1    #Se cuenta esa persona
            TP1 = T + generar_llegada(T) #Se actualiza la llegada del siguiente cliente



        elif TP2 < TP1 and TP2 < TP3:   #Si es que el tiempo de compra va antes que uno de llegada y atención:
            T = TP2 #Actualizo el tiempo a tiempo de compra
            supermercado.personas[persona_que_termina_de_comprar_ahora].ya_compro = True #Digo que ya compró la persona
            caja_que_escoge_persona = escoge_caja_rapida_o_normal() #Veo si escoge caja normal o rápida
            

            if caja_que_escoge_persona == "caja_normal":    #Si es que escoge una caja rápida

                supermercado.personas[persona_que_termina_de_comprar_ahora].escoge_caja_rapida = False

                Hay_alguna_caja_desocupada = False  #Verifico si es que hay alguna caja desocupada
                cajas_desocupadas = []    
                for i in range(len(supermercado.cajas)):    
                    if supermercado.cajas[i].Ocupada == False and supermercado.cajas[i].Cerrada == False:
                        Hay_alguna_caja_desocupada = True
                        cajas_desocupadas.append(supermercado.cajas[i].indice_de_caja)

                
                if Hay_alguna_caja_desocupada==True:    #Si es que había una caja desocupada

                    Tiempo_que_durara_esta_atencion= rd.lognormvariate(0.97,0.57)  #Creo un tiempo que durará esta atención caja normal

                    caja_escogida = cajas_desocupadas[rd.randint(0, len(cajas_desocupadas)-1)]    #Escojo una caja random entre las que estaban desocupadas
                    supermercado.cajas[caja_escogida].Ocupada = True    #La caja escogida se está ocupando ahora
                    supermercado.cajas[caja_escogida].persona_siendo_atendida = persona_que_termina_de_comprar_ahora #Le especifico que persona entró a la caja
                    supermercado.cajas[caja_escogida].tiempo_de_uso += Tiempo_que_durara_esta_atencion  #Le agrego al tiempo de uso de la caja el tiempo que durará la atención

                    supermercado.personas[persona_que_termina_de_comprar_ahora].hora_de_atencion = T + Tiempo_que_durara_esta_atencion    #Le creo un tiempo de termino de la atención a esta persona
                    supermercado.Personas_atendidas += 1 #Agrego una persona más a los atendidos
                    
                else:   #Si es que no hay cajas desocupadas
                    
                    fila_menor = np.inf
                    for i in range(len(supermercado.cajas)):    #Busco entre todas las cajas la menor fila
                        if supermercado.cajas[i].Cola < fila_menor and supermercado.cajas[i].Cerrada == False:
                            fila_menor=supermercado.cajas[i].Cola

                    cajas_de_menor_fila=[]
                    for i in range(len(supermercado.cajas)): #Busco entre todas las cajas las que tengan esta menor fila
                        if supermercado.cajas[i].Cola == fila_menor and supermercado.cajas[i].Cerrada == False:
                            cajas_de_menor_fila.append(supermercado.cajas[i].indice_de_caja)

                    caja_escogida = cajas_de_menor_fila[rd.randint(0, len(cajas_de_menor_fila)-1)]  #Escojo una caja entre todas las que tengan menor fila
                    supermercado.cajas[caja_escogida].Cola += 1 #Agregamos al contador de la fila de esta caja una persona más
                    
                    supermercado.cajas[caja_escogida].orden_de_clientes_en_cola.append(persona_que_termina_de_comprar_ahora) #Agrego la persona a la fila de la caja

                    supermercado.personas[persona_que_termina_de_comprar_ahora].hora_que_entra_en_cola = T  #Indico el tiempo que empezó a hacer la fila la persona

            elif caja_que_escoge_persona == "caja_rapida":  #Si es que escoje caja rápida

                supermercado.personas[persona_que_termina_de_comprar_ahora].escoge_caja_rapida = True

                Hay_alguna_caja_desocupada = False  #Verifico si es que hay alguna caja rápida desocupada
                cajas_desocupadas = []    
                for i in range(len(supermercado.cajas_rapidas)):    
                    if supermercado.cajas_rapidas[i].Ocupada == False:
                        Hay_alguna_caja_desocupada = True
                        cajas_desocupadas.append(supermercado.cajas_rapidas[i].indice_de_caja)

                if Hay_alguna_caja_desocupada==True:    #Si es que había una caja rápida desocupada

                    Tiempo_que_durara_esta_atencion= rd.expovariate(0.57)  #Creo un tiempo que durará esta caja rápida

                    caja_escogida = cajas_desocupadas[rd.randint(0, len(cajas_desocupadas)-1)]    #Escojo una caja random entre las que estaban desocupadas
                    supermercado.cajas_rapidas[caja_escogida].Ocupada = True    #La caja escogida se está ocupando ahora
                    supermercado.cajas_rapidas[caja_escogida].persona_siendo_atendida = persona_que_termina_de_comprar_ahora #Le especifico que persona entró a la caja
                    supermercado.cajas_rapidas[caja_escogida].tiempo_de_uso += Tiempo_que_durara_esta_atencion  #Le agrego al tiempo de uso de la caja el tiempo que durará la atención

                    supermercado.personas[persona_que_termina_de_comprar_ahora].hora_de_atencion = T + Tiempo_que_durara_esta_atencion    #Le creo un tiempo de termino de la atención a esta persona
                    supermercado.Personas_atendidas += 1 #Agrego una persona más a los atendidos
                
                else: #Si no hay cajas rápidas desocupadas:
                    supermercado.Cola_rapida += 1 #Agregamos al contador de la fila de cajas rápidas una persona más
                    
                    supermercado.fila_cajas_rapidas.append(persona_que_termina_de_comprar_ahora) #Agrego la persona a la fila de la caja rápida

                    supermercado.personas[persona_que_termina_de_comprar_ahora].hora_que_entra_en_cola = T  #Indico el tiempo que empezó a hacer la fila la persona

        elif TP3 < TP1 and TP3 < TP2:   #Si es que el tiempo de atención va antes que uno de llegada y compra:
            T = TP3 #Actualizo el tiempo a tiempo de atención
            supermercado.personas[persona_que_es_atendida_ahora].ya_fue_atendido = True

            if supermercado.personas[persona_que_es_atendida_ahora].escoge_caja_rapida == False: #Si es que la persona que va a ser atendida estaba en caja normal

                for i in range(len(supermercado.cajas)):
                    if supermercado.cajas[i].persona_siendo_atendida == persona_que_es_atendida_ahora:  #Busco la caja donde acaba de ser atendida la persona
                        caja_atendiendo = i
                
                if supermercado.cajas[caja_atendiendo].Cerrada == True:
                    supermercado.personas[persona_que_es_atendida_ahora].se_atiende_en_caja_cerrada=True    #Reviso si la persona se atendió en una caja que estaba cerrada

                if supermercado.cajas[caja_atendiendo].Cola > 0:    #Reviso si esta caja tiene una cola, y si es que sí:
                    persona_que_iba_despues_de_la_que_acaba_de_ser_atendida = supermercado.cajas[caja_atendiendo].orden_de_clientes_en_cola[0] #Veo quién iba después de la persona que acaba de ser atendida
                    supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].tiempo_total_en_cola = T - supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].hora_que_entra_en_cola #Calculo cuanto estuvo esperando esta persona en la fila
                    supermercado.cajas[caja_atendiendo].orden_de_clientes_en_cola=supermercado.cajas[caja_atendiendo].orden_de_clientes_en_cola[1:] #Elimino a esta persona de la fila
                    supermercado.cajas[caja_atendiendo].Cola -= 1   #Quito del contador de la cola a una persona 

                    Tiempo_que_durara_esta_atencion = rd.lognormvariate(0.97,0.57)  #Creo un tiempo que durará esta atención de esta nueva persona

                    supermercado.cajas[caja_atendiendo].persona_siendo_atendida = persona_que_iba_despues_de_la_que_acaba_de_ser_atendida   #Actualizo la persona que esta siendo atendida ahora   
                    supermercado.cajas[caja_atendiendo].tiempo_de_uso += Tiempo_que_durara_esta_atencion    #Agrego tiempo de uso a la caja
                    supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].hora_de_atencion = T + Tiempo_que_durara_esta_atencion #Creo tiempo de termino de atención para esta persona
                    supermercado.Personas_atendidas += 1    #Agrego una persona más a los atendidos
                    

                else:   #Si es que no había cola en la caja:
                    supermercado.cajas[caja_atendiendo].Ocupada = False #Cambio el estado de la caja a desocupada
            
            elif supermercado.personas[persona_que_es_atendida_ahora].escoge_caja_rapida == True: #Si es que la persona que va a ser atendida estaba en caja rápida

                for i in range(len(supermercado.cajas_rapidas)):
                    if supermercado.cajas_rapidas[i].persona_siendo_atendida == persona_que_es_atendida_ahora:  #Busco la caja donde acaba de ser atendida la persona
                        caja_rapida_atendiendo = i
                
                
                if supermercado.Cola_rapida > 0:
                    
                    persona_que_iba_despues_de_la_que_acaba_de_ser_atendida = supermercado.fila_cajas_rapidas[0] #Veo quién iba después de la persona que acaba de ser atendida
                    supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].tiempo_total_en_cola = T - supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].hora_que_entra_en_cola #Calculo cuanto estuvo esperando esta persona en la fila
                    supermercado.fila_cajas_rapidas=supermercado.fila_cajas_rapidas[1:] #Elimino a esta persona de la fila
                    supermercado.Cola_rapida -= 1   #Quito del contador de la cola a una persona

                    Tiempo_que_durara_esta_atencion = rd.expovariate(0.57)  #Creo un tiempo que durará esta atención de esta nueva persona

                    supermercado.cajas_rapidas[caja_rapida_atendiendo].persona_siendo_atendida = persona_que_iba_despues_de_la_que_acaba_de_ser_atendida   #Actualizo la persona que esta siendo atendida ahora   
                    supermercado.cajas_rapidas[caja_rapida_atendiendo].tiempo_de_uso += Tiempo_que_durara_esta_atencion    #Agrego tiempo de uso a la caja
                    supermercado.personas[persona_que_iba_despues_de_la_que_acaba_de_ser_atendida].hora_de_atencion = T + Tiempo_que_durara_esta_atencion #Creo tiempo de termino de atención para esta persona
                    supermercado.Personas_atendidas += 1    #Agrego una persona más a los atendidos

                else:   #Si es que no había cola en la caja:
                    supermercado.cajas_rapidas[caja_rapida_atendiendo].Ocupada = False #Cambio el estado de la caja a desocupada     

        #Estado del supermercado para las siguientes iteraciones        


        for i in range(len(supermercado.personas)): #Reviso todas las personas del supermercado
            if supermercado.personas[i].ya_compro == False: #Reviso si ya compraron
                Horas_de_compras_totales.append(supermercado.personas[i].hora_de_compra)    #Si aun no compra, su tiempo de compra es considerado
            if supermercado.personas[i].ya_fue_atendido == False:   #Reviso si ya fueron atendidos
                Horas_de_atencion_totales.append(supermercado.personas[i].hora_de_atencion) #Si aun no son atendidos, sus tiempos de atención son considerados
        
        

        if Horas_de_compras_totales != []:
            TP2 = min(Horas_de_compras_totales)     #Veo cual es el tiempo de compra más pequeño
        else:
            TP2 = np.inf
        if Horas_de_atencion_totales != []:    
            TP3 = min(Horas_de_atencion_totales)    #Veo cual es el tiempo de atención más pequeño
        else:
            TP3 = np.inf
        if supermercado.Hora_de_cierre < T:
            TP1 = np.inf

        for i in range(len(supermercado.personas)): #Reviso todas las personas del supermercado
            if supermercado.personas[i].hora_de_compra == TP2:  #Reviso si el tiempo minimo de compra le pertenece a esa persona
                persona_que_termina_de_comprar_ahora=supermercado.personas[i].indice_de_persona   #Si es que le pertenece, será la siguiente persona en comprar
            if supermercado.personas[i].hora_de_atencion == TP3:    #Reviso si el tiempo minimo de atencion le pertenece a esa persona
                persona_que_es_atendida_ahora=supermercado.personas[i].indice_de_persona   #Si es que le pertenece, será la siguiente persona en ser atendida

        supermercado.Personas_que_quedan = supermercado.Personas_totales - supermercado.Personas_atendidas
        
        if supermercado.Hora_de_cierre < T and supermercado.Personas_que_quedan==0: #Condición de stop
            Stop=True
            T_ultimo=T

#Orden de outputs obtenidos
    for i in range(len(supermercado.personas)): #Calculamos promedio total de espera
        ESTOT += supermercado.personas[i].tiempo_total_en_cola
    for i in range(len(supermercado.cajas)):    #Calculamos promedio total de porcentaje de ocupación de cajas normales
        Porcentaje_sumado_cajas_normales += supermercado.cajas[i].tiempo_de_uso*100/T
    for i in range(len(supermercado.cajas_rapidas)):    #Calculamos promedio total de porcentaje de ocupación de cajas rápidas
        Porcentaje_sumado_cajas_rapidas += supermercado.cajas_rapidas[i].tiempo_de_uso*100/T
    
    if cantidad_intervalos_temporales > 0:  #Si es que hay intervalos
        
        for i in range(cantidad_intervalos_temporales):    #Para cada intervalo temporal
            personas_en_ese_intervalo=0
            for a in range(supermercado.Personas_totales): #Para cada persona, reviso si pertenece a ese intervalo temporal
                if supermercado.personas[a].hora_que_entra_en_cola == np.inf: #Además, reviso si es que existe su tiempo que inicio una cola, ya que si no entró a una cola, no tendrá uno
                    supermercado.personas[a].hora_que_entra_en_cola = supermercado.personas[a].hora_de_compra

                tiempo_en_la_mitad_de_su_espera_en_cola=(2*(supermercado.personas[a].hora_que_entra_en_cola)+supermercado.personas[a].tiempo_total_en_cola)/2
                tiempo_que_empieza_su_atencion = supermercado.personas[a].hora_que_entra_en_cola + supermercado.personas[a].tiempo_total_en_cola

                
                if  supermercado.personas[a].hora_que_entra_en_cola >= intervalos[i].tiempo_inicio and supermercado.personas[a].hora_que_entra_en_cola < intervalos[i].tiempo_final: #Aqui se decide con que criterio una persona pertenece a un intervalo o a otro
                    
                    intervalos[i].tiempos_de_espera.append(supermercado.personas[a].tiempo_total_en_cola)
                    personas_en_ese_intervalo+=1
                
                if tiempo_que_empieza_su_atencion >= intervalos[i].tiempo_inicio and tiempo_que_empieza_su_atencion < intervalos[i].tiempo_final and supermercado.personas[a].escoge_caja_rapida == False and supermercado.personas[a].se_atiende_en_caja_cerrada==False:

                    if supermercado.personas[a].hora_de_atencion >= intervalos[i].tiempo_inicio and supermercado.personas[a].hora_de_atencion < intervalos[i].tiempo_final:
                        intervalos[i].tiempos_de_ocupacion.append(supermercado.personas[a].hora_de_atencion-tiempo_que_empieza_su_atencion)
                    else:
                        intervalos[i].tiempos_de_ocupacion.append(intervalos[i].tiempo_final - tiempo_que_empieza_su_atencion)
                        intervalos[i+1].tiempos_de_ocupacion.append(supermercado.personas[a].hora_de_atencion - intervalos[i].tiempo_final)

            Promedios_por_intervalos.append(sum(intervalos[i].tiempos_de_espera)/personas_en_ese_intervalo)
            if i != (cantidad_intervalos_temporales-1):
                Promedios_por_intervalo_cajas_normales.append(sum(intervalos[i].tiempos_de_ocupacion)*100/((intervalos[i].cajas_abiertas+0.005)*(intervalos[i].tiempo_final-intervalos[i].tiempo_inicio)))
            else:
                Promedios_por_intervalo_cajas_normales.append(sum(intervalos[i].tiempos_de_ocupacion)*100/((intervalos[i].cajas_abiertas+0.005)*(T_ultimo-intervalos[i].tiempo_inicio)))
    
        Promedio_ocupacion_real=[]
        for i in range(cantidad_intervalos_temporales):
            if i != (cantidad_intervalos_temporales-1):
                Promedio_ocupacion_real.append(Promedios_por_intervalo_cajas_normales[i]*(intervalos[i].tiempo_final-intervalos[i].tiempo_inicio))
            else:
                Promedio_ocupacion_real.append(Promedios_por_intervalo_cajas_normales[i]*(T_ultimo-intervalos[i].tiempo_inicio))
        Promedio_ocupacion_real=sum(Promedio_ocupacion_real)/(T_ultimo)

        for i in range(len(intervalos)):
            print(intervalos[i].cajas_abiertas)

    return [(ESTOT/supermercado.Personas_totales),(Promedio_ocupacion_real),
            (Porcentaje_sumado_cajas_rapidas/len(supermercado.cajas_rapidas)),(Promedios_por_intervalos),(Promedios_por_intervalo_cajas_normales)] #Returneamos estos promedios

    
if __name__ == '__main__':
    # Archivo
    path = 'Datos_Simulacion_Opti.txt'
    file = open(path, 'w', encoding='utf-8')

    for a in range(30):
        #Decisiones
        Tiempo_simulación=720 #Para día completo: 720, Para 12:50 a 15:00: 160
        Cajas_normales= a+1
        Cajas_rapidas=8
        intervalos_temporales=4
        veces_que_se_abren_cajas=0
        veces_que_se_cierran_cajas=0

        iteraciones=30
        intervalos_temporales_lista_inicio=[0,100,300,500]
        intervalos_temporales_lista_final=[100,300,500,100000000]

        hora_que_cierra_cajas=[]
        cuantas_cajas_cierra=[]

        hora_apertura_de_cajas=[]
        cuantas_cajas_abre=[]


        #Creación intervalos temporales
        if intervalos_temporales>0:
            intervalos = create_intervalos_temporales(intervalos_temporales,intervalos_temporales_lista_inicio,intervalos_temporales_lista_final)
        else:
            intervalos=[]
        #Creación veces que se abre cajas:
        if veces_que_se_abren_cajas>0:
            apertura_de_cajas = create_veces_que_se_abren_cajas(veces_que_se_abren_cajas,)
        else:
            apertura_de_cajas=[]
        #Creación veces que se cierra cajas:
        if veces_que_se_cierran_cajas>0:
            cierre_de_cajas = create_veces_que_se_cierran_cajas(veces_que_se_cierran_cajas)
        else:
            cierre_de_cajas=[]

        #Resultados
        initial_time = time.time()
        suma1=0
        suma2=0
        suma3=0
        suma4=[0] * intervalos_temporales
        suma5=[0] * intervalos_temporales
        for i in range(iteraciones):
            simu=Simulacion(Tiempo_simulación,Cajas_normales,Cajas_rapidas,intervalos_temporales,veces_que_se_abren_cajas,veces_que_se_cierran_cajas)
            suma1+=simu[0]
            suma2+=simu[1]
            suma3+=simu[2]
            suma4 = [a + b for a, b in zip(simu[3], suma4)]
            suma5 = [a + b for a, b in zip(simu[4], suma5)]

            line = f"Promedio de espera simulación {i} : {simu[0]} \nPorcentaje de ocupación cajas normales {i} : {simu[1]} \nPorcentaje de ocupación cajas rápidas {i} : {simu[2]} \nPromedio de espera por intervalo{i} : {simu[3]} \nPorcentaje ocupación por intervalos: {simu[4]} % \n\n"
            file.write(line)

            print("Promedio de espera simulación",i,":",simu[0],"\nPorcentaje de ocupación cajas normales",i,": ",simu[1],
                "\nPorcentaje de ocupación cajas rápidas",i,": ",simu[2],
                "\nPromedio de espera por intervalo",i,": ",simu[3],
                "\nPorcentaje de ocupación por intervalo",i,": ",simu[4])

        final_time = time.time()

        line = f"\nCajas abiertas: {a+1}----------------\nPromedio de espera total: {suma1/iteraciones} minutos\nPromedio ocupación de cajas normales total: {suma2/iteraciones} %\nPromedio ocupación de cajas rápidas total: {suma3/iteraciones} % \nPromedio espera por intervalos: {[elemento / iteraciones for elemento in suma4]} minutos \nPromedio ocupación por intervalos: {[elemento / iteraciones for elemento in suma5]} % $"
        file.write(line)
        
        print("\nCajas abiertas:",a+1," ----------------\nPromedio de espera total:",suma1/iteraciones,"minutos\nPromedio ocupación de cajas normales total:",suma2/iteraciones,
            "%\nPromedio ocupación de cajas rápidas total:",suma3/iteraciones,
            "%\nPromedio espera por intervalos:",[elemento / iteraciones for elemento in suma4],"minutos",
            "%\nPromedio ocupación por intervalos:",[elemento / iteraciones for elemento in suma5],"%")
        print("\n----------------\nTiempo total de ejecución:",final_time-initial_time,"segundos")

        #AJUSTAR PORCENTAJE DE OCUPACIÓN DE CAJAS QUE SE ABREN DESPUÉS

        #1Preguntarle al gerente cómo dividen un día (a que hora cierran y abren cajas?)(Si no funciona hablando con el gerente, verlo por mi propia cuenta)
    file.close()