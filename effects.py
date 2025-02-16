import pygame
import animation
import random

class Effect(animation.AnimateSprite):
    def __init__(self, game, name, size, effect_type, value):
        super().__init__(name, size,game)  # Gère l'image ou l'animation
        self.size=size
        self.game = game
        self.effect_type = effect_type
        self.value = value
        
        self.animate("marche") 
        self.rect = self.image.get_rect() 
     
        
      

    

    def apply(self, target):
        if isinstance(target, self.game.player.__class__):

            if self.effect_type == "lent" and not hasattr(self, 'has_slowed') or not self.has_slowed:
                target.velocity *= 0.2  # Réduit la vitesse
                target.health -= 2
                self.has_slowed = True #réduit la vitesse (ex. valeur 0.5 pour ralentir de 50%)
            elif self.effect_type == "attak":
                target.health -= self.value  # Réduit la santé
            elif self.effect_type == "soin":
                target.health = min(target.max_health, target.health + self.value)  # Soigne sans dépasser la santé max

 
  

class Poison(Effect):
    def __init__(self, game, x, y, size, damage_per_tick):
        self.delay = 5000
        super().__init__(game, name="Poison", size=(150, 100), effect_type="lent", value=damage_per_tick)
        self.rect = self.image.get_rect()

        # Positionnement
        self.rect.x = random.randint(2, 500 - self.rect.width)
        self.rect.y = 540
        self.spawn_time = pygame.time.get_ticks()
        self.has_slowed = False
       
        self.last_update = pygame.time.get_ticks()
        self.update_interval = 1000  # Mise à jour toutes les secondes
        self.duration=2
       

    def update(self):
        self.animate("marche")
        target = self.game.player

        # Vérifie la collision et applique l'effet
        if self.game.check_collision(target, [self]):
            print(f"Collision détectée avec Poison !")
            self.apply(target)

        # Réduction de la durée chaque seconde
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.update_interval:
            self.last_update = current_time
            if self.duration > 0:
                self.duration -= 5
                print(f"Durée restante du poison : {self.duration}")
            else:
                print("L'effet poison est terminé.")
                self.remove(target)
                self.kill()  # Supprimer l'effet du jeu
                return True  # Marque la fin de l'effet
        return False  # Si l'effet continue
    def remove(self, target):
        if self.effect_type == "lent":
            target.velocity = target.original_velocity

    

class Star(Effect):
    def __init__(self, game, x, y, size, damage_per_tick):
        super().__init__(game, name="Star", size=(150,100), effect_type="attak", value=damage_per_tick)
        self.rect.topleft = (x, y)

    def update(self):
        """
        Inflige des dégâts à la cible et met à jour la durée de l'effet.
        """
        self.animate("marche")
        from game import Game
        target = self.game.player
        if self.game.check_collision(target, [self]):  # Vérifie la collision avec le joueur
            if target.health > 0:
                target.health -= self.value # Inflige les dégâts du poison
                
                print(f"{target.__class__.__name__} perd {self.value} points de santé à cause du poison.")
            target.health = min(target.health + 30, target.max_health)



        # Réduire la durée de l'effet et vérifier si terminé
        if super().update():  # Appelle la méthode parent pour gérer la durée
            print(f"L'effet soin est terminé pour {target.__class__.__name__}.")
            return True  # Retourne True si l'effet est terminé
        return False  # L'effet continue





