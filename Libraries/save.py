from tkinter import font, ttk, filedialog
from reportlab.pdfgen import canvas as reportlab_canvas
from reportlab.lib.pagesizes import letter
import tempfile

def sauvegarder_texte(): #Sauvegarde la traduction en pdf
    chemin_fichier = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])

    if chemin_fichier:
        chemin_image = "Images/printWTRMK.jpg"
        image = Image.open(chemin_image)

        pdf = reportlab_canvas.Canvas(chemin_fichier, pagesize=letter)
        pdf.setFont("Helvetica", 12)

        nouvelle_largeur = image.width / 1.5
        nouvelle_hauteur = image.height / 1.5

        x_aligne_gauche = 0
        y_haut = letter[1] - nouvelle_hauteur

        pdf.drawInlineImage(chemin_image, x_aligne_gauche, y_haut, width=nouvelle_largeur, height=nouvelle_hauteur)

        contenu = zone_texte_2.get(1.0, tk.END)
        
        contenu = contenu.replace("■", "\n")

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