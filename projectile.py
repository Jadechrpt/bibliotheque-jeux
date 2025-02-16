import pygame
from animation import AnimateSprite  

#classe du projectile du joeuur 
class Projectile(AnimateSprite): 

    # constructeur de la classe 
    def __init__(self, entity, velocity=15, angle=0, sprite_tag="projectile"): 
        super().__init__("projectile", size=(400, 250))
        self.velocity = velocity
        self.entity = entity 
        self.image = None 
        self.rect = None
        
        
        #positionner le projectile au nievau du joueur 
        self.origin_image = self.image  # Image originale pour la rotation
        self.angle = angle 

    def rotate(self): 
         #tourner le projectle 
        
            self.angle += 12
            self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
            self.rect = self.image.get_rect(center=self.rect.center) # faire en sorte que le projectile tourne en fonction du centre de l'image projectile 


    def remove(self): 
            self.entity.all_projectile.remove(self)
            
            print("projectile sup")


    #faire deplacer les projectile 
    def move(self): 
        self.rect.x += self.velocity
        

        #si collision avec un monstre, suprimmer le projectile et impacter les monstres touchés
        for monster in  self.entity.game.check_collision(self, self.entity.game.all_monster): 
             #enlever le projectile 
             self.remove()
             #infliger les degats
             monster.damage(self.entity.attack)
        #detruire les projectile  une fois que le projectile quitte l'ecran 
        if self.rect.x>1080:
             self.remove()

              
class ProjectilePlayer(Projectile):
    def __init__(self, player): 
        # Appeler le constructeur de la classe parente (Projectile)
        super().__init__(player)  
        self.animation_speed_factor = 20
        self.image = pygame.image.load('PygameAssets-main/playe2r.png')  # Image spécifique du projectile du joueur
        self.image = pygame.transform.scale(self.image, (80, 50))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        # Positionner le projectile au niveau du joueur
        self.rect.x = player.rect.x -50#décaler
        self.rect.y = player.rect.y-30
        self.speed= 2

        self.origin_image = self.image
        self.angle = 0  # Pas de rotation initiale

    def move(self):
        
        if "marche" in self.frames:
            frame_index = (pygame.time.get_ticks() // (100 // self.animation_speed_factor)) % len(self.frames["marche"])
            self.image = pygame.transform.scale(self.frames["marche"][frame_index], (80, 50))

        
        # Déplacer le projectile vers la droite
        self.rect.x -= self.speed
        self.animate("marche")
        super().move()             
            
class ProjectileMonster(Projectile):
    def __init__(self, monster): 
        super().__init__(monster,  sprite_tag="projectile_monster")  # Appeler le constructeur de la classe parente (Projectile)
        self.animation_speed_factor = 20
        self.sprite_name="projectile_monster"
        self.image = pygame.image.load('PygameAssets-main/playe2r.png')  # Image spécifique du projectile du monstre
        self.image = pygame.transform.scale(self.image, (80, 50))  # Taille plus petite pour le projectile
        self.rect = self.image.get_rect()
        self.rect.center = monster.rect.center  # Positionner au centre du monstre
        self.speed = 5  # Vitesse du projectile
        self.origin_image = self.image
        self.angle = 0  
        

    def move(self):
        if "marche" in self.frames:
            frame_index = (pygame.time.get_ticks() // (100 // self.animation_speed_factor)) % len(self.frames["marche"])
            self.image = pygame.transform.scale(self.frames["marche"][frame_index], (80, 50))

 
        self.rect.x -= self.speed  # Déplace le projectile vers la gauche
        # Vérifier la collision avec le joueur
        if self.entity.game.check_collision(self, self.entity.game.all_player):
            self.entity.game.player.damage(self.entity.attack)  # Infliger des dégâts au joueur
            self.remove()  # Supprimer le projectile

        # Supprimer le projectile s'il sort de l'écran
        if self.rect.x < 0:
            self.remove()

