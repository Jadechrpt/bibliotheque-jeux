import pygame
from projectile import ProjectilePlayer
from animation import AnimateSprite  # Assurez-vous que le chemin vers animation.py est correct

#classe joueur
class Player(AnimateSprite):
    def __init__(self, game):
       
        super().__init__("player")
        self.game = game
        
        self.health= 100 #vie du joueur
        self.max_health= 100
        self.attack = 20
        self.velocity = 10
        self.original_velocity = self.velocity  # Sauvegarder la vitesse initiale
        self.all_projectile= pygame.sprite.Group() #losque le oueur tire plusieurs projectilzs, ils osnt rangés dans un groupe
        
        self.animate("immobile")
        self.rect = self.image.get_rect() #on recupere les coordonnées du jeu pour le deplacement
        self.rect.x = 400
         # Taille de l'écran
        self.rect.y = 525
       
        #parametre pour le saut:
        self.saut = False  # état du saut
        self.gravity = 1.2 # gravité
        self.force_saut = -15  # force du saut
        self.vitesse_saut = 0  # vitesse verticale du joueur
        self.font = pygame.font.Font("PygameAssets-main/Police.ttf", 25)
        

    #fait predre de la vie lorqu'il y a une collision avec un monstre
    def damage(self, amount):
        self.game.sound_manager.play("degat",0.3)
        #vérifier si le monstre est encore vivant (self.health >= 0)
        if self.health- amount > amount:
            self.health -= amount
        else:  # Si la vie du joueur atteint 0 ou moins
            
            self.game.game_over()
            self.animate("mort") 



    def update(self):
        # Met à jour l'animation du joueur en fonction de son état
        if self.saut:
           
            self.animate("marche")  # L'animation peut être mise à jour en fonction de l'action
        elif self.game.pressed.get(pygame.K_RIGHT) or self.game.pressed.get(pygame.K_LEFT):
            self.animate("marche")
        elif self.game.pressed.get(pygame.K_z):
            self.animate("attack")
        else:
            self.animate("immobile")
        if self.game.pressed.get(pygame.K_RIGHT):
            self.move_right()
        elif self.game.pressed.get(pygame.K_LEFT):
            self.move_left()



    def barre_de_vie(self, surface):
        #faire apparaitre la barre de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x +50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (11,210,46), [self.rect.x +50, self.rect.y + 20, self.health, 7])


    def launch_projectile(self):
        projectile = ProjectilePlayer(self)  # Crée un projectile
        #creer une nouv instance de la classe projectile
        self.all_projectile.add(ProjectilePlayer(self))

        self.game.sound_manager.play("projectile",0.4)
    def move_right(self):
        screen_width, _ = pygame.display.get_window_size()  # Récupérer la largeur de l'écran
    
        # Vérifier si le joueur peut encore avancer sans sortir de l'écran
        if self.rect.x + self.velocity + self.rect.width < screen_width:
        #verif si le joueur n'est pas en collisisona vec monstre
            if not  self.game.check_collision(self, self.game.all_monster):
                self.rect.x+= self.velocity

    def move_left(self):
         # Empêcher le joueur de sortir de l'écran en prenant en compte sa largeur
        if self.rect.x - self.velocity >= -40:  
            self.rect.x -= self.velocity
       
   

    def jump(self):
        # gérer le saut uniquement si le joueur n'est pas déjà en l'air
        self.game.sound_manager.play("chat",0.4)
        if not self.saut:
            self.vitesse_saut = self.force_saut
            self.saut = True

    def apply_gravity(self):
        # appliquer la gravité et gérer la chute
        self.vitesse_saut  += self.gravity
        self.rect.y += self.vitesse_saut
        # vérifier si le joueur est au sol
        if self.rect.y >= 525:  # 500 correspond au sol
            self.rect.y = 525
            self.saut = False
            self.vitesse_saut  = 0