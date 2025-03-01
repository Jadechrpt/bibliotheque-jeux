#Pac-man
# Import bibliothèque
import pygame
import sys
import time
import random
import os

# Initialisation de Pygame
pygame.init()
#audio
pygame.mixer.init()

# Initialisation du module de police
pygame.font.init()

# déf tick
clock = pygame.time.Clock()

# Centrer la fenêtre
os.environ['SDL_VIDEO_CENTERED'] = '1'

#images pacman
def charger_images(dossier, prefixe="Pac_man"):
    images = {}
    for fichier in sorted(os.listdir(dossier)):  # Trier pour garantir l'ordre
        if fichier.startswith(prefixe) and fichier.endswith(".png"):
            nom_cle = fichier.replace(".png", "").replace('_', '')  # Clé sans extension et sans _
            chemin_complet = os.path.join(dossier, fichier)
            images[nom_cle] = pygame.image.load(chemin_complet)
    return images

# Exemple d'utilisation
dossier_images = "image_pacman"  # Remplace par le chemin de ton dossier
images_pacman = charger_images(dossier_images)

#autres images
fantome_image = pygame.image.load('fantome_classique.png')
fantome_image_intelligent = pygame.image.load('fantome_intelligent.png')
obs_ver = pygame.image.load('barre_hor_100pix.png')
obs_hor = pygame.image.load('barre_vertical_100pix.png')
pieces_image = pygame.image.load('Pac_man.png')
vitamine_image = pygame.image.load('fantome.png')
boost_vitesse = pygame.image.load('bonus.png')
malchance = pygame.image.load('malus.png')

# création de la liste des différents bonus possible
liste_bonus = [vitamine_image, boost_vitesse, malchance]

class PartiePacman:
    #Variable :
    #Score
    score = 0
    dernier_score = 0
    meilleur_score = 0
    #temps
    temps = 1
    frame_seconde =120
    #Taille des bords screen
    largeur = 1200
    hauteur = 700
    #def variable boucle
    running = True
    valide_reso = True
    # partie en cours :
    partie_en_cours = False
    #Menu
    play = False
    parametre = False
    #boutons
    difficulte = 0
    son_var = 0
    # variable d'affiche labyrinthe
    type_labyrinthe = 6

    @classmethod
    def gestion_niveau(cls):
        #apparition bonus
        if cls.temps % (15*cls.frame_seconde) == 0:
            bonus_groupe.add(Bonus(random.choice(Bonus.position), random.choice(liste_bonus)))

        #Augmentation du temps
        cls.temps += 1

# Pac_man
class LePacMan(pygame.sprite.Sprite):
    # Image de Pac_man + rect
    def __init__(self):
        super().__init__()
        # définition des variables : image, rect, direction...
        self.image = pygame.transform.scale(images_pacman['Pacmandroiteouvert'], (60, 60))
        self.direction_x = 'droite'
        self.direction_y = ''
        self.rect = self.image.get_rect()
        # définition de x et y + position de départ :
        self.initial_x = 50
        self.initial_y = 50
        self.rect.centerx = self.initial_x
        self.rect.centery = self.initial_y
        self.vitesse = 2
        self.force = False
        self.temps_force = 0
        self.temps_vitesse = 0
        # Variable de vie
        self.vie = True
        self.temps_malus = 0
        self.anime = 'ouvert'
        self.temps_anime = 0
        self.liste_anime = ['ouvert', '', 'ferme', '']
        self.choix_anime = 0

    def verif_bonus (self): #verifiacation de la durée des bonus + désactivation suivant le type
        if self.force :
            if (PartiePacman.temps - Pac_man.temps_force)/PartiePacman.frame_seconde > 10:
                self.force = False
        if self.vitesse > 2 :
            if (PartiePacman.temps - self.temps_vitesse)/PartiePacman.frame_seconde > 10:
                self.vitesse = 2
        if self.vitesse < 2 :
            if PartiePacman.temps > self.temps_malus:
                self.vitesse = 2

    # Mouvement Pac_man
    def deplacement(self):
        keys = pygame.key.get_pressed()
        # Sauvegarde la position initiale avant le déplacement
        self.ancienne_position_x = self.rect.x
        self.ancienne_position_y = self.rect.y
        #temps animation
        self.ancien_temps_anime = self.temps_anime

        # Essaye de déplacer Pac_man
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.vitesse, 0)
            if self.temps_anime == self.ancien_temps_anime:
                self.temps_anime += 1
            self.direction_x = 'gauche'
            self.verif_col(True)
        elif keys[pygame.K_RIGHT] and self.rect.right < PartiePacman.largeur:
            self.rect.move_ip(self.vitesse, 0)
            if self.temps_anime == self.ancien_temps_anime:
                self.temps_anime += 1
            self.direction_x = 'droite'
            self.verif_col(True)
        else :
            self.direction_x = ''
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -self.vitesse)
            if self.temps_anime == self.ancien_temps_anime:
                self.temps_anime += 1
            self.direction_y = 'haut'
            self.verif_col(False)
        elif keys[pygame.K_DOWN] and self.rect.bottom < PartiePacman.hauteur:
            self.rect.move_ip(0, self.vitesse)
            if self.temps_anime == self.ancien_temps_anime:
                self.temps_anime += 1
            self.direction_y = 'bas'
            self.verif_col(False)
        else :
            self.direction_y = ''

        if self.temps_anime>60/self.vitesse:
            self.temps_anime = 0
            if self.choix_anime != 3 :
                self.choix_anime +=1
            else :
                self.choix_anime =0
            self.anime = self.liste_anime[self.choix_anime]

        #actualisation de la variable vitamine
        self.vitamine = 'vitamine' if self.force else ''

        # L'image dépend de la direction et s'actualise dans le mouvement
        if self.direction_y != '' or self.direction_x != '':
            self.image = pygame.transform.scale(images_pacman[f'Pacman{self.direction_x}{self.direction_y}{self.anime}{self.vitamine}'], (60, 60))

    def verif_col(self, hor):# vérification de la collision avec les obstacles sur les différents axes
        for obs in bordures:
            if self.rect.colliderect(obs.rect):
                if hor:
                    self.rect.x = self.ancienne_position_x
                    break
                else:
                    self.rect.y = self.ancienne_position_y
                    break

    #gestion des collisions avec les fantomes en fonction de la force
    def collision_fantome (self, groupe_actif, groupe_mort):
        # Gestion des collisions
        if pygame.sprite.spritecollide(self, groupe_actif, False):
            if not self.force :
                self.vie = False
            else :
                for un_fantome in pygame.sprite.spritecollide(Pac_man, groupe_actif, False):
                    groupe_actif.remove(un_fantome)
                    un_fantome.active = False
                    groupe_mort.append(un_fantome)
                    if PartiePacman.son_var ==1:
                        son_kill.play()

    #Fonction général appelée dans la boucle rassemblant la gestion entière du pacman
    def action (self, groupe_actif, groupe_mort):
        self.verif_bonus()
        self.deplacement()
        self.collision_fantome(groupe_actif, groupe_mort)
        screen.blit(self.image, self.rect)

# classe : Les fantomes
class Fantome(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super().__init__()
        # Définition des variables
        self.image = pygame.transform.scale(fantome_image, (42, 50))
        self.rect = self.image.get_rect()
        # définition de x et y + position de départ :
        self.initial_x = position_x
        self.initial_y = position_y
        self.rect.centerx = position_x
        self.rect.centery = position_y
        # Vitesse du fantome
        self.vitesse = 2
        self.speed_x = -self.vitesse
        self.speed_y = 0
        # Création de la variable d'activation
        self.active = False
        #intelligence du fantome
        self.intelligence = False
        #variables direction
        self.direction = 'droite'
        self.tableau_direction = ['gauche', 'droite', 'haut', 'bas']

    def image_actu(self): #changement de l'image en fonction de l'intelligence du fantome
        if self.intelligence :
            self.image = pygame.transform.scale(fantome_image_intelligent, (42, 50))
        else :
            self.image = pygame.transform.scale(fantome_image, (42, 50))

    #gestion des possibilités de mouvement pour chaque fantome
    def Radar(self, bordures):
        # Réinitialise dico pour chaque appel pour actualiser les booléens
        self.dict_oppose = {'gauche' : ['droite', (-self.vitesse, 0), self.rect.left > Pac_man.rect.right],
                           'droite' : ['gauche', (self.vitesse, 0), self.rect.right < Pac_man.rect.left],
                           'haut' : ['bas', (0, -self.vitesse), self.rect.top > Pac_man.rect.bottom],
                           'bas' : ['haut', (0, self.vitesse), self.rect.bottom < Pac_man.rect.top]}

        #les radars commencent avec la bordure de l'écran comme référence
        self.radar_ver_gauche = self.rect.left
        self.radar_ver_droit = PartiePacman.largeur - self.rect.right
        self.radar_hor_haut = self.rect.top
        self.radar_hor_bas = PartiePacman.hauteur - self.rect.bottom

        #boucle de détéction des obstacles, sur l'axe horizontal si l'obstacle et vertical et inversement
        for obs in bordures:
            if not obs.direction :
                # Vérifie si le fantôme et l'obstacle sont alignés verticalement
                if (self.rect.top < obs.rect.bottom) and (self.rect.bottom > obs.rect.top):
                    # Calcul de la distance pour le côté gauche
                    if self.rect.left > obs.rect.right:  
                        distance_gauche = abs(self.rect.left - obs.rect.right)
                        # Met à jour le radar si une plus petite distance est trouvée
                        if distance_gauche < self.radar_ver_gauche:
                            self.radar_ver_gauche = distance_gauche
                
                    # Calcul de la distance pour le côté droit
                    if self.rect.right < obs.rect.left:  
                        distance_droite = abs(self.rect.right - obs.rect.left)
                        # Met à jour le radar si une plus petite distance est trouvée
                        if distance_droite < self.radar_ver_droit:
                            self.radar_ver_droit = distance_droite

            else :
                # Vérifie si le fantôme et l'obstacle sont alignés horizontalement
                if (self.rect.left < obs.rect.right) and (self.rect.right > obs.rect.left):
                    # Calcul de la distance pour le haut
                    if self.rect.top > obs.rect.bottom:  
                        distance_haut = abs(self.rect.top - obs.rect.bottom)
                        # Met à jour le radar si une plus petite distance est trouvée
                        if distance_haut < self.radar_hor_haut:
                            self.radar_hor_haut = distance_haut
                
                    # Calcul de la distance pour le bas
                    if self.rect.bottom < obs.rect.top:  
                        distance_bas = abs(self.rect.bottom - obs.rect.top)
                        # Met à jour le radar si une plus petite distance est trouvée
                        if distance_bas < self.radar_hor_bas:
                            self.radar_hor_bas = distance_bas

        #gestion finale des possibilités
        self.possibilite = [self.radar_ver_gauche, self.radar_ver_droit, self.radar_hor_haut, self.radar_hor_bas]
        #si la valeur de la distance > 100 : on garde la possibilité et on la nomme sinon on n'y va pas
        for i in range (len(self.possibilite)):
            self.possibilite[i] = self.tableau_direction[i] if self.possibilite[i] > 100 else False
        while False in self.possibilite :
            self.possibilite.remove(False)
        #on enlève le retour en arrière si on peut
        if self.dict_oppose[self.direction][0] in self.possibilite and len(self.possibilite) > 1 :
           self.possibilite.remove(self.dict_oppose[self.direction][0])
        # si le fantome est intelligent, il va chercher à se rapprocher le plus possible du pacman
        if self.intelligence :
            if self.direction in self.possibilite and self.dict_oppose[self.direction][2]:
                self.possibilte = [self.direction]
            for trajectoire in self.possibilite:
                if self.dict_oppose[trajectoire][2] :
                    self.possibilite = [trajectoire]
        #augmente les chances de continuer sa route s'il peut
        if self.direction in self.possibilite:
           self.possibilite.append(self.direction)
        #choix final de la direction aléatoire parmi les possibilités restantes
        self.direction = random.choice(self.possibilite)

    # déplacer le fantome
    def deplacement(self):
        # on actualise nos radars à toutes les intersections
        if self.rect.centerx % 100 == 50 and self.rect.centery % 100 == 50:
            self.Radar(bordures)

        # Déplacement du fantome en fonction de la direction choisie
        self.rect.x += self.dict_oppose[self.direction][1][0]
        self.rect.y += self.dict_oppose[self.direction][1][1]

    # déplacer plus bliter le fantome soit la gestion complète du fantome pour une partie
    def action (self):
        self.deplacement()
        screen.blit(self.image, self.rect)

    #gestion globale de l'activation
    timer = 0
    @classmethod
    def activation (cls, groupe, groupe_actif):
        #Activation des fantomes :
        if PartiePacman.temps > cls.timer and len(Fantome_groupe)>0:
            Fantome_groupe[0].active = True
            cls.timer += 5 * PartiePacman.frame_seconde
            #changement de liste pour les fantomes actifs
            for fantome in Fantome_groupe:
                if fantome.active:  # Si le fantôme est actif
                    groupe.remove(fantome)  # Retirer le fantôme de la liste originale
                    groupe_actif.append(fantome)  # Ajouter le fantôme à la liste des actifs

#Création du pacman
Pac_man = LePacMan()

class Text:
    # Définir les couleurs :
    noir = (0, 0, 0)
    vert = (0, 255, 0)
    bleu = (0, 0, 255)
    rouge = (255, 0, 0)
    rose = (255, 192, 203)
    violet = (160, 32, 240)
    blanc = (255, 255, 255)
    orange = (255, 128, 0)
        
    def __init__(self, taille, couleur, position, variable=None, prefix=""):
        #paramètres du text
        self.couleur = couleur
        self.font = pygame.font.Font(None, taille)
        self.position = position
        self.variable = variable
        self.prefix = prefix
        self.update()

    #actualisation de ce texte
    def update(self, variable=None, position = None, taille = None):
        if variable is not None:
            self.variable = variable
        if position is not None :
            self.position = position
        if taille is not None:
            self.font = pygame.font.Font(None, taille)
        text_content = f"{self.prefix}{self.variable}" if self.variable is not None else self.prefix
        self.surface = self.font.render(text_content, True, self.couleur)
        if self.position[0] == '':
            self.rect = self.surface.get_rect(center=(self.position[1], self.position[2]))
        if self.position[0] == 'd':
            self.rect = self.surface.get_rect(topright=(self.position[1], self.position[2]))
        if self.position[0] == 'g':
            self.rect = self.surface.get_rect(topleft=(self.position[1], self.position[2]))

#stockage des textes sous forme de dictionnaire pour faire évoluer le texte plus facilement en l'associant à sa variable, etc
dico_text_reso = {"hauteur" : [Text(PartiePacman.largeur // 16, Text.noir, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 1.5), variable=PartiePacman.hauteur),
                               lambda : PartiePacman.hauteur, lambda : ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 1.5), lambda : PartiePacman.largeur // 16],
                "largeur" : [Text(PartiePacman.largeur // 16, Text.noir, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 8), variable=PartiePacman.largeur),
                             lambda : PartiePacman.largeur, lambda : ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 8), lambda : PartiePacman.largeur // 16],
                "info_reso1" : [Text(PartiePacman.largeur // 26, Text.rouge, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 3), variable=None, prefix='Si la résolution est différente de la définition par défaut soit 1200/700,'),
                                lambda : None, lambda : ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 3), lambda : PartiePacman.largeur // 26],
                "info_reso2" : [Text(PartiePacman.largeur // 26, Text.rouge, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 3 + PartiePacman.hauteur // 16), variable=None, prefix='seule la carte aléatoire sera disponible (éviter en dessous de 600/600)'),
                                lambda : None, lambda : ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 3 + PartiePacman.hauteur // 16), lambda : PartiePacman.largeur // 26]}


# Définir les dimensions de la fenêtre + titre
screen = pygame.display.set_mode((PartiePacman.largeur, PartiePacman.hauteur), pygame.RESIZABLE)
pygame.display.set_caption('Pac Man')

#Classe bouton
class Bouton(pygame.sprite.Sprite):
    def __init__(self, x, y, image_bouton, action, opacite):
        super().__init__()
        self.image = pygame.image.load(image_bouton).convert_alpha()  # Charge l'image du bouton
        self.image.set_alpha(opacite)#Pour pouvoir faire des boutons semi-transparents
        self.rect = self.image.get_rect()  # Récupère le rectangle de l'image pour faciliter les collisions
        self.rect.center = (x, y)  # Positionne le bouton à (x, y)
        self.action = action  # Fonction à appeler lors du clic

    def update(self):
        #Met à jour le bouton, vérifie si le clic est sur le bouton et fait l'action du bouton et return True quand il est cliqué
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.action != None:
                    self.action()
                if PartiePacman.son_var == 1:
                    son_clique.play()
                return True

#la fonction générale de modification de l'écran
def resolution_screen(x, y):
    PartiePacman.largeur += x * 100
    PartiePacman.hauteur += y * 100
    Bouton_reso_0_largeur.rect.topleft = (PartiePacman.largeur // 4, PartiePacman.hauteur // 8)
    Bouton_reso_1_largeur.rect.topleft = (int(PartiePacman.largeur / 4 * 3), PartiePacman.hauteur // 8)
    Bouton_reso_0_hauteur.rect.topleft = (PartiePacman.largeur // 4, int(PartiePacman.hauteur / 1.5))
    Bouton_reso_1_hauteur.rect.topleft = (int(PartiePacman.largeur / 4 * 3), int(PartiePacman.hauteur / 1.5))
    Bouton_reso_valide.rect.topleft = (PartiePacman.largeur // 2 - 100, PartiePacman.hauteur - 86)
    screen = pygame.display.set_mode((PartiePacman.largeur, PartiePacman.hauteur), pygame.RESIZABLE)
    pygame.display.update()
    time.sleep(0.1)

#Les plus petites qui appellent la grande avec en paramètres la modification à faire
def reso_moins_largeur ():
    resolution_screen(-1, 0)

def reso_plus_largeur ():
    resolution_screen(1, 0)

def reso_moins_hauteur ():
    resolution_screen(0, -1)

def reso_plus_hauteur ():
    resolution_screen(0, 1)

def reso_valide ():
    PartiePacman.valide_reso = False
    time.sleep(0.4)

# Les boutons du menu resolution :
Bouton_reso_0_largeur = Bouton(PartiePacman.largeur // 4, PartiePacman.hauteur // 8, 'bouton_pause.png', reso_moins_largeur, 255)
Bouton_reso_1_largeur = Bouton(int(PartiePacman.largeur / 4 * 3), PartiePacman.hauteur // 8, 'bouton_pause.png', reso_plus_largeur, 255)
Bouton_reso_0_hauteur = Bouton(PartiePacman.largeur // 4, PartiePacman.hauteur // 1.5, 'bouton_pause.png', reso_moins_hauteur, 255)
Bouton_reso_1_hauteur = Bouton(int(PartiePacman.largeur / 4 * 3), PartiePacman.hauteur // 1.5, 'bouton_pause.png', reso_plus_hauteur, 255)
Bouton_reso_valide = Bouton(PartiePacman.largeur // 2, PartiePacman.hauteur - 86, 'bouton_jouer.png', reso_valide, 255)
menu_reso = pygame.sprite.Group(Bouton_reso_0_largeur, Bouton_reso_1_largeur, Bouton_reso_0_hauteur, Bouton_reso_1_hauteur, Bouton_reso_valide)

# le menu resolution, la boucle qui gère la résolution de l'écran tant que l'utilisateur ne valide pas
while PartiePacman.valide_reso and PartiePacman.running :
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PartiePacman.running = False
            # modification par l'utilisateur sans utiliser les boutons
            elif event.type == pygame.VIDEORESIZE:
                # pri en compte des nouvelles valeurs + arrondi à la centaine inférieure
                PartiePacman.largeur, PartiePacman.hauteur  = event.w // 100 * 100, event.h // 100 * 100
                #pour actualiser la position des boutons
                resolution_screen(0, 0)
                # changement du screen
                #screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    #actualisation des boutons + fond blanc
    screen.fill(Text.blanc)
    menu_reso.update()
    menu_reso.draw(screen)
        
    # actualisation du texte
    for i in dico_text_reso :
        dico_text_reso[i][0].update(dico_text_reso[i][1](), dico_text_reso[i][2](), dico_text_reso[i][3]())
        screen.blit(dico_text_reso[i][0].surface, dico_text_reso[i][0].rect)

    #actualisation du screen :
    pygame.display.flip()

#Chargement des sons
son_clique = pygame.mixer.Sound("son_clique.wav")
son_piece = pygame.mixer.Sound("coin.mp3")
son_game_over = pygame.mixer.Sound("game_over.mp3")
son_victoire = pygame.mixer.Sound("victoire.mp3")
son_kill = pygame.mixer.Sound("kill.wav")

# gérer le volume :
son_piece.set_volume(0.5)

# Créer les classes Sprite :
# Classe bonus :
class Bonus(pygame.sprite.Sprite):
    def __init__(self, positionxy, type_bonus):
        super().__init__()
        # définition des variables
        self.image = type_bonus
        self.rect = self.image.get_rect()
        # définition de x et y + position de départ :
        self.rect.centerx = positionxy[0]
        self.rect.centery = positionxy[1]
        self.categorie = type_bonus
    #position possible pour les bonus
    position = []
    for x in range(50, PartiePacman.largeur - 49, 100):  # Boucle pour l'axe x
        for y in range(50, PartiePacman.hauteur - 49, 100):  # Boucle pour l'axe y
            position.append((x, y))

    # vérifie la collision avec le pacman et produit les effets en fonction du bonus/malus
    def verif_collision (self, groupe_vie):
        if self.rect.colliderect(Pac_man.rect):
            groupe_vie.remove(self)
            if self.categorie == pieces_image:
                PartiePacman.score += 50
                if PartiePacman.son_var == 1:
                    son_piece.play()
            elif self.categorie == boost_vitesse:
                Pac_man.vitesse=4
                Pac_man.temps_vitesse = PartiePacman.temps
            elif self.categorie == malchance:
                Pac_man.vitesse=1
                Pac_man.temps_malus = PartiePacman.temps + PartiePacman.frame_seconde * 5
            else:
                Pac_man.force = True
                Pac_man.temps_force = PartiePacman.temps
       
        
# Classe : Obstacle
class Obstacle:
    def __init__(self, position, hor):
        # définition des variables
        if hor :
            self.image = pygame.transform.scale(obs_hor, (100, 15))
        else :
            self.image = pygame.transform.scale(obs_ver, (15, 100))
        self.direction = hor
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.casse = False

    #fonction qui déssine l'obstacle
    def draw(self, screen):
        screen.blit(self.image, self.rect)

#une fonction complete qui va dessiner un labyrinthe pour la partie.
def creation_random_labyrinthe ():
    #Tous les 100 pix, on a un choix, case, troué à 2 ou 3 endroits si on a à proximité une case déjà étudié alors, on n'y fait pas de trous
    # création des cases :
    class LesCases:
        def __init__(self, x, y):
            self.visit = False
            self.x = x
            self.y = y
    case_ = LesCases
    cases = {}
    for x in range (0, PartiePacman.largeur - 99, 100):
        for y in range (0, PartiePacman.hauteur - 99, 100):
            cases[x, y] = case_(x, y)

    # création des bordures
    murs ={}
    sols ={}
    for x in range (0, PartiePacman.largeur - 99, 100):
        for y in range (0, PartiePacman.hauteur - 99, 100):
            murs[x, y] = Obstacle((x, y), False)
            sols[x, y] = Obstacle((x, y), True)

    #possibilités du cassage des obstacles
    for xy, case_ in cases.items():
        case_.visit = True
        possibilite = [1, 2, 3, 4]
        if xy[0] == 0:
            possibilite[0] = 0
        else :
            case_gauche = cases.get((xy[0]-100, xy[1]))
            if case_gauche.visit:
                possibilite[0] = 0
        if xy[0] == PartiePacman.largeur-100:
            possibilite[1] = 0
        else :
            case_droite = cases.get((xy[0]+100, xy[1]))
            if case_droite.visit:
                possibilite[1] = 0
        if xy[1] == 0:
            possibilite[2] = 0
        else :
            case_haut = cases.get((xy[0], xy[1]-100))
            if case_haut.visit:
                possibilite[2] = 0
        if xy[1] == PartiePacman.hauteur-100:
            possibilite[3] = 0
        else :
            case_bas = cases.get((xy[0], xy[1]+100))
            if case_bas.visit:
                possibilite[3] = 0
        non_zero_values = [x for x in possibilite if x != 0] # cequelonveutajouter for valeurdeliste in liste if condition (le if est facultatif)
        #on sélectionne l'obstacle à casser puis on le déclare cassé
        if len(non_zero_values) >0:
            cassage = random.choice(non_zero_values)
        else :
            cassage = 0
        if cassage == 1:
            obs_cas = murs.get((xy[0], xy[1]))
        elif cassage == 2:
            obs_cas = murs.get((xy[0]+100, xy[1]))
        elif cassage == 3:
            obs_cas = sols.get((xy[0], xy[1]))
        elif cassage == 4:
            obs_cas = sols.get((xy[0], xy[1]+100))
        if cassage != 0:
            obs_cas.casse = True

    #on supprime les obstacles au bord de l'écran
    elements_mur_supr = [key for key in murs if key[0] == 0]
    elements_sol_supr = [key for key in sols if key[1] == 0]
    for key in elements_mur_supr:
        del murs[key]
    for key in elements_sol_supr:
        del sols[key]

    #on supprime les obstacles cassés
    murs_verif = []
    sols_verif = []
    for xy, mur0 in murs.items():
        if not mur0.casse:
            murs_verif.append((xy[0], xy[1]))
    for xy, sol0 in sols.items():
        if not sol0.casse:
            sols_verif.append((xy[0], xy[1]))

    # Trier les obstacles par leurs coordonnées pour faciliter l'analyse
    murs_verif = sorted(murs_verif)
    sols_verif = sorted(sols_verif)
        
    # Vérifier les murs consécutifs sur une ligne (x constant, y change)
    for x, y in murs_verif:
        if ((x, y + 100) in murs_verif) and ((x, y + 200) in murs_verif):
            consecutif = random.randint(1, 3)
            if consecutif == 1:
                murs_verif.remove((x, y))
            elif consecutif == 2:
                murs_verif.remove((x, y + 100))
            else :
                murs_verif.remove((x, y + 200))
        
    # Vérifier les murs consécutifs sur une colonne (y constant, x change)
    for x, y in sols_verif:
        if ((x + 100, y) in sols_verif) and ((x + 200, y) in sols_verif):
            consecutif = random.randint(1, 3)
            if consecutif == 1:
                sols_verif.remove((x, y))
            elif consecutif == 2:
                sols_verif.remove((x + 100, y))
            else :
                sols_verif.remove((x + 200, y))

    #regroupe les listes en une seule avec des paramètres et la retourne pour utilisation dans le code global
    liste_final_murs = [(x, y) for x, y in murs_verif]
    liste_final_sols = [(x, y) for x, y in sols_verif]
    bordures_random = [Obstacle(xy, False) for xy in liste_final_murs] + [Obstacle(xy, True) for xy in liste_final_sols]
    return bordures_random
            
# Créer une instance des sprites
Fantome_groupe = [Fantome(PartiePacman.largeur - 50, 50), Fantome(50, PartiePacman.hauteur - 50), Fantome(PartiePacman.largeur - 50, PartiePacman.hauteur - 50)]
Fantome_groupe_actif = []
Fantome_groupe_absent = [Fantome(50, 50)]

dico_bordures = {1 :
    #Horizontaux
    [Obstacle((0, 200), True), Obstacle((0, 300), True), Obstacle((0, 400), True),Obstacle((100, 100), True), Obstacle((100, 200), True), Obstacle((100, 300), True),
    Obstacle((100, 600), True),Obstacle((100, 700), True),Obstacle((200, 400), True),Obstacle((300, 100), True),Obstacle((300, 400), True),Obstacle((415, 300), True),
    Obstacle((400, 400), True),Obstacle((400, 600), True),Obstacle((500, 100), True),Obstacle((500, 500), True),Obstacle((600, 100), True),Obstacle((600, 500), True),
    Obstacle((700, 300), True),Obstacle((700, 400), True),Obstacle((715, 600), True),Obstacle((800, 100), True),Obstacle((800, 400), True),Obstacle((900, 400), True),
    Obstacle((1000, 100), True),Obstacle((1000, 200), True),Obstacle((1000, 300), True), Obstacle((1000, 600), True),Obstacle((1000, 700), True),Obstacle((1100, 200), True),
    Obstacle((1100, 300), True),Obstacle((1100, 400), True),
    #Verticaux :
    Obstacle((300, 0), False),Obstacle((900, 0), False),Obstacle((185, 100), False),Obstacle((300, 100), False),Obstacle((400, 100), False),Obstacle((800, 100), False),
    Obstacle((900, 100), False),Obstacle((1000, 100), False),Obstacle((300, 200), False),Obstacle((500, 200), False),Obstacle((600, 200), False),Obstacle((700, 200), False),
    Obstacle((900, 200), False),Obstacle((600, 300), False),Obstacle((100, 400), False),Obstacle((200, 400), False),Obstacle((300, 400), False),Obstacle((400, 400), False),
    Obstacle((800, 400), False),Obstacle((900, 400), False),Obstacle((1000, 400), False),Obstacle((1100, 400), False),Obstacle((400, 500), False),Obstacle((600, 500), False),
    Obstacle((800, 500), False),Obstacle((300, 600), False),Obstacle((600, 600), False),Obstacle((900, 600), False)],

                 2 :
    #Horizontaux
    [Obstacle((0, 200), True),Obstacle((100, 100), True),Obstacle((100, 200), True),Obstacle((100, 300), True), Obstacle((100, 400), True),Obstacle((100, 500), True),Obstacle((200, 100), True),
    Obstacle((200, 200), True), Obstacle((200, 400), True),Obstacle((300, 100), True),Obstacle((300, 400), True),Obstacle((400, 200), True),Obstacle((400, 300), True),Obstacle((400, 600), True),
    Obstacle((500, 200), True),Obstacle((500, 600), True),Obstacle((600, 200), True),Obstacle((600, 600), True),Obstacle((700, 200), True),Obstacle((700, 300), True),Obstacle((700, 600), True),
    Obstacle((800, 100), True),Obstacle((800, 400), True),Obstacle((900, 100), True),Obstacle((900, 200), True),Obstacle((900, 400), True),Obstacle((1000, 100), True),Obstacle((1000, 200), True),
    Obstacle((1000, 300), True),Obstacle((1000, 400), True),Obstacle((1000, 500), True),Obstacle((1100, 200), True),
    #Verticaux
    Obstacle((100, 500), False),Obstacle((100, 600), False),Obstacle((200, 500), False),Obstacle((300, 300), False),Obstacle((300, 400), False),Obstacle((300, 500), False),Obstacle((400, 400), False),
    Obstacle((500, 0), False),Obstacle((500, 300), False),Obstacle((500, 400), False),Obstacle((600, 0), False),Obstacle((600, 100), False),Obstacle((600, 200), False),Obstacle((600, 300), False),
    Obstacle((600, 500), False),Obstacle((700, 0), False),Obstacle((700, 300), False),Obstacle((700, 400), False),Obstacle((800, 400), False),Obstacle((900, 300), False),Obstacle((900, 400), False),
    Obstacle((900, 500), False),Obstacle((1000, 500), False),Obstacle((1100, 500), False),Obstacle((1100, 600), False)],

                 3 :
	#horizontaux
	[Obstacle((0, 300), True),Obstacle((100, 200), True),Obstacle((100, 300), True),Obstacle((115, 400), True),Obstacle((215, 100), True),Obstacle((200, 200), True),Obstacle((200, 300), True),
	Obstacle((200, 600), True),Obstacle((300, 200), True),Obstacle((300, 600), True),Obstacle((400, 200), True),Obstacle((400, 300), True),Obstacle((400, 500), True),Obstacle((500, 100), True),
	Obstacle((515, 400), True),Obstacle((500, 600), True),Obstacle((600, 100), True),Obstacle((600, 300), True),Obstacle((600, 600), True),Obstacle((700, 200), True),Obstacle((700, 400), True),
	Obstacle((700, 500), True),Obstacle((800, 100), True),Obstacle((800, 500), True),Obstacle((900, 100), True),Obstacle((900, 400), True),Obstacle((900, 500), True),Obstacle((900, 600), True),
	Obstacle((1015, 300), True),Obstacle((1000, 400), True),Obstacle((1000, 500), True),Obstacle((1100, 400), True),
	#verticaux
	Obstacle((100, 100), False),Obstacle((100, 400), False),Obstacle((100, 600), False),Obstacle((200, 300), False),Obstacle((200, 500), False),Obstacle((300, 0), False),Obstacle((300, 400), False),
    Obstacle((400, 100), False),Obstacle((400, 200), False),Obstacle((400, 400), False),Obstacle((500, 600), False), Obstacle((600, 100), False),Obstacle((600, 300), False), Obstacle((600, 500), False),
	Obstacle((685, 0), False),Obstacle((800, 200), False),Obstacle((800, 400), False),Obstacle((800, 500), False),Obstacle((900, 600), False),Obstacle((900, 200), False),Obstacle((1000, 100), False),
	Obstacle((1000, 300), False),Obstacle((1100, 000), False),Obstacle((1100, 200), False),Obstacle((1100, 500), False)],

                 4 :
    #horizontaux
	[Obstacle((0, 400), True),Obstacle((100, 100), True),Obstacle((100, 600), True),Obstacle((200, 200), True),Obstacle((200, 500), True),Obstacle((300, 100), True),Obstacle((315, 600), True),
	Obstacle((500, 200), True),Obstacle((500, 500), True),Obstacle((600, 200), True),Obstacle((600, 500), True),Obstacle((700, 100), True),Obstacle((715, 600), True),Obstacle((800, 100), True),
    Obstacle((815, 600), True),Obstacle((900, 300), True),Obstacle((1000, 100), True),Obstacle((1000, 300), True),Obstacle((1000, 600), True),Obstacle((1100, 400), True),
    #verticaux
	Obstacle((100, 100), False),Obstacle((100, 200), False),Obstacle((100, 500), False),Obstacle((200, 200), False),Obstacle((200, 400), False),Obstacle((300, 300), False),Obstacle((400, 100), False),
    Obstacle((400, 200), False),Obstacle((400, 400), False),Obstacle((400, 500), False),Obstacle((500, 0), False),Obstacle((500, 200), False),Obstacle((500, 400), False),Obstacle((500, 600), False),
    Obstacle((600, 0), False),Obstacle((600, 300), False),Obstacle((600, 600), False),Obstacle((700, 200), False),Obstacle((685, 400), False),Obstacle((800, 200), False),Obstacle((800, 300), False),
    Obstacle((800, 400), False),Obstacle((900, 100), False),Obstacle((900, 200), False),Obstacle((900, 400), False),Obstacle((900, 500), False),Obstacle((1000, 200), False),Obstacle((1000, 400), False),
	Obstacle((1100, 100), False),Obstacle((1085, 500), False)],

                 5 :
    # horizontaux
    [Obstacle((0, 200), True),Obstacle((115, 100), True),Obstacle((100, 300), True),Obstacle((100, 600), True),Obstacle((200, 400), True),Obstacle((315, 100), True),Obstacle((315, 200), True),
    Obstacle((300, 300), True),Obstacle((300, 600), True),Obstacle((400, 600), True),Obstacle((500, 100), True),Obstacle((500, 500), True),Obstacle((500, 600), True),Obstacle((600, 100), True),
    Obstacle((600, 500), True),Obstacle((600, 600), True),Obstacle((1100, 200), True),Obstacle((1000, 100), True),Obstacle((1000, 300), True),Obstacle((1015, 600), True),Obstacle((900, 400), True),
    Obstacle((800, 100), True),Obstacle((800, 200), True),Obstacle((800, 300), True),Obstacle((800, 600), True),Obstacle((700, 600), True),Obstacle((600, 100), True),Obstacle((600, 500), True),
    Obstacle((600, 600), True),Obstacle((500, 100), True),Obstacle((500, 500), True),Obstacle((500, 600), True),

    # verticaux
    Obstacle((100, 300), False),Obstacle((100, 500), False),Obstacle((200, 0), False),Obstacle((185, 200), False),Obstacle((200, 400), False),Obstacle((300, 500), False),Obstacle((400, 100), False),
    Obstacle((400, 300), False),Obstacle((400, 400), False),Obstacle((500, 100), False),Obstacle((500, 200), False),Obstacle((500, 415), False),Obstacle((600, 200), False),Obstacle((600, 300), False),
    Obstacle((1100, 300), False),Obstacle((1100, 500), False),Obstacle((1000, 0), False),Obstacle((1000, 200), False),Obstacle((1000, 400), False),Obstacle((885, 500), False),Obstacle((800, 100), False),
    Obstacle((800, 300), False),Obstacle((800, 400), False),Obstacle((700, 100), False),Obstacle((700, 200), False),Obstacle((700, 415), False),Obstacle((600, 200), False),Obstacle((600, 300), False)]}


bonus_groupe = pygame.sprite.Group()
bonus_morts_groupe = pygame.sprite.Group()

# Définition des autres textes :
dico_text_autre = {"Victoire" : Text(PartiePacman.largeur // 4, Text.vert, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 2 - PartiePacman.hauteur // 4), variable=None, prefix='Victoire !'),
             "Défaite" : Text(PartiePacman.largeur // 4, Text.rouge, ('', PartiePacman.largeur // 2, PartiePacman.hauteur // 2 - PartiePacman.hauteur // 4), variable=None, prefix='Défaite !')}

dico_text_menu = {"meilleur_score" : [Text(PartiePacman.largeur // 20, Text.noir, ('', PartiePacman.largeur // 4.5, PartiePacman.hauteur // 9), variable= PartiePacman.meilleur_score, prefix='Meilleur score : ')
                                 , lambda : PartiePacman.meilleur_score],
                 "dernier_score" : [Text(PartiePacman.largeur // 20, Text.noir, ('', PartiePacman.largeur // 1.6, PartiePacman.hauteur // 9), variable= PartiePacman.dernier_score, prefix='Dernier score : ')
                                , lambda : PartiePacman.dernier_score]}

dico_text_jeux = {"score" : [Text(PartiePacman.largeur // 16, Text.violet, ('g', 0, 0), variable= PartiePacman.score, prefix='Score : '),
                             lambda : PartiePacman.score, lambda : True],
                  "malus" : [Text(PartiePacman.largeur // 32, Text.violet, ('d', PartiePacman.largeur, PartiePacman.hauteur // 7 * 2), variable=(Pac_man.temps_malus - PartiePacman.temps) // PartiePacman.frame_seconde, prefix='Durée malus : '),
                              lambda : (Pac_man.temps_malus - PartiePacman.temps) // PartiePacman.frame_seconde, lambda : Pac_man.temps_malus > PartiePacman.temps],
                "fantome" : [Text(PartiePacman.largeur // 32, Text.rouge, ('d', PartiePacman.largeur, PartiePacman.hauteur // 7 + PartiePacman.hauteur // 14), variable= int((Fantome.timer - PartiePacman.temps) / PartiePacman.frame_seconde + 1), prefix='Prochain fantome : '),
                             lambda : int((Fantome.timer - PartiePacman.temps) / PartiePacman.frame_seconde + 1), lambda : len(Fantome_groupe) > 0],
                "force" : [Text(PartiePacman.largeur // 32, Text.orange, ('d', PartiePacman.largeur, PartiePacman.hauteur // 14), variable= int((Pac_man.temps_force + 10 * PartiePacman.frame_seconde - PartiePacman.temps) / PartiePacman.frame_seconde + 1), prefix='Effet vitamine : '),
                           lambda : int((Pac_man.temps_force + 10 * PartiePacman.frame_seconde - PartiePacman.temps) / PartiePacman.frame_seconde + 1), lambda :Pac_man.force],
                "vitesse" : [Text(PartiePacman.largeur // 32, Text.orange, ('d', PartiePacman.largeur, PartiePacman.hauteur // 7), variable= int((Pac_man.temps_vitesse + 10 * PartiePacman.frame_seconde - PartiePacman.temps) / PartiePacman.frame_seconde + 1), prefix='Effet vitesse : '),
                             lambda : int((Pac_man.temps_vitesse + 10 * PartiePacman.frame_seconde - PartiePacman.temps) / PartiePacman.frame_seconde + 1), lambda : Pac_man.vitesse > 2],
                "bonus" : [Text(PartiePacman.largeur // 32, Text.bleu, ('d', PartiePacman.largeur, 0), variable= int((15 * PartiePacman.frame_seconde - (PartiePacman.temps % (15 * PartiePacman.temps))) / PartiePacman.temps), prefix='Prochain bonus : '),
                           lambda : int((15 * PartiePacman.frame_seconde - (PartiePacman.temps % (15 * PartiePacman.frame_seconde))) / PartiePacman.frame_seconde), lambda : True]}

# Le Menu :
# Les fonctions des boutons :
def play_on (): #Fonction qui lance le jeu (play est une condition au lancement du jeu, par défaut, elle vaut 0)
    if not PartiePacman.play:
        PartiePacman.play = True
        restart()
        if PartiePacman.difficulte == 0:
            facile()
        elif PartiePacman.difficulte == 1:
            moyen()
        else:
            difficile()
    time.sleep(0.1)

#fonction qui gère la mise en pause du jeu
def reprendre_f ():
    PartiePacman.play = False if PartiePacman.play else True
    time.sleep(0.1)

#ouverture du menu des paramètres
def open_parametre ():
    PartiePacman.parametre = True if not PartiePacman.parametre else False
    if PartiePacman.parametre :
        Bouton_parametre.image.set_alpha(125)
    else :
        Bouton_parametre.image.set_alpha(255)

#fonctions gérant la difficulté
def facile ():
    PartiePacman.difficulte = 0
    restart()
    if len(Fantome_groupe) > 3:
        Fantome_groupe_absent.append(Fantome_groupe[3])
        Fantome_groupe.remove(Fantome_groupe[3])
    Bouton_facile.image.set_alpha(125)
    Bouton_moyen.image.set_alpha(255)
    Bouton_difficile.image.set_alpha(255)
    time.sleep(0.1)
def moyen ():
    PartiePacman.difficulte = 1
    restart()
    Fantome_groupe[3].intelligence = True
    Fantome_groupe[3].image_actu()
    Bouton_facile.image.set_alpha(255)
    Bouton_moyen.image.set_alpha(125)
    Bouton_difficile.image.set_alpha(255)
    time.sleep(0.1)
def difficile ():
    PartiePacman.difficulte = 2
    restart()
    for un_fantome in Fantome_groupe:
        un_fantome.intelligence = True
        un_fantome.image_actu()
    Bouton_facile.image.set_alpha(255)
    Bouton_moyen.image.set_alpha(255)
    Bouton_difficile.image.set_alpha(125)
    time.sleep(0.1)

# sélection d'un labyrinthe
def lab (number):
    restart()
    PartiePacman.type_labyrinthe = number
    time.sleep(0.1)

#activation/désactivation du son
def son ():
    PartiePacman.son_var = 1 if PartiePacman.son_var == 0 else 0
    time.sleep(0.1)

#redémarre la partie avec les paramètres par défaut de tout
def restart ():
    creation_random_labyrinthe()
    Pac_man.image = pygame.transform.scale(images_pacman['Pacmandroiteouvert'], (60, 60))
    Pac_man.force = False
    Pac_man.temps_malus = 0
    PartiePacman.partie_en_cours = False
    Pac_man.rect.centerx = Pac_man.initial_x
    Pac_man.rect.centery = Pac_man.initial_y
    Pac_man.vie = True
    Pac_man.vitesse = 2
    PartiePacman.score = 0
    PartiePacman.temps = 0
    Fantome.timer = 0
    for un_fantome in Fantome_groupe_actif:
        un_fantome.active = False
        Fantome_groupe.append(un_fantome)
    for un_fantome in Fantome_groupe_absent:
        un_fantome.active = False
        Fantome_groupe.append(un_fantome)
        Fantome_groupe_absent.remove(un_fantome)
    Fantome_groupe_actif.clear()
    for un_fantome in Fantome_groupe:
        un_fantome.intelligence = False
        un_fantome.image_actu()
        un_fantome.rect.centerx = un_fantome.initial_x
        un_fantome.rect.centery = un_fantome.initial_y
    if Fantome_groupe[0].rect.centerx == 50 and Fantome_groupe[0].rect.centery == 50:
        fantome_deplace = Fantome_groupe.pop(0)
        Fantome_groupe.append(fantome_deplace)
    bonus_groupe.empty()

# création des boutons
Bouton_play = Bouton(int(PartiePacman.largeur / 2), PartiePacman.hauteur - 86, 'bouton_jouer.png', play_on, 255)
Bouton_parametre = Bouton(PartiePacman.largeur - 100, 50, 'bouton_parametres.png', open_parametre, 255)
Bouton_facile = Bouton(int((PartiePacman.largeur // 2) - 300), int(PartiePacman.hauteur / 2 + PartiePacman.hauteur / 6), 'bouton_facile.png', facile, 125)
Bouton_difficile = Bouton(int((PartiePacman.largeur // 2) + 300), int(PartiePacman.hauteur / 2 + PartiePacman.hauteur / 6), 'bouton_difficile.png', difficile, 255)
Bouton_moyen = Bouton(PartiePacman.largeur // 2, int(PartiePacman.hauteur / 2 + PartiePacman.hauteur / 6), 'bouton_moyen.png', moyen, 255)
Bouton_play_bis = Bouton(PartiePacman.largeur // 2, 25, 'bouton_pause.png', reprendre_f, 255)
Bouton_son_0 = Bouton(100, 50, 'bouton_son_0.png', son, 255)
Bouton_son_1 = Bouton(100, 50, 'bouton_son_1.png', son, 255)

#assignations à un groupe
Bouton_groupe_menu = pygame.sprite.Group(Bouton_play, Bouton_parametre)
Bouton_groupe_parametre = pygame.sprite.Group(Bouton_play, Bouton_parametre, Bouton_facile, Bouton_moyen, Bouton_difficile)
Bouton_groupe_son = [Bouton_son_0, Bouton_son_1]
Bouton_groupe_level = pygame.sprite.Group(Bouton_play_bis)

#dictionnaire des boutons labyrinthe
dico_bouton_lab = {1 : Bouton(225, 250, 'niveau1.png', None, 255),
                   2 : Bouton(600, 250, 'niveau2.png', None, 255),
                   3 : Bouton(975, 250, 'niveau3.png', None, 255),
                   4 : Bouton(225, 450, 'niveau4.png', None, 255),
                   5 : Bouton(600, 450, 'niveau5.png', None, 255),
                   6 : Bouton(975, 450, 'niveau6.png', None, 125)}

# Boucle principale du jeu
while PartiePacman.running :
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PartiePacman.running = False

    # Text meilleur et dernier score
    for i in dico_text_menu :
        dico_text_menu[i][0].update(dico_text_menu[i][1](), None, None)
                
    # Menu Jouer : gestion des boutons et affichage du text
    while not PartiePacman.play and PartiePacman.running and not PartiePacman.parametre :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PartiePacman.running = False
        screen.fill(Text.blanc)
        #boutons :
        Bouton_groupe_menu.draw(screen)
        Bouton_groupe_menu.update()
        if PartiePacman.largeur == 1200 and PartiePacman.hauteur ==700:
            for i in dico_bouton_lab :
                 if dico_bouton_lab[i].update():
                    lab(i)
                 if i == PartiePacman.type_labyrinthe:
                    dico_bouton_lab[i].image.set_alpha(125)
                 else :
                    dico_bouton_lab[i].image.set_alpha(255)
                 screen.blit(dico_bouton_lab[i].image, dico_bouton_lab[i].rect)
        if PartiePacman.partie_en_cours :
            screen.blit(Bouton_play_bis.image, Bouton_play_bis.rect)
            Bouton_play_bis.update()
        #text :
        for i in dico_text_menu:
            screen.blit(dico_text_menu[i][0].surface, dico_text_menu[i][0].rect)
        pygame.display.flip()

    #utilisation pour faire une pause entre chaque menu/éviter les doubles cliques
    time.sleep(0.3)

    # Menu paramètre : gestion des boutons
    while not PartiePacman.play and PartiePacman.running and PartiePacman.parametre :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PartiePacman.running = False
        screen.fill(Text.noir)
        #boutons :
        Bouton_groupe_parametre.draw(screen)
        Bouton_groupe_parametre.update()
        screen.blit(Bouton_groupe_son[PartiePacman.son_var].image, Bouton_groupe_son[PartiePacman.son_var].rect)
        Bouton_groupe_son[PartiePacman.son_var].update()
        if PartiePacman.partie_en_cours :
            screen.blit(Bouton_play_bis.image, Bouton_play_bis.rect)
            Bouton_play_bis.update()
        pygame.display.flip()

    time.sleep(0.3)

    # Définition du labyrinthe
    if not PartiePacman.partie_en_cours:
        bordures = dico_bordures[PartiePacman.type_labyrinthe] if PartiePacman.type_labyrinthe != 6 else creation_random_labyrinthe()

        # si la partie n'est pas en cours, elle va sans doute commencer, création des pièces
        for x, y in Bonus.position:
            bonus_groupe.add(Bonus((x, y), pieces_image))  # Ajouter la pièce au groupe

    #partie en cours
    if PartiePacman.play :
        PartiePacman.partie_en_cours = True


    # Boucle jeu
    while Pac_man.vie and PartiePacman.running and PartiePacman.hauteur*PartiePacman.largeur*0.005 != PartiePacman.score and PartiePacman.play and len(Fantome_groupe)+len(Fantome_groupe_actif)!=0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PartiePacman.running = False

        # Effacer l'écran en le remplissant de rose
        screen.fill(Text.rose)

        #mouvement pacman
        Pac_man.action(Fantome_groupe_actif, Fantome_groupe_absent)

        # gestion bonus
        for objet in bonus_groupe:
            objet.verif_collision(bonus_groupe)
        for objet in bonus_groupe: # Deux boucles, car ne pas blit celui qui est éliminé
            screen.blit(objet.image, objet.rect)

        #fonction gestion niveau
        PartiePacman.gestion_niveau()

        # Dessiner les obstacles
        for obs in bordures:
            obs.draw(screen)

        #gestion des fantomes
        Fantome.activation(Fantome_groupe, Fantome_groupe_actif)
        for un_fantome in Fantome_groupe_actif:
            un_fantome.action()

        # Dessiner le text
        for i in dico_text_jeux :
            dico_text_jeux[i][0].update(dico_text_jeux[i][1]())
            if dico_text_jeux[i][2]():
                screen.blit(dico_text_jeux[i][0].surface, dico_text_jeux[i][0].rect)
        
        #Dessiner les boutons 
        Bouton_groupe_level.draw(screen)
        Bouton_groupe_level.update()
        # Mettre à jour l'affichage
        pygame.display.flip()

        # Limitation fps
        clock.tick(PartiePacman.frame_seconde)

    #sortie de la partie
    #actu variable dernier et meilleur score
    PartiePacman.dernier_score = PartiePacman.score if PartiePacman.score != 0 else PartiePacman.dernier_score
    PartiePacman.meilleur_score = PartiePacman.dernier_score if PartiePacman.dernier_score > PartiePacman.meilleur_score else PartiePacman.meilleur_score

    #Défaite :
    if not Pac_man.vie :
        screen.blit(dico_text_autre['Défaite'].surface, dico_text_autre['Défaite'].rect)
        pygame.display.flip()
        if PartiePacman.son_var == 1:
            son_game_over.play()
        time.sleep(3)
        restart()
    #Victoire :
    elif PartiePacman.hauteur*PartiePacman.largeur*0.005==PartiePacman.score or len(Fantome_groupe)+len(Fantome_groupe_actif)==0:
        screen.blit(dico_text_autre['Victoire'].surface, dico_text_autre['Victoire'].rect)
        pygame.display.flip()
        if PartiePacman.son_var ==1:
            son_victoire.play()
        time.sleep(3)   
        restart()

    #retour au menu
    PartiePacman.play = False
    time.sleep(0.3)
    
# fermer le jeu
pygame.quit()
sys.exit()