from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import matplotlib as plt


k = np.arange(1,9,0.4)


root = Tk()

class Funçoes():

    

    def evaluate(self):
        self.lb_6.configure(text = "oi")


    pass



class Application(Funçoes):
    #Tudo que estiver no init sera inicializado quando a classe for chamada
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_de_tela()
        self.widgets_frame_1()
        root.mainloop()  
    def tela(self):
        self.root.title("Title")
        #self.root.configure(background = "#B0E0E6" )
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        #self.root.maxsize(width = 800, height = 800)
        self.root.minsize(width = 1000, height = 600)
    def frames_de_tela(self):
        #bd = borda, bg = background, relx = porcentagem do tamanho total da tela que fica posicionado no eixo horizontal
        #Frames sao pequenas janelas dentro da janela principal

        #frame_1 = frame da direita contendo as infos
        #frame_2 = frame do grafico
        self.frame_1 = Frame(self.root, bd = 2, bg = "#6495ED", highlightbackground = "#000000", highlightthickness = 2)
        self.frame_1.place(relx = 0.615 , rely = 0.01, relwidth = 0.38, relheight = 0.98 )
        self.frame_2 = Frame(self.frame_1, bd = 1, bg = "#D8BFD8", highlightbackground = "#800000", highlightthickness = 4)
        self.frame_2.place(relx = 0 , rely = 0, relwidth = 1, relheight = 0.67)
        self.frame_3 = Frame(self.root, bd = 2, bg = "#6495ED", highlightbackground = "#000000", highlightthickness = 2)
        self.frame_3.place(relx = 0.23 , rely = 0.01, relwidth = 0.38, relheight = 0.98 )



    def codigo_entry_calc(self, sv):
        variavel_1 = self.codigo_entry_var.get()
        variavel_2 = float(self.codigo_entry_var.get())

        if self.codigo_entry_var.get() != "":
            self.lb1_var.set("Min Value: {:.2f}kNm" .format(-300.000))

    def widgets_frame_1(self):
        #criaçao label e entrada do codigo
        #lb_1 = valor minimo, lb_2 = valor maximo, lb_3 = ponto do valor minimo, lb_4 = ponto do valor maximo
        self.codigo_entry_var = StringVar()
        self.lb1_var = StringVar()

        self.lb1_var.set("Min Value: {:.2f}kNm" .format(-302.542))
        
        self.lb_1 = Label(self.frame_1, textvariable=self.lb1_var)
        self.lb_1.place(relx = 0.01, rely = 0.69, relwidth = 0.485)
        self.lb_2 = Label(self.frame_1, text = "Max Value: {:.2f}kNm" .format(394.634))
        self.lb_2.place(relx = 0.01, rely = 0.74, relwidth = 0.485)
        self.lb_3 = Label(self.frame_1, text = "Point Min Value: {:.2f}m" .format(9,94))
        self.lb_3.place(relx = 0.51, rely = 0.69, relwidth = 0.485)
        self.lb_4 = Label(self.frame_1, text = "Point Max Value: {:.2f}m" .format(40,5322))
        self.lb_4.place(relx = 0.51, rely = 0.74, relwidth = 0.485)
        self.lb_5 = Label(self.frame_1, text = "Ponto: ")
        self.lb_5.place(relx = 0.01, rely = 0.79, relwidth = 0.2325)#relwidth = 0.485
        self.lb_6 = Label(self.frame_1, text = " Momento: {:.2f}" .format(75.34))
        self.lb_6.place(relx = 0.51, rely = 0.79, relwidth = 0.485)

        
        self.codigo_entry = Entry(self.frame_1, textvariable=self.codigo_entry_var)
        self.codigo_entry.place(relx = 0.26, rely = 0.79, relwidth = 0.2325, relheight = 0.035) #relx = 0.51 relwidth = 0.485
        self.codigo_entry.bind("<Return>", self.codigo_entry_calc)

        self.botao1 = Button(self.frame_1, text = "Fx", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao1.place(relx = 0.01, rely = 0.84, relwidth = 0.485, relheight = 0.05)
        self.botao2 = Button(self.frame_1, text = "Fy", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao2.place(relx = 0.01, rely = 0.89, relwidth = 0.485, relheight = 0.05)
        self.botao3 = Button(self.frame_1, text = "Fz", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao3.place(relx = 0.01, rely = 0.94, relwidth = 0.485, relheight = 0.05)
        self.botao4 = Button(self.frame_1, text = "Mx", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao4.place(relx = 0.51, rely = 0.84, relwidth = 0.485, relheight = 0.05)
        self.botao5 = Button(self.frame_1, text = "My", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao5.place(relx = 0.51, rely = 0.89, relwidth = 0.485, relheight = 0.05)
        self.botao6 = Button(self.frame_1, text = "Mz", bd = 4, bg = "#6A5ACD"
        , fg = "white")
        self.botao6.place(relx = 0.51, rely = 0.94, relwidth = 0.485, relheight = 0.05)

        


    def endloop(self):
        del root.mainloop

Application()


