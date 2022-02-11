#mf_esfpoint_if
#FUNÇÃO QUE RETORNA O VALOR MÁXIMO DE MX NO PONTO E NA BARRA
def MaxEsf_Point_MX(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MX/1000)
    return(max(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MÍNIMO DE MX NO PONTO E NA BARRA
def MinEsf_Point_MX(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MX/1000)
    return(min(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MÁXIMO DE MY NO PONTO E NA BARRA
def MaxEsf_Point_MY(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MY/1000)
    return(max(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MÍNIMO DE MY NO PONTO E NA BARRA
def MinEsf_Point_MY(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MY/1000)
    return(min(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MÁXIMO DE MZ NO PONTO E NA BARRA
def MaxEsf_Point_MZ(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MZ/1000)
    return(max(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MÍNIMO DE MZ NO PONTO E NA BARRA
def MinEsf_Point_MZ(Bar,Point,Length,listcomb,force_serv):
    listenvolv = []
    #Length = IRobotBar(bars.Get(Bar)).Length
    for i in range(len(listcomb)):
        listenvolv.append(force_serv.Value(Bar,listcomb[i],Point/Length).MZ/1000)
    return(min(listenvolv))
#
    #EX: int(3.6/precisão)
    #EX: for i in range(9,14):
        #print(force_serv.Value(1,i,(3.6/6)).MY/1000)
    #EX: EsfPointValue(1,"My",2.8)
    #EX: MaxEsfValue(1,"My")
