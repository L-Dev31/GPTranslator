#  -----------------------------------------------------------------------------
#  GPTranslator 2024
#  Ce logiciel en python a été développé dans le cadre du concours "Trophées NSI"
#
#  Graphisme de l'interface : Léo Tosku
#  Programmation : Léo Tosku, Korail Lamothe Jacob
#  Base de donnée C.Guadeloupéen-Français : Léo Tosku, Korail Lamothe Jacob 
#
#  Sonny Rupaire - Sainte Rose (97129) - Guadeloupe (971)
#  -----------------------------------------------------------------------------           
#                     
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@          
#  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  
#  @@@@@@@@@@@@@@@@@@@@@@@@@                             
#  @@@@@@@@@@@@@@@@@@@@@@                 
#              @@@@@@@@                    
#              @@@@@@                      
#              @@@@@                       
#              @@@@                        
#              @@@                         
#               @                          
#                                          

#Biblioteques
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import font, ttk, filedialog
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.pagesizes import letter
import tempfile
import webbrowser

#Biblioteques de GPTranslator
from Libraries.traduction import traduire_texte
from Libraries.save import sauvegarder_texte

#Langues de traductions
langue_source = 'fr'  
langue_cible = 'ht'   

#Fonctions d'apparences
def redimensionner_element(event):
    canvas.coords(langue1, 200, 48)
    canvas.coords(langue2, 600, 48)
    canvas.coords(zone_texte, larg_init / 4 - 160, (haut_init - 50) / 2.3)
    canvas.coords(zone_texte_2, larg_init / 4 + 260, (haut_init - 50) / 2.3)

def survol_entree(tag):
    changer_image(tag, actif=True)

def survol_sortie(tag):
    changer_image(tag, actif=False)

def copier_texte(): #Copie dans le presse papier
    contenu_texte_2 = zone_texte_2.get("1.0", tk.END)
    fenetre.clipboard_clear()
    fenetre.clipboard_append(contenu_texte_2)
    fenetre.update()

def changer_image(tag, actif):
    if tag == "image_survol":
        chemin_image = "Images/activatedTSLARW.png" if actif else "Images/deactivatedTSLARW.png"
        nouvelle_image = Image.open(chemin_image).resize((50, 50), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
        nouvelle_image_tk = ImageTk.PhotoImage(nouvelle_image)
        canvas.itemconfig(tag, image=nouvelle_image_tk)
        canvas.image_translation = nouvelle_image_tk
    elif tag == "image_survol_2":
        chemin_image = "Images/activatedSWARW.png" if actif else "Images/deactivatedSWARW.png"
        nouvelle_image = Image.open(chemin_image).resize((40, 40), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
        nouvelle_image_tk = ImageTk.PhotoImage(nouvelle_image)
        canvas.itemconfig(tag, image=nouvelle_image_tk)
        canvas.image_switch = nouvelle_image_tk  
    elif tag == "image_survol_print":
        chemin_image = "Images/activatedPRTBTN.png" if actif else "Images/deactivatedPRTBTN.png"
        nouvelle_image = Image.open(chemin_image).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
        nouvelle_image_tk = ImageTk.PhotoImage(nouvelle_image)
        print_button.configure(image=nouvelle_image_tk)
        print_button.image_print = nouvelle_image_tk
    elif tag == "image_survol_copy":
        chemin_image = "Images/activatedCPYBTN.png" if actif else "Images/deactivatedCPYBTN.png"
        nouvelle_image = Image.open(chemin_image).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
        nouvelle_image_tk = ImageTk.PhotoImage(nouvelle_image)
        copy_btn.configure(image=nouvelle_image_tk)
        copy_btn.image_copy = nouvelle_image_tk
    elif tag == "image_survol_save":
        chemin_image = "Images/activatedSAVBTN.png" if actif else "Images/deactivatedSAVBTN.png"
        nouvelle_image = Image.open(chemin_image).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
        nouvelle_image_tk = ImageTk.PhotoImage(nouvelle_image)
        save_btn.configure(image=nouvelle_image_tk)
        save_btn.image_save = nouvelle_image_tk

def texte_pied_page(): #texte footer
    texte_bas = "GPTranslator, 2024. Léo Tosku - Korail Lamothe Jacob "
    police_texte_bas = ("SeuratPro", 12)
    x_bas = larg_init / 2
    y_bas = (haut_init + 50) / 2 + 140
    canvas.create_text(x_bas, y_bas, text=texte_bas, font=police_texte_bas, fill="black", anchor=tk.CENTER, tag="footer_text")
    canvas.tag_raise("footer_text")
    return y_bas

#Traductions
def changer_langue(event): #Inversion de la langue source/cible
    echange_contenu()
    texte1 = canvas.itemcget(langue1, "text")
    texte2 = canvas.itemcget(langue2, "text")
    canvas.itemconfig(langue1, text=texte2)
    canvas.itemconfig(langue2, text=texte1)
    global langue_source, langue_cible
    langue_source, langue_cible = langue_cible, langue_source
    traduire_texte_zone_1()

def echange_contenu(): #Inversion des textes 
    contenu_texte_1 = zone_texte.get(1.0, tk.END)
    contenu_texte_2 = zone_texte_2.get(1.0, tk.END)
    zone_texte_2.config(state=tk.NORMAL)
    zone_texte.delete(1.0, tk.END)
    zone_texte.insert(tk.END, contenu_texte_2.strip())
    zone_texte_2.delete(1.0, tk.END)
    zone_texte_2.insert(tk.END, contenu_texte_1.strip())
    zone_texte_2.config(state=tk.DISABLED)

def traduire_texte_zone_1(event=None):
    contenu_zone_texte_1 = zone_texte.get(1.0, tk.END).strip()
    texte_traduit = traduire_texte(contenu_zone_texte_1, langue_source, langue_cible)
    
    texte_formate = ""
    for phrase in texte_traduit.split(". "):
        phrase_formatee = phrase.capitalize()
        texte_formate += phrase_formatee + ". "

    texte_formate = texte_formate[:-2]

    zone_texte_2.config(state=tk.NORMAL)
    zone_texte_2.delete(1.0, tk.END)
    zone_texte_2.insert(tk.END, texte_formate)
    zone_texte_2.config(state=tk.DISABLED)

def imprimer_texte(): #Impression du .pdf
    fichier_temporaire = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    chemin_fichier_temporaire = fichier_temporaire.name
    fichier_temporaire.close()

    chemin_image = "Images/printWTRMK.jpg"
    contenu = zone_texte_2.get(1.0, tk.END)

    image = Image.open(chemin_image)
    pdf = reportlab_canvas.Canvas(chemin_fichier_temporaire, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    nouvelle_largeur = image.width / 1.5
    nouvelle_hauteur = image.height / 1.5

    x_aligne_gauche = 0
    y_haut = letter[1] - nouvelle_hauteur

    pdf.drawInlineImage(chemin_image, x_aligne_gauche, y_haut, width=nouvelle_largeur, height=nouvelle_hauteur)

    contenu = contenu.replace("■■", "\n")

    x_texte_gauche = x_aligne_gauche + 10
    y_texte_bas = y_haut - 10 - 15

    largeur_texte_max = letter[0] - x_texte_gauche - 10

    lignes = contenu.split('\n')
    objet_texte = pdf.beginText(x_texte_gauche, y_texte_bas)
    objet_texte.setFont("Helvetica", 12)
    objet_texte.setFillColorRGB(0, 0, 0)

    for ligne in lignes:
        objet_texte.textLine(ligne)

    pdf.drawText(objet_texte)

    pdf.save()

    webbrowser.open(chemin_fichier_temporaire)

#Apparence
fenetre = tk.Tk()
fenetre.title("GPTranslator")

img_icone = "Images/icon.png"
icone = Image.open(img_icone).resize((32, 32), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
icone_tk = ImageTk.PhotoImage(icone)
fenetre.iconphoto(True, icone_tk)

chemin_police = "Font/seurat_pro.otf"
fenetre.tk.call("tk", "scaling", 2.0)
police_personnalisee = font.Font(family="SeuratPro", size=13, weight="normal")

style = ttk.Style()
style.configure("EtiquettePerso.TLabel", font=police_personnalisee)

larg_init = 800
haut_init = 480

chemin_img_fond = "Images/bgimg.jpg"
img_fond = Image.open(chemin_img_fond).resize((larg_init, haut_init - 50), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
photo_fond = ImageTk.PhotoImage(img_fond)

canvas = tk.Canvas(fenetre, width=larg_init, height=haut_init - 50)
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=photo_fond, tags="bg_image")

langue1 = canvas.create_text(200, 48, text="Français", font=("SeuratPro", 13), fill="black")
langue2 = canvas.create_text(600, 48, text="Créole Guadeloupéen", font=("SeuratPro", 13), fill="black")

chemin_img_survol = "Images/deactivatedTSLARW.png"
img_traduction = Image.open(chemin_img_survol).resize((50, 50), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
img_traduction_tk = ImageTk.PhotoImage(img_traduction)

canvas.create_image(larg_init / 2, (haut_init - 50) / 2 - 50, anchor=tk.CENTER, image=img_traduction_tk, tags="image_survol")
canvas.image_translation = img_traduction_tk

chemin_img_survol_2 = "Images/deactivatedSWARW.png"
img_switch = Image.open(chemin_img_survol_2).resize((40, 40), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
img_switch_tk = ImageTk.PhotoImage(img_switch)

canvas.create_image(larg_init / 2, (haut_init - 50) / 2 + 30, anchor=tk.CENTER, image=img_switch_tk, tags="image_survol_2")
canvas.image_switch = img_switch_tk

chemin_img_copie = "Images/deactivatedCPYBTN.png"
img_copie = Image.open(chemin_img_copie).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
img_copie_tk = ImageTk.PhotoImage(img_copie)

y_bas = texte_pied_page()

copy_btn = ttk.Button(fenetre, image=img_copie_tk, style="EtiquettePerso.TLabel", command=copier_texte)
copy_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
copy_btn.image_copy = img_copie_tk

chemin_img_sauvegarde = "Images/deactivatedSAVBTN.png"
img_sauvegarde = Image.open(chemin_img_sauvegarde).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
img_sauvegarde_tk = ImageTk.PhotoImage(img_sauvegarde)

save_btn = ttk.Button(fenetre, image=img_sauvegarde_tk, style="EtiquettePerso.TLabel", command=sauvegarder_texte)
save_btn.place(relx=0.4, rely=0.8, anchor=tk.CENTER)
save_btn.image_save = img_sauvegarde_tk

chemin_img_impression = "Images/deactivatedPRTBTN.png"
img_impression = Image.open(chemin_img_impression).resize((25, 25), Image.BICUBIC if hasattr(Image, 'BICUBIC') else Image.BICUBIC)
img_impression_tk = ImageTk.PhotoImage(img_impression)

print_button = ttk.Button(fenetre, image=img_impression_tk, style="EtiquettePerso.TLabel", command=imprimer_texte)
print_button.place(relx=0.6, rely=0.8, anchor=tk.CENTER)
print_button.image_print = img_impression_tk

#Zone de texte 0 (langue source)
zone_texte = tk.Text(
    fenetre,
    wrap="word",
    height=10,
    width=int(40 * 0.75),
    font=("SeuratPro", 9),
    bd=0,
    insertbackground='black',
    selectbackground='pink',
)
zone_texte.place(x=larg_init / 4 - 160, y=(haut_init - 50) / 2.3, anchor=tk.W)

#Zone de texte 1 (langue cible)
zone_texte_2 = tk.Text(
    fenetre,
    wrap="word",
    height=10,
    width=int(40 * 0.75),
    font=("SeuratPro", 9),
    bd=0,
    insertbackground='black',
    selectbackground='lightblue',
)
zone_texte_2.place(x=larg_init / 4 + 260, y=(haut_init - 50) / 2.3, anchor=tk.W)
zone_texte_2.config(state=tk.DISABLED)

#transitions des images en survol et actions..
canvas.tag_bind("image_survol", "<Enter>", lambda event: survol_entree("image_survol"))
canvas.tag_bind("image_survol", "<Leave>", lambda event: survol_sortie("image_survol"))

canvas.tag_bind("image_survol_2", "<Enter>", lambda event: survol_entree("image_survol_2"))
canvas.tag_bind("image_survol_2", "<Leave>", lambda event: survol_sortie("image_survol_2"))

canvas.tag_bind("image_survol_2", "<Button-1>", changer_langue)
canvas.tag_bind("image_survol", "<Button-1>", traduire_texte_zone_1)

copy_btn.bind("<Enter>", lambda event: survol_entree("image_survol_copy"))
copy_btn.bind("<Leave>", lambda event: survol_sortie("image_survol_copy"))

save_btn.bind("<Enter>", lambda event: survol_entree("image_survol_save"))
save_btn.bind("<Leave>", lambda event: survol_sortie("image_survol_save"))

print_button.bind("<Enter>", lambda event: survol_entree("image_survol_print"))
print_button.bind("<Leave>", lambda event: survol_sortie("image_survol_print"))

#Interdiction du resize de la fenaître
fenetre.resizable(width=False, height=False)

fenetre.mainloop()


