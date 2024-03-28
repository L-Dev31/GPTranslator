import re
import string
import requests
import json

def charger_base_de_donnees(langue_cible): #Chargement de la base de donnée Creole Guadeloupéen-Français
    nom_fichier = f"Dictionary/LngDB-{langue_cible.lower()}.json"
    with open(nom_fichier, "r", encoding="utf-8") as fichier_json:
        return json.load(fichier_json)
    
def traduire_texte(texte, langue_source='fr', langue_cible='ht'): #Traduction Creole Guadeloupéen-Français
    base_de_donnees = charger_base_de_donnees(langue_cible)
    traduction = []

    mots = re.findall(r"[\w’]+(?:'\w+)?|¤+|[^\s,]", texte)

    mots_modifies = []
    for mot in mots:
        if "'" in mot:
            mot_parts = mot.split("'")
            mots_modifies.extend(mot_parts)
        else:
            mots_modifies.append(mot)

    while mots_modifies: #coupe la phrase introduite dans le traducteur mot par mot jusqu'a ce que le groupe de mots existe dans la base de donnée 
        for i in range(len(mots_modifies), 0, -1):
            sous_phrase = ' '.join(mots_modifies[:i])
            if sous_phrase.lower() in base_de_donnees:
                print("Groupe de mots trouvé dans la base de données :", sous_phrase)
                traduction_groupe = base_de_donnees[sous_phrase.lower()]
                traduction.append(traduction_groupe)
                mots_modifies = mots_modifies[i:]
                print("Mots traduits ajoutés à la liste de traduction.")
                break
       
        else: #regard si le dernier mot existe dans la base de donnée 
            dernier_mot = mots_modifies[-1].strip(string.punctuation)  # Corrected line
            print("Dernier mot après suppression :", dernier_mot)
            if dernier_mot.lower() in base_de_donnees:
                traduction_mot = base_de_donnees[dernier_mot.lower()]
                traduction.append(traduction_mot)
                print("Traduction du dernier mot trouvée dans la base de données :", traduction_mot)    

            else: #si il n'existe pas traduit le mot en créole haitien 
                print("Mot non trouvé dans la base de données. Tentative de traduction avec Google Translate.")
                try:
                    traduction_mot = traduire_avec_google_translate(dernier_mot, langue_source, langue_cible)
                    if traduction_mot is not None:
                        traduction.append(traduction_mot)
                        print("Traduction du dernier mot obtenue avec Google Translate :", traduction_mot)
                except Exception as e:
                    print("Une erreur s'est produite lors de la traduction avec Google Translate :", e)
                    traduction.append(dernier_mot)

            if dernier_mot == "":
                print("Dernier mot vide après suppression. Ignoré.")
                
            if mots_modifies:
                mots_modifies.pop(-1)

    traduction_sans_special = [mot for mot in traduction if mot != " ' "]

    return ' '.join(traduction_sans_special)

def traduire_avec_google_translate(texte, langue_source='fr', langue_cible='ht'): #Traduction en Creole Haïtien
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={langue_source}&tl={langue_cible}&dt=t&q={texte}"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            traduction = response.json()[0][0][0]
            return traduction
        except (IndexError, KeyError) as e:
            print("Erreur lors de l'analyse de la réponse de l'API Google Translate :", e)
            return f"Erreur lors de la traduction de '{texte}'."
    else:
        return f"Erreur lors de la traduction de '{texte}'."