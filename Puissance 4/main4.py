import pygame
import os #pour police
from pygame import mixer#pour mettre de la musique

pygame.init()
mixer.init()

score_joueur1=0
score_joueur2=0

# variables importantes
LARGEUR_CASE = 100
ROSE = (255, 192, 203)
ROUGE =(255,0,0)
JAUNE = (255,255,0)
VIOLET =(191, 162, 219)
BLEU= (64, 224, 208)
CLAIR = (240, 240, 240)
RAYON = int(LARGEUR_CASE / 2) -4# rayon cercle pour determiner leur taille, plus peite marge -4
NB_LIGNE = 6
NB_COLONNE = 7

#variable de positions
largeur = NB_COLONNE * LARGEUR_CASE
hauteur = (NB_LIGNE + 1) * LARGEUR_CASE  #laisse une ligne vide en haut
taille = (largeur, hauteur)
ecran = pygame.display.set_mode(taille)#On définit la fenêtre avec la taille calculée
pygame.display.set_caption("Jeu")


#vaariables necessaire pour trouver la police
chemin_police = os.path.join("fonts", "PWHappyChristmas.ttf")
myfont = pygame.font.Font(chemin_police, 40)

chemin_police_score= os.path.join("fonts", "CuteBold.ttf")
scorefont= pygame.font.Font(chemin_police_score, 30)

chemin_police_fin = os.path.join("fonts", "game_over.ttf")
game_over_font= pygame.font.Font(chemin_police_fin, 70)

#variavle pour l'image du neoud, le chemin, et pour le redimensionner
chemin_image_noeud = os.path.join("images", "noeudnouc.png")  # Remplacez par le chemin de votre image de nœud
image_noeud = pygame.image.load(chemin_image_noeud)
image_noeud = pygame.transform.scale(image_noeud, (100, 100))#redimensioner

#Musique de fond :
mixer.music.load("glitter (1).mp3")#la musique se joue une  fois
mixer.music.play(-1)#faire jouer la musique en boucle


#variables pour le jeu
game_over = False  # Pour l'instant on ne fait que tester l'affichage
joueur = 1 #le joueur ets par defaut le 1
score_joueur1=0
score_joueur2=0

#creation  plateau vide
def creer_plateau():
    plateau = []  # liste vide
    for i in range(NB_LIGNE -1, -1, -1):  
        ligne = [0] * NB_COLONNE  
        plateau.append(ligne)  

    return plateau  # retourne le plateau rempli de 0

def afficher_plateau(plateau):
    print("État actuel du plateau :")
    for ligne in range(NB_LIGNE - 1, -1, -1):  # afiche de la dernière ligne à la première
        print(plateau[ligne])


#  dessine  plateau du jeu
def dessiner_plateau(plateau):
    # Dessiner rectangle par rapport : surface, couleur, dimension, position
    pygame.draw.rect(ecran, ROSE, (0, LARGEUR_CASE, largeur, hauteur - LARGEUR_CASE ), )

    # dzsiner les cercles blancs pour emplacements vides
    for colonne in range(NB_COLONNE):  # Pour chaque colonne
        for ligne in range(NB_LIGNE):  # Pour chaque ligne
            position_gauche = colonne * LARGEUR_CASE  # Bord gauche de la colonne
            x = position_gauche + LARGEUR_CASE / 2  # position horizontale du cercle

              #bord haut de la ligne(on met la ligne tout en haut tout en bas )
            y = hauteur - (ligne + 1) * LARGEUR_CASE + LARGEUR_CASE / 2    # Positin verticale du cercle
            # Dessiner le cercle noir
            pygame.draw.circle(ecran, CLAIR, (x, y), RAYON)  # ajusté pour l'espace

        #Dans matrice :  jeton rouge est affiché pour 1,  jeton jaune pour 2 , 0 : Case vide, quand les jours jouent, le tableau est mis a jour
            if plateau[ligne][colonne] == 1: #si le joueur 1 joue,
                pygame.draw.circle(ecran, VIOLET, (x, y), RAYON) #on crée un jeton rouge

            if plateau[ligne][colonne] == 2: #si le joueur 2 joue a cet emplacement
                pygame.draw.circle(ecran, BLEU, (x, y), RAYON) #on crée un jeton Jaune a cet emplacement
# affichage

    pygame.display.update()

#fonction permettant de trouver une case vide dans la colonne choisie par l'utilisateur



def trouver_case_vide(plateau, colonne):
    # Parcourir les lignes du bas vers le haut (de 5 à 0)
    for ligne in range(NB_LIGNE ):
        if plateau[ligne][colonne] == 0:  # Vérifie si la case est vide
            return ligne  # Renvoie la ligne si elle est vide
    return -1

#fonction permettant d'affecter la valeur 1 ou 2 à une case selon le joueur
def lacher_jeton(joueur, plateau, ligne, colonne_souris):
    plateau[ligne][colonne_souris]= joueur  #la case prends la valeur du joueur donc soit1 soit 2
    dessiner_plateau(plateau)




#Verifier si la partie est nul c'est a dir si toutes les cases sont utilisées et qu'il n'y a pas de victoires
def partie_nulle(plateau):
    for colonne in range (7):
        ligne = trouver_case_vide(plateau, colonne )
        if ligne !=-1:
            return False
    return True#Si aucune case vide n'est trouvée la partie est nulle

def joueur_gagnant(plateau, joueur):
    for ligne in range(6):
        jeton_aligné=0

        #verifier si 4 jetons alignés horizontalement
        for colonne in range(7):
            if plateau[ligne][colonne]==joueur: #pour le joueur1
                jeton_aligné+=1
                if jeton_aligné ==4:
                    return True
            else:
                jeton_aligné=0#reinitialisation des jetons

    #verificaton verticale :
    for colonne in range (7):
        jeton_aligné=0
        for ligne in range(6):
            if plateau[ligne][colonne]==joueur:
                jeton_aligné+=1
                if jeton_aligné==4:
                    return True
            else:
                jeton_aligné=0
    #verification diagonale ver le haut droit :
    for ligne in range(6): #parcours chaque ligne
        for colonne in range(7): #parcours chaque colonne
            jeton_aligné=0
            #pour chaque iteration , la colonne et la ligne augmente de i  pour verifier la diagonale
            for i in range(4):
                ligne_verif = ligne +i
                colonne_verif = colonne +i
                if ligne_verif <6 and colonne_verif<7: #verifier que cela reste dans la grille
                    if plateau[ligne_verif][colonne_verif]==joueur: #si joueur 1
                        jeton_aligné+=1
                    else:
                        break #sortir de la boucle si jeton rouge ou vide
            if jeton_aligné==4:
                return True

    #diagonalele ver le bas :
    for ligne in range (NB_LIGNE - 1, 2, -1): # seulement 3 colonnes peuvent avoir une diagonales decsendante car sinon pas assez d'espaces
        for colonne in range(NB_COLONNE - 3): #parcours chaque colonne
            jeton_aligné=0
            #pour chaque iteration , la colonne et la ligne augmente de i  pour verifier la diagonale
            for i in range(4):
                ligne_verif = ligne -i #vue que c'est decendant on soustrait
                colonne_verif = colonne +i
                if ligne_verif <6 and colonne_verif <7: #verifier que cela reste dans la grille
                    if plateau[ligne_verif][colonne_verif]==joueur: #si joueur
                        jeton_aligné+=1
                    else:
                        break #sortir de la boucle si jeton rouge ou vide
            if jeton_aligné==4:
                return True
            else:
                jeton_aligné=0
    return False

#on met une image comme si on créée un renctagle
def rectangle_fin_de_partie():
    # Dessiner le rectangle

    texte_game_over = game_over_font.render(" GAME OVER ", True, ROUGE)
    texte_rect = texte_game_over.get_rect(center=(largeur // 2, 50))  # Position Y à 50 pixels du haut
    ecran.blit(texte_game_over, texte_rect)

    print("dessin du triangle")
    image_background = pygame.image.load("images/fenetre_finale.png")
    rectangle_largeur = largeur // 1.005 # Largeur du rectangle
    rectangle_hauteur = hauteur//1.15 # Hauteur du rectangle

    image_background = pygame.transform.scale(image_background, (int(rectangle_largeur), int(rectangle_hauteur)) ) # Redimensionner image


    rectangle_x = (largeur - rectangle_largeur) // 2  # Centré horizontalement
    rectangle_y = 80 # Centré verticalement
    ecran.blit(image_background, (rectangle_x, rectangle_y)) # on met l'image au lieu de dessiner un rectangle : pygame.draw.rect(ecran, ROUGE, (rectangle_x, rectangle_y, rectangle_largeur, rectangle_hauteur))




#on creer une classe bouton qui nous servira par exemple a rejouer une partie ou quitter. cela permet de directement creer un bouton en lui affectant un texte, et une position
class Button :
    def __init__(self, text, x_position, y_position):
        self.text= text
        self.x_position= x_position
        self.y_position= y_position

    def draw(self, ecran):
        bouton_texte= myfont.render(self.text, True, JAUNE)#on recupere le txete entré et on lui affete la police
        button_rect= pygame.Rect((self.x_position,self.y_position), (170, 50))#on position  le rectangle du boutoon
        pygame.draw.rect(ecran, ROUGE,button_rect, 0, 5 )#on dessine le rectangle en question
        ecran.blit(bouton_texte,(self.x_position+3, self.y_position+3) )#on affiche le texte mais on ajoute 3 pixel sur les cotés et en haut pour qu'il ne sit pas collé au rectangle

    #on verifie si le bouton est cliqué
    def verif_click(self):
        position_souris= pygame.mouse.get_pos()#on obtient la position de la souris
        print(f"Position de la souris : {position_souris}")
        clique_gauche= pygame.mouse.get_pressed()[0]#on veryfie si le clique gauche de la souris est actionné
        button_rect= pygame.Rect((self.x_position,self.y_position), (170, 50))
        print(f"Click gauche : {clique_gauche}")
        if clique_gauche and button_rect.collidepoint(position_souris): # si la souris est cliqué et qu'elle est du le rectangle crée
            return True
        else:
            return False

    def hide(self):  # méthode pour cacher le bouton
        self.visible = False

    def show(self):  # méthode pour afficher le bouton
        self.visible = True
button_rejouer= Button("rejouer", 265, 500)#on crée le bouton rejouer


def afficher_scores():
    score_text1 = scorefont.render(f"JOUEUR 1: {score_joueur1}", True, ROSE)
    score_text2= scorefont.render(f" JOUEUR2: {score_joueur2}", True, ROSE)
    ecran.blit(score_text1, [200, 415])
    ecran.blit(score_text2, [350, 415])



#fonction pour savoir si la partie est terminé
def victoire_ou_nul(joueur ):
    global score_joueur1, score_joueur2
    if joueur_gagnant(plateau, joueur): #verification de victoires



        #bloc de code servant a jouer les musique de victoire :)
        chemin_victoire1= os.path.join("son", "victoire_1.mp3")
        victoire1_sound= mixer.Sound(chemin_victoire1)
        victoire1_sound.play()
        chemin_victoire_musique= os.path.join("son", "victoirereal.mp3")
        victoire_musique= mixer.Sound(chemin_victoire_musique)
        victoire_musique.play()


        print(f"Le joueur {joueur} Gagné ! Bravo ! Joueur {3 - joueur} Shame on you")#afficher dans console si victoire
        texte1 = myfont.render(f"LE JOUEUR {joueur} GAGNE", True, VIOLET)
        texte2 = myfont.render(f" JOUEUR {3-joueur} perdant ", True, BLEU)

        rectangle_fin_de_partie()
        ecran.blit(texte1, [170, 250])# Affiche texte_image à (50, 10) : 50 pixels à droite et 10 pixels en bas.
        ecran.blit(image_noeud, (305, 95))


        if joueur == 1:
            score_joueur1 += 1  # Incrémente le score du joueur 1
        elif joueur  == 2:
            score_joueur2 += 1  # Incrémente le score du joueur 2

        afficher_scores()

        button_rejouer.draw(ecran)

        pygame.display.update()  # Mettre à jour l'affichage pour que texte1 soit visible
        pygame.time.delay(2000)
        ecran.blit(texte2, [160, 315])#

        chemin_musique_perdant= os.path.join("son", "perdant.mp3")
        victoire_musique= mixer.Sound(chemin_musique_perdant)
        victoire_musique.play()



        pygame.display.update()

        return True

    if partie_nulle(plateau) == True :
        chemin_nul = os.path.join("son", "ANMLCat_Grognement chat 3 (ID 1887)_LS.wav")
        nul_sound= mixer.Sound(chemin_nul)
        nul_sound.play()
        print("Aucun gagnant la partie es nulle :()")
        textenul2 = myfont.render("Trop Nul", True, ROUGE)
        ecran.blit(textenul2, [70, 10])
        return True
    return False

def rejouer(joueur_gagnant):
    global joueur, plateau, score_joueur1, score_joueur2  # Gardez les autres variables si nécessaire

    ecran.fill(CLAIR)
    joueur = joueur_gagnant  # Le joueur qui a gagné commence
    plateau = creer_plateau()  # Réinitialiser le plateau
    dessiner_plateau(plateau)  # Dessiner le nouveau plateau
    print(f"Partie recommencée ! Joueur {joueur} commence.")  # Afficher qui commence

    return plateau


    # affichage
pygame.display.update()

plateau = creer_plateau()










afficher_plateau(plateau)

if joueur_gagnant(plateau, 1):
    print("Gagné ! Bravo ! Le joueur 1 a gagné !")
    game_over = True
else:
    print("Le joueur 1 n'a pas gagné.")


# Utiliser fonction pour creer tableau rose
dessiner_plateau(plateau)


dessiner_plateau(plateau)
#Tant que game over est faux, programme pred en compte les clicks de souris et lorsque la croix rouge est cliqué, fin du programme
while not game_over:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over = True

        #si le joueur déplace le jeton avec la souris
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(ecran, CLAIR, (0, 0, largeur, LARGEUR_CASE))
            # Position de la souris
            posx = event.pos[0]  # Définir posx ici

            # Si c'est le joueur 1, on dessine un jeton rouge
            if joueur == 1:
                pygame.draw.circle(ecran, VIOLET, (posx, int(LARGEUR_CASE / 2)), RAYON)
            # Si c'est le joueur 2, on dessine un jeton jaune
            elif joueur==2:
                pygame.draw.circle(ecran, BLEU, (posx, int(LARGEUR_CASE / 2)), RAYON)


            # Mettre l'écran à jour
            pygame.display.update()


        #si le joeur  clique sur la souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("click détécté")#verifier que le click est detecté
            pygame.draw.rect(ecran,CLAIR,(0,0,largeur,LARGEUR_CASE))#pour que la partie du haut soit claire

            posx = event.pos[0] #coordonnées de x lorsque le joeuur clqiue sur la souris
            colonne_souris= posx // LARGEUR_CASE #determiner colonne choisi par l'utilisateur
            print(f"Colonne choisie: {colonne_souris+1}")#verifier la colone choisie
            if 0 <= colonne_souris < 7: #s'assurer que la colone est valide donc positive et >7
                # Lorsque le JOEUR1 joue

                ligne = trouver_case_vide(plateau, colonne_souris)
                if ligne != -1:  # Si la ligne est vide
                    lacher_jeton(joueur, plateau, ligne, colonne_souris)

                    print(f"Placing token: {joueur} at line {ligne}, column {colonne_souris}")
                    if joueur==1:
                        paillette_sound= mixer.Sound("jeton .mp3")
                        paillette_sound.play()
                    elif joueur ==2:
                        chemin_jeton = os.path.join("son", "ANMLCat_Petit miaulement d un chat (ID 0494)_LS.wav")
                        bleu_sound= mixer.Sound(chemin_jeton)
                        bleu_sound.play()




                    if victoire_ou_nul(joueur)==True:
                            button_rejouer.show()  # Affiche le bouton après la victoire/nul
                            game_over = True  # Terminer la partie pour déclencher le bouton "Rejouer"

                    # Sinon, change de joueur
                    else:
                            joueur = 2 if joueur == 1 else 1


    # Si la partie est terminée, on vérifie si le bouton "Rejouer" est cliqué
    while game_over:
        # Vérifier continuellement si le bouton "Rejouer" est cliqué
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rejouer.verif_click():  # Si le bouton est cliqué
                    plateau = rejouer(joueur)  # Rejouer directement
                    button_rejouer.hide()  # Cache le bouton après le clic
                    game_over = False
                    break















    # Utiliser fonction pour creer tableau rose

pygame.display.update()
pygame.time.wait(3000)
# Quitter pygame
pygame.quit()