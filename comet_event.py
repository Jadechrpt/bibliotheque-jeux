import pygame 
from comet import Comet
#créer une classe pour gérer l'evenement
class CometFallEvent: 
    #creer un compteur lors du chargement 
    def __init__(self, game): 
        self.percent = 0
        self.percent_speed = 50
        self.game= game #avoir l'acce a la classe game 
        self.fall_mode= False #va permettre de stopper l'apparition de monstre dans le jeu 

        #definir un groupe de sprite pour stocker les pelotes de laine
        self.all_comets = pygame.sprite.Group()
    
    
    def add_percent(self): 
        if self.game.current_level > 1:
            self.percent += self.percent_speed/100
    
    #si la barre de l'enevenement est pleine , 
    def is_full_loaded(self): 
        return self.percent >= 100
    
    def reset_percent(self):
        self.percent= 0

    def meteor_fall(self): 
        #faire apparraitre plusieurs cometes
        for i in range(10): 
            #apparaitre une pelote de laine 
            self.all_comets.add(Comet(self)) #ajoute les cometes


    def attempt_fall(self): 
        #si la barre de comet est totalement cahrgée
        if self.is_full_loaded() and not self.fall_mode: 
            print("pluie de pelote de laine!")
            self.meteor_fall()
           
            self.fall_mode= True #activer l'évènement 
    #mettre a joueur une barre 
    def update_bar(self, surface): 

        #ajouter du poucentage a la barre d'evenement 
        self.add_percent()

        #barre d'arriere plan (noir)
        pygame.draw.rect(surface, (0,0,0), [
            0, #absicce 
           surface.get_height()- 20, #placer par rapport a la hauteur (ordonné)
           surface.get_width(), #longueur de la fenetre 
           10 #epaisseur de la barre 
        ])
        #barre , de chargement de l'evenement (rouge )
        pygame.draw.rect(surface, (187, 11, 11), [
            0, #absicce 
           surface.get_height()- 20, #placer par rapport a la hauteur (ordonné)
           (surface.get_width()/100)*self.percent, # definir la longueur de la barre en fonction du pourcentage de l'evenement 
           10 #epaisseur de la barre 
        ])


