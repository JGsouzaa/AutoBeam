# -*- coding: utf-8 -*-
#1-------------------------------BIBLIOTECAS-----------------------------------------------------------#
#Importando bibliotecas
    #O módulo clr é um módulo de strings
    #Utilizando o pythonnet o módulo clr serve como um python package
import clr 
    #Biblioteca que habilita o CLR(Common Language Runtime) no python
        #1 - CLR é um componente da maquina virtual .NET da microsoft que gerencia a execução
        #   de programas .NET
        #2 - instalando pythonnet ele utiliza o clr como acesso ao CLR do windows
import numpy as np
    #Biblioteca que suporta array e matrizes
import matplotlib.pyplot as plt
    #Biblioteca para geração de gráficos
import pandas as pd
    #Biblioteca pra manipulação e análise de dados
#2--------------------------------MÓDULOS----------------------------------------------------------#
clr.AddReference('C:\Program Files\Autodesk\Autodesk Robot Structural Analysis Professional 2021\System\Exe\Interop.RobotOM.dll')
    #Adiciona a referencia ao python package (torna acessível via python)
    #Da acesso aos módulos da biblioteca compartilhada do Robot (Habilita a utilização dos objetos do Robot)
from RobotOM import *
    #Importa tudo que esta contido no RobotOM
from matplotlib import pyplot as plt
#------------------------------------------------------------------------------------------#
import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()
#3---------------------------------VARIAVEIS DE INICIO---------------------------------------------------------#
#Módulo de referências iniciais
from mr_initial import *
project.Open("C:\Temp\\projeto2.rtd")
    #Abre o projeto ja existente
#Módulo de referências do projeto
from mr_project import *
#VARIAVEL precisão CONDIZ COM A PRECISÃO A SER USADA AO COLETAR OS DADOS DAS BARRAS (Ex: precisão = 0.1 -> DADOS COLETADOS DE 0.1 em 0.1, MX(0.0), MX(0.1), MX(0.2))
precisão = 0.01 #em m
#4---------------------------------COLETANDO DADOS DO ROBOT---------------------------------------------------------#
#Função que retorna uma seleção contendo apenas casos de carga do tipo COMB(Combinação)
    #No robot cada definição de carga ou combinação de carga é interpretado como caso de carga, para isso precisa-se filtrar para não gastar tempo e processamento com casos de carga do tipo carga simples
def case_comb_selection():
    case_selection = RobotSelection(selections.Create(2))
        #Cria uma seleção para os casos de carga 
    for i in range(cas_col.Count):
        if IRobotCase(cases.Get(i+1)).AnalizeType == 0:
            case_selection.AddOne(i+1)
        else:
            pass
    return(case_selection)
#Classe que retorna funçoes para a seleção atual do projeto
class Current_Selection():
    def Node_Selection():
        current_selection = RobotSelection(selections.Get(0))
        return(current_selection)
    def Bar_Selection():
        current_selection = RobotSelection(selections.Get(1))
        return(current_selection)
    def Case_Selection():
        current_selection = RobotSelection(selections.Get(2))
        return(current_selection)
    def Group_Selection():
        current_selection = RobotSelection(selections.Get(3))
        return(current_selection)
    def Painel_Selection():
        current_selection = RobotSelection(selections.Get(4))
        return(current_selection)
    def Finite_Element_Selection():
        current_selection = RobotSelection(selections.Get(5))
        return(current_selection)
    def Geometrical_Object_Selection():
        current_selection = RobotSelection(selections.Get(6))
        return(current_selection)
    def Volumetric_Object_Selection():
        current_selection = RobotSelection(selections.Get(7))
        return(current_selection)
    def Undefined_Selection():
        current_selection = RobotSelection(selections.Get(-1))
        return(current_selection)
    def Object_Selection():
        current_selection = RobotSelection(selections.Get(-2))
        return(current_selection)
#Módulo de funções que retornam valores dos esforços
from mf_internalforces import *
#Módulo de funções que retornam informações sobre a secção transversal do elemento de barra
from mf_section_props import *
#Cria uma referência da seleção atual de barras
current_selection = Current_Selection.Bar_Selection()
#cria uma lista com os numeros das barras contidas na seleção atual
i2 = 0
list_bars = []
for i in range(current_selection.Count):
    while current_selection.Contains(i2) == False:
        i2 += 1
    else:
        list_bars.append(i2)
        i2 += 1
#Cria uma referência da seleção atual de casos de carga do tipo COMBINAÇÃO
comb_cases_selection = case_comb_selection()
#Cria uma lista com os casos de carga do tipo COMBINAÇÃO
listcomb = []
for i in range(1, case_comb_selection().Count + 1):
    listcomb.append(comb_cases_selection.Get(i))
#5.1---------------------------------MATERIAIS---------------------------------------------------------#
#5.1.1------------------------------------CONCRETO------------------------------------------------------#
#CRIAÇÃO DE DICIONARIOS E LOOP PARA VERIFICAR 
dic_MatName = {}
dic_fck = {}
dic_MElasticidade = {}
dic_Poisson = {}
dic_MCisalhamento = {}
dic_PesoEsp = {}
dic_CoefExpTerm = {}
dic_CoefAmort = {}
for i in range(len(list_bars)):
        i2 = list_bars[i]
        MaterialData = IRobotMaterialData(IRobotLabel(IRobotBar(bars.Get(i2)).GetLabel(8)).Data)
        dic_MatName[f'Barra_{i2}_MatName'] = MaterialData.Name
        dic_fck[f'Barra_{i2}_fck'] = MaterialData.RE/(10**6) #MPa
        dic_MElasticidade[f'Barra_{i2}_MElasticidade'] = MaterialData.E/(10**9) #GPa
        dic_Poisson[f'Barra_{i2}_Poisson'] = MaterialData.NU
        dic_MCisalhamento[f'Barra_{i2}_MCisalhamento'] = MaterialData.Kirchoff/(10**9) #GPa
        dic_PesoEsp[f'Barra_{i2}_PesoEsp'] = MaterialData.RO/(10**3) #kN/m3
        dic_CoefExpTerm[f'Barra_{i2}_CoefExpTerm'] = MaterialData.LX #1/ºC
        dic_CoefAmort[f'Barra_{i2}_CoefAmort'] = MaterialData.DumpCoef
#MATERIAIS NA SELEÇAO SAO IGUAIS?
for j2 in range(len(list_bars)-1):
    i2 = list_bars[j2]
    i3 = list_bars[j2+1]
    if dic_MatName[f'Barra_{i2}_MatName'] == dic_MatName[f'Barra_{i3}_MatName']:
        MatName_Iguais = True
    else:
        MatName_Iguais = False
if MatName_Iguais == True:
    fck = dic_fck[f'Barra_{i2}_fck']
    del dic_fck
    MElasticidade = dic_MElasticidade[f'Barra_{i2}_MElasticidade']
    del dic_MElasticidade
    Poisson = dic_Poisson[f'Barra_{i2}_Poisson']
    del dic_Poisson
    MCisalhamento = dic_MCisalhamento[f'Barra_{i2}_MCisalhamento']
    del dic_MCisalhamento
    PesoEsp = dic_PesoEsp[f'Barra_{i2}_PesoEsp']
    del dic_PesoEsp
    CoefExpTerm = dic_CoefExpTerm[f'Barra_{i2}_CoefExpTerm']
    del dic_CoefExpTerm
    CoefAmort = dic_CoefAmort[f'Barra_{i2}_CoefAmort']
    del dic_CoefAmort
else:
    print("Materiais da seleção são diferentes e possuem propriedades diferentes")
#5.2---------------------------------SEÇÃO DA SELEÇÃO---------------------------------------------------------#
#from m_selection_section import *
dic_height = {}
dic_width = {}
#COLETA E ARMAZENA DADOS DE SEÇAO DA SELEÇAO
for i in range(len(list_bars)):
    i2 = list_bars[i]
    #Cria dicionarios que armazenam dados de base e altura da seleção de barras
    dic_height[f'Barra_{i2}_Altura'] = height(i2)
    dic_width[f'Barra_{i2}_Base'] = width(i2)
#FAZ A VERIFICAÇÃO DE HOMOGENIDADE DA SEÇÃO TRANSVERSAL AO LONGO DA SELEÇÃO
for j in range(len(list_bars)-1):
    #Seleciona a primeira barra e a barra seguinte
    i2 = list_bars[j]
    i3 = list_bars[j+1]
    #Verifica se os dados de altura são iguais entre as barras
    if dic_height[f'Barra_{i2}_Altura'] == dic_height[f'Barra_{i3}_Altura']:
        Alturas_Iguais = True
    else:
        Alturas_Iguais = False
    #Verifica se os dados de base são iguais entre as barras
    if dic_width[f'Barra_{i2}_Base'] == dic_width[f'Barra_{i3}_Base']:
        Bases_Iguais = True
    else:
        Bases_Iguais = False
#VERIFICA SE HÃ HOMOGENIDADE EM TODA A SELEÇÃO
if Alturas_Iguais == True:
    Altura_barras_selection = dic_height[f'Barra_{i2}_Altura']
    del dic_height
else:
    height_selection = str("Altura variável")
if Bases_Iguais == True:
    Base_barras_selection = dic_width[f'Barra_{i2}_Base']
    del dic_width
else:
    width_selection = str("Base variável")
#SE ALTURA OU BASE FOSSEM DIFERENTES DEVE-SE FAZER UM DIMENSIONAMENTO/VERIFICAÇAO PARA CADA SEÇAO  
#5.3---------------------------------DADOS DE ESFORÇOS DAS BARRAS---------------------------------------------------------#
#MODELO BASE: force_serv.Value(BARRA,CASO_DE_CARGA,PONTO/COMPRIMENTO)
#Loop para variar o numero da barra
for i in range (len(list_bars)):
    #Definindo listas para armazenar os dados coletados
    dMx = []; dMy = []; dMz = []; dFx = []; dFy = []; dFz = []; Results_df = []
    j=0
    i2 = list_bars[i]
    viga = IRobotDataObject(bars.Get(current_selection.Get(i2)))
    Length = IRobotBar(bars.Get(i2)).Length
    #Loop para variar os casos de carga
    for j in range(len(listcomb)):
        locals()[f'p_{i+1}'] = []
        cas_numb = listcomb[j]
        k=0
        L = IRobotBar(bars.Get(i2)).Length 
        #Coleta os momentos Mx,My e Mz para a barra, caso de carga e precisão selecionados
        #Loop para variar o ponto com base na precisão adotada
        for k in np.arange(0,Length + precisão ,precisão):
            f_serv = force_serv.Value(i2, cas_numb, k/L) #(BARRA,CASO,PONTO)
            dMx.append(MomentoX(f_serv))
            dMy.append(MomentoY(f_serv))
            dMz.append(MomentoZ(f_serv))
            dFx.append(ForçaX(f_serv))
            dFy.append(ForçaY(f_serv))
            dFz.append(ForçaZ(f_serv))
            locals()[f'p_{i+1}'].append(round(k, 2))
            #p.append(k)
        #Cria uma base de dados para cada Barra e Caso de carga selecionados
        locals()["Viga_" + str(i2) + "_Caso_" + str(IRobotCase(cases.Get(cas_numb)).Name
            )] = pd.DataFrame([dMx, dMy, dMz, dFx, dFy, dFz], columns = locals()
                [f'p_{i+1}'], index = ["Mx","My","Mz", "Fx", "Fy", "Fz"])
        dMx = []; dMy = []; dMz = []; dFx = []; dFy = []; dFz = []
        print("Viga_" + str(i2) + str(IRobotCase(cases.Get(comb_cases_selection.Get(j+1))).Name))
del dMx; del dMy; del dMz; del dFx; del dFy; del dFz
#6---------------------------------GERADORES DE GRÁFICOS---------------------------------------------------------#
#Módulo de funções para plotar gráficos dos elementos de barras
from mf_graphs_if import *
#FUNÇÃO QUE RETORNA O GRÁFICO DA ENVOLVENTE DE ESFORÇOS PARA UMA DADA BARRA E UM DADO ESFORÇO
def Envolvente(Esforço,Barra, Lista_Pontos, EscalaX, EscalaY): #(str, int, list, float, float)
    listenvolv = []
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))   
    del listprov; del prov
    vigaplot = listenvolv
    Esf_max = max(vigaplot)
    Ponto_max = Lista_Pontos[vigaplot.index(Esf_max)]
    Esf_min = min(vigaplot)
    Ponto_min = Lista_Pontos[vigaplot.index(Esf_min)]
    Text_max = "Maximo " + str(Esforço) + ": " + str(Esf_max) + " Ponto: " + str(Ponto_max)
    Text_min = "Minimo " + str(Esforço) + "; " + str(Esf_min) + " Ponto: " + str(Ponto_min)   
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title("Envolvente " +IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento " + Esforço + " [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.annotate(Text_max, xy=(Length/2,Esf_max), fontsize = 15, bbox = dict(facecolor = "green", alpha = 0.5))
    plt.annotate(Text_min, xy=(Length/2,Esf_min), fontsize = 15, bbox = dict(facecolor = "red", alpha = 0.5)) 
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DA ENVOLVENTE PARA TODA A SELEÇÃO 
def EnvolventeCompleta(Esforço,EscalaX,EscalaY): #(str, float/int, float/int)
    Viga_Completa = []
    p_tot = []
    List_Length = []
    Length_0 = 0
    List_Length.append(Length_0)   
    for k in range(len(list_bars)):
        i2 = list_bars[k]
        NumbViga = current_selection.Get(i2)
        #Cria lista com envolvente para cada barra
        locals()[f"listenvolv_{k+1}"] = []
        #Loop para pegar os valores envolventes ao longo de cada barra 
        for i in range(len(eval("p_%d" %(k+1)))):
            locals()[f"listprov_{k+1}"] = []
            for j in range(len(listcomb)):
                locals()[f"prov_{k+1}"] = eval("Viga_%d_Caso_COMB%d" %(NumbViga,j+1)).loc[Esforço].to_numpy()[i]
                eval("listprov_%d" %(k+1)).append(eval("prov_%d" %(k+1)))
            if abs(max(eval("listprov_%d" %(k+1)))) > abs(min(eval("listprov_%d" %(k+1)))):
                eval("listenvolv_%d" %(k+1)).append(max(eval("listprov_%d" %(k+1))))
            else:
                eval("listenvolv_%d" %(k+1)).append(min(eval("listprov_%d" %(k+1))))   

        VigaRef = eval("listenvolv_%d" %(k+1))
        Viga_Completa.append(VigaRef)
        globals()[f"Length_{k+1}"] = IRobotBar(bars.Get(i2)).Length + eval("Length_%d" %k)
        List_Length.append(eval("Length_%d" %(k+1)))
        #Cria lista das coordenadas das barras, onde termina uma começa a outra
        locals()[f"p_{k+1}"] = [(x+List_Length[k]) for x in eval("p_%d" %(k+1))]
        p_tot.append(eval("p_%d" %(k+1)))
        i2 += 1
    p_tot = [item for sublist in p_tot for item in sublist]
    Viga_Completa = [item for sublist in Viga_Completa for item in sublist]
    plt.plot(p_tot,Viga_Completa)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaY)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title("Viga completa")
    plt.gca().invert_yaxis()
    plt.ylabel("Momento " + Esforço + " [kN]")
    plt.xlabel("Ponto na viga")
    plt.axhline(y=0, color="k", linestyle="-")
    for i in range(current_selection.Count+1):
        plt.axvline(x= List_Length[i], color = "k", linestyle = "-")
    plt.show()
#
    #EX: Envolvente("My",1,p_1,1,1)
    #EX: EnvolventeCompleta("My",1,1)
#Range para fazer a envolvente de esforços dos elementos de barra isolados
for i in range(len(list_bars)):
    barra = list_bars[i]
    lista = eval("p_%d" %barra)
    Envolvente("My",barra, lista, 1,1)
#7---------------------------------FUNÇÕES PARA O DATAFRAME---------------------------------------------------------#
#Módulo de funções que retornam valores específicos dos esforços internos dos elemntos de barra
#FUNÇÃO QUE RETORNA O VALOR MÁXIMO DE ESFORÇO PARA UMA DADA BARRA
def MaxEsfValue(Barra,Esforço,Lista_Pontos): #(int,str,list)
    listenvolv = []
    #Lista_Pontos = eval("p_%d" %Barra)
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))
    return(max(listenvolv)) #kNm
#FUNÇÃO QUE RETORNA O VALOR MÍNIMO DE ESFORÇO PARA UMA DADA BARRA
def MinEsfValue(Barra,Esforço,Lista_Pontos): #(int,str,list)
    listenvolv = []
    #Lista_Pontos = eval("p_%d" %Barra)
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))
    return(min(listenvolv))
#FUNÇÃO QUE RETORNA O VALOR MAXIMO DE ESFORÇO PARA UMA DADA BARRA
def MaxEsfPoint(Barra,Esforço,Lista_Pontos): #(int,str,list)
    listenvolv = []
    #Lista_Pontos = eval("p_%d" %Barra)
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))
    return(listenvolv.index(max(listenvolv))*precisão) #m
#FUNÇÃO QUE RETORNA O PONTO ONDE OCORRE O VALOR MÍNIMO NA BARRA
def MinEsfPoint(Barra,Esforço,Lista_Pontos): #(int,str,list)
    listenvolv = []
    Lista_Pontos = eval("p_%d" %Barra)
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))
    return(listenvolv.index(min(listenvolv))*precisão) #m
#FUNÇÃO QUE RETORNA O VALOR MÁXIMO (UTILIZANDO TODAS AS COMBINAÇÕES) PARA O PONTO NA BARRA
def MaxEsfPointValue(Barra,Esforço,Ponto,Lista_Pontos): #(int,str, int/float,list)
    listenvolv = []
    Lista_Pontos = eval("p_%d" %Barra)
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))
    return(listenvolv[int(np.ceil(Ponto/precisão))]) #m

#8---------------------------------FUNÇÕES PARA O FORCE SERVER---------------------------------------------------------#
from mf_esfpoint_if import * 
#9-------------------------------------DADOS PRÉ-ESTABELECIDOS PELO USUARIO-----------------------------------------------------#
#9.1------------------------------------MATERIAIS------------------------------------------------------#
#9.1.1------------------------------------CONCRETO------------------------------------------------------#
#PARAMETROS DE CALCULO ESTABELECIDOS PELA NORMA DE REFERENCIA
#Norma de referência: NPEN-1992
coef_seg_conc = 1.5 #Item 2.4.2.4
fck = fck #Dado de projeto (Informação extraida do robot)
PesoEsp_conc = PesoEsp
alfa_cc = 1.0 #Item 3.1.6 (1) - NOTA
fcd = (alfa_cc*fck)/coef_seg_conc #Expressao (3.15)
fcm = fck + 8 #MPa
#fctm
if fck > 50: #MPa
    fctm = 2.12*np.log(1+(fcm/10)) #MPa
else:
    fctm = 0.3*fck**(2/3) #MPa
fctk_005 = 0.7*fctm
fctk_095 = 1.3*fctm
Ecm = 22*((fcm/10)**0.3) #fcm em MPa #GPa
#Def_ec1
if 0.7*fcm**0.31 <= 2.8:
    Def_ec1 = 0.7*fcm**0.31 #/1000
else:
    Def_ec1 = 2.8 #/1000
#Def_ecu1
if fck < 50: #MPa
    Def_ecu1 = 3.5 #/1000
else:
    Def_ecu1 = 2.8+27*(((98-fcm)/100)**4) #/1000
#Def_ec2
if fck < 50: #MPa
    Def_ec2 = 2 #/1000
else:
    Def_ec2 = 2+0.085*(fck-50)**0.53 #/1000
#Def_ecu2
if fck < 50: #MPa
    Def_ecu2 = 3.5 #/1000
else:
    Def_ecu2 = 2.6 + 35*((90-fck)/100)**4 #/1000
#n
if fck < 50: #MPa
    n = 2
else:
    n = 1.4+23.4*((90-fck)/100)**4
#Def_ec3
if fck < 50: #MPa
    Def_ec3 = 1.75 #/1000
else:
    Def_ec3 = 1.75+0.55*((fck-50)/40) #/1000
#Def_ecu3
if fck < 50: #MPa
    Def_ecu3 = 3.5 #/1000
else:
    Def_ecu3 = 2.6+35*((90-fck)/100)**4
alfa_ct = 1.0 #Nota Expressão (3.16)
fctd = alfa_ct*fctk_005/coef_seg_conc #Expressão (3.16) 
Ec = MElasticidade
#9.1.2------------------------------------AÇO------------------------------------------------------#
#PARAMETROS DE CALCULO ESTABELECIDOS PELA NORMA DE REFERENCIA
#Norma de referência: NPEN-1992
coef_seg_aço = 1.15 #Item 2.4.2.4
fyk = 500 #Dado de projeto(escolhido Aço A500) #MPa
fyd = fyk/coef_seg_aço #Figura 3.8
PesoEsp_aço= 7850 #Item 3.2.7 (3) #kg/m3
Es = 200  #Item 3.2.7 (4) #GPa
Def_eyd = fyd/Es #Item 5.8.8.3
Def_es = Def_ec2 #Item 6.1 (5) #Limite imposto inicialmente, dependendo da situação muda (Compatibilidade da deformação)
#9.2-------------------------------------Verificação ULS-----------------------------------------------------#
#9.2.1-------------------------------------Armaduras Longitudinais-----------------------------------------------------#
#CALCULO BASEADO NO DIAGRAMA RETANGULAR DE TENSÕES
#NPEN1992 Item 3.1.7 (3)
if fck <= 50: #MPa
    lambda_conc = 0.8
    eta_conc = 1
elif fck <= 90: #MPa
    lambda_conc = 0.8 - (fkc - 50)/400
    eta_conc = 1 - (fck - 50)/200
else:
    print("Distribuição retangular de tensões pela NPEN1992 (Eurocódigo 2) não suportado, reduza o fck")
    exit()
####.2.1.1-------------------------------------Informações de entrada-----------------------------------------------------#
#ESCOLHIDO O MÍNIMO DE 10mm PARA BARRAS LONGITUDINAIS E MÁXIMO DE 20mm
list_d_aço = [6, 8, 10, 12, 16, 20, 25, 32, 40] #mm
range_d_long = range(list_d_aço.index(10), list_d_aço.index(20) + 1) #Minimo 10mm, max 20mm
h = Altura_barras_selection #m
b = Base_barras_selection #m
#Item 8.2 (NPEN1992) {ESPAÇAMENTO ENTRE AS BARRAS}
#Admitindo que dg + k2 é inferior às outras parcelas
s_k1 = 1 #Item 8.2(2) NOTA #mm
s_k2 = 5 #Item 8.2(2) NOTA #mm
recob_min = 10 #Vida util de 50 anos(classe estrutural 4) #mm
recob_nom = 20 #mm
recob = recob_min
#9.2.1.2-------------------------------------Funções de cálculo-----------------------------------------------------#
#Função que retorna o dimensionamento para barra, ponto e esforço (retorna para a combinação mais desfavorável no ponto)
#FUNÇÃO QUE RETORNA O EIXO NEUTRO CALCULADO TENDO A ALTURA UTIL E O MED
def fEixoNeutro(b, h, d, lambda_conc, eta_conc, fcd, Med): #(float, float, float, float, float, float, float) (m, m, m, adimensional, adimensional, kN/m2, kNm)
    #Variaveis que dependem da seçao e do material, nao irao variar se a seçao for constante e o material o mesmo
    konstant = b*lambda_conc*eta_conc*fcd
    #Eixo Neutro para Med positivo
    EixoNeutro1 = ((konstant*d) + np.sqrt((konstant*d)**2 - 4*(konstant*lambda_conc/2)*(abs(Med))))/(2*konstant*lambda_conc/2) #m
    EixoNeutro2 = ((konstant*d) - np.sqrt((konstant*d)**2 - 4*(konstant*lambda_conc/2)*(abs(Med))))/(2*konstant*lambda_conc/2) #m
    if EixoNeutro1 < 0:
        EixoNeutro = EixoNeutro2
    elif EixoNeutro2 < 0:
        EixoNeutro = EixoNeutro1
    else:
        EixoNeutro = min(EixoNeutro1, EixoNeutro2)
    return (EixoNeutro) #m
#FUNÇÃO QUE RETORNA O EIXO NEUTRO CALCULADO TENDO A ÁREA DE AÇO
def fEixoNeutroAs(b, lambda_conc, eta_conc, fcd, fyd, As): #(float, float, float, float, float, float) (m, adimensional, adimensional, kN/m2, kN/m2, cm2)
    As = As/10000 #m2
    EixoNeutro = As*fyd/(b*lambda_conc*eta_conc*fcd) #m
    return(EixoNeutro)
#FUNÇÃO QUE RETORNA A ÁREA A SER ADOTADA TENDO A LIMITAÇÃO DA AREA MINIMA E AREA MAXIMA TENDO O EIXO NEUTRO CALCULADO
def fAs_adotada (lambda_conc, eta_conc, b, EixoNeutro, fcd, fyd, As_min, As_max): #(float, float, float, float, float, float, float, float) (adimensional, adimensional, m, m, kN/m2, kN/m, cm2, cm2)
    #Calcula a área após ter o Eixo Neutro calculado
    As_calc = (lambda_conc*eta_conc*b*EixoNeutro*fcd/fyd) *10000 #cm2
    #Verificação das áreas mínima e máxima
    if As_calc < As_min:
        #print("Área menor que a área mínima, adotada área mínima")
        As_adotada = As_min
    else:
        As_adotada = As_calc
    if As_adotada > As_max:
        #print("Área ultrapassa área máxima, adotada área máxima")
        As_adotada = As_max
    else:
        pass
    return(As_adotada) #cm2
#FUNÇÃO QUE RETORNA A ALTURA UTIL PARA CAMADAS IGUALMENTE DISTRIBUIDAS (m, m, mm, mm, cm, mm, adimensional, adimensional, cm)
def fd_camadas(b, h, recob, d_estribo, s_adotado, d_long, n_barras, arredond_mm, s_min): #(float, float, float, float, float, float, int, float, float) (m, m, mm, mm, cm, mm, adimensional, adimensional, cm)
    s_camadas = s_min
    #Numero de barras por camada (Manipulaçao da equaçao que calcula o espaçamento)
    n_barras_camada = int((((b*1000) - 2*recob - 2*d_estribo) + (s_adotado*10))/((s_adotado*10) + d_long))
    #Número de camadas
    n_camadas = np.ceil(n_barras/n_barras_camada)
    #print("Número de camadas: %d" %n_camadas)
    #print("Numero de barras nas %d camadas: %d" %((n_camadas - 1),n_barras_camada ))
    #print("Espaçamento das %d camadas: %dcm" %((n_camadas - 1),s_adotado))
    #Numero de barras disponiveis para a ultima camada
    n_disp = n_barras - (n_camadas-1)*n_barras_camada
    n_barras_ultima_camada = n_disp
    #Verificação da necessidade de espaçar barras na ultima camada (existe espaçamento apenas se existirem pelo menos 2 barras)
    if n_barras_ultima_camada <= 1:
        s_ultima_camada = 0
    else:
        s_ultima_camada = ((b*1000)-2*recob-2*d_estribo - n_barras_ultima_camada*d_long)/(n_barras_ultima_camada - 1)/10
        s_ultima_camada = arredond_mm*int(s_ultima_camada*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
        #print("Espaçamento da ultima camada: %dcm" %s_ultima_camada)
    #RECALCULA A ALTURA UTIL (CRIA LISTAS PARA Yg, Area e Yg*Area para armazenar a cada interaçao os valores e no final apenas
    # utilizar a soma dos valores Yg*Area e Area para calcular o Yg total)
    list_Yg = []
    list_Areas = []
    list_Yg_Area = []
    Yg1 = recob + d_estribo + d_long/2
    Area_1 = n_barras_camada*np.pi*d_long**2/4
    Yg_Area = Yg1*Area_1
    list_Yg.append(Yg1)
    list_Areas.append(Area_1)
    list_Yg_Area.append(Yg_Area)
    #Calcula o centro de massa e a area para todas as camadas
    for j in range (1, int(n_camadas)-1):
        locals()[f"Yg{j+1}"]= eval(f"Yg{j}") + d_long/2 + s_camadas + d_long/2 #mm2
        locals()[f"Area_{j+1}"] = n_barras_camada*np.pi*d_long**2/4 #mm2
        list_Yg.append(eval(f"Yg{j+1}"))
        list_Areas.append(eval(f"Area_{j+1}")) #
        Yg_Area = eval(f"Yg{j+1}")*eval(f"Area_{j+1}") #mm3
        list_Yg_Area.append(Yg_Area)
    #Calcula o centro de massa e a area da ultima camada
    Yg_ultima_camada = eval("Yg%d" %(int(n_camadas)-1)) + d_long/2 + s_camadas + d_long/2 #mm
    Area_ultima_camada = n_barras_ultima_camada*np.pi*d_long**2/4 #mm2
    Yg_Area = Yg_ultima_camada*Area_ultima_camada #mm3
    list_Yg.append(Yg_ultima_camada)
    list_Areas.append(Area_ultima_camada)
    list_Yg_Area.append(Yg_Area)
    #Calcula o centro de massa total de todas as camadas
    Yg = sum(list_Yg_Area)/sum(list_Areas) #mm
    #Calcula a nova altura util
    d = h - Yg/1000 #m
    return(d)
#FUNÇÃO QUE RETORNA A ÁREA DE ARMADURA NECESSÁRIA PARA UM DADO MED
def As_Med(Barra, Ponto, Esforço, d, fcd, lambda_conc, eta_conc, h, s_k1, s_k2, Med, As_min, As_max, d_long, d_estribo): #(int, float, str, float, float, float, float, float, int, int, float, float, float, float, float)
    #               (adimensional, m, adimensional, mm, MPa, adimensional, adimensional, m, adimensional, adimensional, kNm, cm2, cm2, mm, mm)
    #Dicionario para armazenar as informações de cálculo
    dic_As_Med = {}
    d = d/1000 #m
    fcd = fcd*1000 #kN/m2
    #Cálculo do Eixo Neutro tendo a altura util (d) definida
    EixoNeutro = fEixoNeutro(b, h, d, lambda_conc, eta_conc, fcd, Med)
    fcd = fcd/1000 #MPa
    #Calcula a área para o Eixo Neutro calculado
    As_adotada = fAs_adotada (lambda_conc, eta_conc, b, EixoNeutro, fcd, fyd, As_min, As_max)
    #Calcula o numero de barras para a area calculada
    n_barras = np.ceil((As_adotada*100)*4/(np.pi*d_long**2))
    #print("Diâmetro: %dmm" %d_long)
    #print("Eixo Neutro: {:.3f}m" .format(EixoNeutro))
    #print("Área de armadura necessária: {:.3f}cm2".format(As_adotada))
    #Calcula a área para as barras reais
    As_real = n_barras*np.pi*(d_long/10)**2/4 #cm2
    #print("%dØ%d({:.2f}cm2)" .format(As_real) %(n_barras, d_long) )
    #ITEM 8.2 (2)
    if s_k1*d_long < 20: 
        s_min = 20 #mm
    else:
        s_min = s_k1*d_long #mm
        #print("Diâmetro: %dmm" %d_long)
    print("Espaçamento Mínimo: %dcm" %(s_min/10))
    dic_As_Med["s_min"] = s_min/10 #mm
    #Verificar se há espaçamento entre as barras (deve haver mais de 2 barras)
    if n_barras <=1:
        s_calc = 0
    else:
        s_calc = ((b*1000) - 2*recob - 2*d_estribo - n_barras*d_long)/(n_barras - 1)/10 #cm
        arredond_mm = 5 #arredondar para 5 em 5mm
        s_calc = arredond_mm*int(s_calc*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
        #print("Espaçamento calculado: %dcm" %s_calc)
        #Faz a verificação do espaçamento calculado com o mínimo
        if s_calc < (s_min/10):
            s_adotado = s_min/10 #cm
        else:
            s_adotado = s_calc #cm
        #Distância que verifica a disposição das armaduras numa unica linha, essa distância é o mínimo exigido de
        #de base da seção para que seja possível posicionar todas as barras na linha
        dist = (s_adotado*10)*(n_barras - 1) + 2*recob + 2*d_estribo + n_barras*d_long
        #Admite que não existem mais camadas de armaduras (linhas)
        camadas = False
        #Faz a verificação da distância com a dimensão real da peça
        while dist > (b*1000):
            #Necessária mais de uma camada de armaduras
            camadas = True
            #print("Necessária mais uma camada de armaduras")
            #Cálcula a nova altura útil para mais que uma camada, ja retorna o numero de camadas necessarios
            d = fd_camadas(b, h, recob, d_estribo, s_adotado, d_long, n_barras, arredond_mm, s_min) #mm
            fcd = fcd*1000 #kN/m2
            #Recalcula o eixo neutro para a altura util dada
            EixoNeutro = fEixoNeutro(b, h, d, lambda_conc, eta_conc, fcd, Med) #m
            fcd = fcd/1000 #MPa
            #Recalcula a Área a ser adotada para o novo Eixo Neutro
            As_adotada = fAs_adotada (lambda_conc, eta_conc, b, EixoNeutro, fcd, fyd, As_min, As_max)
            #Recalcula o número de barras
            n_barras = np.ceil((As_adotada*100)*4/(np.pi*d_long**2))
            d = fd_camadas(b, h, recob, d_estribo, s_adotado, d_long, n_barras, arredond_mm, s_min) #mm
            #Recalcula a Área real
            As_real = n_barras*np.pi*(d_long/10)**2/4 #cm2
            #Recalcula o espaçamento 
            s_calc = ((b*1000) - 2*recob - 2*d_estribo - n_barras*d_long)/(n_barras - 1)/10 #cm
            arredond_mm = 5 #arredondar para 5 em 5mm
            s_calc = arredond_mm*int(s_calc*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
            if s_calc < (s_min/10):
                s_adotado = s_min/10 #cm
            else:
                s_adotado = s_calc #cm
            s_camadas = s_min #mm
            #Recalcula o numero de barras por camada
            n_barras_camada = int((((b*1000) - 2*recob - 2*d_estribo) + (s_adotado*10))/((s_adotado*10) + d_long))
            #Recalcula o numero de camadas
            n_camadas = np.ceil(n_barras/n_barras_camada)
            #Recalcula o numero de barras disponiveis para a ultima camada
            n_disp = n_barras - (n_camadas-1)*n_barras_camada
            n_barras_ultima_camada = n_disp
            #Verifica se existe espaçamento (min 2 barras)

            
            if n_barras_ultima_camada <= 1:
                s_ultima_camada = 0
            else:
                #Recalcula o espaçamento na ultima camada
                s_ultima_camada = ((b*1000)-2*recob-2*d_estribo - n_barras_ultima_camada*d_long)/(n_barras_ultima_camada - 1)/10
                s_ultima_camada = arredond_mm*int(s_ultima_camada*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
            #Recalcula a dist
            dist = (s_camadas)*(n_barras_camada - 1) + 2*recob + 2*d_estribo + n_barras_camada*d_long
            #print(dist)
        EixoNeutro = fEixoNeutroAs(b, lambda_conc, eta_conc, fcd, fyd, As_real)
        Mrd = b*lambda_conc*EixoNeutro*eta_conc*fcd*(d-(lambda_conc*EixoNeutro/2))*10**3
        while abs(Mrd) < abs(Med):
            n_barras = n_barras + 1
            As_real = n_barras*np.pi*(d_long/10)**2/4 #cm2
            if n_barras <=1:
                s_calc = 0
            else:
                s_calc = ((b*1000) - 2*recob - 2*d_estribo - n_barras*d_long)/(n_barras - 1)/10 #cm
                arredond_mm = 5 #arredondar para 5 em 5mm
                s_calc = arredond_mm*int(s_calc*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
                #print("Espaçamento calculado: %dcm" %s_calc)
                #Faz a verificação do espaçamento calculado com o mínimo
                if s_calc < (s_min/10):
                    s_adotado = s_min/10 #cm
                else:
                    s_adotado = s_calc #cm
                #Distância que verifica a disposição das armaduras numa unica linha, essa distância é o mínimo exigido de
                #de base da seção para que seja possível posicionar todas as barras na linha
                dist = (s_adotado*10)*(n_barras - 1) + 2*recob + 2*d_estribo + n_barras*d_long
                #Admite que não existem mais camadas de armaduras (linhas)
                camadas = False
                #Faz a verificação da distância com a dimensão real da peça
                while dist > (b*1000):
                    #Necessária mais de uma camada de armaduras
                    camadas = True
                    #print("Necessária mais uma camada de armaduras")
                    #Cálcula a nova altura útil para mais que uma camada, ja retorna o numero de camadas necessarios
                    d = fd_camadas(b, h, recob, d_estribo, s_adotado, d_long, n_barras, arredond_mm, s_min) #mm
                    fcd = fcd*1000 #kN/m2
                    #Recalcula o eixo neutro para a altura util dada
                    EixoNeutro = fEixoNeutro(b, h, d, lambda_conc, eta_conc, fcd, Med) #m
                    fcd = fcd/1000 #MPa
                    #Recalcula a Área a ser adotada para o novo Eixo Neutro
                    As_adotada = fAs_adotada (lambda_conc, eta_conc, b, EixoNeutro, fcd, fyd, As_min, As_max)
                    #Recalcula o número de barras
                    n_barras = np.ceil((As_adotada*100)*4/(np.pi*d_long**2))
                    d = fd_camadas(b, h, recob, d_estribo, s_adotado, d_long, n_barras, arredond_mm, s_min) #mm
                    #Recalcula a Área real
                    As_real = n_barras*np.pi*(d_long/10)**2/4 #cm2
                    #Recalcula o espaçamento 
                    s_calc = ((b*1000) - 2*recob - 2*d_estribo - n_barras*d_long)/(n_barras - 1)/10 #cm
                    arredond_mm = 5 #arredondar para 5 em 5mm
                    s_calc = arredond_mm*int(s_calc*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
                    if s_calc < (s_min/10):
                        s_adotado = s_min/10 #cm
                    else:
                        s_adotado = s_calc #cm
                    s_camadas = s_min #mm
                    #Recalcula o numero de barras por camada
                    n_barras_camada = int((((b*1000) - 2*recob - 2*d_estribo) + (s_adotado*10))/((s_adotado*10) + d_long))
                    #Recalcula o numero de camadas
                    n_camadas = np.ceil(n_barras/n_barras_camada)
                    #Recalcula o numero de barras disponiveis para a ultima camada
                    n_disp = n_barras - (n_camadas-1)*n_barras_camada
                    n_barras_ultima_camada = n_disp
                    #Verifica se existe espaçamento (min 2 barras)
                    if n_barras_ultima_camada <= 1:
                        s_ultima_camada = 0
                    else:
                        #Recalcula o espaçamento na ultima camada
                        s_ultima_camada = ((b*1000)-2*recob-2*d_estribo - n_barras_ultima_camada*d_long)/(n_barras_ultima_camada - 1)/10
                        s_ultima_camada = arredond_mm*int(s_ultima_camada*10/arredond_mm)/10 #Arredonda para um inteiro menor próximo de 5mm #cm
                    #Recalcula a dist
                    dist = (s_camadas)*(n_barras_camada - 1) + 2*recob + 2*d_estribo + n_barras_camada*d_long
                    #print(dist)
            Mrd = b*lambda_conc*EixoNeutro*eta_conc*fcd*(d-(lambda_conc*EixoNeutro/2))*10**3     
        #Armazena as informaçoes de calculo no objeto sob formato de dicionario
        if camadas == True:
            print("Número de camadas: %d" %n_camadas)
            print("Numero de barras nas %d camadas: %d" %((n_camadas - 1),n_barras_camada ))
            print("Espaçamento das %d camadas: %dcm" %((n_camadas - 1),s_adotado))
            print("Número de barras na ultima camada: %d" %n_barras_ultima_camada)
            print("Espaçamento da ultima camada: %dcm" %s_ultima_camada)
            dic_As_Med["n_camadas"] = n_camadas
            dic_As_Med["n_barras_camada"] = n_barras_camada
            dic_As_Med["s_adotado"] = s_adotado
            dic_As_Med["s_ultima_camada"] =s_ultima_camada
            dic_As_Med["n_barras_ultima_camada"] = n_barras_ultima_camada
            del s_camadas; del n_barras_camada
        else:
            print("Espaçamento calculado: {:.2f}cm" .format(s_calc))
            dic_As_Med["s_calc"] = s_calc
            pass
    Mrd = b*lambda_conc*EixoNeutro*eta_conc*fcd*(d-(lambda_conc*EixoNeutro/2))*10**3  
    As_calc = (lambda_conc*eta_conc*b*EixoNeutro*fcd/fyd) *10000 #cm2
    As_dif = (As_real - As_adotada)
    print("Eixo Neutro: {:.3f}m" .format(EixoNeutro))
    print("Área de armadura necessária: {:.3f}cm2".format(As_adotada))
    print("%dØ%d({:.2f}cm2)" .format(As_real) %(n_barras, d_long) )
    print("Área residual: {:.2f}cm2\n".format(As_dif))
    dic_As_Med["d_long"] = d_long
    dic_As_Med["n_barras"] = n_barras
    dic_As_Med["Mrd"] = Mrd
    dic_As_Med["EixoNeutro"] = EixoNeutro
    dic_As_Med["As_adotada"] = As_adotada
    dic_As_Med["As_real"] = As_real
    dic_As_Med["text_dim"] = ("%dØ%d({:.2f}cm2)" .format(As_real) %(n_barras, d_long))
    dic_As_Med["As_dif"] = As_dif
    dic_As_Med["Altura_Util"] = d
    return(dic_As_Med)
#FUNÇÃO QUE DIMENSIONA A ARMADURA PARA UM DADO MED, DIAMETRO DE ESTRIBO E DIAMETRO LONGITUDINAL
def fd_long(d_estribo, recob, fctm, fyk, b, h, Point, Med, Barra, d_long): #(float, float, float, float, float, float, float, float, float, float) (mm, mm, MPa, MPa, MPa, m, m, m, kNm, adimensional, mm)
    bt = b #m#CONTINUAR PG 109 EB2, 154 EC2
    dic_arm_long = {}
    #Cria objeto para armazenar as informaçoes de dimensionamento
    globals()[f"d_long_{d_long}"] = DimULS_d_long() 
    #Calcula altura util inicial
    d = (h*1000) - recob - d_estribo - (d_long/2) #mm
    #Cálcula a área mínima e máxima
    As_min = 0.26*(fctm/fyk)*(bt*10)*d #item 9.2.1.1 Expressão (9.1N) #cm2
    if As_min >= 0.0013*bt*d*10:
        pass
    else:
        As_min = 0.0013*bt*d*10 #cm2
    Ac = b*h*10**4 #cm2
    As_max = 0.04*Ac #Item 9.2.1.1 (NOTA) #cm2
    #Classe de exposição X0
    ####.2.1.3-------------------------------------DIM SEÇÃO MEIO VÃO BARRA 1-----------------------------------------------------#
    dic = eval(f"d_long_{d_long}")
    dic.PontoMPositivo = Point
    dic.dic_As_Med = As_Med(Barra, Point, "My", d, fcd, lambda_conc, eta_conc,
        h, s_k1, s_k2, Med, As_min, As_max, d_long, d_estribo)
    dic.As_adotada = dic.dic_As_Med["As_adotada"]
    dic.EixoNeutro = dic.dic_As_Med["EixoNeutro"]
    dic.s_min = dic.dic_As_Med["s_min"]
    if "s_calc" in dic.dic_As_Med.keys():
        dic.s_calc = dic.dic_As_Med["s_calc"]
    if "n_camadas" in dic.dic_As_Med.keys():
        dic.n_camadas = dic.dic_As_Med["n_camadas"]
    if "n_barras_camada" in dic.dic_As_Med.keys():
        dic.n_barras_camada = dic.dic_As_Med["n_barras_camada"]
    if "s_adotado" in dic.dic_As_Med.keys():
        dic.s_adotado = dic.dic_As_Med["s_adotado"]
    if "s_ultima_camada" in dic.dic_As_Med.keys():
        dic.s_ultima_camada = dic.dic_As_Med["s_ultima_camada"]
    if "n_barras_ultima_camada" in dic.dic_As_Med.keys():
        dic.n_barras_ultima_camada = dic.dic_As_Med["n_barras_ultima_camada"]
    if "Altura_Util" in dic.dic_As_Med.keys():
        dic.Altura_Util = dic.dic_As_Med["Altura_Util"]
    if "As_real" in dic.dic_As_Med.keys():
        dic.As_real = dic.dic_As_Med["As_real"]
    if "n_barras" in dic.dic_As_Med.keys():
        dic.n_barras = dic.dic_As_Med["n_barras"]
    if "Mrd" in dic.dic_As_Med.keys():
        dic.Mrd = dic.dic_As_Med["Mrd"]
    if "d_long" in dic.dic_As_Med.keys():
        dic.d_long = dic.dic_As_Med["d_long"]
    dic.text_dim = dic.dic_As_Med["text_dim"]
    dic.As_dif = dic.dic_As_Med["As_dif"]
    return(dic) 
#9.2.1.3-------------------------------------Classes para criação dos objetos-----------------------------------------------------#
#Classe para objetos onde serao armazenadas as informaçoes de dimensionamento ULS d_long
class DimULS_d_long():
    pass
#Classe para objetos onde serao armazenadas as informaçoes de todos os dimensionamentos para as barras
class DimULS_Med():
    def __init__(self, d_estribo, Point, Med, Barra):
    # self.d_long = d_long
        self.d_estribo = d_estribo
        self.Point = Point
        self.Med = Med
        self.Barra = Barra
    def fDimensionamento(self, d_long):    
        #locals()[f"d_long_{d_long}"] = fd_long(d_estribo, recob, fctm, fyk, b, h, Point, Med, Barra, d_long) 
        return(fd_long(d_estribo, recob, fctm, fyk, b, h, Point, Med, Barra, d_long))
class DimULS():
    pass
#9.2.1.4-------------------------------------Dimensionamento-----------------------------------------------------#
#Cria objetos com informaçoes de dimensionamento para as barras da seleção
j2 = 1
for j in range(1, current_selection.Count + 1):
    #-----------DIMENSIONAMENTO POR VALOR MÁXIMO NA BARRA
    #Pega o numero da barra na seleção
    while current_selection.Contains(j) == False:
        j2 += 1
    else: 
        pass
    print(f"Barra{j2}: ")
    #ADOTADO ESTRIBOS DE 8mm
    d_estribo = list_d_aço[1]
    #Pega MedMaximo(positivo)
    Lista_Pontos = eval("p_%d" %j2)
    Med = MaxEsfValue(j2,"My",Lista_Pontos)
    #Pega o ponto onde ocorre o valor maximo
    Lista_Pontos = eval("p_%d" %j2)
    Point = round(MaxEsfPoint(j2, "My", Lista_Pontos), 2)
    Barra = j2
    Length = IRobotBar(bars.Get(Barra)).Length
    #Cria um objeto para armazenar dados do Momento positivo
    MedPositivo = DimULS_Med(d_estribo, Point, Med, Barra)
    #Cria um dicionario para armazenar os objetos do dimensionamento variando diametros longitudinais
    dic_obj_fDimensionamento = {}
    #ADOTANDO O MINIMO DE 10mm PARA O DIAMETRO LONGITUDINAL E O MAXIMO DE 20mm
    print(f"\nMomento positivo ({Med}kNm)\n")
    for i in range_d_long:
        d_long = list_d_aço[i]
        #Armazena os valores do dimensionamento de todos os diametros longitudinais no dicionario
        dic_obj_fDimensionamento[("d_long_%d" %d_long)] = MedPositivo.fDimensionamento(d_long)
    #Adiciona o dicionario ao objeto do Med 
    MedPositivo.DimensionamentoLong = dic_obj_fDimensionamento





    #----------DIMENSIONAMENTO POR VALOR NOS NÓS

    #Nós barra em questão e barra adjacente
    Node1 = IRobotBar(bars.Get(j2)).StartNode
    Node2 = IRobotBar(bars.Get(j2)).EndNode
    #Valores MY no inicio e fim da barra (cada barra começa no seu StartNode e termina em seu EndNode)
        #OBS: Não há como fazer o dimensionamento acessando o valor nos nós pois é diferente
    End_Bar = IRobotBar(bars.Get(Barra)).Length
    Value_Start = round(MinEsf_Point_MY(Barra,0,Length,listcomb,force_serv), 2)
    Value_End = round(MinEsf_Point_MY(Barra,End_Bar,Length,listcomb,force_serv), 2)
    #Cria um objeto com atributos de interesse ao caso em questão
    MedNegativo = DimULS_Med(d_estribo, Point, Med, Barra)
    MedNegativo.__delattr__("Med")
    MedNegativo.__delattr__("d_estribo")
    MedNegativo.__delattr__("Point")
    #MedNegativo.__delattr__("Barra")
    if Value_Start < 0:
        Med = Value_Start
        Point = 0
        #Cria um dicionario para armazenar os objetos do dimensionamento variando diametros longitudinais
        dic_obj_fDimensionamento = {}
        print(f"\nMomento negativo no inicio ({Med}kNm)\n")
        for i in range_d_long:
            d_long = list_d_aço[i]
            dic_obj_fDimensionamento[("d_long_%d" %d_long)] = MedNegativo.fDimensionamento(d_long)        
            #list_obj_fDimensionamento.append(eval(f"Barra_{j}_MedNegativo").fDimensionamento(d_long))
        MedNegativo.StartNode = DimULS()
        MedNegativo.StartNode.DimensionamentoLong = dic_obj_fDimensionamento
        MedNegativo.StartNode.Node = Node1
        MedNegativo.StartNode.Med = Med

    if Value_End < 0:
        Med = Value_End
        Point = IRobotBar(bars.Get(j2)).Length
        #Cria um dicionario para armazenar os objetos do dimensionamento variando diametros longitudinais
        dic_obj_fDimensionamento = {}   
        print(f"\nMomento negativo no final ({Med}kNm)\n")
        for i in range_d_long:
            d_long = list_d_aço[i] 
            dic_obj_fDimensionamento[("d_long_%d" %d_long)] = MedNegativo.fDimensionamento(d_long)        
            #list_obj_fDimensionamento.append(eval(f"Barra_{j}_MedNegativo").fDimensionamento(d_long))
        MedNegativo.EndNode = DimULS()
        MedNegativo.EndNode.DimensionamentoLong = dic_obj_fDimensionamento
        MedNegativo.EndNode.Node = Node2
        MedNegativo.EndNode.Med = Med
    locals()[f"Barra_{j2}_ULS"] = DimULS()
    eval(f"Barra_{j2}_ULS").Med_Positivo = MedPositivo
    eval(f"Barra_{j2}_ULS").Med_Negativo = MedNegativo
    j2 += 1
#Modifica o dimensionamento atendendo o critério de compatibilidade entre o final de uma barra e o inicio de outra
for i in range(len(list_bars) - 1):
    #Pega atributos da barra em estudo e da barra adjacente para analizar suas relações
    j2 = list_bars[i]
    lista_barras_conectadas = []
    #Range que pega todas as outras barras
    for k in range(len(list_bars)):
        i2 = list_bars[k]
        Length_Bar_1 = IRobotBar(bars.Get(j2)).Length
        Length_Bar_2 = IRobotBar(bars.Get(i2)).Length
        Node_Bar_1 = eval(f"Barra_{j2}_ULS").Med_Negativo.EndNode.Node
        Node_Bar_2 = eval(f"Barra_{i2}_ULS").Med_Negativo.StartNode.Node
        #Verifica se as barras anteriores estao conectadas na mesma
        if i >= 1:    
            for k2 in range(i,len(list_bars)):
                x = eval(f"Barra_{list_bars[i-1]}_ULS").Barras_conectadas
                if (k2 in x != False):
                    if lista_barras_conectadas.__contains__(k2) != True:
                        lista_barras_conectadas.append(k2)
        #Verifica se o ponto onde ocorre o momento em analise esta localizado no inicio ou no final da barra
        if Node_Bar_1 == Node_Bar_2:
            print("Compatibilização de dimensionamento dos elementos de barra %d e %d"%(j2,i2))
            Med_Node_1 = eval(f"Barra_{j2}_ULS").Med_Negativo.EndNode.Med
            Med_Node_2 = eval(f"Barra_{i2}_ULS").Med_Negativo.StartNode.Med
            New_Med_Neg = min(Med_Node_1,Med_Node_2)
            lista_barras_conectadas.append(i2)
                #Cria um objeto com atributos de interesse ao caso em questão
            if eval(f"Barra_{j2}_ULS").Med_Negativo.EndNode.Med != New_Med_Neg:
                print("Modificação do dimensionamento do elemento de barra %d"%j2)
                Med = New_Med_Neg
                print(f"\nMomento negativo no final ({Med}kNm)\n")
                Point = IRobotBar(bars.Get(j2)).Length 
                #Cria um dicionario para armazenar os objetos do dimensionamento variando diametros longitudinais
                dic_obj_fDimensionamento = {}
                for i3 in range_d_long:
                    d_long = list_d_aço[i3] 
                    dic_obj_fDimensionamento[("d_long_%d" %d_long)] = MedNegativo.fDimensionamento(d_long)        
                eval(f"Barra_{j2}_ULS").Med_Negativo.EndNode.DimensionamentoLong = dic_obj_fDimensionamento
                eval(f"Barra_{j2}_ULS").Med_Negativo.EndNode.Med = Med
            if eval(f"Barra_{i2}_ULS").Med_Negativo.StartNode.Med != New_Med_Neg:
                print("Modificação do dimensionamento do elemento de barra %d"%i2)
                Med = New_Med_Neg
                print(f"\nMomento negativo no inicio ({Med}kNm)\n")
                Point = 0
                #Cria um dicionario para armazenar os objetos do dimensionamento variando diametros longitudinais
                dic_obj_fDimensionamento = {}
                for i3 in range_d_long:
                    d_long = list_d_aço[i3] 
                    dic_obj_fDimensionamento[("d_long_%d" %d_long)] = MedNegativo.fDimensionamento(d_long)    
                eval(f"Barra_{i2}_ULS").Med_Negativo.StartNode.DimensionamentoLong = dic_obj_fDimensionamento
                eval(f"Barra_{i2}_ULS").Med_Negativo.StartNode.Med = Med
    eval(f"Barra_{j2}_ULS").Barras_conectadas = lista_barras_conectadas
#Descartando dimensionamentos com mais de 1 camada
for i in range(1, current_selection.Count + 1):
    Barra = eval(f"Barra_{i}_ULS")
    MedPositivo = Barra.Med_Positivo
    MedNegativo_1 = Barra.Med_Negativo.StartNode
    MedNegativo_2 = Barra.Med_Negativo.EndNode

    dicdim1 = {}
    dicdim2 = {}
    dicdim3 = {}
    dicAs1 = {}
    dicAs2 = {}
    dicAs3 = {}
    #Pega e armazena os valores de dimensionamento que não contém mais de 1 camada de barras
    for j in range_d_long:

        ref = list_d_aço[j]
        x1 = MedPositivo.DimensionamentoLong[f"d_long_{ref}"]
        x2 = MedNegativo_1.DimensionamentoLong[f"d_long_{ref}"]
        x3 = MedNegativo_2.DimensionamentoLong[f"d_long_{ref}"]
        if not hasattr(x1,"n_camadas") == True:
            dicdim1[f"d_long{ref}"] = x1
            dicAs1[f"d_long{ref}"] = x1.As_dif
        if not hasattr(x2,"n_camadas") == True:
            dicdim2[f"d_long{ref}"] = x2
            dicAs2[f"d_long{ref}"] = x2.As_dif
        if not hasattr(x3,"n_camadas") == True:
            dicdim3[f"d_long{ref}"] = x3
            dicAs3[f"d_long{ref}"] = x3.As_dif
    MedPositivo.listdim = dicdim1
    MedPositivo.ArmLong = dicdim1[min(dicAs1)]
    MedNegativo_1.listdim = dicdim2
    MedNegativo_1.ArmLong = dicdim2[min(dicAs2)]
    MedNegativo_2.listdim = dicdim3
    MedNegativo_2.ArmLong = dicdim3[min(dicAs3)]
#9.2.1.4-------------------------------------Funções auxiliares-----------------------------------------------------#
#FUNÇÃO QUE CALCULA O MRD TENDO UMA ÁREA DE ARMADURA
def CalcMrd(As, b, eta_conc, lambda_conc, fcd, fyd, d): #(float, float, float, float, float, float, float) (cm, m, adimensional, adimensional, MPa, MPa, m)
    EixoNeutro = fEixoNeutroAs(b, lambda_conc, eta_conc, fcd, fyd, As) #m
    Mrd = b*lambda_conc*EixoNeutro*eta_conc*(fcd*10**3)*(d-(EixoNeutro*lambda_conc/2))
    return(Mrd)
#9.2.2-------------------------------------Disposições Construtivas-----------------------------------------------------#
#Função que retorna os pontos onde há a troca de sinais
def change_signal(Barra, Esforço):
    
    listenvolv = []
    Lista_Pontos = eval(f"p_{Barra}")
    #Loop para realizar a envolvente das combinações
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))   
    del listprov; del prov
    vigaplot = listenvolv
    
    list_ponto_troca = []
    ind = 0
    vigaplot_temp = []
    lista_temp = []
    last_signal = vigaplot[0]
    #Loop para criar a lista com os pontos onde ocorre a troca de sinal
    for v in vigaplot:
        if (last_signal > 0 and v < 0) or (last_signal < 0 and v > 0):
           list_ponto_troca.append([vigaplot.index(last_signal), vigaplot.index(v)])
           vigaplot_temp = []
           lista_temLisp = []

        vigaplot_temp.append(v)
        lista_temp.append(Lista_Pontos[ind])
        last_signal = v
        ind = ind + 1
    return(list_ponto_troca)
#NPEN1992 Item 9.2.1.4 (2)
cot_ang_teta = 2.5 #Item 6.2.3 (2): 1<=cotg(ang_teta)<=2,5
cot_ang_alfa = 0 #Estribos posicionados perpendicularmente ao eixo da viga
#Classe para objetos de dispensa
class dispensa():
    pass
#Função que calcula o lbd para momentos positivos
def calc_lbd_Pos(Barra, Apoio):
    x = eval(f"Barra_{list_bars[i]}_ULS.Med_Positivo.ArmLong")
    #Calculo do alfa 1
    #NPEN-1992 - Figura 8.3
    a = x.s_calc #cm
    c1 = recob/10 #cm
    c = c1 #cm
    cd = min(a/2, c1, c)
    #NPEN-1992 - Quadro 8.2 
    if  cd > 3*x.d_long/10: #cm
        alfa_1 = 0.7
    else:
        alfa_1 = 1
    alfa_2 = 1 - 0.15*(cd*10-3*x.d_long)/(x.d_long) 
    if alfa_2 < 0.7:
        alfa_2 = 0.7
    elif alfa_2 > 1:
        alfa_2 = 1
    alfa_3 = 1 #admitindo caso desfavoravel
    alfa_4 = 1 #nao existem armaduras transversais soldadas
    Lista_Pontos = eval("p_%d" %Barra)
    R_apoio = MaxEsfValue(Barra,"Fz",Lista_Pontos) #kN
    A_apoio = height(Apoio) * width(Apoio)
    p = R_apoio/(A_apoio*10**3) #MPa
    alfa_5 = 1 - 0.04*p    
    if alfa_5 < 0.7:
        alfa_5 = 0.7
    elif alfa_5 > 1:
        alfa_5 = 1
    #CALCULANDO Lb,req
    eta_1 = 1 #Condições de boa aderência
    if x.d_long <= 32:
        eta_2 = 1
    else:
        eta_2 = (132 - x.d_long)/100
    fbd = 2.25*eta_1*eta_2*fctd #MPa #Item 8.4.2 (2) Equação (8.2)
    lb_req = (x.d_long/1000)*(fyd)/(4*fbd) #m #Item 8.4.3 (2) Equação (8.3)
    lbd = alfa_1*alfa_2*alfa_3*alfa_4*alfa_5*lb_req  #Item 8.4.4 (1)
    lb_min = max(0.3*lb_req, 10*x.d_long/1000, 0.01)
    if lbd < lb_min:
        lbd = lb_min
    return(lbd)
#Função que calcula o lbd para momentos negativos
def calc_lbd_Neg(Barra, Apoio):
    y = eval(f"Barra_{list_bars[i]}_ULS.Med_Negativo")
    #if Node == y.EndNode.Node:
    #    x = y.EndNode.ArmLong
    #else:
    #    x = y.StartNode.ArmLong
    #Calculo do alfa 1
    #NPEN-1992 - Figura 8.3
    a = x.s_calc #cm
    c1 = recob/10 #cm
    c = c1 #cm
    cd = min(a/2, c1, c)
    #NPEN-1992 - Quadro 8.2 
    if  cd > 3*x.d_long/10: #cm
        alfa_1 = 0.7
    else:
        alfa_1 = 1
    alfa_2 = 1 - 0.15*(cd*10-3*x.d_long)/(x.d_long) 
    if alfa_2 < 0.7:
        alfa_2 = 0.7
    elif alfa_2 > 1:
        alfa_2 = 1
    alfa_3 = 1 #admitindo caso desfavoravel
    alfa_4 = 1 #nao existem armaduras transversais soldadas
    Lista_Pontos = eval("p_%d" %Barra)
    R_apoio = MaxEsfValue(Barra,"Fz",Lista_Pontos) #kN
    A_apoio = height(Apoio) * width(Apoio)
    p = R_apoio/(A_apoio*10**3) #MPa
    alfa_5 = 1 - 0.04*p    
    if alfa_5 < 0.7:
        alfa_5 = 0.7
    elif alfa_5 > 1:
        alfa_5 = 1
    #CALCULANDO Lb,req
    eta_1 = 1 #Condições de boa aderência
    if x.d_long <= 32:
        eta_2 = 1
    else:
        eta_2 = (132 - x.d_long)/100
    fbd = 2.25*eta_1*eta_2*fctd #MPa #Item 8.4.2 (2) Equação (8.2)
    lb_req = (x.d_long/1000)*(fyd)/(4*fbd) #m #Item 8.4.3 (2) Equação (8.3)
    lbd = alfa_1*alfa_2*alfa_3*alfa_4*alfa_5*lb_req  #Item 8.4.4 (1)
    lb_min = max(0.3*lb_req, 10*x.d_long/1000, 0.01)
    if lbd < lb_min:
        lbd = lb_min
    return(lbd)
#Função que retorna a lista de armaduras que podem ser dispensadas, obedecendo o critério de simetria de dispensas na seção transversal
def lista_dispensa(TotalBars):
    #Lista de dispensas
    lista_dispensa = []
    #Verificação se o número de barras é par ou impar (Altera a lista de barras que podem ser dispensadas)
    if TotalBars %2 == 0:
        lista_dispensa = [2]
        i2 = 0
        for k in range(2, TotalBars - 2):
        #Adicionando barras pares na lista
            if k % 2 == 0:
                lista_dispensa.append(k + lista_dispensa[i2])
    else:
        lista_dispensa = [1]
        i2 = 0
        for k in range(1, TotalBars - 1):
        #Adicionando barras pares na lista
            if k % 2 == 0:
                lista_dispensa.append(k + lista_dispensa[i2])
    return(lista_dispensa)
#Função que calcula o comprimento de dispensa assim como os pontos onde vai ser dispensada a armadura 
def dispensa_positiva(Limite, precisão, Barra, Mrd, ObjDispensa, Length, cot_ang_teta, cot_ang_alfa, x, list_Med_Antes, list_Med_Depois, lbd):
    #-------------------------------------VALORES ANTES DO LIMITE-----------------------------------------------------#
    #Pega o valor mais proximo do Mrd como MedListAntes
    MedListAntes = min(list_Med_Antes, key = lambda x:abs(x-Mrd))
    #Loop pra pegar o valor mais próximo que não seja maior que o Mrd
    i = 0
    while Mrd < MedListAntes:
        MedListAntes = min(list_Med_Antes, key = lambda x:abs(x-(Mrd - i)))
        i += 1
    #Pega o index da lista e converte para o ponto real da barra com 1 casa de precisão decimal
    PontoAntes = round(list_Med_Antes.index(MedListAntes)*precisão, 1)
    #ADICIONA A PARTE TRANSLADADA DO DIAGRAMA
    z = 0.9*x.Altura_Util #m #ITEM 6.2.3 (1)
    al = round(z*((cot_ang_teta) - (cot_ang_alfa)/2), 2) #m #ITEM 9.2.1.3 (2) 
    #Adiciona as informações antes do ponto Limite ao objeto de dispensa
    ObjDispensa.al = round(al, 2)
    ObjDispensa.lbd = round(lbd, 2)
    ObjDispensa.Mrd = round(Mrd, 2)
    if round(PontoAntes, 2) < 0:
        ObjDispensa.PontoEsquerda = 0
    else:
        ObjDispensa.PontoEsquerda = round(PontoAntes, 2)
    ObjDispensa.PontoEsquerda_al_lbd = ObjDispensa.PontoEsquerda - round(al + lbd, 2)
    ObjDispensa.MedEsquerda = MedListAntes
    #-------------------------------------VALORES DEPOIS DO LIMITE-----------------------------------------------------#
    #Cria uma lista de valores máximos a partir do ponto de valor maximo da barra (ponto Limite) até o final
    #Pega o valor mais proximo do Mrd como MedListDepois
    MedListDepois = min(list_Med_Depois, key = lambda x:abs(x-Mrd))
    #Loop pra pegar o valor mais próximo que não seja maior que o Mrd
    i = 0
    while Mrd < MedListDepois:
        MedListDepois = min(list_Med_Depois, key = lambda x:abs(x-(Mrd - i)))
        i += 1
    #Pega o index da lista e converte para o ponto real da barra com 1 casa de precisão decimal
    PontoDepois = (len(list_Med_Antes))*precisão + round((list_Med_Depois.index(MedListDepois)-1)*precisão,1)
    #Adiciona as informações antes do ponto Limite ao objeto de dispensa
    if round(PontoDepois, 2) > Length:
        ObjDispensa.PontoDireita = Length
    else:
        ObjDispensa.PontoDireita = round(PontoDepois, 2)
    ObjDispensa.PontoDireita_al_lbd = ObjDispensa.PontoDireita + round(al + lbd, 2)
    ObjDispensa.MedDireita = MedListDepois
    ObjDispensa.Comprimento = round(abs(ObjDispensa.PontoDireita_al_lbd - ObjDispensa.PontoEsquerda_al_lbd),2)
    ObjDispensa.MedListAntes = list_Med_Antes
    ObjDispensa.MedListDepois = list_Med_Depois
#Função que calcula o comprimento de dispensa assim como os pontos onde vai ser dispensada a armadura 
def dispensa_negativa(LimiteInf, LimiteSup, precisão, Barra, Mrd, ObjDispensa, Length, cot_ang_teta, cot_ang_alfa, x, list_Med, lbd):
    #-------------------------------------VALORES ANTES DO LIMITE-----------------------------------------------------#
    #Pega o valor mais proximo do Mrd como MedListAntes
    MedList = min(list_Med, key = lambda x:abs(x-Mrd))
    #Loop pra pegar o valor mais próximo que não seja maior que o Mrd
    i = 0
    while Mrd > MedList:
        MedList = min(list_Med, key = lambda x:abs(x-(Mrd + i)))
        i += 1
    #Pega o index da lista e converte para o ponto real da barra com 1 casa de precisão decimal
    Ponto = round(list_Med.index(MedList)*precisão, 1) + LimiteInf
    #ADICIONA A PARTE TRANSLADADA DO DIAGRAMA
    z = 0.9*x.Altura_Util #m #ITEM 6.2.3 (1)
    al = round(z*((cot_ang_teta) - (cot_ang_alfa)/2), 2) #m #ITEM 9.2.1.3 (2) 
    #Adiciona as informações antes do ponto Limite ao objeto de dispensa
    ObjDispensa.al = round(al, 2)
    ObjDispensa.lbd = round(lbd, 2)
    ObjDispensa.Mrd = round(Mrd, 2)
    ObjDispensa.Med = MedList
    if round(Ponto, 2) < 0:
        ObjDispensa.Ponto = 0
    else:
        ObjDispensa.Ponto = round(Ponto, 2)
    if not LimiteSup >= IRobotBar(bars.Get(Barra)).Length:
        ObjDispensa.Ponto_al_lbd = ObjDispensa.Ponto + round(al + lbd, 2)
        ObjDispensa.Comprimento = LimiteInf + round(ObjDispensa.Ponto_al_lbd, 2)
    else:
        ObjDispensa.Ponto_al_lbd = ObjDispensa.Ponto - round(al + lbd, 2)
        ObjDispensa.Comprimento = LimiteSup - round(ObjDispensa.Ponto_al_lbd, 2)
#Loop para realizar a dispensa automatica de armaduras positivas
for i in range(len(list_bars)):
    #DISPENSA POSITIVA
    dic_dispensa = {}
    x = eval(f"Barra_{list_bars[i]}_ULS.Med_Positivo.ArmLong")
    #Verifica se o numero de barras sao pares ou impares
    if x.n_barras % 2 == 0:
        Totalbars = int(x.n_barras)
    else:
        Totalbars = int(x.n_barras)
    lista_disp = []
    lista_disp = lista_dispensa(Totalbars)
    Barra = list_bars[i]
    Length = IRobotBar(bars.Get(Barra)).Length
    Lista_Pontos = eval("p_%d" %Barra)
    Limite_Positivo = round(MaxEsfPoint(Barra,"My",Lista_Pontos), 2)
    listas = change_signal(Barra, "My")
    Limite_Startnode = listas[0][1]*precisão
    Limite_Endnode = listas[1][1]*precisão
    list_Med_Antes = []
    #Range pra lista de momentos antes do ponto maximo
    for k in np.arange(0, Limite_Positivo + precisão, precisão):
        list_Med_Antes.append(round(MaxEsf_Point_MY(Barra,k,Length,listcomb,force_serv),2))
    list_Med_Depois = []
    #Range pra lista de momentos depois do ponto maximo
    for k in np.arange(Limite_Positivo, Length + precisão, precisão):
        list_Med_Depois.append(round(MaxEsf_Point_MY(Barra,k,Length,listcomb,force_serv),2))
    #Calculo de lbd
    lbd = calc_lbd_Pos(Barra, 4)
    #Range pra efetuar o calculo da dispensa das armaduras positivas
    for j in range(len(lista_disp)):
        #Calcula a area nova com uma barra a menos
        xas = (x.n_barras-lista_disp[j])*np.pi*(x.d_long/10)**2/4 #cm2
        #calcula novamente o Mrd
        xmrd = CalcMrd(xas, b, eta_conc, lambda_conc, fcd, fyd, x.Altura_Util)
        #Cria um objeto para armazenar as informaçoes da dispensa
        locals()[f"dispensa_{j+1}"] = dispensa()
        #Calcula a dispensa
        dispensa_positiva(Limite_Positivo, precisão, Barra, xmrd, eval(f"dispensa_{j+1}"), Length, cot_ang_teta, cot_ang_alfa, x, list_Med_Antes, list_Med_Depois, lbd)
        #Armazena as informações num dicionario
        dic_dispensa[f"Dispensa_{j+1}"] = eval(f"dispensa_{j+1}")
        eval(f"dispensa_{j+1}").Barras_dispensadas = lista_disp[j] 
    z = 0.9*x.Altura_Util #m #ITEM 6.2.3 (1)
    al = round(z*((cot_ang_teta) - (cot_ang_alfa)/2), 2) #m #ITEM 9.2.1.3 (2)
    #Cria um objeto de dispensa e armazena as informações calculadas nele
    locals()[f"dispensa_{j+2}"] = dispensa()
    eval(f"dispensa_{j+2}").PontoEsquerda_al_lbd = Limite_Startnode - round(al + lbd, 2)
    eval(f"dispensa_{j+2}").PontoDireita_al_lbd = Limite_Endnode + round(al + lbd, 2)
    eval(f"dispensa_{j+2}").MedDireita = 0
    eval(f"dispensa_{j+2}").MedEsquerda = 0
    dic_dispensa[f"Dispensa_{j+2}"] = eval(f"dispensa_{j+2}")
    #Vincula o objeto de dispensa ao objeto de dimensionamento
    eval(f"Barra_{list_bars[i]}_ULS").Dispensa_Positiva = dic_dispensa
    
    #DISPENSA NEGATIVA
    dic_dispensa_startnode = {}
    dic_dispensa_endnode = {}
    x1 = eval(f"Barra_{list_bars[i]}_ULS.Med_Negativo.StartNode.ArmLong")
    x2 = eval(f"Barra_{list_bars[i]}_ULS.Med_Negativo.EndNode.ArmLong")
    #Verificação se o numero de barras é par ou não para ambos os casos
    if x1.n_barras % 2 == 0:
        Totalbars1 = int(x1.n_barras)
    else:
        Totalbars1 = int(x1.n_barras)
    if x2.n_barras % 2 == 0:
        Totalbars2 = int(x2.n_barras)
    else:
        Totalbars2 = int(x2.n_barras)
    lista_disp_StartNode = []
    lista_disp_EndNode = []
    lista_disp_StartNode = lista_dispensa(Totalbars1)
    lista_disp_EndNode = lista_dispensa(Totalbars2)
    #Calcula lbd
    lbd_start = calc_lbd_Neg(Barra, 4)
    list_Med = []
    #Range pra lista de momentos do primeiro nó
    for k in np.arange(0, Limite_Startnode + precisão, precisão):
        list_Med.append(round(MinEsf_Point_MY(Barra,k,Length,listcomb,force_serv),2))
    #Calculo da dispensa no primeiro nó
    for j in range(len(lista_disp_StartNode)):
        #Calcula a area nova com uma barra a menos
        xas1 = (x1.n_barras-lista_disp_StartNode[j])*np.pi*(x1.d_long/10)**2/4 #cm2
        #calcula novamente o Mrd
        xmrd1 = - CalcMrd(xas1, b, eta_conc, lambda_conc, fcd, fyd, x1.Altura_Util)
        #Cria um objeto para armazenar as informaçoes da dispensa
        locals()[f"dispensa_{j+1}_StartNode"] = dispensa()
        locals()[f"StartNode"] = dispensa()
        #Realiza o calculo da dispensa
        dispensa_negativa(0, Limite_Startnode, precisão, Barra, xmrd1, eval(f"dispensa_{j+1}_StartNode"), Length, cot_ang_teta, cot_ang_alfa, x1, list_Med, lbd)
        dic_dispensa_startnode[f"Dispensa_{j+1}"] = eval(f"dispensa_{j+1}_StartNode")
        StartNode.Dispensa = dic_dispensa_startnode
        eval(f"dispensa_{j+1}_StartNode").Barras_dispensadas = lista_disp_StartNode[j]
    z = 0.9*x1.Altura_Util #m #ITEM 6.2.3 (1)
    al = round(z*((cot_ang_teta) - (cot_ang_alfa)/2), 2) #m #ITEM 9.2.1.3 (2)
    #Cria um objeto de dispensa pra armazenar as informações do momento negativo do primeiro nó nele
    locals()[f"dispensa_{j+2}_StartNode"] = dispensa()
    eval(f"dispensa_{j+2}_StartNode").Ponto_al_lbd = Limite_Startnode + round(al + lbd, 2)
    eval(f"dispensa_{j+2}_StartNode").Med = 0
    dic_dispensa_startnode[f"Dispensa_{j+2}"] = eval(f"dispensa_{j+2}_StartNode")
    list_Med = []
    #Range pra lista de momentos do segundo nó
    for k in np.arange(Limite_Endnode, Length + precisão, precisão):
        list_Med.append(round(MinEsf_Point_MY(Barra,k,Length,listcomb,force_serv),2))
    #Calculo da dispensa no segundo nó
    for j in range(len(lista_disp_EndNode)):
        xas2 = (x2.n_barras-lista_disp_EndNode[j])*np.pi*(x1.d_long/10)**2/4 #cm2
        xmrd2 = - CalcMrd(xas2, b, eta_conc, lambda_conc, fcd, fyd, x2.Altura_Util)
        locals()[f"dispensa_{j+1}_EndNode"] = dispensa()
        locals()[f"EndNode"] = dispensa()
        dispensa_negativa(Limite_Endnode, Length, precisão, Barra, xmrd2, eval(f"dispensa_{j+1}_EndNode"), Length, cot_ang_teta, cot_ang_alfa, x2, list_Med, lbd)
        dic_dispensa_endnode[f"Dispensa_{j+1}"] = eval(f"dispensa_{j+1}_EndNode")
        EndNode.Dispensa = dic_dispensa_endnode
        eval(f"dispensa_{j+1}_EndNode").Barras_dispensadas = lista_disp_EndNode[j]
    z = 0.9*x2.Altura_Util #m #ITEM 6.2.3 (1)
    al = round(z*((cot_ang_teta) - (cot_ang_alfa)/2), 2) #m #ITEM 9.2.1.3 (2) 
    #Cria um objeto de dispensa pra armazenar as informações do momento negativo do segundo nó nele
    locals()[f"dispensa_{j+2}_EndNode"] = dispensa()
    eval(f"dispensa_{j+2}_EndNode").Med = 0
    eval(f"dispensa_{j+2}_EndNode").Ponto_al_lbd = Limite_Endnode - round(al + lbd, 2)
    dic_dispensa_endnode[f"Dispensa_{j+2}"] = eval(f"dispensa_{j+2}_EndNode")
    #Cria um objeto de referencia dentro do objeto de dimensionamento e atribui os dimensionamentos de ambos os
        #nós nele
    eval(f"Barra_{list_bars[i]}_ULS").Dispensa_Negativa = dispensa()
    eval(f"Barra_{list_bars[i]}_ULS.Dispensa_Negativa").StartNode = StartNode
    eval(f"Barra_{list_bars[i]}_ULS.Dispensa_Negativa").EndNode = EndNode
#Função que retorna o gráfico transladado
def Grafico_Transladado(Esforço,Barra,EscalaX, EscalaY): #(str,int,list)
    #DIAGRAMA DE ENVOLVENTE DE ESFORÇOS
    listenvolv = []
    Lista_Pontos = eval(f"p_{Barra}")
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))   
    del listprov; del prov
    vigaplot = listenvolv
    
    zpos = 0.9*eval(f"Barra_{list_bars[0]}_ULS.Med_Positivo.ArmLong.Altura_Util") #m 
    al_1 = zpos*((cot_ang_teta) - (cot_ang_alfa)/2) #m 

    #TRANSLAÇÃO DO DIAGRAMA DE ENVOLVENTE
    Lista_Pontos_Transladado = []
    for i in range(len(listenvolv)):
        element = listenvolv[i]
        if element > 0 and i <= int(len(listenvolv)/2) :
            Lista_Pontos_Transladado.append(p_1[i] - al_1)
        elif element < 0 and i <= int(len(listenvolv)/2): 
            Lista_Pontos_Transladado.append(p_1[i] + al_1)
        elif element > 0 and i > int(len(listenvolv)/2):
            Lista_Pontos_Transladado.append(p_1[i] + al_1)
        elif element < 0 and i > int(len(listenvolv)/2):
            Lista_Pontos_Transladado.append(p_1[i] - al_1)    
    
    #DISPENSA DE ARMADURAS (DIAGRAMA RESISTENTE)
    #PARTE PARA A DISPENSA POSITIVA NO PLOT
    y = eval(f"Barra_{Barra}_ULS")
    x = y.Dispensa_Positiva

    list_med_disp_direita = []
    list_point_direita = []
    list_med_disp_esquerda = []
    list_point_esquerda = []
    PontoEsquerda = x["Dispensa_1"].PontoEsquerda - x["Dispensa_1"].al
    PontoDireita = x["Dispensa_1"].PontoDireita + x["Dispensa_1"].al
    list_med_disp_direita = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_direita = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), PontoDireita]
    list_med_disp_esquerda = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_esquerda = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), PontoEsquerda]

    #RANGE DO PLOT DO ESFORÇO RESISTENTE
    for i in range(len(x)):
        k = x[f"Dispensa_{i+1}"]
        list_med_disp_direita.append(k.MedDireita)
        list_med_disp_esquerda.append(k.MedEsquerda)
        list_point_direita.append(k.PontoDireita_al_lbd)
        list_point_esquerda.append(k.PontoEsquerda_al_lbd)

    #DISPENSA DOS MOMENTOS NEGATIVOS

    list_med_disp_StartNode = []
    list_point_StartNode = []
    list_med_disp_EndNode = []
    list_point_EndNode = []
    y1 = eval(f"Barra_{Barra}_ULS")
    x1 = y.Dispensa_Negativa.StartNode
    y2 = eval(f"Barra_{Barra}_ULS")
    x2 = y.Dispensa_Negativa.EndNode
    Ponto_StartNode = x1.Dispensa["Dispensa_1"].Ponto + x1.Dispensa["Dispensa_1"].al
    Ponto_EndNode = x2.Dispensa["Dispensa_1"].Ponto - x2.Dispensa["Dispensa_1"].al
    list_med_disp_StartNode = [-round(y.Med_Negativo.StartNode.ArmLong.Mrd, 2), -round(y.Med_Negativo.StartNode.ArmLong.Mrd, 2)]
    list_point_StartNode = [round(y.Med_Negativo.StartNode.ArmLong.PontoMPositivo, 2), Ponto_StartNode]
    list_med_disp_EndNode = [-round(y.Med_Negativo.EndNode.ArmLong.Mrd, 2), -round(y.Med_Negativo.EndNode.ArmLong.Mrd, 2)]
    list_point_EndNode = [round(y.Med_Negativo.EndNode.ArmLong.PontoMPositivo, 2), Ponto_EndNode]

    #RANGE DO PLOT DO ESFORÇO RESISTENTE
    for i in range(len(x1.Dispensa)):
        k1 = x1.Dispensa[f"Dispensa_{i+1}"]
        list_med_disp_StartNode.append(k1.Med)
        list_point_StartNode.append(k1.Ponto_al_lbd)
    #list_med_disp_StartNode.append(0)
    #list_point_StartNode.append(k1.Ponto + k1.al)
    for i in range(len(x2.Dispensa)):
        k2 = x2.Dispensa[f"Dispensa_{i+1}"]
        list_med_disp_EndNode.append(k2.Med)
        list_point_EndNode.append(k2.Ponto_al_lbd)
    #list_med_disp_EndNode.append(0)
    #list_point_EndNode.append(k2.Ponto - k2.al)

    plt.plot(Lista_Pontos, vigaplot, color = "green", label = "Momento Solicitante")
    plt.plot(list_point_direita, list_med_disp_direita, color = "maroon", label = "Momento Resistente Positivo")
    plt.plot(list_point_esquerda, list_med_disp_esquerda, color = "maroon")
    plt.plot(Lista_Pontos_Transladado,listenvolv, color = "darkorange", label = "Grafico Transaladado")
    plt.plot(list_point_StartNode, list_med_disp_StartNode, color = "maroon", label = "Momento Resistente Negativo")
    plt.plot(list_point_EndNode, list_med_disp_EndNode, color = "maroon")

    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title("Translação " +IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento " + Esforço + " [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.legend()
    plt.show()
#Função que recalcula o comprimento da barra de aço para a parte negativa do diagrama
def otimization_neg (Barra, Esforço, LimiteInf, LimiteSup, ObjDispensa, List_MR_MS):

    for i in range(len(ObjDispensa.Dispensa)):
        k = ObjDispensa.Dispensa[f"Dispensa_{i+1}"]
        if not LimiteSup >= IRobotBar(bars.Get(Barra)).Length:
            k.Novo_Comprimento = round(LimiteInf + List_MR_MS[i+2], 2)     
        else:
            k.Novo_Comprimento = round(LimiteSup - List_MR_MS[i+2], 2)
#Função que recalcula o comprimento da barra de aço para a parte positiva do diagrama
def otimization_pos (Barra, Esforço, ObjDispensa, List_MR_MS_Esquerda, List_MR_MS_Direita):

    for i in range(len(ObjDispensa)):
        k = ObjDispensa[f"Dispensa_{i+1}"]
        k.Novo_Comprimento = round(-List_MR_MS_Esquerda[i+1] + List_MR_MS_Direita[i+1], 2)
#Função que retorna o gráfico transladado com a armadura ja otimizada
def Grafico_Transladado_Otimizado(Esforço,Barra,EscalaX, EscalaY): #(str,int,list)
    reducao = 0.14 #m
    #DIAGRAMA DE ENVOLVENTE DE ESFORÇOS
    Length = IRobotBar(bars.Get(Barra)).Length
    listenvolv = []
    Lista_Pontos = eval(f"p_{Barra}")
    for i in range(len(Lista_Pontos)):
        listprov = []
        for j in range(len(listcomb)):
            prov = eval("Viga_%d_Caso_COMB%d" %(Barra,j+1)).loc[Esforço].to_numpy()[i]
            listprov.append(prov)
        if abs(max(listprov)) > abs(min(listprov)):
            listenvolv.append(max(listprov))
        else:
            listenvolv.append(min(listprov))   
    del listprov; del prov
    vigaplot = listenvolv
    
    zpos = 0.9*eval(f"Barra_{list_bars[0]}_ULS.Med_Positivo.ArmLong.Altura_Util") #m 
    al_1 = zpos*((cot_ang_teta) - (cot_ang_alfa)/2) #m 

    #TRANSLAÇÃO DO DIAGRAMA DE ENVOLVENTE
    Lista_Pontos_Transladado = []
    for i in range(len(listenvolv)):
        element = listenvolv[i]
        if element > 0 and i <= int(len(listenvolv)/2) :
            Lista_Pontos_Transladado.append(eval(f"p_{Barra}")[i] - al_1)
        elif element < 0 and i <= int(len(listenvolv)/2): 
            Lista_Pontos_Transladado.append(eval(f"p_{Barra}")[i] + al_1)
        elif element > 0 and i > int(len(listenvolv)/2):
            Lista_Pontos_Transladado.append(eval(f"p_{Barra}")[i] + al_1)
        elif element < 0 and i > int(len(listenvolv)/2):
            Lista_Pontos_Transladado.append(eval(f"p_{Barra}")[i] - al_1)    

    #DISPENSA DE ARMADURAS (DIAGRAMA RESISTENTE)
    #PARTE PARA A DISPENSA POSITIVA NO PLOT
    y = eval(f"Barra_{Barra}_ULS")
    x = y.Dispensa_Positiva

    list_med_disp_direita = []
    list_point_direita = []
    list_med_disp_esquerda = []
    list_point_esquerda = []
    PontoEsquerda = x["Dispensa_1"].PontoEsquerda - x["Dispensa_1"].al
    PontoDireita = x["Dispensa_1"].PontoDireita + x["Dispensa_1"].al
    list_med_disp_direita = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_direita = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), PontoDireita]
    list_med_disp_esquerda = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_esquerda = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), PontoEsquerda]
    
    #RANGE DO PLOT DO ESFORÇO RESISTENTE
    for i in range(len(x)):
        k = x[f"Dispensa_{i+1}"]
        list_med_disp_direita.append(k.MedDireita)
        list_med_disp_esquerda.append(k.MedEsquerda)
        list_point_direita.append(k.PontoDireita_al_lbd)
        list_point_esquerda.append(k.PontoEsquerda_al_lbd)

    #DISPENSA DOS MOMENTOS NEGATIVOS
    list_MR_MS_StartNode = []
    list_MR_MS_EndNode = []
    list_med_disp_StartNode = []
    list_point_StartNode = []
    list_med_disp_EndNode = []
    list_point_EndNode = []
    y1 = eval(f"Barra_{Barra}_ULS")
    x1 = y.Dispensa_Negativa.StartNode
    y2 = eval(f"Barra_{Barra}_ULS")
    x2 = y.Dispensa_Negativa.EndNode
    Ponto_StartNode = x1.Dispensa["Dispensa_1"].Ponto + x1.Dispensa["Dispensa_1"].al
    Ponto_EndNode = x2.Dispensa["Dispensa_1"].Ponto - x2.Dispensa["Dispensa_1"].al
    list_med_disp_StartNode = [-round(y.Med_Negativo.StartNode.ArmLong.Mrd, 2), -round(y.Med_Negativo.StartNode.ArmLong.Mrd, 2)]
    list_point_StartNode = [round(y.Med_Negativo.StartNode.ArmLong.PontoMPositivo, 2), Ponto_StartNode]
    list_med_disp_EndNode = [-round(y.Med_Negativo.EndNode.ArmLong.Mrd, 2), -round(y.Med_Negativo.EndNode.ArmLong.Mrd, 2)]
    list_point_EndNode = [round(y.Med_Negativo.EndNode.ArmLong.PontoMPositivo, 2), Ponto_EndNode]

    #RANGE DO PLOT DO ESFORÇO RESISTENTE
    for i in range(len(x1.Dispensa)):
        k1 = x1.Dispensa[f"Dispensa_{i+1}"]
        list_med_disp_StartNode.append(k1.Med)
        list_point_StartNode.append(k1.Ponto_al_lbd)
        

    for i in range(len(x2.Dispensa)):
        k2 = x2.Dispensa[f"Dispensa_{i+1}"]
        list_med_disp_EndNode.append(k2.Med)
        list_point_EndNode.append(k2.Ponto_al_lbd)


    list_MR_MS_StartNode.append(list_point_StartNode[0])
    list_MR_MS_StartNode.append(Lista_Pontos_Transladado[0])
    for i in range(2, len(list_med_disp_StartNode) - 1):
        k = Lista_Pontos_Transladado[listenvolv.index(list_med_disp_StartNode[i])]
        list_MR_MS_StartNode.append(k)
    list_MR_MS_StartNode.append(x1.Dispensa[f"Dispensa_{i}"].Ponto_al_lbd)
    listas = change_signal(Barra, "My")
    Limite_StartNode = listas[0][0]*precisão
    Limite_EndNode = listas[1][0]*precisão
    otimization_neg(Barra, Esforço, 0,  Limite_StartNode, x1, list_MR_MS_StartNode)

    list_MR_MS_EndNode.append(list_point_EndNode[0])
    list_MR_MS_EndNode.append(Lista_Pontos_Transladado[len(Lista_Pontos_Transladado) - 1])
    for i in range(2, len(list_med_disp_EndNode) - 1):
        k = Lista_Pontos_Transladado[listenvolv.index(list_med_disp_EndNode[i])]
        list_MR_MS_EndNode.append(k)
    list_MR_MS_EndNode.append(x2.Dispensa[f"Dispensa_{i}"].Ponto_al_lbd)
    otimization_neg(Barra, Esforço, Limite_EndNode,  Length, x2, list_MR_MS_EndNode)
       


    #-----------------------------------------------------------------------------------------------------------------------

    last_term = Lista_Pontos_Transladado[0]
    lista_Ponto_Direita = []
    lista_Ponto_Esquerda = []
    for v in range(len(Lista_Pontos_Transladado)):
        if Lista_Pontos_Transladado[v] - last_term > 2*precisão:
            lista_Ponto_Esquerda.append(last_term)
            last_term = Lista_Pontos_Transladado[v]
            lista_Ponto_Direita.append(last_term)
        last_term = Lista_Pontos_Transladado[v]


    #DISPENSA DOS MOMENTOS POSITIVOS
    list_MR_MS_Direita = []
    list_MR_MS_Esquerda = []
    list_med_disp_Direita = []
    list_point_Direita = []
    list_med_disp_Esquerda = []
    list_point_Esquerda = []
    y = eval(f"Barra_{Barra}_ULS")
    x = y.Dispensa_Positiva
    lbd = calc_lbd_Pos(Barra, 4)
    Ponto_Esquerda = x["Dispensa_1"].PontoEsquerda - x["Dispensa_1"].al
    Ponto_Direita = x["Dispensa_1"].PontoDireita + x["Dispensa_1"].al
    list_med_disp_Esquerda = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_Esquerda = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), round(lista_Ponto_Esquerda[0], 2)  ]
    list_med_disp_Direita = [round(y.Med_Positivo.ArmLong.Mrd, 2), round(y.Med_Positivo.ArmLong.Mrd, 2)]
    list_point_Direita = [round(y.Med_Positivo.ArmLong.PontoMPositivo, 2), round(lista_Ponto_Direita[0], 2)]

    #RANGE DO PLOT DO ESFORÇO RESISTENTE
    for i in range(len(x)):
        k = x[f"Dispensa_{i+1}"]
        list_med_disp_Direita.append(k.MedDireita)
        list_med_disp_Esquerda.append(k.MedEsquerda)
        list_point_Direita.append(k.PontoDireita_al_lbd)
        list_point_Esquerda.append(k.PontoEsquerda_al_lbd)




    list_MR_MS_Esquerda.append(list_point_Esquerda[0])
    list_MR_MS_Esquerda.append(list_point_Esquerda[1])
    for i in range(2, len(list_med_disp_Esquerda) - 1):
        k = Lista_Pontos_Transladado[listenvolv.index(list_med_disp_Esquerda[i])]
        list_MR_MS_Esquerda.append(k - reducao)
    list_MR_MS_Esquerda.append(x[f"Dispensa_{i}"].PontoEsquerda_al_lbd)
    listas = change_signal(Barra, "My")

    list_MR_MS_Direita.append(list_point_Direita[0])
    list_MR_MS_Direita.append(list_point_Direita[1])
    for i in range(2, len(list_med_disp_Direita) - 1):
        k = Lista_Pontos_Transladado[listenvolv.index(list_med_disp_Direita[i])]
        list_MR_MS_Direita.append(k + reducao)
    list_MR_MS_Direita.append(x[f"Dispensa_{i}"].PontoDireita_al_lbd)
    otimization_pos(Barra, Esforço, x, list_MR_MS_Esquerda, list_MR_MS_Direita)




        
    plt.plot(list_MR_MS_StartNode, list_med_disp_StartNode, color = "maroon", label = "Momento Resistente Negativo")
    plt.plot(list_MR_MS_EndNode, list_med_disp_EndNode, color = "maroon")
    plt.plot(Lista_Pontos, vigaplot, color = "green", label = "Momento Solicitante")
    plt.plot(list_MR_MS_Direita, list_med_disp_Direita, color = "maroon", label = "Momento Resistente Positivo")
    plt.plot(list_MR_MS_Esquerda, list_med_disp_Esquerda, color = "maroon")
    #plt.plot(list_point_direita, list_med_disp_direita, color = "yellow", label = "Momento Resistente")
    #plt.plot(list_point_esquerda, list_med_disp_esquerda, color = "yellow")
    plt.plot(Lista_Pontos_Transladado,listenvolv, color = "darkorange", label = "Grafico Transaladado")
    #plt.plot(list_point_StartNode, list_med_disp_StartNode)
    #plt.plot(list_point_EndNode, list_med_disp_EndNode)

    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title("Translação Reduzida " +IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento " + Esforço + " [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.legend()
    plt.show()
#Range de plots do grafico transladado e grafico transladado otimizado
for i in range(len(list_bars)):
    barra = list_bars[i]
    lista = eval("p_%d" %barra)
    Grafico_Transladado("My",barra,1,1)
    Grafico_Transladado_Otimizado("My",barra,1,1)


pr.disable()

s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())


print(".")
