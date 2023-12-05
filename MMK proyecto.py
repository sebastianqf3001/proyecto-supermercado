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
        

class Caja:
    def __init__(self, indice, tipo):
        self.indice_de_caja = indice
        self.Ocupada = False
        self.persona_siendo_atendida = -1   #Aquí va el índice de la persona
        self.Cola = 0
        self.orden_de_clientes_en_cola=[] #Aquí va el índice de la persona
        self.tiempo_de_uso=0
        self.caja_rapida=tipo

def ExponentialInstance(lambd):
    u = np.random.uniform(0, 1)
    return -np.log(1 - u) / lambd


# def taylor_serie(x):  #Taylor Día completo
#         y = 4.833468511100568e-61 * (x - 368.0)**25 + 1.104321097541718e-59 * (x - 368.0)**24 + -6.764502240882454e-55 * (x - 368.0)**23 + -1.164401773589306e-53 * (x - 368.0)**22 + 4.1460818454159185e-49 * (x - 368.0)**21 + 4.667870353711148e-48 * (x - 368.0)**20 + -1.4659596525009974e-43 * (x - 368.0)**19 + -7.746370031433263e-43 * (x - 368.0)**18 + 3.3167058552077726e-38 * (x - 368.0)**17 + -5.671961723527083e-39 * (x - 368.0)**16 + -5.037697259426038e-33 * (x - 368.0)**15 + 2.1449400770960893e-32 * (x - 368.0)**14 + 5.246041343119162e-28 * (x - 368.0)**13 + -3.0614021619992635e-27 * (x - 368.0)**12 + -3.758438093424414e-23 * (x - 368.0)**11 + 1.4169551592324059e-22 * (x - 368.0)**10 + 1.8287770822228958e-18 * (x - 368.0)**9 + 4.140212800064939e-18 * (x - 368.0)**8 + -5.834669245448097e-14 * (x - 368.0)**7 + -6.155984615892722e-13 * (x - 368.0)**6 + 1.1341045785547847e-09 * (x - 368.0)**5 + 1.884961111267024e-08 * (x - 368.0)**4 + -1.1601179506002755e-05 * (x - 368.0)**3 + -0.00019698650221112288 * (x - 368.0)**2 + 0.04565345572605308 * (x - 368.0)**1 + 6.0506699555558985 * (x - 368.0)**0
#         return y

#6.992949261062695 #Tasa max Día completo

def taylor_serie(x):    #Taylor de 12:50 a 15:00
    y = -1.52376276542353e-82 * (x - 4800.0)**20 + -1.2931581044293425e-78 * (x - 4800.0)**19 + -7.00808257807493e-75 * (x - 4800.0)**18 + 4.111209901067969e-71 * (x - 4800.0)**17 + 2.219064059920795e-66 * (x - 
4800.0)**16 + 4.7104589446191605e-62 * (x - 4800.0)**15 + 7.835326579048999e-58 * (x - 4800.0)**14 + 1.0068344086441171e-53 * (x - 4800.0)**13 + 1.1247020764670005e-49 * (x - 4800.0)**12 + 1.8278877760677984e-46 * (x - 4800.0)**11 + -5.588726612225112e-42 * (x - 4800.0)**10 + -6.543255429683764e-37 * (x - 4800.0)**9 + -1.8340246083850404e-33 * (x - 4800.0)**8 + -2.155225116442326e-28 * (x - 4800.0)**7 + 4.3656108445878755e-24 * (x - 4800.0)**6 + -5.015060681829637e-21 * (x - 4800.0)**5 + -2.0041607724575117e-16 * (x - 4800.0)**4 + 7.228088186884462e-13 * (x - 4800.0)**3 + 2.014061532911628e-09 * (x - 4800.0)**2 + -1.001818337280383e-05 * (x - 4800.0)**1 + 0.0812096793456032 * (x - 4800.0)**0
    return y

def generar_llegada(T):
    aceptar=False
    tasa_maxima= 6.099  #Poner tasa de día completo o de 12:50 a 15:00
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

def Simulacion(Tfin,cantidad_de_cajas_normales, cantidad_de_cajas_rapidas):
    T = 0 # Reloj
    Stop=False

    supermercado = Supermercado(Tfin,cantidad_de_cajas_normales,cantidad_de_cajas_rapidas)    #Creo supermercado
    indice_persona=0
    
    TP1 = generar_llegada(T) # llegada de cliente 1
    TP2 = np.inf # compra de cliente 1
    TP3 = np.inf # atencion de cliente 1

    ESTOT=0 #Variable auxiliar guardadora de tiempos de espera
    Porcentaje_sumado_cajas_normales=0 #Variable auxiliar guardadora de porcentajes de ocupación cajas normales
    Porcentaje_sumado_cajas_rapidas=0   #Variable auxiliar guardadora de porcentajes de ocupación cajas rápidas


    while (Stop==False): #condición de stop
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
                    if supermercado.cajas[i].Ocupada == False:
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
                        if supermercado.cajas[i].Cola < fila_menor:
                            fila_menor=supermercado.cajas[i].Cola

                    cajas_de_menor_fila=[]
                    for i in range(len(supermercado.cajas)): #Busco entre todas las cajas las que tengan esta menor fila
                        if supermercado.cajas[i].Cola == fila_menor:
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
  
    for i in range(len(supermercado.personas)):
        ESTOT += supermercado.personas[i].tiempo_total_en_cola
    for i in range(len(supermercado.cajas)):
        Porcentaje_sumado_cajas_normales += supermercado.cajas[i].tiempo_de_uso*100/T
    for i in range(len(supermercado.cajas_rapidas)):
        Porcentaje_sumado_cajas_rapidas += supermercado.cajas_rapidas[i].tiempo_de_uso*100/T
    return [(ESTOT/supermercado.Personas_totales),(Porcentaje_sumado_cajas_normales/len(supermercado.cajas)),
            (Porcentaje_sumado_cajas_rapidas/len(supermercado.cajas_rapidas))] #Calculamos promedio de espera y promedio de porcentaje de ocupación


if __name__ == '__main__':

    #Decisiones
    Tiempo_simulación=160
    Cajas_normales=12
    Cajas_rapidas=8

    iteraciones=10

    # Archivo
    path = 'simulation.txt'
    file = open(path, 'w', encoding='utf-8')

    #Resultados
    initial_time = time.time()
    suma1=0
    suma2=0
    suma3=0
    for i in range(iteraciones):
        simu=Simulacion(Tiempo_simulación,Cajas_normales,Cajas_rapidas)
        suma1+=simu[0]
        suma2+=simu[1]
        suma3+=simu[2]

        line = f"Promedio de espera simulación {i} : {simu[0]} \nPorcentaje de ocupación cajas normales {i} : {simu[1]} \nPorcentaje de ocupación cajas rápidas {i} : {simu[2]}\n\n"
        file.write(line)

        print("Promedio de espera simulación",i,":",simu[0],"\nPorcentaje de ocupación cajas normales",i,": ",simu[1],
            "\nPorcentaje de ocupación cajas rápidas",i,": ",simu[2])

    final_time = time.time()

    line = f"\n----------------\nPromedio de espera total: {suma1/iteraciones} minutos\nPromedio ocupación de cajas normales total: {suma2/iteraciones} %\nPromedio ocupación de cajas rápidas total: {suma3/iteraciones} %"
    file.write(line)
    
    print("\n----------------\nPromedio de espera total:",suma1/iteraciones,"minutos\nPromedio ocupación de cajas normales total:",suma2/iteraciones,
        "%\nPromedio ocupación de cajas rápidas total:",suma3/iteraciones,"%")
    print("\n----------------\nTiempo total de ejecución:",final_time-initial_time,"segundos")

    file.close()

    #1Preguntarle al gerente cómo dividen un día (a que hora cierran y abren cajas?)(Si no funciona hablando con el gerente, verlo por mi propia cuenta)
    #2Hacer los intervalos en el modelo
    #3Abrir y cerrar cajas