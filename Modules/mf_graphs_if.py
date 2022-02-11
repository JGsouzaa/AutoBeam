#mf_graphs_if
#FUNÇÃO QUE RETORNA O GRÁFICO DE MOMENTO NA DIREÇÃO MX
def graficoMx(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["Mx"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento Mx [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DE MOMENTO NA DIREÇÃO MY
def graficoMy(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["My"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento My [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DE MOMENTO NA DIREÇÃO MZ
def graficoMz(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["Mz"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Momento Mz [kNm]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DE FORÇA NA DIREÇÃO FX
def graficoFx(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["Fx"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Força Fx [kN]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DE FORÇA NA DIREÇÃO FX
def graficoFy(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["Fy"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Força Fy [kN]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#FUNÇÃO QUE RETORNA O GRÁFICO DE FORÇA NA DIREÇÃO FX
def graficoFz(Barra, Bar_Data_Frame, Lista_Pontos, EscalaX, EscalaY): #(int, pd.df, list, int/flloat, int/float)
    #Pontos é uma lista
    vigaplot = Bar_Data_Frame.loc["Fz"].to_numpy()
    plt.plot(Lista_Pontos, vigaplot)
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    plt.xlim(xmin*EscalaX, xmax*EscalaX)
    plt.ylim(ymin*EscalaY, ymax*EscalaY)
    plt.title(IRobotBar(bars.Get(Barra)).Name)
    plt.gca().invert_yaxis()
    plt.ylabel("Força Fz [kN]")
    plt.xlabel("Ponto na Barra")
    plt.axhline(y=0, color="k", linestyle="-")
    plt.axvline(x=Length, color = "k", linestyle ="-")
    plt.axvline(x=0, color = "k", linestyle ="-")
    plt.show()
#
    #EX: graficoMx(1, Viga_1_Caso_COMB1, p_1, 1, 1)
#FUNÇÃO QUE RETORNA O GRAFICO DA VIGA COMPLETA
def graficoVigaCompleta(Esforço, Combinação, EscalaX, EscalaY): #(str, int, float/int, float/int)
    Viga_Completa = []
    p_tot = []
    List_Length = []
    Length_0 = 0
    List_Length.append(Length_0)   
    for i in range(len(list_bars)):
        i2 = list_bars[i]
        NumbViga = i2
        VigaRef = eval("Viga_%d_Caso_COMB%d" % (NumbViga,Combinação))
        Viga_Completa.append(VigaRef.loc[Esforço].to_numpy())
        globals()[f"Length_{i+1}"] = IRobotBar(bars.Get(i2)).Length + eval("Length_%d" %i)
        List_Length.append(eval("Length_%d" %(i+1)))
        locals()[f"p_{i+1}"] = [(x+List_Length[i]) for x in eval("p_%d" %(i+1))]
        p_tot.append(eval("p_%d" %(i+1)))
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
    #EX: graficoVigaCompleta("My",1,1,1)  
