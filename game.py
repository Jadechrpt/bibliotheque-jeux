from player import Player
from monster import Bunny, Alien, Little, Turtle
from effects import Poison, Star
from comet_event import CometFallEvent
from sounds import SoundManager
from projectile import ProjectileMonster
import pygame
import random 
import math

# Initialisation de Pygame
pygame.init()
class Game:

    def __init__(self, screen):
        self.screen = screen
        
        #définir si le jeu commencé ou non
        self.start_party = False
        #joeuur generé lorsque patie est crée
        self.all_player= pygame.sprite.Group()
        self.player= Player(self)
        self.all_player.add(self.player)
    

        # Groupe pour gérer les effets (comme les poisons)
        self.all_effects = pygame.sprite.Group()
        poison = Poison(self, 200, 500, (50, 50), 2)
        star = Star(self, 200, 500, (50, 50), 2)
        self.all_effects.add(poison)

        #gererla pluie de pelote de laines
        self.comet_event= CometFallEvent(self)
        #groupe de monstres
        self.all_monster = pygame.sprite.Group() #gruope de sprite monster
        self.all_projectile = pygame.sprite.Group()
        #attribu pour gerer le son
        self.sound_manager = SoundManager()
        #initialiser le score du joueur
        self.font = pygame.font.Font("PygameAssets-main/Police.ttf", 25)
        self.score = 0
        self.current_level = 0
        self.pressed= {}#associé touche du clavier préssées
        self.game_over_val = False  # Ajoute un attribut pour savoir si le jeu est fini
        self.last_star_spawn = 0  



    def game_over(self):
         if not self.game_over_val:
            self.game_over_val = True  # Marque la fin du jeu
            self.start_party = False  # Arrête la partie en cours
            
        
    def reset(self):
        """Réinitialise complètement le jeu après un Game Over."""
        self.__init__(self.screen)  # Réinitialise toute la classe Game
    

    def reset_game(self):
        # Réinitialiser les éléments du jeu
        self.game_over_val = False
        self.start_party = False
        self.all_monster= pygame.sprite.Group()
        self.player.health= self.player.max_health 
        self.score = 0
        self.current_level = 0
        self.all_projectile=pygame.sprite.Group()
        self.all_effects = pygame.sprite.Group()  # Réinitialiser le groupe d'effets
        self.comet_event = CometFallEvent(self)
        self.all_player.empty()  # Vider les joueurs
        self.player = Player(self)  # Réinitialiser le joueur à son état de départ
        self.all_player.add(self.player)
        self.pressed = {}
          
        print("Jeu réinitialisé")



    #faire apparaitre les monstres au lancement de la partie
    def start(self, level):
        
        self.start_party = True
        self.current_level = level
        self.all_effects.empty()#vider les effets, pour eviter qles duplications inutiles
        if level == 1:
            self.spawn_monster(Bunny)
            self.spawn_monster(Bunny)
            self.spawn_monster(Bunny)
            self.spawn_monster(Little)
            self.spawn_monster(Little)
            self.spawn_monster(Turtle)
            self.spawn_monster(Turtle)

        elif level == 2:
            self.spawn_effect(Poison, 200, 500, size=(50, 50), value=1)
            
            self.spawn_monster(Bunny)
            self.spawn_monster(Alien)
            self.spawn_monster(Bunny)
            self.spawn_monster(Little)
            self.spawn_monster(Little)
            


            for monster in self.all_monster:
                if isinstance(monster, Alien):  # verifier les insistance (ici un alien )
                    monster.shoot()
        elif level == 3:
            for i in range(5):
                self.spawn_monster(Alien)
            for i in range(3):
                self.spawn_monster(Bunny)
        print(f"Niveau {level} démarré avec {len(self.all_monster)} monstres")


    def add_score(self, points= 10):
        self.score += points
    
   
        
         



    def update(self, screen ):
        score_text= self.font.render(f"Score : {self.score}", 1, (0,0,0))
        screen.blit(score_text, (20,20))
         #mettre l'image du joeur
        screen.blit(self.player.image, self.player.rect)
       
        #actualiser la barre de vie du joueur
        self.player.barre_de_vie(screen )




    
        # Vérifie si le score est un multiple de 50 et que l'étoile n'a pas déjà spawn à ce score
        if self.score >= 20 and self.score % 20 == 0:
            if not any(isinstance(effect, Star) for effect in self.all_effects):  # Vérifie qu'il n'y a pas déjà une étoile
                self.spawn_effect(Star, random.randint(50, 750), 480, size=(50, 50), duration=5, value=2)  # Hauteur ajustée
                print(f"⭐ Une étoile est apparue ! Score actuel : {self.score}")
                self.last_star_spawn = self.score  # Met à jour le dernier score où une étoile a spawn



            
        temps_jeu = pygame.time.get_ticks()
        if self.start_party and self.player:  # S'assurer que le jeu a commencé
            if self.current_level > 1:  # Ne pas afficher la barre au niveau 1
                self.comet_event.update_bar(screen)
                self.comet_event.attempt_fall()

        for effect in self.all_effects:
            if self.check_collision(self.player, [effect]): 
                print(f"Collision détectée avec {effect.__class__.__name__}")  #
                effect.apply(self.player)
                self.all_effects.remove(effect)
                if effect.update(): 
                    print(f"Effet {effect.__class__.__name__} terminé, suppression.")
                    self.all_effects.remove(effect)

        self.all_effects.update()
        self.all_effects.draw(screen)
         # Met à jour les animations des effets
        
        #recuperer les projectiles dujoeurus
        for projectile in self.player.all_projectile:
            projectile.move()  # Déplace chaque projectile du joueur
            screen.blit(projectile.image, projectile.rect)

        for projectile in self.all_projectile:  # Groupe global des projectiles
            projectile.move()
            screen.blit(projectile.image, projectile.rect)

        self.player.update()
       #recuperer les monstres, pour les faire avancer
        for monster in self.all_monster: 
            monster.barre_de_vie(screen)
            monster.update()
             # Met à jour chaque monstre
            monster.forward( )
           
            if isinstance(monster, Alien):
                monster.shoot()
        #récupérer les comètes du jeu
        for comet in self.comet_event.all_comets:
            comet.fall()


        # afficher le groupe de projectile
        self.player.all_projectile.draw(screen)
        
        #afficher le groupe de monstres
        self.all_monster.draw(screen)
        #faire appariatre dans le jeu la pluie de pelote de laine
        self.comet_event.all_comets.draw(screen)

        # verif direction joueur a gauche ou a droite ET LE D2PLACER
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width <screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()





    #colisions dans le jeu avec le sprite mis en parametre
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask) #verifié si le sprite chosii rentre en collisison avec un groupe de sprites


    def spawn_monster(self, monster_class_name):
        new_monster = monster_class_name(self)
        self.all_monster.add(new_monster)


    def spawn_effect(self, effect_class_name, x, y, size=(50, 50), duration=5, value=2):
        effect = effect_class_name(self, x, y, size, value)
        if effect_class_name == Star and any(isinstance(effect, Star) for effect in self.all_effects):
            return
         # Enregistre le temps d'apparition
        self.all_effects.add(effect)


class GameOver(Game):
    def __init__(self, screen, game):
        super().__init__(screen)  # Appeler le constructeur de la classe parente (Game)
        self.game = game
        self.font = pygame.font.Font("PygameAssets-main/Police.ttf", 100)
        self.game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))  # Texte rouge
        self.game_over_rect = self.game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))  # Centré

        # Bouton de redémarrage
        self.play_button = pygame.image.load("PygameAssets-main/button.png")
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = math.ceil(screen.get_width() / 3.33)
        self.play_button_rect.y = math.ceil(screen.get_height() / 1.5)

    def display(self):
        # Afficher l'écran Game Over
        self.screen.blit(self.game_over_text, self.game_over_rect)
        self.screen.blit(self.play_button, self.play_button_rect)

    def handle_events(self):
       
        
    # Gérer les événements du bouton "Rejouer"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.game.reset_game()  # Réinitialiser le jeu
                    return "bienvenue"  # Retour au menu principal après avoir cliqué sur "Rejouer"
        return None
                

