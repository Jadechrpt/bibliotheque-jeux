import pygame
from pygame.locals import *
import random
pygame.init()

pygame.mixer.music.load("bubble.mp3")
# Configuration de l'écran
screen = pygame.display.set_mode((1100, 487))
pygame.display.set_caption("cat runner")
background = pygame.image.load("ciel.jpeg").convert()
largeur_screen= screen.get_width()
hauteur_screen= screen.get_height()
#variables generales
vitesse_g = 6 #vitesse generale, des obstacles et du sol
sol = 380  
points = 0
font = pygame.font.Font('retro.ttf', 40)
death = 0
obstacles=[1,2,3]#les 3 obstacles qui peuvent apparaitre avant que points = 3000 : 1=Arbre ; 2=ArbreG ; 3=Pelote (à partir de 3000 : 4=oiseau)
recommencer = 1 #permet de différencier la simple pause du jeu avec celle qui suit une défaite, qui nécessite de recommencer le jeu (variable utilisée dans restart)
highest_score = 0 #affiché HI sur le screen
start=0 #pour afficher le texte de début de partie
quitter=0 

# Sprites
#NUAGES
nuage = pygame.image.load("nuage.png").convert_alpha() 
nuage = pygame.transform.scale(nuage, (250, 250))
largeur_nuage= nuage.get_width() 
vitesse_x_nuage = 1 #vitesse moins élevée que pour celle des obstacles et du sol
pos_x_nuage, pos_y_nuage = screen.get_width(), random.choice([-40,0,50,100,150])

#ARBRES
arbre = pygame.image.load("arbre.png").convert_alpha() 
arbre = pygame.transform.scale(arbre, (110, 100))
arbreRect = arbre.get_rect()
arbreMask = pygame.mask.from_surface(arbre)
arbreImage = arbreMask.to_surface()
largeur_arbre= arbre.get_width()
pos_x_arbre, pos_y_arbre = screen.get_width(), sol

#PELOTES
pelote = pygame.image.load("pelote.png").convert_alpha() 
pelote = pygame.transform.scale(pelote, (110, 90))
peloteRect = pelote.get_rect()
peloteMask = pygame.mask.from_surface(pelote)
peloteImage = peloteMask.to_surface()
largeur_pelote= pelote.get_width()
pos_x_pelote, pos_y_pelote = screen.get_width(), sol



#GRAND ARBRE
arbreG = pygame.image.load("arbreG.png").convert_alpha() 
arbreG= pygame.transform.scale(arbreG, (110, 100))
arbreGRect = arbreG.get_rect()
arbreGMask = pygame.mask.from_surface(arbreG)
arbreGImage = arbreGMask.to_surface()
largeur_arbreG= arbreG.get_width()
pos_x_arbreG, pos_y_arbreG = screen.get_width(), sol



#OISEAUX
oiseau = pygame.image.load("oiseau.png").convert_alpha() 
oiseau = pygame.transform.scale(oiseau, (80, 60))
largeur_oiseau= oiseau.get_width()
pos_x_oiseau, pos_y_oiseau = screen.get_width(), random.choice([260,320,sol])
oiseau2 = pygame.image.load("oiseau2.png").convert_alpha() #2eme image de l'oiseau pour faire l'animation
oiseau2 = pygame.transform.scale(oiseau2, (80, 60))
largeur_oiseau2= oiseau2.get_width()
vitesse_x_oiseau2 = 6
pos_x_oiseau2, pos_y_oiseau2 = screen.get_width(), random.choice([260,320,380])

bird_frames = [oiseau,oiseau2] #alternance des deux images
bird_frame_index = 0
bird_animation_speed = 200  # Temps en ms entre chaque image
last_bird_update = pygame.time.get_ticks()

oiseau_rect1 = bird_frames[bird_frame_index].get_rect()
oiseau_rect1.topleft = (pos_x_oiseau, pos_y_oiseau)
oiseau_rect2 = bird_frames[bird_frame_index].get_rect()
oiseau_rect2.topleft = (pos_x_oiseau2, pos_y_oiseau2)



#CHAT
taille_chat = (150,100)
chat_base = pygame.image.load("chat_immobile.png").convert_alpha() #chat de base
chat_base = pygame.transform.scale(chat_base, taille_chat)  # Redimensionner
chat_2 = pygame.image.load("chat2.png").convert_alpha() #2eme image qui alterne avec la premiere quand il court
chat_2 = pygame.transform.scale(chat_2, taille_chat)  
chat_saut = pygame.image.load("chat_saut.png").convert_alpha() #chat qui saute
chat_saut = pygame.transform.scale(chat_saut, taille_chat)

current_image_chat = chat_base  # Image du chat qui s'affiche
chatRect = current_image_chat.get_rect()
chatMask = pygame.mask.from_surface(current_image_chat)
chatImage = chatMask.to_surface()
chatRect.topleft = (70, sol)

#alternance des deux images de chat pour donner l'impression qu'il court
anim_timer = 0  # Chronomètre pour alterner les images
anim_delai = 150  # Délai en millisecondes entre chaque alternance

#Saut
sauter = False  # Indique si le chat est en train de sauter
vitesse_saut = 0
gravite = 0.75


#image du sol = ground
ground = pygame.image.load("sol.png").convert_alpha() 
ground = pygame.transform.scale(ground, (3047, 47))
largeur_ground= ground.get_width() 
pos_x_ground=0 
pos_y_ground=440 

def high_score(last_score):
        global highest_score
        if highest_score< last_score-1 : #-1 car il me rajoute 1 par rapport au nb de points affiché au moment du game over
                highest_score = last_score-1
        return highest_score
        
def collision(rect1, rect2):
        return rect1.colliderect(rect2)

def score():
        global points, vitesse_g
        score = font.render("HI: " + str(highest_score) + "  " + "Points: " + str(points), True, (245,40,145,0.8))
        scoreRect = score.get_rect()
        scoreRect.center = (970, 40) 
        screen.blit(score, scoreRect)
        points += 1
        if vitesse_g <= 11:
                if points % 400 == 0:
                    vitesse_g += 1
        if points % 100 == 0:
                    random.choice(obstacles)

def restart() :
                global points,death,start,quitter,recommencer
                pause = True
                font = pygame.font.Font('retro.ttf', 40)
                while pause and (start == 0 or death >0) :
                        if death == 0 and start==0:
                                text = font.render("Cliquez sur la touche espace, flèche du haut ou return pour commencer",True, (245,40,145,0.8))
                                textRect = text.get_rect()
                                textRect.center = (largeur_screen//2, hauteur_screen//2 ) #au milieu de l'ecran
                                screen.blit(text, textRect)
                                pygame.display.flip()
                        elif death >0 :
                                text = font.render("Game Over",True, (245,40,145,0.8))
                                textRect = text.get_rect()
                                textRect.center = (largeur_screen//2, hauteur_screen//2) 
                                screen.blit(text, textRect)
                                pygame.display.flip()#pour qu'il m'affiche le texte
                        for event in pygame.event.get():
                                                if event.type==KEYDOWN:
                                                        if event.key == K_RETURN or event.key == K_SPACE or event.key == K_UP :
                                                                if death == 0 and start==0:
                                                                        pygame.display.flip()
                                                                        pygame.mixer.music.unpause()
                                                                        start+=1
                                                                        recommencer = 0
                                                                        pause = False
                                                                elif death >0 :
                                                                        recommencer = 1
                                                                        pause = False
        
                                                elif event.type == QUIT:
                                                        quitter = 1
                                                        pause = False
                                                        
                                                        

# Boucle principale
main = True
clock = pygame.time.Clock()
while main :
        if quitter == 1:
                break
        
        if recommencer ==1: #pour chaque début de partie
                #affichage de l'écran de base avant de (re)commencer une partie
                screen.blit(background, (0, 0))
                screen.blit(ground, (pos_x_ground, pos_y_ground))  
                screen. blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                screen.blit(nuage, (pos_x_nuage,pos_y_nuage))
                current_image_chat = chat_base
                chatRect.bottom = sol + taille_chat[1]
                screen.blit(current_image_chat, chatRect)
                screen.blit(chatImage, (0,-110))
                vitesse_g = 6 #je la réinitialise
                #réinitialisation de la position de tous les objets pour éviter qu'ils aparaissent à l'écran après
                pos_x_arbre, pos_y_arbre = screen.get_width(), sol
                pos_x_pelote, pos_y_pelote = screen.get_width(), sol
                pos_x_arbreG, pos_y_arbreG = screen.get_width(), sol
                pos_x_oiseau, pos_y_oiseau = screen.get_width(), random.choice([260,320,sol])
                pygame.display.flip()
                
                #pour affiché le bon texte dans restart
                death = 0
                start = 0
                restart()
                
                #le jeu (re)commence
                pygame.mixer.music.play(-1)
                continuer = True
                
        while continuer:
                        clock.tick(60)
                        if recommencer ==1 or quitter==1:
                                break
                        for event in pygame.event.get():
                                if event.type == QUIT :
                                        quitter = 1
                                        break
                                elif event.type == KEYDOWN:
                                        if (event.key == K_SPACE or event.key == K_UP) and chatRect.bottom == sol + 100 :
                                                sauter = True
                                                vitesse_saut = -20
                                        elif event.key == K_p :
                                                pause = True
                                                while pause :
                                                        for event in pygame.event.get():
                                                                        if event.type==KEYDOWN:
                                                                                if event.key == K_RETURN :
                                                                                               pause = False
                                                                        elif event.type == QUIT:
                                                                                pause = False
                                                                                continuer = False
                                


                                    
                        #defilement des nuages
                        pos_x_nuage -= vitesse_x_nuage
                        if pos_x_nuage == -largeur_nuage :
                                pos_x_nuage, pos_y_nuage = screen.get_width(), random.choice([-40,0,50,100,150])

                        #DÉPLACEMENT OBSTACLES
                        if points == 3000:
                                obstacles.append(4)
                        
                        if points==0 or len(obs_t) == 0:
                                obs_t = []
                                obs_t.append(random.choice(obstacles))
                        if 1 in obs_t :
                                #ARBRE
                                #defilement des arbres
                                pos_x_arbre -= vitesse_g
                                if pos_x_arbre <= -largeur_arbre :
                                        obs_t.remove(1)
                                        pos_x_arbre, pos_y_arbre = screen.get_width(), sol
                                
                                arbreRect = arbre.get_rect()
                                arbreRect.topleft = (pos_x_arbre, pos_y_arbre)
                                if len(obs_t)>= 1 :
                                        if obs_t[0] == 1 and pos_x_arbre <= largeur_screen/2 and len(obs_t)<2:
                                                        obs_t.append(random.choice(obstacles))
                                if chatRect.colliderect(arbreRect):
                                        if chatMask.overlap(arbreMask,(pos_x_arbre-chatRect.topleft[0],pos_y_arbre-chatRect.topleft[1])):
                                                death=1
                                                pygame.mixer.music.pause()

                                
                
                
                        if 2 in obs_t :
                                # GRAND ARBRE
                                
                                pos_x_arbreG -= vitesse_g
                                if pos_x_arbreG <= -largeur_arbreG :
                                        obs_t.remove(2)
                                        pos_x_arbreG, pos_y_arbreG = screen.get_width(), sol
                                arbreGRect = arbreG.get_rect()
                                arbreGRect.topleft = (pos_x_arbreG, pos_y_arbreG)
                                if len(obs_t)>= 1 :
                                        if obs_t[0] == 2 and pos_x_arbreG <= largeur_screen/2 and len(obs_t)<2:
                                                        obs_t.append(random.choice(obstacles))
                                if chatRect.colliderect(arbreGRect):
                                        if chatMask.overlap(arbreGMask,(pos_x_arbreG-chatRect.topleft[0],pos_y_arbreG-chatRect.topleft[1])):
                                                death=1
                                                pygame.mixer.music.pause()
                                                
                                


                        if 3 in obs_t :
                                #PELOTE
                                
                                pos_x_pelote -= vitesse_g
                                if pos_x_pelote <= -largeur_pelote :
                                        obs_t.remove(3)
                                        pos_x_pelote, pos_y_pelote = screen.get_width(), sol
                                peloteRect = pelote.get_rect()
                                peloteRect.topleft = (pos_x_pelote, pos_y_pelote)
                                if len(obs_t)>= 1 :
                                        if obs_t[len(obs_t)-1] == 3 and pos_x_pelote <= largeur_screen/2 and len(obs_t)<2:
                                                        obs_t.append(random.choice(obstacles))
                                                        #print(obs_t)
                                if chatRect.colliderect(peloteRect):
                                        if chatMask.overlap(peloteMask,(pos_x_pelote-chatRect.topleft[0],pos_y_pelote-chatRect.topleft[1])):
                                                death=1
                                                pygame.mixer.music.pause()
                               

                        if 4 in obs_t :
                                # Animation des oiseaux
                                current_time = pygame.time.get_ticks()  # Temps actuel en millisecondes
                                if current_time - last_bird_update > bird_animation_speed:  # Temps écoulé pour changer d'image
                                        bird_frame_index = (bird_frame_index + 1) % len(bird_frames)  # Passer à la prochaine image
                                        last_bird_update = current_time
                                # Déplacement horizontal de l'oiseau
                                pos_x_oiseau -= vitesse_g+0.7
                                if pos_x_oiseau <= -largeur_oiseau:  # Si l'oiseau sort de l'écran
                                        obs_t.remove(4)
                                        pos_x_oiseau, pos_y_oiseau = screen.get_width(), random.choice([260, 320, 380])
                                if len(obs_t)>= 1 :
                                        if obs_t[0] == 4 and pos_x_oiseau <= largeur_screen/2 and len(obs_t)<2:
                                                        obs_t.append(random.choice(obstacles))
                                                        #print(obs_t)

                                oiseau_rect1 = oiseau.get_rect()
                                oiseau_rect1.topleft = (pos_x_oiseau, pos_y_oiseau)
                                
                                oiseau_rect2 = oiseau2.get_rect()
                                oiseau_rect2.topleft = (pos_x_oiseau2, pos_y_oiseau2)
                                if (chatRect.colliderect(oiseau_rect1) or chatRect.colliderect(oiseau_rect2)):
                                        death=1
                                        pygame.mixer.music.pause()
                        #CHAT                
                        #pour que le chat "court"
                        anim_timer += clock.get_time()
                        if anim_timer >= anim_delai: #le timer est utiliser comme délai d'alternance entre les images(quand le timer = delai,il change d'image)
                                anim_timer = 0 
                                if current_image_chat == chat_base:
                                        current_image_chat = chat_2
                                else:
                                        current_image_chat = chat_base

                        
                        
                        # Gérer le saut Chat
                        if sauter:
                                chatRect.y += vitesse_saut  # Appliquer la vitesse 
                                vitesse_saut += gravite # Appliquer la gravité
                                current_image_chat = chat_saut
                        if chatRect.bottom >= sol + taille_chat[1]:  # Si le chat atteint le sol
                                chatRect.bottom = sol + taille_chat[1]
                                sauter = False

                
                    # Mettre à jour l'écran
                        screen.blit(background, (0, 0))
                        score()
                        screen.blit(chatImage, (0,-110))
                        screen.blit(ground, (pos_x_ground, pos_y_ground))  
                        screen. blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                        if pos_x_ground <= -largeur_ground:
                                screen.blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                                pos_x_ground = 0
                        pos_x_ground -=vitesse_g
                        
                        screen.blit(nuage, (pos_x_nuage,pos_y_nuage))
                        screen.blit(arbre, (pos_x_arbre, pos_y_arbre))
                        screen.blit(arbreG, (pos_x_arbreG, pos_y_arbreG))
                        screen.blit(pelote, (pos_x_pelote, pos_y_pelote))
                        screen.blit(bird_frames[bird_frame_index], (pos_x_oiseau, pos_y_oiseau))# Dessiner l'oiseau
                        screen.blit(current_image_chat, chatRect)
                        
                        if quitter == 1:
                                continuer = False       
                        pygame.display.update()
                       
                        if death == 1 and recommencer == 0:
                                high_score(points)
                                points = 0
                                restart()
                        if quitter == 1:
                                continuer = False
        pygame.mixer.music.stop()
pygame.quit()
