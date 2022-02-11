#mr_project
from mr_initial import *
#Definindo variaveis
preferences = project.Preferences
    #Referencia de acesso às preferencias do projeto
structure = project.Structure
    #Referencia de acesso à estrutura do projeto
bars = structure.Bars
    #Server de acesso ás barras
labels = structure.Labels
    #Server de acesso a seções
selections = structure.Selections
    #Server de acesso às seleções
results = structure.Results
    #Server de acesso aos resultados
r_Bars = results.Bars
    #resultados para barras
cases = structure.Cases
    #Server de acesso aos casos de carga
obj = structure.Objects
    #Server de acesso aos objetos contidos na estrutura
force_serv = r_Bars.Forces
    #Acessa o servidor de resultados para barras
nodes_serv = structure.Results.Nodes
    #Acessa o serviro de resultados para os nós
bar_col = RobotBarCollection(bars.GetAll())
    #Pega todas as barras no projeto
cas_col = IRobotCaseCollection(cases.GetAll())
    #Pega todos os casos de carga no projeto
