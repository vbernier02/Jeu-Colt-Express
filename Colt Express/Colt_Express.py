from tkinter import *
from tkinter import ttk
from random import *
from random import sample
from tkinter import messagebox
import pygame
from pygame import *
import tkinter.font as font
from PIL import Image, ImageTk

import time
score = 0


pygame.mixer.init()

class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.title("COLT EXPRESS")
        self.resizable(False, False)
        for F in (Menu, Jeu):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Menu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        img = Image.open("image_western.jpg")
        img = img.resize((1000,810))
        img=ImageTk.PhotoImage(img)
        label_img= Label(self,image=img,bg='white')
        label_img.image = img
        label_img.pack()

        label = Label(self, text="COLT EXPRESS", font = ('Helvatical bold',30))
        label.pack(pady=10,padx=10)
        label.place(x=500 ,y=200, anchor="center")

        bouton = ttk.Button(self, text="Jouer",width = 30,command=lambda: controller.show_frame(Jeu))
        bouton.pack()
        bouton.place(x=500 , y=350 ,anchor="center")

        bouton2 = ttk.Button(self, text="Quitter",width=30,command=self.quit)
        bouton2.pack()
        bouton2.place(x=500 , y=430 ,anchor="center")

class Jeu(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.nb_tour = 10
        self.audio_jeu=pygame.mixer.Sound("jeu.wav")
        self.audio_jeu.set_volume(0.5)
        self.audio_jeu.play()

        self.audio_train=pygame.mixer.Sound("train.wav")
        self.audio_train.set_volume(0.5)
        self.audio_train.play()

        self.audio_fin=pygame.mixer.Sound("music.wav")
        self.audio_fin.set_volume(0.5)

        self.audio_braquage=pygame.mixer.Sound("braquage.wav")
        self.audio_braquage.set_volume(1)

        self.audio_tir=pygame.mixer.Sound("tir.wav")
        self.audio_tir.set_volume(0.5)

        self.son = True

        self.icone = Image.open("son.png").resize((50,50))
        self.icone = ImageTk.PhotoImage(self.icone)
        self.mute = Image.open("sonmute.png").resize((50,50))
        self.mute = ImageTk.PhotoImage(self.mute)

        #Création du butin disponible dans le train
        self.argent = Butin().init()

        #Total du train
        self.total = Butin().total(self.argent)

        #Création des string d'action
        self.action1=StringVar()
        self.action2=StringVar()
        self.action3=StringVar()
        self.action1.set("Action 1:")
        self.action2.set("Action 2:")
        self.action3.set("Action 3:")

        #texte de score
        self.var_label = StringVar()
        self.var_label.set("Votre score : 0")

        #Création du train non visible par l'utilisateur
        self.exterieur=[[],[],[],[],[]]
        self.interieur=[[],[],[],[],[]]

        #création de la position sur Marshall dans le train
        self.sherif = [[],[],[],[],["M"]]
        self.position_sheriff = 4
        
        #création de la liste d'action joueur
        self.action=[]

        #Direction de départ du Marshall
        # -1 pour la gauche
        # 1 pour la droite
        self.choix = -1

        #Création de l'interface
        self.frame = Frame(self,width = 1000, height = 700, bg= 'ivory')
        self.frame.grid(row = 2, column = 0)

        #Images du fond
        img2 = Image.open("image_jeu.jpg")
        img2 = img2.resize((1000,700))
        img2=ImageTk.PhotoImage(img2)

        label_img2= Label(self,image=img2,bg='white')
        label_img2.image = img2
        label_img2.place(x=0,y=0)

        #Image du haut de la fenêtre
        img3 = Image.open("pancarte.png")
        img3 = img3.resize((500,250))
        img3=ImageTk.PhotoImage(img3)

        label_img3= Label(self,image=img3,bg="black")
        label_img3.image = img3
        label_img3.place(x=0,y=0)

        label_img4= Label(self,image=img3,bg="black")
        label_img4.image = img3
        label_img4.place(x=500,y=0)

        #Image du train
        img = Image.open("train3.png")
        img = img.resize((600,150))
        img=ImageTk.PhotoImage(img)
        label_img= ttk.Label(self,image=img)
        label_img.image = img
        label_img.place(x=200,y=400)

        #Frame des commandes en bas de l'écran
        self.lframe = LabelFrame(self,text="Action")
        self.lframe.grid(row = 3, column = 0)



        #style ttk pour les boutons
        self.style = ttk.Style(self)
        self.style.theme_use('alt')

        #Label des butins à l'interieur du train
        self.wagon4 = Label(self, text=f"Wagon 4 : {self.argent[0]}",font = ('Helvatical bold',12))
        self.wagon4.place(x=20,y=160)

        self.wagon3 = Label(self, text=f"Wagon 3 : {self.argent[1]}",font = ('Helvatical bold',12))
        self.wagon3.place(x=20,y=140)

        self.wagon2 = Label(self, text=f"Wagon 2 : {self.argent[2]}",font = ('Helvatical bold',12))
        self.wagon2.place(x=20,y=120)

        self.wagon1 = Label(self, text=f"Wagon 1 : {self.argent[3]}",font = ('Helvatical bold',12))
        self.wagon1.place(x=20,y=100)

        self.locomotive = Label(self, text=f"Locomotive : {self.argent[4]}",font = ('Helvatical bold',12))
        self.locomotive.place(x=20,y=80)

        self.tour = Label(self, text=f"Tour restant : {self.nb_tour}",font = ('Helvatical bold',12))
        self.tour.place(x=20,y=200)

        #Les boutons
        #Quitter le jeu
        self.fuir = ttk.Button(self.lframe, command=self.fuir,text="Fuir")
        self.fuir.grid(row = 1, column = 0, padx=20)

        #Tirer (inutile car il y à un seul bandit)
        self.tirer_button = ttk.Button(self.lframe, command=self.tir,text="Tirer")
        self.tirer_button.grid(row = 1, column = 1, padx=20)

        #Braquage d'un wagon
        self.braquage_button = ttk.Button(self.lframe, command=self.AppendBR,text="Braquage")
        self.braquage_button.grid(row = 1, column = 2, padx=20)

        #Déplacement du bandit
        self.action_button = ttk.Button(self.lframe, command=self.AppendDD,text="droite")
        self.action_button.grid(row = 1, column = 5, padx=10)

        self.action_button2 = ttk.Button(self.lframe, command=self.AppendDG,text="gauche")
        self.action_button2.grid(row = 1, column = 3, padx=10)
  
        self.action_button4 = ttk.Button(self.lframe, command=self.AppendDH,text="Haut")
        self.action_button4.grid(row = 0, column = 4)

        self.action_button3 = ttk.Button(self.lframe, command=self.AppendDB,text="Bas")
        self.action_button3.grid(row = 2, column = 4)

        #Couper le son du jeu
        self.btn_son = Button(self,image=self.icone, command=self.Son)
        self.btn_son.place(x=30 , y=725)        

        #Confirmer les 3 actions du bandits pour les exécuter
        self.confirme = ttk.Button(self.lframe, command=self.Confirmation,text ='Confirmer actions')
        self.confirme.grid(row = 2, column = 2)


        #reset les actions pour rechoisir nos 3 actions
        self.reset = ttk.Button(self.lframe, command=self.reset,text ='Annuler actions')
        self.reset.grid(row = 2, column = 1)

        #Score
        self.label_score = ttk.Label(self, textvariable=self.var_label,font = ('Helvatical bold',12))
        self.label_score.place(x = 700, y = 20)

        
        #Score total du train
        self.label_score_total = ttk.Label(self, text=f"La valeur du train est estimée à {self.total} dollars",font = ('Helvatical bold',12))
        self.label_score_total.place(x = 580, y = 190)

        #Historique en listbox
        self.liste = Listbox(self, height=5, width=50)
        self.liste.place(x=550, y =70)

        #Affichage des actions sélectionner
        self.label_action = ttk.Label(self, textvariable=self.action1,font = ('Helvatical bold',12))
        self.label_action.place(x=110 , y=650 )
        self.label_action2 = ttk.Label(self, textvariable=self.action2,font = ('Helvatical bold',12))
        self.label_action2.place(x=410 , y=650 )
        self.label_action3 = ttk.Label(self, textvariable=self.action3,font = ('Helvatical bold',12))
        self.label_action3.place(x=710 , y=650 )

        #Création du Bandit
        self.bandit1 = Bandit()
        self.bandit1.nom_bandit = "Bandit1"

        #Position initial du bandit
        self.exterieur[self.bandit1.position].append("B1")

        #Coordonée du bandit sur l'interface de départ
        self.x = 250
        self.y = 410

        #Coordonée du Marshall sur l'interface de départ
        self.i = 700
        self.j = 470

        #Icône du bandit
        self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
        self.label_bandit.place(x = self.x, y = self.y)

        #Icône du Marshall
        self.label_marshall = Label(self,text="M", bg='white',font = ('Helvatical bold',19))
        self.label_marshall.place(x = self.i, y = self.j)

    def AppendDD(self):
        if len(self.action)<3:
            self.action.append(self.deplacement_droit)
            if len(self.action)==1:
                self.action1.set("Action 1: deplacement à droit")
            if len(self.action)==2:
                self.action2.set("Action 2: deplacement à droit")
            if len(self.action)==3:
                self.action3.set("Action 3: deplacement à droit")   
        else:
            print("liste full")

    def AppendDG(self):
        if len(self.action)<3:
            self.action.append(self.deplacement_gauche)
            if len(self.action)==1:
                self.action1.set("Action 1: deplacement à gauche")
            if len(self.action)==2:
                self.action2.set("Action 2: deplacement à gauche")
            if len(self.action)==3:
                self.action3.set("Action 3: deplacement à gauche") 
        else:
            print("liste full")

    def AppendDH(self):
        if len(self.action)<3:
            self.action.append(self.deplacement_haut)
            if len(self.action)==1:
                self.action1.set("Action 1: deplacement à haut")
            if len(self.action)==2:
                self.action2.set("Action 2: deplacement à haut")
            if len(self.action)==3:
                self.action3.set("Action 3: deplacement à haut") 
        else:
            print("liste full")

    def AppendDB(self):
        if len(self.action)<3:
            self.action.append(self.deplacement_bas)
            if len(self.action)==1:
                self.action1.set("Action 1: deplacement à bas")
            if len(self.action)==2:
                self.action2.set("Action 2: deplacement à bas")
            if len(self.action)==3:
                self.action3.set("Action 3: deplacement à bas") 
        else:
            print("liste full")

    def AppendBR(self):
        if len(self.action)<3:
            self.action.append(self.braquage)
            if len(self.action)==1:
                self.action1.set("Action 1: Braquage")
            if len(self.action)==2:
                self.action2.set("Action 2: Braquage")
            if len(self.action)==3:
                self.action3.set("Action 3: Braquage") 
        else:
            print("liste full")

    def reset(self):
        self.action1.set("Action 1:")
        self.action2.set("Action 2:")
        self.action3.set("Action 3:")
        self.action.clear()

    def Confirmation(self):
        if not(self.action):
            print("Liste vide")
        elif len(self.action)!=3:
            print("liste incomplete")
        else:
            if self.action[0] == self.deplacement_droit:
                self.deplacement_droit()
            if self.action[0] == self.deplacement_gauche:
                self.deplacement_gauche()
            if self.action[0] == self.deplacement_haut:
                self.deplacement_haut()
            if self.action[0] == self.deplacement_bas:
                self.deplacement_bas()
            if self.action[0] == self.braquage:
                self.braquage()
            self.after(1000, self.Confirmation2)

    def Confirmation2(self):
        if self.action[1] == self.deplacement_droit:
            self.deplacement_droit()
        if self.action[1] == self.deplacement_gauche:
            self.deplacement_gauche()
        if self.action[1] == self.deplacement_haut:
            self.deplacement_haut()
        if self.action[1] == self.deplacement_bas:
            self.deplacement_bas()
        if self.action[1] == self.braquage:
            self.braquage()
        self.after(1000, self.Confirmation3)

    def Confirmation3(self):      
        if self.action[2] == self.deplacement_droit:
            self.deplacement_droit()
        if self.action[2] == self.deplacement_gauche:
            self.deplacement_gauche()
        if self.action[2] == self.deplacement_haut:
            self.deplacement_haut()
        if self.action[2] == self.deplacement_bas:
            self.deplacement_bas()
        if self.action[2] == self.braquage:
            self.braquage()
        self.action1.set("Action 1:")
        self.action2.set("Action 2:")
        self.action3.set("Action 3:")        
        self.action.clear()
        self.nb_tour -= 1
        self.tour.config(text=f"Tour restant : {self.nb_tour}")
        if self.nb_tour == 0:
            self.fin_de_jeu()

    #Déplacement droit du bandit
    def deplacement_droit(self):
        pos = self.bandit1.position
        place = self.bandit1.place
        if self.bandit1.place == "exterieur":
            self.exterieur[pos] = []
            pos += 1
            if pos > len(self.exterieur)-1:
                pos -= 1
                self.exterieur[pos].append("B1")
                self.liste.insert(0, f"{self.bandit1.nom_bandit} ne peut pas se déplacer à droite !") 
            else:                
                self.bandit1.position = pos
                self.exterieur[pos].append("B1")
                self.liste.insert(0, f"Déplacement à droite de {self.bandit1.nom_bandit}")

                self.label_bandit.destroy()
                self.x += 110
                if self.x > 700:
                    self.x = 700
                self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
                self.label_bandit.place(x = self.x, y = self.y)       
                self.IA_sheriff()
        else:
            self.interieur[pos] = []
            pos += 1
            if pos > len(self.interieur)-1:
                pos -= 1
                self.interieur[pos].append("B1")
            else:
                self.bandit1.position = pos
                self.interieur[pos].append("B1")
                self.liste.insert(0, f"Déplacement à droite de {self.bandit1.nom_bandit}")               
            if self.bandit1.position == self.position_sheriff:
                self.perd_argent()
            self.label_bandit.destroy()
            self.x += 110

            if self.x > 700:
                self.x = 700
            self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
            self.label_bandit.place(x = self.x, y = self.y)        
            self.IA_sheriff()


    #Déplacement gauche du bandit      
    def deplacement_gauche(self):
        pos = self.bandit1.position
        place = self.bandit1.place
        if self.bandit1.place == "exterieur":
            self.exterieur[pos] = []
            pos -= 1
            if pos < 0:
                pos += 1
                self.exterieur[pos].append("B1") 
                self.liste.insert(0, f"{self.bandit1.nom_bandit} ne peut pas se déplacer à gauche !")
            else:
                self.bandit1.position = pos
                self.exterieur[pos].append("B1")
                self.liste.insert(0, f"Déplacement à gauche de {self.bandit1.nom_bandit}")
                self.label_bandit.destroy()
                self.x -= 110
                if self.x < 250:
                    self.x = 250     
                self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
                self.label_bandit.place(x = self.x, y = self.y)
                self.IA_sheriff()
        else:
            self.interieur[pos] = []

            pos -= 1
            if pos < 0:
                pos += 1
                self.interieur[pos].append("B1")
            else:
                self.bandit1.position = pos

                self.interieur[pos].append("B1")

                self.liste.insert(0, f"Déplacement à gauche de {self.bandit1.nom_bandit}")

            if self.bandit1.position == self.position_sheriff:
                self.perd_argent()

            self.label_bandit.destroy()
            self.x -= 110
            if self.x < 250:
                self.x = 250 
            self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
            self.label_bandit.place(x = self.x, y = self.y)      
            self.IA_sheriff()

    #Déplacement bas du bandit
    def deplacement_bas(self):
        pos = self.bandit1.position
        place = self.bandit1.place

        if self.bandit1.place == "exterieur":
            self.exterieur[pos] = []
            self.bandit1.place = "interieur"
            self.interieur[pos].append("B1")


            self.liste.insert(0, f"{self.bandit1.nom_bandit} rentre à l'interieur")
            

            self.label_bandit.destroy()
            self.y += 60    
            self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
            self.label_bandit.place(x = self.x, y = self.y) 

            if self.bandit1.position == self.position_sheriff:
                self.perd_argent()
            
            self.IA_sheriff()

    #Déplacement haut du bandit
    def deplacement_haut(self):
        self.IA_sheriff()
        pos = self.bandit1.position
        place = self.bandit1.place

        if self.bandit1.place == "interieur":
            self.interieur[pos] = []
            self.bandit1.place = "exterieur"
            self.exterieur[pos].append("B1")

            self.liste.insert(0, f"{self.bandit1.nom_bandit} grimpe sur le toit")            

            self.label_bandit.destroy()
            self.y -= 60    
            self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
            self.label_bandit.place(x = self.x, y = self.y)

    #Braquage des passager
    def braquage(self):
        self.IA_sheriff()
        global score
        butin = self.argent[self.bandit1.position]
        if self.interieur == [[],[],[],[],[]]:
            self.liste.insert(0, f"Braquage : Il n'y a personne sur le toit du train")
            self.label_bandit.destroy() 
            self.label_bandit = Label(self,text="B1", bg='white',font = ('Helvatical bold',19))
            self.label_bandit.place(x = self.x, y = self.y)

            if self.bandit1.position == self.position_sheriff:
                self.perd_argent() 
        else:
            if butin != []:
                if self.bandit1.position == self.position_sheriff:
                    self.perd_argent()    
                a = butin[0]
                self.liste.insert(0, f"{self.bandit1.nom_bandit} a détroussé les voyageurs ({butin[0]})")
                self.audio_braquage.play()
                butin.pop(0)
                self.argent[self.bandit1.position] == butin
                self.bandit1.score.append(a)
                if a == "bourse":
                    score += 100
                    self.labelscore = "Votre score : " + str(score)
                    self.var_label.set(self.labelscore)
                if a == "bourses":
                    score += 200
                    self.labelscore = "Votre score : " + str(score)
                    self.var_label.set(self.labelscore)
                if a == "bijou":
                    score += 500
                    self.labelscore = "Votre score : " + str(score)
                    self.var_label.set(self.labelscore)
                if a == "magot":
                    score += 1000
                    self.labelscore = "Votre score : " + str(score)
                    self.var_label.set(self.labelscore)

                self.wagon1.configure(text=f"Wagon 1 : {self.argent[3]}")
                self.wagon2.configure(text=f"Wagon 2 : {self.argent[2]}")
                self.wagon3.configure(text=f"Wagon 3 : {self.argent[1]}")
                self.wagon4.configure(text=f"Wagon 4 : {self.argent[0]}")
                self.locomotive.configure(text=f"Locomotive : {self.argent[4]}")
            else:
                self.liste.insert(0, f"Braquage : plus rien à braquer dans ce wagon")
                if self.bandit1.position == self.position_sheriff:
                    self.perd_argent()                  
                

    #Tirer sur les autres bandits
    def tir(self):
        pass

    #Son du jeu et changement d'icone du bouton
    def Son(self):
        global i
        if self.son==True:
            self.btn_son['image'] = self.mute
            self.audio_jeu.set_volume(0)
            self.audio_train.set_volume(0)
            self.audio_fin.set_volume(0)
            self.audio_braquage.set_volume(0)
            self.audio_tir.set_volume(0)
            self.son = False
        else:
            self.btn_son['image'] = self.icone
            self.audio_jeu.set_volume(1)
            self.audio_train.set_volume(0.5)
            self.audio_fin.set_volume(0.5)
            self.audio_braquage.set_volume(0.5)
            self.audio_tir.set_volume(0.5)
            self.son = True

    #Quand un bandit se fait tirer dessus
    def perd_argent(self):
        global score
        pos = self.bandit1.position

        if self.bandit1.score !=[]:
            item = self.bandit1.score[len(self.bandit1.score)-1]
            self.audio_tir.play()
            self.liste.insert(0, f"{self.bandit1.nom_bandit}, s'est fait tirer dessus !")
            self.liste.insert(0, f"{self.bandit1.nom_bandit} a perdu {item}")
            self.bandit1.score.pop(len(self.bandit1.score)-1)
            self.argent[pos].append(item)
            if item == "bourse":
                score -= 100
                self.labelscore = "Votre score : " + str(score)
                self.var_label.set(self.labelscore)
            if item == "bourses":
                score -= 200
                self.labelscore = "Votre score : " + str(score)
                self.var_label.set(self.labelscore)
            if item == "bijou":
                score -= 500
                self.labelscore = "Votre score : " + str(score)
                self.var_label.set(self.labelscore)
            if item == "magot":
                score -= 1000
                self.labelscore = "Votre score : " + str(score)
                self.var_label.set(self.labelscore)            

            self.wagon1.configure(text=f"Wagon 1 : {self.argent[3]}")
            self.wagon2.configure(text=f"Wagon 2 : {self.argent[2]}")
            self.wagon3.configure(text=f"Wagon 3 : {self.argent[1]}")
            self.wagon4.configure(text=f"Wagon 4 : {self.argent[0]}")
            self.locomotive.configure(text=f"Locomotive : {self.argent[4]}")

            self.deplacement_haut()
        else:

            self.audio_tir.play()
            self.liste.insert(0, f"{self.bandit1.nom_bandit}, s'est fait tirer dessus !")
            self.deplacement_haut()


    #IA du Marshall
    def IA_sheriff(self):
        pos = self.position_sheriff
        lieu = self.sherif
        choix = self.choix
        if pos == 4:
            self.choix = -1
        elif pos == 0:
            self.choix = 1
        else:
            self.choix = 2
        if self.choix == 2:
            deplacement = randint(0, 1)
            if deplacement == 0:
                self.sherif[self.position_sheriff] = []
                self.position_sheriff += -1
                self.sherif[self.position_sheriff] = ["M"]

                self.label_marshall.destroy()
                self.i -= 105    
                self.label_marshall = Label(self,text="M", bg='white',font = ('Helvatical bold',17))
                self.label_marshall.place(x = self.i, y = self.j)

            else:
                self.sherif[self.position_sheriff] = []
                self.position_sheriff += 1
                self.sherif[self.position_sheriff] = ["M"]

                self.label_marshall.destroy()
                self.i += 105    
                self.label_marshall = Label(self,text="M", bg='white',font = ('Helvatical bold',17))
                self.label_marshall.place(x = self.i, y = self.j)

        elif self.choix == 1:
            self.sherif[self.position_sheriff] = []
            self.position_sheriff += self.choix
            self.sherif[self.position_sheriff] = ["M"]

            self.label_marshall.destroy()
            self.i += 105    
            self.label_marshall = Label(self,text="M", bg='white',font = ('Helvatical bold',17))
            self.label_marshall.place(x = self.i, y = self.j)

        else:
            self.sherif[self.position_sheriff] = []
            self.position_sheriff += self.choix
            self.sherif[self.position_sheriff] = ["M"]   

            self.label_marshall.destroy()
            self.i -= 105    
            self.label_marshall = Label(self,text="M", bg='white',font = ('Helvatical bold',17))
            self.label_marshall.place(x = self.i, y = self.j)

    def fuir(self):
        a = messagebox.askquestion("Voulez vous vraiment fuir ?")
        if a == "yes":
            self.fin_de_jeu()


    def fin_de_jeu(self):
        self.audio_train.stop()
        self.audio_jeu.stop()
        self.audio_fin.play()
        score_final = 0
        for i in range(0, len(self.bandit1.score)):
            if self.bandit1.score[i] == "bourse":
                score_final += 100
            if self.bandit1.score[i] == "bourses":
                score_final += 200
            if self.bandit1.score[i] == "bijou":
                score_final += 500
            if self.bandit1.score[i] == "magot":
                score_final += 1000

        print("Résultat :")
        print(f"{self.bandit1.nom_bandit} à obtenu {score_final} dollars")
        print("########################################")

        self.labelscore = "Votre score : " + str(score_final)
        self.var_label.set(self.labelscore)
        label = ttk.Label(self, text=f"{self.bandit1.nom_bandit} à obtenu {score_final} dollars", font = ('Helvatical bold',40), background='red')
        label.place(x=500 ,y=400, anchor="center")
        self.after(4585,lambda: self.quit())


        return score_final



class Bandit(Tk):
    def __init__(self):

        self.nom_bandit = ""
        self.score = []
        self.position = 0
        self.action = []
        self.place = "exterieur"

class Butin:
    def __init__(self):
        super().__init__()
        self.marshall = bool
    def init(self):
        global i
        argent = [["","","",""],["","","",""],["","","",""],["","","",""]]
        butin = ["bourse","bourses","bijou"]
        for i in range(0,len(argent)):
            for j in range(0,len(argent)):
                r = randint(0, 2)
                a = butin[r]
                argent[i][j] = a
        argent.append(["magot"])
        self.total(argent)
        return argent

    def total(self,argent):
        butin_total = 0
        for i in range(0, 4):
            for j in range(0, 4):
                if argent[i][j] == "bourse":
                    butin_total += 100
                if argent[i][j] == "bourses":
                    butin_total += 200
                if argent[i][j] == "bijou":
                    butin_total += 500
        butin_total += 1000
        return butin_total

    
print("########################################")
print("#######       COLT EXPRESS       #######")
print("########################################")
print()


app = Application()
app.mainloop()

print("########################################")
print("# Jeu terminé, merci d'avoir joué ######")
print("########################################")

print()
print("########################################")
print("#######         CREDITS          #######")
print("########################################")
print("# Auteur :         #####################")
print("# Bernier Vincent  #####################")
print("# Poumier Antonin  #####################")
print("# L2-B STN         #####################")
print("########################################")

print("# Crédits :                       ######")
print("# Music du jeu :                  ######") 
print("# David Randel Saddle Up          ######")
print("# 8-Bit RPG Music - Victory Theme ######")
print("########################################")

