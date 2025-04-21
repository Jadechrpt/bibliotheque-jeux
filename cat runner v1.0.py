import pygame
from pygame.locals import *
import random
from random import choice
pygame.init()
pygame.mixer.music.load("bubble.mp3")
logo = pygame.image.load("cat_runner_logo.png")
pygame.display.set_icon(logo)

# Configuration de l'écran
screen = pygame.display.set_mode((1100, 487))
pygame.display.set_caption("cat runner")
background = pygame.image.load("ciel.jpeg").convert()
largeur_screen= screen.get_width()
hauteur_screen= screen.get_height()

#variables generales
vitesse_g = 6 # Vitesse generale des elements (sauf nuage et chat)
sol = 380  
points = 0
font = pygame.font.Font('retro.ttf', 40)
death_count = 0

# --- SPRITES ---
#NUAGES
nuage = pygame.image.load("nuage.png").convert_alpha() 
nuage = pygame.transform.scale(nuage, (250, 250))
largeur_nuage= nuage.get_width() 
vitesse_x_nuage = 1
pos_x_nuage, pos_y_nuage = screen.get_width(), random.choice([-40,0,50,100,150])
derniere_hauteur_nuage = None # Pour éviter des nuages alignés
nuages = [] # Stocke tous les nuages actuellement affichés à l'écran
temps_creation_nuage = random.randint(1500, 4000)  # Intervalle aléatoire de création des nuages entre 1.5 et 4 secondes
dernier_nuage = pygame.time.get_ticks()

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
pelote = pygame.transform.scale(pelote, (110, 100))
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
# Deux images pour animer le vol
oiseau = pygame.image.load("oiseau.png").convert_alpha() 
oiseau = pygame.transform.scale(oiseau, (80, 60))
largeur_oiseau= oiseau.get_width()
pos_x_oiseau, pos_y_oiseau = screen.get_width(), random.choice([260,320,sol])

oiseau2 = pygame.image.load("oiseau2.png").convert_alpha()
oiseau2 = pygame.transform.scale(oiseau2, (80, 60))
largeur_oiseau2= oiseau2.get_width()
vitesse_x_oiseau2 = 6
pos_x_oiseau2, pos_y_oiseau2 = screen.get_width(), random.choice([260,320,380])

bird_frames = [oiseau,oiseau2] #alternance les deux images de vol
bird_frame_index = 0
bird_animation_speed = 200  # Temps en ms entre deux images
last_bird_update = pygame.time.get_ticks()


#CHAT
taille_chat = (150,100)
chat_base = pygame.image.load("chat_immobile.png").convert_alpha() 
chat_base = pygame.transform.scale(chat_base, taille_chat)  # Redimensionner
chat_2 = pygame.image.load("chat2.png").convert_alpha() #image alternée du chat quand il court
chat_2 = pygame.transform.scale(chat_2, taille_chat)  
chat_saut = pygame.image.load("chat_saut.png").convert_alpha() #chat qui saute
chat_saut = pygame.transform.scale(chat_saut, taille_chat)

#Position du chat à l'ecran et niveau du sol
current_image_chat = chat_base  # l'image du chat qui s'affiche
chatRect = current_image_chat.get_rect()
chatMask = pygame.mask.from_surface(current_image_chat)
chatImage = chatMask.to_surface()
chatRect.topleft = (70, sol)

# Animation chat
anim_timer = 0  # Chronomètre pour alterner les images
anim_delai = 150  # Délai en millisecondes entre chaque alternance


# SOL
ground = pygame.image.load("sol.png").convert_alpha() 
ground = pygame.transform.scale(ground, (3047, 47))
largeur_ground= ground.get_width() 
pos_x_ground=0 
pos_y_ground=440 

# variables générales
sauter = False  
vitesse_saut = 0 
highest_score = 0
recommencer = 1
obs_t = []

# Vérifie la collision entre deux rectangles        
def collision(rect1, rect2):
        return rect1.colliderect(rect2)

#meilleur score
def high_score(last_score):
        global highest_score
        if highest_score< last_score-1 :
                highest_score = last_score-1
        return highest_score

# Affiche le score et augmente la difficulté progressivement (vitesse + gravité)
def score():
        global points, vitesse_g,gravite
        score = font.render("High Score: " + str(highest_score) + "  " + "Score: " + str(points), True, (245,40,145,0.8))
        scoreRect = score.get_rect()
        scoreRect.center = (900, 40) #au coin de l'ecran
        screen.blit(score, scoreRect)
        points += 1

        #augmentation vitesse et gravité progressive
        if vitesse_g <= 12:
                if points % 400 == 0:
                    vitesse_g += 1
                    gravite+=0.04
        
        if points % 100 == 0:
                    random.choice(obstacles)

# Crée un nuage avec position aléatoire (et différente du précédent)
def creer_nuage():
    global derniere_hauteur_nuage,nuage,pos_x_nuage,pos_y_nuage,vitesse_x_nuage
    
    #pour éviter les nuages alignés
    while pos_y_nuage == derniere_hauteur_nuage:
        pos_y_nuage = random.choice([-40,0,50,100,150])
    derniere_hauteur_nuage = pos_y_nuage
    
    return {
        "image": nuage,
        "x": pos_x_nuage,
        "y": pos_y_nuage,
        "vitesse": vitesse_x_nuage
    }

# Recommencer le jeu
start=0
def restart() :
                pygame.mixer.music.pause()
                global points,death_count,start,quitter,recommencer
                pause = True
                font = pygame.font.Font('retro.ttf', 40)
                while pause and (start == 0 or death_count >0) :
                        if death_count == 0 and start==0:
                                text = font.render("Cliquez sur la touche espace, flèche du haut ou return pour commencer",True, (245,40,145,0.8))
                                textRect = text.get_rect()
                                textRect.center = (largeur_screen//2, hauteur_screen//2 ) #au milieu de l'ecran
                                screen.blit(text, textRect)
                                pygame.display.flip()
                        elif death_count >0 :
                                game_over = font.render("Game Over",True, (245,40,145,0.8))
                                game_overRect = game_over.get_rect()
                                game_overRect.center = (largeur_screen//2, hauteur_screen//2) 
                                screen.blit(game_over, game_overRect)
                                pygame.display.flip()#pour qu'il m'affiche le texte
                        for event in pygame.event.get():
                                                if event.type==KEYDOWN:
                                                        if event.key == K_RETURN or event.key == K_SPACE or event.key == K_UP :
                                                                if death_count == 0 and start==0:
                                                                        pygame.display.flip()
                                                                        pygame.mixer.music.unpause()
                                                                        start+=1
                                                                        recommencer = 0
                                                                        pause = False
                                                                elif death_count >0 :
                                                                        recommencer = 1
                                                                        pygame.mixer.music.pause()
                                                                        pause = False
                                                
        
                                                elif event.type == QUIT:
                                                        quitter = 1
                                                        pause = False
                                                        
                                                        

# === BOUCLE PRINCIPALE DU JEU ===
main = True
continuer = True
clock = pygame.time.Clock()
quitter = 0
while main :
        if quitter == 1:
                break

        # Réinitialisation si le jeu recommence
        if recommencer ==1:
                obstacles=[1,2,3]
                screen.blit(background, (0, 0))
                screen.blit(ground, (pos_x_ground, pos_y_ground))  
                screen. blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                screen.blit(nuage, (pos_x_nuage,pos_y_nuage))
                current_image_chat = chat_base
                chatRect.bottom = sol + taille_chat[1]
                screen.blit(current_image_chat, chatRect)
                screen.blit(chatImage, (0,-110))
                pygame.display.flip()
                death_count = 0
                start = 0
                death = 0
                vitesse_g = 6
                gravite = 0.85
                restart()
                pygame.mixer.music.play(-1)
                pos_x_arbre, pos_y_arbre = screen.get_width(), sol
                pos_x_pelote, pos_y_pelote = screen.get_width(), sol
                pos_x_arbreG, pos_y_arbreG = screen.get_width(), sol
                pos_x_oiseau, pos_y_oiseau = screen.get_width(), random.choice([260,320,sol])
                chatMask = pygame.mask.from_surface(current_image_chat)
                arbreMask = pygame.mask.from_surface(arbre)
                arbreGMask = pygame.mask.from_surface(arbreG)
                peloteMask = pygame.mask.from_surface(pelote)
                continuer = True
                
        while continuer:
                        clock.tick(60) # Limite à 60 FPS
                        if recommencer ==1 or quitter==1:
                                break
                        # --- GESTION DES ÉVÉNEMENTS CLAVIER ---
                        for event in pygame.event.get():
                                if event.type == QUIT :
                                        quitter = 1
                                        break
                                
                        keys = pygame.key.get_pressed()
                        #Detection de la pause
                        if keys[pygame.K_p]:
                                        pause = True
                                        while pause :
                                                pygame.mixer.music.pause()
                                                #texte arreter la pause
                                                font_pause = pygame.font.Font('retro.ttf', 26)
                                                t_pause = font_pause.render("cliquer 'return' pour continuer",True, (245,40,145,0.8),(255,231,245,1))
                                                t_pauseRect = t_pause.get_rect()
                                                t_pauseRect.center = (900,65)
                                                screen.blit(t_pause, t_pauseRect)
                                                pygame.display.flip()
                                                for event in pygame.event.get():
                                                                 if event.type==KEYDOWN:
                                                                        if event.key == K_RETURN :
                                                                                pygame.mixer.music.unpause()
                                                                                pause = False
                                                                 elif event.type == QUIT:
                                                                        quitter = 1
                                                                        pause = False
                                                                        continuer = False
                        # Détection du saut                                                        
                        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and chatRect.bottom == sol + 100 :
                                sauter = True
                                vitesse_saut = -20

                        # --- GESTION DES NUAGES ---
                        # Création aléatoire de nouveaux nuages
                        if pygame.time.get_ticks() - dernier_nuage > temps_creation_nuage:
                            if len(nuages) < 3:  
                                nuages.append(creer_nuage())  
                            dernier_nuage = pygame.time.get_ticks()  
                            temps_creation_nuage = random.randint(1500, 10000)  

                        # Déplacement et suppression des nuages hors écran
                        for nuage_c in nuages[:]:  # Copie de la liste pour modification pendant la boucle
                            nuage_c["x"] -= nuage_c["vitesse"]  # Fait défiler le nuage
                            if nuage_c["x"] < -largeur_nuage:
                                nuages.remove(nuage_c)  # Supprime les nuages sortis de l'écran



                        # --- GESTION DES OBSTACLES ---
                        if points == 2000:
                                obstacles.append(4) # 4 = oiseau, l'oiseau apparait désormais
                        
                        if points==0 or len(obs_t) == 0:
                                obs_t = [] #liste des obstacles présents sur l'écran
                                obs_t.append(random.choice(obstacles))
                                
                        if 1 in obs_t : #ARBRE
                                #defilement des arbres
                                pos_x_arbre -= vitesse_g
                                if pos_x_arbre <= -largeur_arbre :
                                        obs_t.remove(1)
                                        pos_x_arbre, pos_y_arbre = screen.get_width(), sol
                                
                                arbreRect = arbre.get_rect()
                                arbreRect.topleft = (pos_x_arbre, pos_y_arbre)
                                
                                if chatRect.colliderect(arbreRect):
                                        if chatMask.overlap(arbreMask,(pos_x_arbre-chatRect.topleft[0],pos_y_arbre-chatRect.topleft[1])):
                                                death_count+= 1
                                                death=1
                                                sauter = False
                                                pygame.mixer.music.pause()

                                
                
                
                        if 2 in obs_t : # GRAND ARBRE
                                pos_x_arbreG -= vitesse_g
                                if pos_x_arbreG <= -largeur_arbreG :
                                        obs_t.remove(2)
                                        pos_x_arbreG, pos_y_arbreG = screen.get_width(), sol
                                arbreGRect = arbreG.get_rect()
                                arbreGRect.topleft = (pos_x_arbreG, pos_y_arbreG)
                                
                                if chatRect.colliderect(arbreGRect) :
                                        if chatMask.overlap(arbreGMask,(pos_x_arbreG-chatRect.topleft[0],pos_y_arbreG-chatRect.topleft[1])):
                                                death_count+= 1
                                                death=1
                                                sauter = False
                                                pygame.mixer.music.pause()
                                                                                                
                        if 3 in obs_t :#PELOTE
                                pos_x_pelote -= vitesse_g
                                if pos_x_pelote <= -largeur_pelote :
                                        obs_t.remove(3)
                                        pos_x_pelote, pos_y_pelote = screen.get_width(), sol
                                peloteRect = pelote.get_rect()
                                peloteRect.topleft = (pos_x_pelote, pos_y_pelote)
                                
                                if chatRect.colliderect(peloteRect):
                                        if chatMask.overlap(peloteMask,(pos_x_pelote-chatRect.topleft[0],pos_y_pelote-chatRect.topleft[1])):
                                                death_count+= 1
                                                death=1
                                                sauter = False
                                                pygame.mixer.music.pause()
                                                
                        if 4 in obs_t : #OISEAU
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

                                oiseau_rect1 = oiseau.get_rect()
                                oiseau_rect1.topleft = (pos_x_oiseau, pos_y_oiseau)
                                
                                oiseau_rect2 = oiseau2.get_rect()
                                oiseau_rect2.topleft = (pos_x_oiseau2, pos_y_oiseau2)
                                
                                if (chatRect.colliderect(oiseau_rect1) or chatRect.colliderect(oiseau_rect2)):
                                        death_count+= 1
                                        death=1
                                        pygame.mixer.music.pause()

                        # --- GESTION DU CHAT ---                
                        # Animation du chat (course)
                        anim_timer += clock.get_time()
                        if anim_timer >= anim_delai: #délai d'alternance entre les images
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

                
                        # --- AFFICHAGE ---
                        screen.blit(background, (0, 0))
                        score()
                        screen.blit(chatImage, (0,-110))
                        
                        #texte pause
                        font_pause = pygame.font.Font('retro.ttf', 26)
                        t_pause = font_pause.render("cliquer 'p' pour pause",True, (245,40,145,0.8))
                        t_pauseRect = t_pause.get_rect()
                        t_pauseRect.center = (900,65)
                        screen.blit(t_pause, t_pauseRect)
                        
                        #sol
                        screen.blit(ground, (pos_x_ground, pos_y_ground))  
                        screen. blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                        if pos_x_ground <= -largeur_ground:
                                screen.blit (ground, (largeur_ground + pos_x_ground, pos_y_ground))
                                pos_x_ground = 0
                        pos_x_ground -=vitesse_g
                        
                        #nuages 
                        for nuage_t in nuages:
                            screen.blit(nuage_t["image"], (nuage_t["x"], nuage_t["y"]))

                        #obstacles
                        screen.blit(arbre, (pos_x_arbre, pos_y_arbre))
                        screen.blit(arbreG, (pos_x_arbreG, pos_y_arbreG))
                        screen.blit(pelote, (pos_x_pelote, pos_y_pelote))
                        screen.blit(bird_frames[bird_frame_index], (pos_x_oiseau, pos_y_oiseau))# Dessiner l'oiseau
                        screen.blit(current_image_chat, chatRect)

                        # --- FIN DE PARTIE ---
                        if quitter == 1:
                                continuer = False       
                        pygame.display.update()

                        if death == 1 and recommencer == 0:
                                high_score(points)
                                points = 0
                                restart() 

        pygame.mixer.music.stop()
pygame.quit()
