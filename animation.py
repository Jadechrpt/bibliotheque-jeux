import pygame
import os 
from PIL import Image
pygame.init()

# Se placer automatiquement dans le dossier du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#class qui s'occupe d'animer les entités du jeu


class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_name, size=(200, 200), game=None):
        super().__init__()
        self.game = game  # Référence à l'instance du jeu
        self.sprite_name = sprite_name  # Le nom du sprite (par exemple, "bunny", "alien", etc.)
        self.size = size
        self.etat = "immobile"  # État initial
        self.frames = {}  # Dictionnaire pour stocker les frames des animations
        
        

  
        if sprite_name not in AnimateSprite.loaded_frames:
            self.load_animation_images()
            AnimateSprite.loaded_frames[sprite_name] = self.frames  # Cache les frames pour ce sprite
        else:
            self.frames = AnimateSprite.loaded_frames[sprite_name]
       
    # On crée un cache global pour les animations
    loaded_frames = {}
    #méthode pour démarrer l'animation de l'entité
  


    #méthode pour animer l'image, selon l'action de l'instance: marche, attaque, mort, immobile(pour le joueur)
    def load_animation_images(self, loop=False):
        if hasattr(self, 'frames_loaded') and self.frames_loaded:
            return
        #verifier si l'objet est animé
        animation_types = ["marche", "attack", "immobile", "mort", "tourner"]
        for action in animation_types: 
            chemin_folder = os.path.join('PygameAssets-main', self.sprite_name, action)
            if os.path.exists(chemin_folder):
                if action not in self.frames:
                    self.frames[action]= []
                    for j in os.listdir(chemin_folder): 
                        img_path = os.path.join(chemin_folder, j)
                    
                    

                    # Vérifier si le fichier compressé existe
                        if img_path.endswith('.png'):

                            try: 
                                
                                img = pygame.image.load(img_path)  # Charger l'image compressée
                                img = pygame.transform.scale(img, self.size)  # Redimensionner
                                self.frames[action].append(img)
                            except pygame.error as e: 
                                print(f"Erreur de chargement de l'image {img_path}: {e}")
                    print(f"Frames pour l'animation '{action}': {self.frames[action]}")
                




    #animer l'entité en fontion de l'action choisi : mort, marche, attaque..... Aloop= True si l'action se repete en boucle ou loop=False dans le cas ou l'entité meure
    def animate(self, action, loop=True):
        if action in self.frames: 
            self.etat = action  # Met à jour l'état selon l'action
            if loop:
                # Calcul du temps écoulé pour changer d'image toutes les 100 ms
                image = self.frames[self.etat][(pygame.time.get_ticks() // 100) % len(self.frames[self.etat])]
                self.image = pygame.transform.scale(image, self.size)
            else:
                # Pour les actions qui ne bouclent pas, utiliser la première image
                self.image = self.frames[self.etat][0]
        
        else:
            print(f"Aucune image pour l'animation {action}! Utilisation de l'état 'immobile'.")
            self.image = self.frames["immobile"][0]
            self.image = pygame.transform.scale(self.image, self.size)
        


#définir un dictionnaire  qui va charger toutes les images (pour l'animation) de chaque sprite
#chaque clef correspond a un sprite du jeu : mummy1.png, mummy2.png.....
animations= {
    'bunny': AnimateSprite("bunny"),
    'player': AnimateSprite("player"),
    'alien': AnimateSprite("alien"),
    'little': AnimateSprite("little"),
    'turtle': AnimateSprite("turtle"),
    'poison': AnimateSprite("poison"),  # Ajoute l'effet Poison
    'star': AnimateSprite("star"),
    'projectile_player': AnimateSprite("projectile"),
    'projectile_monster': AnimateSprite("projectile_alien"),
    
   
}