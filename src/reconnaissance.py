from image import Image

def lecture_modeles(chemin_dossier):
    fichiers= ['_0.png','_1.png','_2.png','_3.png','_4.png','_5.png','_6.png', 
            '_7.png','_8.png','_9.png']
    liste_modeles = []
    for fichier in fichiers:
        model = Image()
        model.load(chemin_dossier + fichier)
        liste_modeles.append(model)
    return liste_modeles


def reconnaissance_chiffre(image, liste_modeles, S):
    
    image_binarisee = image.binarisation(S)     # On binarise l'Image avec le seuil en paramètre
    image_localisee = image_binarisee.localisation()    # On localise l'Image binarisée précedemment obtenue
    
    # Initialisation des valeurs
    sim = 0
    nb_model = None
    
    # On parcourt la liste des modeles
    for i in range(len(liste_modeles)):
        
        # Si la hauteur ou la largeur de l'Image n'est pas égale à celle du modele liste_modeles[i]
        if (image.H != liste_modeles[i].H) | (image.W != liste_modeles[i].W):
                # On redimensionne l'Image localisée
                image_localisee = image_localisee.resize(liste_modeles[i].H,liste_modeles[i].W)
        
        # On récupère le rapport de similitude entre l'Image et le modele
        c = image_localisee.similitude(liste_modeles[i])
        
        # On regarde si le nouveau rapport est plus élevé que le précédent 
        if sim < c:
            # sim devient le nouveau rapport
            sim = c
            # On sauvegarde l'indice de ce modele
            nb_model = i
    
    # On affiche le modele reconnu
    liste_modeles[nb_model].display("Modele Reconnu")
    
    # On retourne l'indice du modele
    return nb_model
    
    
    
    
    
    
    
    
    
    

