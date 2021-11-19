from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien Ã  afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'Image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle Image binarisee
    #==============================================================================
    def binarisation(self, S):
        
        im_bin = Image() # Instanciation d'un objet Image
        
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))
        
        # Itération pour parcourir l'ensemble du tableau pixels
        for i in range(self.H) :        
            for j in range(self.W) :
                if  self.pixels[i][j] < S : # On vérifie la condition de seuil
                    im_bin.pixels[i][j] = 0 # Les valeurs inférieures deviennent 0
                else:
                    im_bin.pixels[i][j] = 255 # Les valeurs supérieures deviennent 255
                
        return im_bin # On retourne l'Image


    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        im_loc = self # On copie l'Image original

        # Initialisation des valeurs
        c_max = 0
        c_min= im_loc.W
        l_max = 0
        l_min= im_loc.H
        
        # Itération pour parcourir l'ensemble du tableau pixels
        for i in range(self.H) :
            for j in range(self.W) :
                # On vérifie si le pixel de coordonnées i et j est égal à 0
                if im_loc.pixels[i][j] == 0:
                    
                    # Si la valeur en largeur est supérieure ou égale à c_max
                    # on définit c_max comme j
                    if j >= c_max:
                        c_max = j
                    
                    # Si la valeur en largeur est inférieure à c_min
                    # on définit c_min comme j
                    if j < c_min:
                        c_min = j
                    
                    # Si la valeur en hauteur est supérieure ou égale à l_max
                    # on définit l_max comme i
                    if i >= l_max:
                        l_max = i
                    
                    # Si la valeur en hauteur est inférieure à l_min
                    # on définit l_min comme i
                    if i < l_min:
                        l_min = i
        
        
        new_im = Image() # Instanciation d'un objet Image
        
        # On définit le tableau pixels de dimensions l_max-l_min et c_max-x_min
        # La fonction np.zeros remplit le tableau numpy de 0
        new_im.set_pixels(np.zeros((l_max-l_min,c_max-c_min),dtype=np.uint8))
        
        # On change les valeurs du tableau pixels du nouvel objet avec les valeurs
        # composants le rectangle englobant le chiffre
        new_im.pixels = im_loc.pixels[l_min:l_max+1,c_min:c_max+1]
        
        return new_im # On retourne l'Image

    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        
        im_res = Image() # Instanciation d'un objet Image
        
        # On crée un tableau numpy 2D basé sur le tableau pixels redimensionné
        # avec la fonction resize
        pixels_resized = resize(self.pixels, (new_H,new_W), 0)  
         
        # Afin de transformer notre tableau numpy en float a un tableau de pixels
        # en int, on utilise la fcontion numpy uint8()
        im_res.set_pixels(np.uint8(pixels_resized*255))
        
        return im_res # On retourne l'Image
        
    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, im):
        
        # Initialisation des valeurs
        tot = 0
        sim = 0
        hauteur = im.H
        largeur = im.W
        
        im_sim = self # On copie l'Image original
        
        # Itération pour parcourir l'ensemble du tableau pixels
        for i in range(hauteur) :
            for j in range(largeur) :
                # On incrémente tot de 1 pour obtenir le total de pixels
                tot += 1
                
                # On vérifie si les pixels de mêmes coordonnées sont équivalent
                if im_sim.pixels[i][j] == im.pixels[i][j]:
                    sim += 1    # On ajoute 1 à similitude

        return sim/tot # On retourne le rapport sim/tot
        
        