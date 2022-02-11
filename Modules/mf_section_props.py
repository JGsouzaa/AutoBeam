#mf_section_props
from mr_project import *
#BUSCA INFORMAÇÕES DE ALTURA E LARGURA DA SEÇÃO DA BARRA
def height(Barra_Numero):
    obj_barra = IRobotBar(bars.Get(Barra_Numero)) #seleciona a barra 1
    label_secaobarra = IRobotLabel(obj_barra.GetLabel(3)) # seleciona a label "seçao" da barra 1
    data_height = IRobotBarSectionData(label_secaobarra.Data).GetValue(12) # seleciona o valor de HY da barra
    return(data_height)
def width(Barra_Numero):
    obj_barra = IRobotBar(bars.Get(Barra_Numero)) #seleciona a barra 1
    label_secaobarra = IRobotLabel(obj_barra.GetLabel(3)) # seleciona a label "seçao" da barra 1
    data_width = IRobotBarSectionData(label_secaobarra.Data).GetValue(13) # seleciona o valor de HX da barra
    return(data_width)
#ATÉ O MOMENTO DE PRODUÇÃO DA TESE NÃO FOI ENCONTRADO NO FÓRUM ALGUMA MANEIRA DE ACESSAR OS MOMENTOS DE INÉRCIA CALCULADOS PELO ROBOT
    #NO FÓRUM DA AUTODESK HÁ UM POST FEITO PELO AUTOR COM INTUÍTO DE RESOLVER ISSO MAS ATÉ O MOMENTO NÃO FOI RESPONDIDO
    #LINK DO POST: https://forums.autodesk.com/t5/robot-structural-analysis-forum/section-properties-api-robot-moment-of-inertia/m-p/10138557
#AS FUNÇÕES DE MOMENTO DE INÉRCIA SÃO PARA SEÇÕES RETANGULARES E CALCULAM A INÉRCIA COM BASE NA SEÇÃO TRANSVERSAL, SENDO inercia_width PARA MOMENTO DE INÉRCIA
    #EM RELAÇÃO AO EIXO PARALELO À BASE(Width) E inercia_heigth EM RELAÇÃO AO EIXO PARALELO À ALTURA(Heigth)
def inercia_width(Barra_Numero):
    b = height(Barra_Numero)
    h = width(Barra_Numero)
    Iwidth = (b*h**3)/12
    return(Iwidth)
def inercia_height(Barra_Numero):
    b = height(Barra_Numero)
    h = width(Barra_Numero)
    Iheight = (h*b**3)/12
    return(Iheight)