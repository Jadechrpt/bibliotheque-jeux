import pygame
import random


#creer la classe pour gerer la pelote de laine
class Comet(pygame.sprite.Sprite ):

    def __init__(self, comet_event):
        super().__init__()
        #définir l'image de la pelote de laine
        # Charger l'image une seule fois
        if not hasattr(self, 'image'):
            self.image = pygame.image.load("PygameAssets-main/comet.png")
            self.image = pygame.transform.scale(self.image, (500,350))
        self.rect = self.image.get_rect()
        self.comet_event = comet_event
        self.velocity = random.randint(7,14)
        screen_width = self.comet_event.game.screen.get_width()
        self.rect.x = random.randint(-self.image.get_width() // 2, screen_width - self.image.get_width() // 2)  #position aléatoire de la pelote de laine
        self.rect.y = - random.randint(0,800) #hauteur  aléatoire de la pelote de laine
        self.comet_event = comet_event # ajouter comet event dans les propriétées de la classe pour pourvoir apres les supprimer

    #méthode pour supprimer les comètes
    def remove(self):
        self.comet_event.all_comets.remove(self)  # Correctement supprimé de la mémoire
        self.comet_event.game.sound_manager.play("meteorite")
        #verifier si il n'y a plus de pelot e de laine
        if len(self.comet_event.all_comets)== 0:
            print("fin de la lpluie de comètes")
            #remettre la barre de l'evenement à 0
            self.comet_event.reset_percent()
            # faire respawn les monstres
            self.comet_event.game.start(self.comet_event.game.current_level)
    #faire chuter la comete
    def fall(self):

        self.rect.y += self.velocity

        #si  collision avec le sol
        if self.rect.y >=500:
            print("collision vec le sol ")
            self.remove()
            #verifier la presence de pelote de laine dan sle jeu
            if len(self.comet_event.all_comets)==0:
                print("fin de la pluie de pelote de laine")
                #remettre la barre au depart
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False


        #verifier si collision entre la pelote de laine et le joeur
        if self.comet_event.game.check_collision(
            self,self.comet_event.game.all_player
            ):
            print("joueur touché")
            #detruire la pelote de laine
            self.remove()
            #perd des pts de vie (20)
            self.comet_event.game.player.damage(20)


