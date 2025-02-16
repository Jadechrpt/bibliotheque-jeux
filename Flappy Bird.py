#Flappy Bird

#importe les bibliothèques nécessaires
import pygame, sys, random
#variable pour gérer l'écran de jeu, de démarrage, de pause etc
flappy_bird_jeu = 0
#initialisation de Pygame
pygame.init()
#initialsation de la musique
pygame.mixer.init()
#charger la musique de fond
pygame.mixer.music.load("kk.wav")
#Règle le volume
pygame.mixer.music.set_volume(0.5)
#Répète la musique en boucle
pygame.mixer.music.play(-1)
#charge les sons
son_jump = pygame.mixer.Sound("Jump.wav")
son_tuyau_passed = pygame.mixer.Sound("Tuyau passed.wav")
son_game_over = pygame.mixer.Sound("Game over.wav")
#création de la fenêtre et titre
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird Coquette")
#réglage de la position de l'oiseau rose, à 50 du bord et à la moitié de la hauteur
oiseau_rose_x, oiseau_rose_y = 50, 300
#crée des variables servant à régler la gravité et le saut de l'oiseau rose
oiseau_rose_gravite, oiseau_rose_saut, oiseau_rose_vitesse = 0.5, -10, 0
#création de la liste des tuyaux avec leurs paramètres (écart, vitesse, largeur)
tuyaux, tuyau_largeur, tuyau_ecart, vitesse_tuyaux = [], 80, 200, 3
#initialisation du score et du meilleur score
score, meilleur_score = 0, 0
#fonction pour ajouter un nouveau tuyau
def ajouter_tuyau():
    #crée une hauteur aléatoire pour le tuyau du haut
    hauteur = random.randint(100, 400)
    #le tuple (800, hauteur) représente la position x du tuyau (donc tout à droite de l'écran, à x = 800), et la hauteur du tuyau du haut
    tuyaux.append((800, hauteur))
#déplacement/ajout/suppression des tuyaux
def deplacer_tuyaux():
    global tuyaux
    for i in range(len(tuyaux)):
        #attribue les valeurs 800 et hauteur dans le tuple de la liste tuyaux à x et h, pour chaque indice (chaque i)
        x, h = tuyaux[i]
        #la hauteur reste la même mais le x diminue de vitesse_tuyau, donc de 3
        tuyaux[i] = (x - vitesse_tuyaux, h)
    #s'il n'y a pas de tuyau ou si le dernier tuyau est à 300 pixels du bord
    if len(tuyaux) == 0 or tuyaux[-1][0] < 500:
        #ajoute un nouveau tuyau si nécessaire
        ajouter_tuyau()
    #suppression des tuyaux sortis de l'écran:
    nouveaux_tuyaux = []
    for t in tuyaux:
        #garde uniquement les tuyaux visibles
        if t[0] > -tuyau_largeur:
            nouveaux_tuyaux.append(t)
    #met à jour la liste de tuyaux pour supprimer ceux qui ne sont plus visibles dans la fenêtre
    tuyaux = nouveaux_tuyaux
#contrôle le temps et la fluidité du jeu
clock = pygame.time.Clock()
#boucle principale
while True:
    #si on est sur l'écran de démarrage
    if flappy_bird_jeu == 0:
        #couleur de fond de l'écran de démarrage
        fenetre.fill((135, 206, 250))
        #affiche et positionne les textes de l'écran d'accueil
        fenetre.blit(pygame.font.Font(None, 104).render("Flappy Bird Coquette", True, (255, 105, 180)), (400 - pygame.font.Font(None, 104).render("Flappy Bird Coquette", True, (255, 105, 180)).get_width() // 2, 50))
        fenetre.blit(pygame.font.Font(None, 36).render("Appuyer sur ESPACE pour démarrer", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Appuyer sur ESPACE pour démarrer", True, (255, 255, 255)).get_width() // 2, 500))
        fenetre.blit(pygame.font.Font(None, 36).render("Commandes :", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Commandes :", True, (255, 255, 255)).get_width() // 2, 200))
        fenetre.blit(pygame.font.Font(None, 36).render("Sauter :", True, (255, 255, 255)), (150, 250))
        fenetre.blit(pygame.font.Font(None, 36).render("Espace", True, (255, 255, 255)), (150, 300))
        fenetre.blit(pygame.font.Font(None, 36).render("Pause :", True, (255, 255, 255)), (500, 250))
        fenetre.blit(pygame.font.Font(None, 36).render("P", True, (255, 255, 255)), (500, 300))
        #gère les événements pygame
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #touche espace du clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #on bascule sur l'écran de jeu
                    flappy_bird_jeu = 1
    #si on est sur l'écran de jeu
    elif flappy_bird_jeu == 1 :
        #contrôle le déplacement/ajout/suppression des tuyaux en permanence
        deplacer_tuyaux()
        #ajoute la couleur de fond
        fenetre.fill((135, 206, 250))
        #gestion des événements
        for event in pygame.event.get():
            #pour quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #touche du clavier pressée
            if event.type == pygame.KEYDOWN:
                #pour sauter quand le joueur appuie sur la touche espace
                if event.key == pygame.K_SPACE:
                    oiseau_rose_vitesse = oiseau_rose_saut
                    #joue le son du saut
                    son_jump.play()
                #pour mettre en pause quand le joueur appuie sur p
                if event.key == pygame.K_p:
                    flappy_bird_jeu = 3
        #crée la gravité
        oiseau_rose_vitesse += oiseau_rose_gravite
        #permet de faire descendre le personnage avec la gravité, mais aussi de le faire monter lors des sauts
        oiseau_rose_y += oiseau_rose_vitesse
        #création des tuyaux
        for x, h in tuyaux:
            #dessine le tuyau du haut
            pygame.draw.rect(fenetre, (255, 105, 180), (x, 0, tuyau_largeur, h))
            #dessine le tuyau du bas grâce à la variable tuyau_ecart qui représente l'écart entre le tuyau du haut et le tuyau du bas
            pygame.draw.rect(fenetre, (255, 105, 180), (x, h + tuyau_ecart, tuyau_largeur, 600 - h - tuyau_ecart))
            #si l'oiseau rose a la même abscisse que le tuyau, alors le score augmente de 1
            if x == oiseau_rose_x:
                score += 1
                #joue un son quand l'oiseau rose passe un tuyau
                son_tuyau_passed.play()
        #ajout de l'oiseau rose
        fenetre.blit(pygame.transform.scale(pygame.image.load("Oiseau.png"), (50, 50)), (oiseau_rose_x, oiseau_rose_y))
        #affichage du score/meilleur score
        fenetre.blit(pygame.font.Font(None, 36).render(f"Meilleur score : {meilleur_score}", True, (255, 255, 255)), (580, 10))
        fenetre.blit(pygame.font.Font(None, 36).render(f"Score : {score}", True, (255, 255, 255)), (10, 10))
        #détection des collisions:
        #bord : si l'oiseau rose va trop haut ou trop bas
        if oiseau_rose_y > 600 or oiseau_rose_y < 0:
            flappy_bird_jeu = 2
            #joue le son de défaite
            son_game_over.play()
        #tuyaux : si l'oiseau touche des tuyaux
        for x, h in tuyaux:
            if oiseau_rose_x + 50 > x and oiseau_rose_x < x + tuyau_largeur:
                if oiseau_rose_y < h or oiseau_rose_y + 50 > h + tuyau_ecart:
                    flappy_bird_jeu = 2
                    #joue le son de défaite
                    son_game_over.play()
    #si le joueur perd et que l'écran de fin s'affiche
    elif flappy_bird_jeu == 2 :
        #arrête la musique
        pygame.mixer.music.stop()
        #couleur de fond
        fenetre.fill((135, 206, 250))
        #afficher les textes "Game Over", "Rejouer" et "Quitter" et les positionner
        fenetre.blit(pygame.font.Font(None, 104).render("Game Over !", True, (255, 105, 180)), (400 - pygame.font.Font(None, 104).render("Game Over !", True, (255, 105, 180)).get_width() // 2, 200))
        fenetre.blit(pygame.font.Font(None, 36).render("Appuyez sur ESPACE pour rejouer", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Appuyez sur ESPACE pour rejouer", True, (255, 255, 255)).get_width() // 2, 310))
        fenetre.blit(pygame.font.Font(None, 36).render("Appuyez sur ÉCHAP pour quitter", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Appuyez sur ÉCHAP pour quitter", True, (255, 255, 255)).get_width() // 2, 350))
        #gère le meilleur score
        if score > meilleur_score:
            meilleur_score = score
        #met à jour l'affichage
        pygame.display.flip()
        #attendre le choix du joueur : rejouer ou quitter
        for event in pygame.event.get():
            #quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #touche du clavier
            if event.type == pygame.KEYDOWN:
                #rejouer grâce à la touche espace, et revenir dans l'écran de jeu
                if event.key == pygame.K_SPACE:
                    flappy_bird_jeu = 1
                    #réinitialise les variables pour que le joueur puisse rejouer s'il le souhaite
                    oiseau_rose_x, oiseau_rose_y, oiseau_rose_vitesse, tuyaux, score = 50, 300, 0, [], 0
                    #relance la musique
                    pygame.mixer.music.load("kk.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                #quitter grâce à la touche échap
                if event.key == pygame.K_ESCAPE:
                    flappy_bird_jeu = 4
    #on bascule sur l'écran de pause
    elif flappy_bird_jeu == 3 :
        #affichage de l'écran de pause, sur le même modèle que l'écran de démarrage
        fenetre.fill((135, 206, 250))
        fenetre.blit(pygame.font.Font(None, 104).render("Pause", True, (255, 105, 180)), (400 - pygame.font.Font(None, 104).render("Pause", True, (255, 105, 180)).get_width() // 2, 100))
        fenetre.blit(pygame.font.Font(None, 36).render("Commandes :", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Commandes :", True, (255, 255, 255)).get_width() // 2, 200))
        fenetre.blit(pygame.font.Font(None, 36).render("Reprendre :", True, (255, 255, 255)), (200 - pygame.font.Font(None, 36).render("Reprendre :", True, (255, 255, 255)).get_width() // 2, 300))
        fenetre.blit(pygame.font.Font(None, 36).render("P", True, (255, 255, 255)), (200 - pygame.font.Font(None, 36).render("P", True, (255, 255, 255)).get_width() // 2, 340))
        fenetre.blit(pygame.font.Font(None, 36).render("Recommencer :", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Recommencer :", True, (255, 255, 255)).get_width() // 2, 300))
        fenetre.blit(pygame.font.Font(None, 36).render("Espace", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Espace", True, (255, 255, 255)).get_width() // 2, 340))
        fenetre.blit(pygame.font.Font(None, 36).render("Quitter :", True, (255, 255, 255)), (600 - pygame.font.Font(None, 36).render("Quitter :", True, (255, 255, 255)).get_width() // 2, 300))
        fenetre.blit(pygame.font.Font(None, 36).render("Échap", True, (255, 255, 255)), (600 - pygame.font.Font(None, 36).render("Échap", True, (255, 255, 255)).get_width() // 2, 340))
        #gère les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                #touche p pressée, reprend le jeu
                if event.key == pygame.K_p:
                    flappy_bird_jeu = 1
                #touche espace pressée, recommence le jeu
                if event.key == pygame.K_SPACE:
                    flappy_bird_jeu = 1
                    #réinitialise les variables pour que le joueur puisse rejouer
                    oiseau_rose_x, oiseau_rose_y, oiseau_rose_vitesse, tuyaux, score = 50, 300, 0, [], 0
                #touche echap pressée, quitte le jeu
                if event.key == pygame.K_ESCAPE:
                    flappy_bird_jeu = 4
    #on bascule sur l'écran de crédits
    elif flappy_bird_jeu == 4:
        #affichage de l'écran de crédits, sur le même modèle que la pause ou le démarrage
        fenetre.fill((135, 206, 250))
        fenetre.blit(pygame.font.Font(None, 104).render("Merci d'avoir joué !", True, (255, 105, 180)), (75, 20))
        fenetre.blit(pygame.font.Font(None, 36).render("Codeuse :", True, (255, 255, 255)), (110, 120))
        fenetre.blit(pygame.font.Font(None, 36).render("Justine", True, (255, 255, 255)), (120, 160))
        fenetre.blit(pygame.font.Font(None, 36).render("Relecteurs :", True, (255, 255, 255)), (450, 120))
        fenetre.blit(pygame.font.Font(None, 36).render("Arthur, Jade, Alexandre, Clara", True, (255, 255, 255)), (380, 160))
        fenetre.blit(pygame.font.Font(None, 36).render("Inspiré du jeu Flappy Bird", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Inspiré du jeu Flappy Bird", True, (255, 255, 255)).get_width() // 2, 240))
        fenetre.blit(pygame.font.Font(None, 36).render("(mais rendu coquette parce que c'est plus joli)", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("(mais rendu coquette parce que c'est plus joli)", True, (255, 255, 255)).get_width() // 2, 280))
        fenetre.blit(pygame.font.Font(None, 36).render("Sons :", True, (255, 255, 255)), (135, 360))
        fenetre.blit(pygame.font.Font(None, 36).render("Trouvés sur Zedge", True, (255, 255, 255)), (70, 400))
        fenetre.blit(pygame.font.Font(None, 36).render("Musique :", True, (255, 255, 255)), (450, 360))
        fenetre.blit(pygame.font.Font(None, 36).render("Bubblegum Kéké, par Kéké Laglisse", True, (255, 255, 255)), (340, 400))
        fenetre.blit(pygame.font.Font(None, 36).render("Aucun oiseau n'a été blessé durant ce jeu.", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Aucun oiseau n'a été blessé durant ce jeu.", True, (255, 255, 255)).get_width() // 2, 480))
        fenetre.blit(pygame.font.Font(None, 36).render("Appuyer sur ECHAP pour quitter", True, (255, 255, 255)), (400 - pygame.font.Font(None, 36).render("Appuyer sur ECHAP pour quitter", True, (255, 255, 255)).get_width() // 2, 520))
        pygame.display.flip()
        #gère les événements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #quitter avec la touche echap
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    #met à jour l'affichage
    pygame.display.flip()
    #règle le temps et le nombre d'images par seconde
    clock.tick(60)