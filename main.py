import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas

import subprocess
import sys

#from addiction_3 import main

# Chemin absolu vers l'interpréteur Python
python_path = sys.executable

def run_script():
    #main(['C','S','E','V','A'])
    subprocess.run([python_path, "projetS6.py"])

def run_script_inter():
    subprocess.run([python_path, "projetS6_Addiction_Groupe.py"])

def variation_p():
    subprocess.run([python_path, "projetS6_Variation_p.py"])

def variation_lambda():
    subprocess.run([python_path, "projetS6_Variation_lambda.py"])

def variation_env():
    subprocess.run([python_path, "projetS6_Variation_Environnement.py"])

fenetre = tk.Tk()
fenetre.title("Modélisation de l'évolution d'un comportement addictif")
fenetre.state('zoomed')

bg_image = tk.PhotoImage(file="addictions.png")
bg_label = tk.Label(fenetre, image=bg_image)
bg_label.place(relx=0.5, rely=0.5, anchor="center")

titre_label = tk.Label(fenetre, text="Evolution d'un comportement addictif", font=("Helvetica", 24))
titre_label.place(relx=0.5, rely=0.1, anchor="center")

# Fonction pour réinitialiser les cases à cocher
def reset_checkboxes():
    for chk in chks:
        chk.set(0)

def on_click():
    selected_function_names = [var[i] for i, chk in enumerate(chks) if chk.get()]

    if (selected_function_names == []):
        messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins une fonction.")
        return
    
    main(selected_function_names)
    reset_checkboxes()

texte_label = tk.Label(fenetre, text="Modèle à 1 patient", font=("Helvetica", 12))
texte_label.place(relx=0.34, rely=0.23, anchor="center")

texte_label = tk.Label(fenetre, text="Choisissez les courbes que vous souhaitez afficher", font=("Helvetica", 10))
texte_label.place(relx=0.20, rely=0.3, anchor="center")

names = ["Intensité de désir (C)", "Intensité de self-control (S)", "Influence sociétale (E)", "Niveau de vulnérabilité (V)", "Addiction exercée (A)"]
var = ["C", "S", "E", "V", "A"]

chks = [tk.BooleanVar() for i in var]

for i, s in enumerate(var):
    chk = tk.Checkbutton(fenetre, text=names[i], variable=chks[i]).place(relx=0.20, rely=0.35 + i*0.05, anchor="center")

submit_button = tk.Button(fenetre, text="Valider", command=on_click).place(relx=0.20, rely=0.63, anchor="center")

# Bouton "Lancer le script principal"
run_button = tk.Button(fenetre, text="Lancer le script principal", command=run_script).place(relx=0.20, rely=0.8, anchor="center")

# Bouton "Variation p"
p_vari_button = tk.Button(fenetre, text="Variation en fonction de p", command=variation_p).place(relx=0.45, rely=0.35, anchor="center")

# Bouton "Variation lambda"
lambda_vari_button = tk.Button(fenetre, text="Variation en fonction de lambda", command=variation_lambda).place(relx=0.45, rely=0.45, anchor="center")

# Bouton "Variation environnement"
env_vari_button = tk.Button(fenetre, text="Variation en fonction de l'environnement", command=variation_env).place(relx=0.45, rely=0.55, anchor="center")

# Texte "Modèle à 2 patients"
texte_label = tk.Label(fenetre, text="Modèle à 2 patients", font=("Helvetica", 12))
texte_label.place(relx=0.80, rely=0.23, anchor="center")

# Bouton "Modèle avec interraction entre 2 patients"
inter_button = tk.Button(fenetre, text="Modèle à 2 patients", command=run_script_inter).place(relx=0.80, rely=0.35, anchor="center")

# Création du ligne verticale pour séparer les 2 modèles
canvas_vertical = Canvas(fenetre, width=2, height=600)
canvas_vertical.create_line(50, 0, 50, 600, fill="black", width=1)  # Dessine une ligne verticale à la position x=50
canvas_vertical.place(relx=0.63, rely=0.65, anchor="center")


fenetre.mainloop()