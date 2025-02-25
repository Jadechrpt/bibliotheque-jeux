import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()
logo = pygame.image.load("Logo3.png")  
pygame.display.set_icon(logo)

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 600, 600
EPAISSEUR_LIGNE = 10

# Couleurs (en format RGB)
BLANC = (255, 255, 255)
BLEU = (245, 40, 145, 0.8)  # Couleur des lignes de la grille
ROSE = (150, 0, 50)  # Couleur du texte de sélection
ROUGE = (255, 0, 0)  # Couleur pour les résultats
SURVOL = (150, 150, 150)  # Couleur pour le survol des cases

# Configuration de la fenêtre de jeu
fenetre = pygame.display.set_mode((LARGEUR + 50, HAUTEUR + 50))
pygame.display.set_caption("Jeu de Morpion")
fenetre.fill(BLANC)

# diviser l'ecran en 3
TAILLE_CELLULE = LARGEUR // 3

# Grille 3*3
grille = [[None for _ in range(3)] for _ in range(3)]

# premier joueur + scores
joueur_actuel = "X"
score_x=0
score_y=0

# Chargement des images


victoire_image = pygame.image.load("fond.jpg")  
nul_image = pygame.image.load("fond.jpg")  
font_ecran= pygame.image.load("fond.jpg")
img_grille= pygame.image.load("Grille.jpg")



# Redimensionnement des images

victoire_image = pygame.transform.scale(victoire_image, (LARGEUR, HAUTEUR))
nul_image = pygame.transform.scale(font_ecran, (LARGEUR+50, HAUTEUR+50))
font_ecran= pygame.transform.scale(font_ecran, (LARGEUR+50, HAUTEUR+50))
img_grille=pygame.transform.scale(img_grille, (LARGEUR+290, HAUTEUR+290))





# dessiner la grille
def dessiner_grille():
    fenetre.fill(BLANC)
    fenetre.blit(img_grille, (-140, -130))


def dessiner_symbole(ligne, colonne, effet_ajout=True):
    centre_x = (colonne * TAILLE_CELLULE + TAILLE_CELLULE // 2)+25
    centre_y = (ligne * TAILLE_CELLULE + TAILLE_CELLULE // 2)+25
    image = x_image if grille[ligne][colonne] == "X" else o_image
    rect = image.get_rect(center=(centre_x, centre_y))

    if effet_ajout:
        for scale_factor in [0.6, 0.7, 0.8, 0.9, 1.0]:
            fenetre.fill(BLANC)
            dessiner_grille()
            for l in range(3):
                for c in range(3):
                    if grille[l][c] is not None:
                        img = x_image if grille[l][c] == "X" else o_image
                        img_pos = img.get_rect(center=((c * TAILLE_CELLULE + TAILLE_CELLULE // 2)+25, (l * TAILLE_CELLULE + TAILLE_CELLULE // 2)+25))
                        fenetre.blit(img, img_pos)
            temp_image = pygame.transform.scale(image, (int(rect.width * scale_factor), int(rect.height * scale_factor)))
            temp_rect = temp_image.get_rect(center=(centre_x, centre_y))
            fenetre.blit(temp_image, temp_rect)
            pygame.display.flip()
            pygame.time.delay(20) 
    else:
        fenetre.blit(image, rect)

# il y a un gagnant ?
def verifier_gagnant():
    for i in range(3):
        if grille[i][0] == grille[i][1] == grille[i][2] and grille[i][0] is not None:
            return grille[i][0]
        if grille[0][i] == grille[1][i] == grille[2][i] and grille[0][i] is not None:
            return grille[0][i]
    if grille[0][0] == grille[1][1] == grille[2][2] and grille[0][0] is not None:
        return grille[0][0]
    if grille[0][2] == grille[1][1] == grille[2][0] and grille[0][2] is not None:
        return grille[0][2]
    return None

# nul ?
def est_grille_pleine():
    for ligne in grille:
        if None in ligne:
            return False
    return True

# sélectionner un mode de jeu
def mode_jeu():
    fenetre.fill(BLANC)
    fenetre.blit(font_ecran, (0, 0)) 
    font = pygame.font.Font("Kenney Mini.ttf", 30)
    texte_choix1 = font.render("1. Jouer contre un adversaire", True, ROSE)
    texte_choix2 = font.render("2. Jouer contre l'ordinateur", True, ROSE)
    fenetre.blit(texte_choix1, (50, 200))
    fenetre.blit(texte_choix2, (50, 300))
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
                choix = "ordinateur"
    return choix

# chx ordi
def coup_ordinateur(grille):
    # gagner
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is None:
                grille[ligne][colonne] = "O"
                if verifier_gagnant() == "O":
                    return ligne, colonne
                grille[ligne][colonne] = None

    # défendre
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is None:
                grille[ligne][colonne] = "X"
                if verifier_gagnant() == "X":
                    grille[ligne][colonne] = None
                    return ligne, colonne
                grille[ligne][colonne] = None

    # aléa
    cases_vides = [(ligne, colonne) for ligne in range(3) for colonne in range(3) if grille[ligne][colonne] is None]
    return random.choice(cases_vides)

# fin partie
def afficher_resultat(image, message):
    fenetre.fill(BLANC)
    fenetre.blit(image, (0, 0))
    font = pygame.font.Font("Kenney MINI.ttf", 30)
    scores= font.render(f"  score X : {score_x}           score O : {score_y}", True, ROSE)
    texte_message = font.render(message, True, ROSE)
    fenetre.blit(texte_message, (150, 500))
    fenetre.blit(scores, (0, 0))
    pygame.display.flip()
    pygame.time.delay(1000)  # Laisser un délai pour que l'image et le texte apparaissent

    attendre_redemarrage()

# attendre le redémarrage
def attendre_redemarrage():
    while True:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_SPACE:
                return

# redémarrer
def redemarre():
    global grille, joueur_actuel
    grille = [[None for _ in range(3)] for _ in range(3)]
    joueur_actuel = "X"
    fenetre.fill(BLANC)
    dessiner_grille()
    pygame.display.flip()

def menu_selection(mode):
    pygame.init()
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Menu")
    couleur = (250, 0, 150)
    prop = []
    for i in range(7):
        icon = pygame.image.load(f"tete_{i+1}.png")
        prop.append(icon)
    font = pygame.font.Font(None, 50)
    current_index = 0
    transition_speed = 10 
    taille_milieu = 200
    taille_cote = 50
    espace = 250
    scroll_offset = 0
    animating = False
    direction = 0
    size_progress = 1
    animation_speed = 0.02
    selected_icons = []
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(couleur)
        font = pygame.font.Font("Kenney Mini.ttf", 30)
        text = font.render(f"J{len(selected_icons) + 1}", True, (0, 0, 0)) if mode=="adversaire" else font.render(f"J{len(selected_icons) + 1}" if len(selected_icons) + 1==1 else f"choisissez pour l'ordi" , True, (0, 0, 0))
        text2 = font.render(f"Entrée pour sélectionner", True, (0, 0, 0))
        screen.blit(text2, (100, 450))
        screen.blit(text, (screen_width // 2 - 20, 50) if mode=="adversaire" or mode=="ordinateur" and len(selected_icons) + 1==1 else (130, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and not animating:
                    direction = 1
                    animating = True
                    size_progress = 0
                elif event.key == pygame.K_LEFT and not animating:
                    direction = -1
                    animating = True
                    size_progress = 0
                elif event.key == pygame.K_RETURN:
                    selected_icons.append(prop[current_index])
                    prop.remove(prop[current_index])
                    if len(selected_icons) == 2:
                        return selected_icons
        if animating:
            size_progress += animation_speed
            scroll_offset = (espace * direction) * (1 - size_progress)
            if size_progress >= 1:
                animating = False
                current_index = (current_index + direction) % len(prop)
                scroll_offset = 0
                size_progress = 1
        for i in range(-1, 2):
            if animating:
                index = (current_index + i + direction) % len(prop)
            else:
                index = (current_index + i) % len(prop)
            if i == 0:
                icon_size_scaled = taille_cote + (taille_milieu - taille_cote) * size_progress
            else:
                icon_size_scaled = taille_milieu - (taille_milieu - taille_cote) * size_progress
            x_position = (screen_width / 2) - (icon_size_scaled / 2) + (i * espace) + scroll_offset
            y_position = screen_height / 2 - icon_size_scaled / 2
            icon_scaled = pygame.transform.scale(prop[index], (int(icon_size_scaled), int(icon_size_scaled)))
            screen.blit(icon_scaled, (x_position, y_position))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    return selected_icons

# musique
pygame.mixer.music.load("son.mp3")
pygame.mixer.music.play(-1)

#sélection du mode de jeu
mode = mode_jeu()
x_image, o_image = menu_selection(mode)  # Sélection des jetons après choix du mode de jeu
x_image = pygame.transform.scale(x_image, (TAILLE_CELLULE - 60, TAILLE_CELLULE - 60))
o_image = pygame.transform.scale(o_image, (TAILLE_CELLULE - 60, TAILLE_CELLULE - 60))




# Boucle principale du jeu
jeu_en_cours = True
while jeu_en_cours:
    fenetre.fill(BLANC)
    dessiner_grille()

    # Détecter la souris au dessus d'une case et changer la couleur
    souris_x, souris_y = pygame.mouse.get_pos()
    colonne_survol = (souris_x-25) // TAILLE_CELLULE
    ligne_survol = (souris_y-25) // TAILLE_CELLULE
    if 25<souris_x<625 and 25<souris_y<625 and grille[ligne_survol][colonne_survol] is None: pygame.draw.circle(fenetre, SURVOL, ( colonne_survol * TAILLE_CELLULE+125, ligne_survol * TAILLE_CELLULE+125), TAILLE_CELLULE//5, 40 )

    # Dessiner les symboles 
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is not None:
                dessiner_symbole(ligne, colonne, effet_ajout=False)
                
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            jeu_en_cours = False

        if mode == "adversaire":
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1 and 25<evenement.pos[0]<625 and 25<evenement.pos[1]<625:
                x, y = evenement.pos
                colonne = (x - 25) // TAILLE_CELLULE
                ligne = (y - 25) // TAILLE_CELLULE
                if grille[ligne][colonne] is None:
                    grille[ligne][colonne] = joueur_actuel
                    dessiner_symbole(ligne, colonne)  # Ajouter l'effet de placement
                    gagnant = verifier_gagnant()
                    if gagnant:
                        if gagnant=="X":
                            score_x+=1 
                        else :
                            score_y+=1
                        afficher_resultat(victoire_image, f"Le joueur {gagnant} a gagné !")

                        redemarre()
                    elif est_grille_pleine():
                        afficher_resultat(nul_image, "Match nul !")
                        redemarre()
                    joueur_actuel = "O" if joueur_actuel == "X" else "X"
            pygame.display.flip()

        elif mode == "ordinateur":
            if joueur_actuel == "X":
                if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                    x, y = evenement.pos
                    colonne = (x-25) // TAILLE_CELLULE
                    ligne = (y-25) // TAILLE_CELLULE
                    if grille[ligne][colonne] is None:
                        grille[ligne][colonne] = joueur_actuel
                        dessiner_symbole(ligne, colonne)
                        gagnant = verifier_gagnant()
                        if gagnant:
                            afficher_resultat(victoire_image, f"Le joueur {gagnant} a gagné !")
                            redemarre()
                        elif est_grille_pleine():
                            afficher_resultat(nul_image, "Match nul !")
                            redemarre()
                        joueur_actuel = "O"
            else:
                time.sleep(0.25)
                ligne, colonne = coup_ordinateur(grille)
                grille[ligne][colonne] = "O"
                dessiner_symbole(ligne, colonne)
                gagnant = verifier_gagnant()
                if gagnant:
                    afficher_resultat(victoire_image, f"L'ordinateur ({gagnant}) a gagné !")
                    redemarre()
                elif est_grille_pleine():
                    afficher_resultat(nul_image, "Match nul !")
                    redemarre()
                joueur_actuel = "X"
            pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
