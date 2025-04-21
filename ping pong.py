import pygame
from pygame.locals import *
import sys
pygame.init()
pygame.mixer.music.load("cafe.mp3")
logo = pygame.image.load("logo.PNG")
pygame.display.set_icon(logo)


# Configuration de l'écran
WIDTH, HEIGHT = 600, 400
D_PINK = (255, 68, 139, 1)
L_PINK = (255,221,235,1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption ("Ping Pong")

# --- IMAGES ---
#PAUSE
pause = pygame.image.load("pause.png").convert_alpha()
pause = pygame.transform.scale(pause, (30, 30))
pauseRect = pause.get_rect()
pos_x_pause, pos_y_pause = WIDTH - 120, 20
pauseRect.topleft = (pos_x_pause, pos_y_pause)

#UNPAUSE
unpause = pygame.image.load("unpause.png").convert_alpha()
unpause = pygame.transform.scale(unpause, (30, 30))
unpauseRect = unpause.get_rect()
pos_x_unpause, pos_y_unpause = WIDTH - 120, 20
unpauseRect.topleft = (pos_x_unpause, pos_y_unpause)

#MAISON (=aller à l'écran d'accueil)
home = pygame.image.load("home.png").convert_alpha()
home = pygame.transform.scale(home, (30, 30))
homeRect = home.get_rect()
pos_x_home, pos_y_home = WIDTH - 520, 20
homeRect.topleft = (pos_x_home, pos_y_home)

#polices
retro = pygame.font.Font('retro.ttf', 40)
arial_symbols = pygame.font.Font("Arial Unicode.ttf", 20)

#balle
BALL_SPEED = 5
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = BALL_SPEED, BALL_SPEED

#raquettes
paddle_width, paddle_height = 15, 60
left_paddle_x, right_paddle_x = 10, WIDTH - 25
left_paddle_y, right_paddle_y = HEIGHT // 2+50 - paddle_height // 2, HEIGHT // 2+120 - paddle_height // 2
paddle_speed = 7

#variables générales
score_left, score_right = 0, 0
commencer = 0
death = 0
pause_jeu = False

#remet les tailles et vitesse des éléments comme initialement                        
def reset_ball():
        return WIDTH // 2, HEIGHT // 2, BALL_SPEED, BALL_SPEED
def reset_paddles():
        return HEIGHT // 2+50 - paddle_height // 2, HEIGHT // 2+120 - paddle_height // 2

# === MENU D'ACCUEIL ===
# Permet à l'utilisateur de choisir entre deux modes de jeu
def mode_jeu():
    global death,commencer,score_right,score_left,ball_x, ball_y, ball_speed_x, ball_speed_y,left_paddle_y, right_paddle_y
    screen.fill(L_PINK)
    #image
    icone = pygame.image.load("logo.png").convert_alpha()
    icone = pygame.transform.scale(icone, (200, 200))
    iconeRect = icone.get_rect()
    pos_x_icone, pos_y_icone = WIDTH//2-(icone.get_width()//2), 0
    iconeRect.topleft = (pos_x_icone, pos_y_icone)
    #textes
    bienvenue = retro.render("Bienvenue !", True, D_PINK)
    texte_choix1 = retro.render("1. Jouer contre un adversaire", True, D_PINK)
    texte_choix2 = retro.render("2. Jouer seul", True, D_PINK)
    
    screen.blit(icone, (pos_x_icone, pos_y_icone))
    screen.blit(bienvenue, (50, 170))
    screen.blit(texte_choix1, (50, 200))
    screen.blit(texte_choix2, (50, 300))
    pygame.display.flip()
    choix = None
    while choix is None:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_1 or evenement.type == pygame.MOUSEBUTTONDOWN  and 210<evenement.pos[1]<230 and 50<evenement.pos[0]<525:
                choix = "adversaire"
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_2 or evenement.type == pygame.MOUSEBUTTONDOWN  and 310<evenement.pos[1]<330 and 50<evenement.pos[0]<525 :
                choix = "seul"
    #met à jour les variables 
    death = 0
    commencer = 0
    score_right = 0
    score_left = 0
    ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
    left_paddle_y, right_paddle_y = reset_paddles()
    return choix

#=== MEILLEUR SCORE ===
highest_score = 0
def high_score(last_score):
        global highest_score
        if highest_score< last_score :
                highest_score = last_score
        return highest_score

# === ÉCRAN DE GAME OVER / DÉBUT ===
# Affiche un message d'attente tant que le joueur n'appuie pas sur RETURN
def restart() :
                global mode,death,score_right,commencer,pause_jeu
                pause_jeu = True
                while pause_jeu :
                        if death == 1 :
                                game_over = retro.render("Game Over",True, (245,40,145,0.8))
                                game_overRect = game_over.get_rect()
                                game_overRect.center = (WIDTH//2, HEIGHT//2-10) 
                                screen.blit(game_over, game_overRect)
                                text = retro.render("Cliquez sur return pour recommencer",True, (245,40,145,0.8))
                                textRect = text.get_rect()
                                textRect.center = (WIDTH//2, HEIGHT//2+15 ) 
                                screen.blit(text, textRect)
                        elif death == 0 :
                                text = retro.render("Cliquez sur return pour commencer",True, (245,40,145,0.8))
                                textRect = text.get_rect()
                                textRect.center = (WIDTH//2, HEIGHT//2+15 ) 
                                screen.blit(text, textRect)
                        if mode == "adversaire" :
                                        pygame.draw.rect(screen, D_PINK, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
                        pygame.display.flip()
                        
                        for event in pygame.event.get():
                                    if event.type == KEYDOWN:
                                        if event.key == K_RETURN:
                                            death = 0
                                            score_right = 0
                                            commencer = 1
                                            pause_jeu = False
                                        elif event.key == pygame.K_h:
                                            mode = mode_jeu()
                                            pause_jeu = False
                                    elif event.type == pygame.MOUSEBUTTONDOWN and homeRect.collidepoint(event.pos):
                                        mode = mode_jeu()
                                        pause_jeu = False
                                    elif event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()

                                        

# === BOUCLE PRINCIPALE DU JEU ===
pygame.mixer.music.play(-1)
mode = mode_jeu()
ping = True
while ping:
        # --- GESTION DES ÉVÉNEMENTS CLAVIER/SOURIS ---
        for event in pygame.event.get():
                if event.type == KEYDOWN:
                        if event.key == pygame.K_p:
                                pause_jeu = True
                        elif event.key == pygame.K_h:
                                last_score = score_right
                                high_score(last_score)
                                mode = mode_jeu()
                elif event.type == pygame. QUIT:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and pauseRect.collidepoint(event.pos):
                        pause_jeu = True
                elif event.type == pygame.MOUSEBUTTONDOWN and homeRect.collidepoint(event.pos):
                        last_score = score_right
                        high_score(last_score) 
                        mode = mode_jeu()
        while pause_jeu :
                pygame.mixer.music.pause()
                screen.blit(unpause, (pos_x_unpause, pos_y_unpause))
                pygame.display.flip()
                for event in pygame.event.get():
                        if event.type==KEYDOWN:
                                if event.key == K_RETURN or event.key == pygame.K_p  :
                                        pygame.mixer.music.unpause()
                                        pause_jeu = False
                                elif event.key == pygame.K_h :
                                        mode = mode_jeu()
                                        pygame.mixer.music.unpause()
                                        pause_jeu = False
                        elif event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and unpauseRect.collidepoint(event.pos):
                                pygame.mixer.music.unpause()
                                pause_jeu = False
                        elif event.type == pygame.MOUSEBUTTONDOWN and homeRect.collidepoint(event.pos):
                                                        mode = mode_jeu()
                                                        pygame.mixer.music.unpause()
                                                        pause_jeu = False
        
        if mode == "adversaire":
                # - GESTION DES DÉPLACEMENT DES RAQUETTES -
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s] and left_paddle_y > 0:
                        left_paddle_y -= paddle_speed
                if keys [pygame.K_w] and left_paddle_y < HEIGHT - paddle_height:
                        left_paddle_y += paddle_speed
                if keys[pygame.K_UP] and right_paddle_y > 0: 
                        right_paddle_y -= paddle_speed
                if keys [pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
                        right_paddle_y += paddle_speed
                        
                ball_x += ball_speed_x
                ball_y += ball_speed_y

                #si la balle touche une raquette
                if (
                        left_paddle_x < ball_x < left_paddle_x + paddle_width
                        and left_paddle_y < ball_y < left_paddle_y + paddle_height
                ) or (
                        right_paddle_x < ball_x < right_paddle_x + paddle_width
                        and right_paddle_y < ball_y < right_paddle_y + paddle_height
                ):
                        ball_speed_x = -ball_speed_x

                #si la balle sort de l'écran :
                #par le bas/haut
                if ball_y <= 0 or ball_y >= HEIGHT:
                        ball_speed_y = -ball_speed_y
                #par la gauche/droite        
                if ball_x <= 0:
                        score_right += 1
                        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                        
                if ball_x >= WIDTH:
                        score_left += 1
                        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                        left_paddle_y, right_paddle_y = reset_paddles()

                #AFFICHAGE        
                screen.fill(L_PINK)
                screen.blit(pause, (pos_x_pause, pos_y_pause))
                screen.blit(home, (pos_x_home, pos_y_home))
                pygame.draw.rect(screen, D_PINK, (left_paddle_x, left_paddle_y, paddle_width, paddle_height))
                pygame.draw.rect (screen, D_PINK, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
                pygame.draw.ellipse(screen, D_PINK, (ball_x - 10, ball_y - 10, 20, 20))
                
                #commandes
                touche_s = arial_symbols.render("S=↑", True, D_PINK)
                screen.blit(touche_s, (WIDTH // 2 - 270, 15))
                touche_w = arial_symbols.render("W=↓", True, D_PINK)
                screen.blit(touche_w, (WIDTH // 2 - 270, 30))
                touche_up = arial_symbols.render("⌃=↑", True, D_PINK)
                screen.blit(touche_up, (WIDTH // 2 + 230, 15))
                touche_down = arial_symbols.render("⌄=↓", True, D_PINK)
                screen.blit(touche_down, (WIDTH // 2 + 230, 30))
                
                score_display = retro.render(f"{score_left} - {score_right}", True, D_PINK)
                screen.blit(score_display, (WIDTH // 2 - 25, 10))
                pygame.display.flip()
                
                pygame.time.Clock().tick(60)
                
        elif mode == "seul":
                # - GESTION DES DÉPLACEMENT DE LA RAQUETTE -
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and right_paddle_y > 0: 
                        right_paddle_y -= paddle_speed
                if keys [pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
                        right_paddle_y += paddle_speed
                        
                ball_x += ball_speed_x
                ball_y += ball_speed_y
                
                #si la balle touche la raquette
                if (
                        right_paddle_x < ball_x < right_paddle_x + paddle_width
                        and right_paddle_y < ball_y < right_paddle_y + paddle_height
                ):
                        ball_speed_x = -ball_speed_x

                if (
                        right_paddle_x < ball_x < right_paddle_x + paddle_width
                        and right_paddle_y < ball_y < right_paddle_y + paddle_height
                ):
                        score_right += 1
                        
                #si la balle sort de l'écran :
                #par le bas/haut/la gauche
                if ball_y <= 0 or ball_y >= HEIGHT :
                        ball_speed_y = -ball_speed_y
                if ball_x <= 0:
                        ball_speed_x = -ball_speed_x
                #par la droite
                if ball_x >= WIDTH:
                        last_score = score_right
                        high_score(last_score)
                        death,commencer = 1,1 ; restart()
                        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()
                        left_paddle_y, right_paddle_y = reset_paddles()

                #AFFICHAGE              
                screen.fill(L_PINK)
                screen.blit(pause, (pos_x_pause, pos_y_pause))
                screen.blit(home, (pos_x_home, pos_y_home))
                pygame.draw.rect (screen, D_PINK, (right_paddle_x, right_paddle_y, paddle_width, paddle_height))
                pygame.draw.ellipse(screen, D_PINK, (ball_x - 10, ball_y - 10, 20, 20))

                #commandes
                touche_up = arial_symbols.render("⌃=↑", True, D_PINK)
                screen.blit(touche_up, (WIDTH // 2 + 230, 15))
                touche_down = arial_symbols.render("⌄=↓", True, D_PINK)
                screen.blit(touche_down, (WIDTH // 2 + 230, 30))
                
                score_display = retro.render(f'Score : {score_right} - High Score : {highest_score}', True, D_PINK)
                screen.blit(score_display, (WIDTH // 2 - 150, 10))
                pygame.display.flip()
                pygame.time.Clock().tick(60)
                
        #Dès qu'un mode jeu est choisi
        if commencer == 0: 
                restart()
