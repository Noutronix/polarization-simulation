import tkinter as tk
import math
import functools as ft
import sys

def probability(polarizations):
    '''gives the percentage of light that passes through all of the filters'''
    if len(polarizations) != 1:
        polarization1 = polarizations[0]*math.pi/180
        polarization2 = polarizations[1]*math.pi/180
        return round(probability(polarizations[1:])*math.cos(abs(polarization1-polarization2))**2, 3)
    else:
        return 1


def master(input, filter_num=2, rotations=None, input2=None):
    
    clean()
    
    if filter_num < 2:
        filter_num = 2
    if filter_num > 5:
        filter_num = 5

    if rotations==None:
        rotations=[0, 0]

    frm_filters = tk.Frame()

    filters = []
    for i in range(filter_num):
        filters.append(filter(i+1, frm_filters, rotations, (rotations[i] if i<len(rotations) else "0")))
    frm_filters.pack()
    
    c = controls(filters)


def recreate(input, filters, control, input2):
    numbers = list("1234567890.")
    f_num = control.ent_filter_num.get()
    f_num = (2 if not all(i in numbers for i in list(f_num)) or f_num=="" else int(f_num))
    rotations = [f.ent_rotation.get() for f in filters]
    rotations = [int(x) if all(i in numbers for i in list(x)) and x != "" else 0 for x in rotations]
    master(None, f_num, rotations)


class controls:
    def __init__(self, filters):
        self.frm_controls = tk.Frame(relief=tk.GROOVE, borderwidth=5)
        self.frm_controls.pack()

        txt = "Pourcentage de lumière qui passe: {}%".format(round(probability([int(f.ent_rotation.get()) for f in filters])*50, 4))
        self.lbl_brightness = tk.Label(master=self.frm_controls, text=txt)
        self.lbl_brightness.pack()

        self.lbl_filters = tk.Label(master=self.frm_controls, text="Nombre de filtres:")
        self.lbl_filters.pack()

        self.ent_filter_num = tk.Entry(master=self.frm_controls)
        self.ent_filter_num.insert(0, len(filters))
        self.ent_filter_num.pack()

        self.frm_btns = tk.Frame(master=self.frm_controls)
        self.frm_btns.pack()

        self.btn_confirm = tk.Button(master=self.frm_btns, text="Confirmer changements")
        self.btn_confirm.bind("<Button-1>", ft.partial(recreate, 0, filters, self))
        self.btn_confirm.pack(side=tk.LEFT)

        self.btn_return = tk.Button(master=self.frm_btns, text="Retourner au menu")
        self.btn_return.bind("<Button-1>", main)
        self.btn_return.pack(side=tk.RIGHT)


def clean():
    for widget in window.winfo_children():
        widget.pack_forget()



class filter():
    def __init__(self, number, frame, rotations, rotation=0):
        self.number = number

        self.frame = tk.Frame(master=frame, relief=tk.SUNKEN, borderwidth=5)
        self.frame.pack(side=tk.LEFT)

        self.lbl_num = tk.Label(master=self.frame, text="Filtre numéro {}".format(str(number)))
        self.lbl_num.pack()

        self.lbl_rotation = tk.Label(master=self.frame, text="Rotation (en degrées):")
        self.lbl_rotation.pack()

        self.ent_rotation = tk.Entry(master=self.frame)
        self.ent_rotation.insert(0, rotation)
        self.ent_rotation.pack()

        self.light(rotations)

    def light(self, rotations):
        
        if self.number == "1":
            r, g, b = (int(0.5*225) for i in range(3))
        else:
            r, g, b = (int(225*0.5*probability(rotations[:int(self.number)])) for i in range(3))
        
        shade = f'#{r:02x}{g:02x}{b:02x}'
        
        frm = tk.Frame(master=self.frame, relief=tk.SUNKEN, borderwidth=2, bg=shade, width=100, height=50)
        frm.pack()




def bibliographie1(input):
    clean()

    lbl_1 = tk.Label(text='"Quantum Polar Filter." *Math is Fun*, https://www.mathsisfun.com/physics/quantum-polar-filter.html, accédé le 6 Février 2023.')
    lbl_1.pack()
    lbl_annotation1 = tk.Label(text="La source ci-dessus était surtout utile pour trouver la formule I = cos(θ)^2; elle fournit aussi des exemples de la mathematique qui sous-entend la polarisation.")
    lbl_annotation1.pack()
    
    lbl_empty1 = tk.Label()
    lbl_empty1.pack()

    lbl_2 = tk.Label(text='Amos, David. "Python GUI Programming With Tkinter." *Real Python*, https://realpython.com/python-gui-tkinter/, accédé le 6 Février 2023.')
    lbl_2.pack()
    lbl_annotation2 = tk.Label(text="Cette source était essentielle pour que je puisse faire le GUI pour cette simulation. Elle demontre comment utiliser les boutons et les 'entries' pour recevoir de l'information de l'utilisateur.")
    lbl_annotation2.pack()

    lbl_empty2 = tk.Label()
    lbl_empty2.pack()

    btn_return = tk.Button(text="Retourner au menu")
    btn_return.bind("<Button-1>", main)
    btn_return.pack()

    lbl_empty3 = tk.Label()
    lbl_empty3.pack()


def main(input=None):
    clean()
    
    btn_start = tk.Button(text="Commencer la simulation")
    btn_start.bind("<Button-1>", master)
    btn_start.pack()

    btn_biblio = tk.Button(text="Voir la bibliographie")
    btn_biblio.bind("<Button-1>", bibliographie1)
    btn_biblio.pack()

    btn_exit = tk.Button(text="Arrêter la simulation")
    btn_exit.bind("<Button-1>", exit)
    btn_exit.pack()

try:
    window = tk.Tk()
    main()
    window.mainloop()
except:
    sys.exit(0)

def exit(input):
    sys.exit(0)
