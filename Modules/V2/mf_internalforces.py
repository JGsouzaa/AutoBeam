#mf_internalforces
#Definindo funções que retornam o valor dos esforços entrando com parâmetros de
   #Número da barra, numero do caso de carga e ponto de interesse
#Funções que são utilizadas tendo definido o f_serv que é o server onde estão armazenados os resultados de forças, definiu-se assim para poupar processamento
    #no algoritmo que coleta os dados e armazena em dataframes (linha 283 DADOS DE ESFORÇOS DE BARRAS)
def MomentoX(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        #MX1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).MX /1000
        MX1 = f_serv.MX /1000
        return (round(MX1, 2))  
def MomentoY(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        #MY1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).MY /1000
        MY1 = f_serv.MY /1000
        return (round(MY1,2))
def MomentoZ(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        MZ1 = f_serv.MZ /1000
        #MZ1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).MZ /1000
        return (round(MZ1,2))
def ForçaX(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        #FX1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).FX /1000
        FX1 = f_serv.FX /1000
        return (round(FX1, 2))  
def ForçaY(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        #FY1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).FY /1000
        FY1 = f_serv.FY /1000
        return (round(FY1,2 ))  
def ForçaZ(f_serv):
        #L = IRobotBar(bars.Get(Barra_Numero)).Length 
        #FZ1 = force_serv.Value(Barra_Numero, Caso_Numero, Ponto/L).FZ /1000
        FZ1 = f_serv.FZ /1000
        return (round(FZ1, 2))  