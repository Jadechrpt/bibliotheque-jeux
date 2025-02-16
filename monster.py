import pygame
import random
from animation import AnimateSprite  # Assurez-vous que le chemin vers animation.py est correct
from projectile import ProjectileMonster
from player import Player
clock = pygame.time.Clock()

clock.tick(60)
delta_time = clock.tick(60) / 1000.0  # Temps écoulé en secondes (1 ms = 0.001 s)

#classe qui crée les monstres

class Monster(AnimateSprite):
    positions_monstre = {
        "bunny": 0.79,  # 80% de la hauteur de l'écran
        "little": 0.81,  # 75% de la hauteur de l'écran
        "turtle": 0.85,  # 70% de la hauteur de l'écran
        "alien": 0.65,  # 65% de la hauteur de l'écran
        "default": 0.8  # Position par défaut à 80% de la hauteur
    }

    def __init__(self, game, name, size, offset= 0):
        super().__init__(name, size) #
        self.size=size
        self.game= game
        self.health = 100
        self.max_health = 100
        self.attack = 2
        self.animate("marche")
       
        self.rect = self.image.get_rect() #coordonnées du monstre
        self.rect.x = 900 + random.randint(0, 300) #faire spawn les mosntre aléatoirement
        screen_width, screen_height = pygame.display.get_window_size()

        # Positionnement vertical ajusté par type de monstre
        self.rect.y = int(self.positions_monstre.get(name, self.positions_monstre["default"]) * screen_height)
        self.loot_amount = 10 #nombre de pts gagnés
        self.all_projectile = pygame.sprite.Group()
        self.shoot_delay = 1000
        self.last_shot_time = pygame.time.get_ticks()
        self.sound_manager=game.sound_manager
        

        
       
    def update(self):
        # Animation en fonction de l'état du monstre
        if self.health <= 0:
            self.animate("mort")  # Animation de mort
        else:
            self.animate("marche")  # Animation de marche ou mouvement

        # Déplacement du monstre
        self.forward()

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity= random.randint(1,self.default_speed)

    #changer le nombre de points gaganer selon l'entité
    def set_loot_amount(self, amount):
        self.loot_amount= amount

    def damage(self, amount):
        #lui faire perdre le montant des degats mis en parametre
        self.health-= amount

        #vérifier si le monstre est encore vivant (self.health >= 0)
        if self.health <= 0:
            self.animate("mort") 
            # le faire respawn, nouv monstre
            self.rect.x= 900+ random.randint(0,300)
            self.velocity= random.randint(1,3)
            self.health= self.max_health #remettre le maximum de vie au monstre
            #augmente le score
            self.game.add_score(self.loot_amount)
    # methode pour afficher la barre de vie adapté pour chaque monstre : 
    def barre_de_vie(self, surface):
        
        bar_width = self.rect.width * 0.4# 
        health_width = (self.health / self.max_health) * bar_width  # 
      
        bar_x = self.rect.x + (self.rect.width - bar_width) // 2  
        bar_y = self.rect.y + self.rect.height * 0.1 
        pygame.draw.rect(surface, (60, 63, 60), [bar_x, bar_y, bar_width, 5])
        pygame.draw.rect(surface, (11, 210, 46), [bar_x, bar_y, health_width, 5])


    #déplacer le monstre
    def forward(self):
        if isinstance(self, Turtle):
            
            self.rect.x -= self.velocity  # Déplacement de la tortue sans se soucier de la collision
            if self.game.check_collision(self, self.game.all_player):
                # Infliger des dégâts si collision avec le joueur
                self.game.player.damage(self.attack)
                self.animate("attack")
                self.game.sound_manager.play("turtle",0.5)
        else: 
            #deplacement si aucune collision avec le joeur(variable groupe de joeuur crée)
            if not self.game.check_collision(self, self.game.all_player):
                self.rect.x-= self.velocity
            
            #si collision  avec le joueur :
            else:
                #infliger des dégats à notre joueur
                self.game.player.damage(self.attack)
                self.animate("attack")  
                

#classe pour la bunny, objet
class Bunny(Monster):
    def __init__(self, game):
        super().__init__(game, "bunny", (300,150))
        self.attack = 0.1
        
        self.set_speed(3)
        self.set_loot_amount(5)

class Little(Monster):
    def __init__(self, game):
        super().__init__(game, "little", (150,120))
        self.attack =0.1
        self.set_speed(3)
        self.set_loot_amount(2)


class Turtle(Monster):
    def __init__(self, game,offset=10):
        super().__init__(game, "turtle", (130,130))
        self.set_speed(50)
        self.set_loot_amount(2)
        self.rect.x -= self.velocity  # Déplacement vers la gauche
        


#classe pour le boss
class Alien(Monster):
    def __init__(self, game):
        super().__init__(game, "alien", (450,300))
       
        self.health= 250
        self.max_health= 250
        self.set_speed(1)
        self.attack = 0.2
        self.set_loot_amount(80)
        self.shoot_delay = random.randint(8000, 8000)
        self.last_shot_time = pygame.time.get_ticks()
        self.is_attacking = False
        self.temps_animation = pygame.time.get_ticks() # timer pour ralentir 
        self.vitesse_attack=500 # delai entrechaque image 
        self.attack_pause=900
        self.sound_manager=game.sound_manager
        

    def shoot(self):
    


        # Vérifier si le temps écoulé depuis le dernier tir est suffisant
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.animate("attack") 
            self.is_attacking = True
            # Créer un projectile et l'ajouter au groupe global
            projectile = ProjectileMonster(self)
            self.all_projectile.add(projectile)  # Ajouter au groupe local du monstre
            self.game.all_projectile.add(projectile)  # Ajouter au groupe global du jeu
            self.last_shot_time = current_time
            self.shoot_delay = random.randint(4000, 60000)  # Nouveau délai pour le prochain tir
            print("Alien a tiré un projectile !")
            self.temps_animation = pygame.time.get_ticks()


    def update(self):
        # Si l'Alien est en train d'attaquer, on garde l'animation d'attaque
        if self.is_attacking:
            if pygame.time.get_ticks() - self.temps_animation >= self.vitesse_attack:
                self.animate("attack")  # Met à jour l'animation d'attaque
                self.game.sound_manager.play("projectile",0.4)
        
                self.game.sound_manager.play("alienbark",0.5)

    # Si l'attaque est terminée après le délai d'attaque
            if pygame.time.get_ticks() - self.temps_animation > self.attack_pause:
                self.is_attacking = False  # L'attaque est terminée
                self.animate("marche") 

        # Après l'attaque, on le remet en mode marche
        if not self.is_attacking and pygame.time.get_ticks() - self.last_shot_time > 500:  # Par exemple 500ms
            self.is_attacking = False  # L'attaque est terminée
            self.animate("marche")  # Revenir à l'animation de marche

        # Déplacement du monstre (seulement si l'Alien n'attaque pas)
        if not self.is_attacking:
            self.forward()  # On permet à l'Alien de se déplacer seulement s'il n'attaque pas

    def forward(self):
        # Si l'Alien n'attaque pas, il avance normalement
        if not self.is_attacking:
            self.rect.x -= self.velocity  # Déplacer l'Alien vers la gauche (ou direction souhaitée)

