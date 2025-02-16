#Tamagotchi

#importe les bibliothèques
import pygame, time, sys, os
from random import randint, choice
#initialise
pygame.init()
#musique + sons
pygame.mixer.init()
pygame.mixer.music.load("kk.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
miaou = pygame.mixer.Sound("miaou.wav")
#crée la couleur pour le fond
Couleur_fond = (135, 206, 250)
#crée la fenêtre
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tamagotchi Coquette")
#variable pour le mode de jeu (personnalisaton, mini jeu etc)
jeu = 0
#télécharge toutes les images et règle leur taille
l = pygame.transform.scale(pygame.image.load("l.png"), (153, 96))
r = pygame.transform.scale(pygame.image.load("r.png"), (153, 96))
c = pygame.transform.scale(pygame.image.load("c.png"), (153, 96))
o = pygame.transform.scale(pygame.image.load("o.png"), (153, 96))
f = pygame.transform.scale(pygame.image.load("f.png"), (153, 96))
n = pygame.transform.scale(pygame.image.load("n.png"), (153, 96))
p = pygame.transform.scale(pygame.image.load("p.png"), (153, 96))
coeur = pygame.transform.scale(pygame.image.load("coeur.png"), (100, 100))
shop = pygame.transform.scale(pygame.image.load("shop.png"), (300, 200))
fleche = pygame.transform.scale(pygame.image.load("fleche.png"), (200, 100))
eau = pygame.transform.scale(pygame.image.load('eau.png'), (400, 200))
poulet = pygame.transform.scale(pygame.image.load("poulet.png"), (400, 200))
lait = pygame.transform.scale(pygame.image.load('lait.png'), (400, 200))
croquettes = pygame.transform.scale(pygame.image.load('croquettes.png'), (400, 200))
patee = pygame.transform.scale(pygame.image.load('patee.png'), (400, 200))
poisson = pygame.transform.scale(pygame.image.load('poisson.png'), (400, 200))
fdroite = pygame.transform.scale(pygame.image.load("flechedroite.png"), (200, 100))
fgauche = pygame.transform.scale(pygame.image.load("flechegauche.png"), (200, 100))
piece = pygame.transform.scale(pygame.image.load("piece.png"), (150, 75))
douche = pygame.transform.scale(pygame.image.load("douche.png"), (250, 150))
savon = pygame.transform.scale(pygame.image.load("savon.png"), (250, 150))
manette = pygame.transform.scale(pygame.image.load("manette.png"), (250, 150))
lampe = pygame.transform.scale(pygame.image.load("lampe.png"), (250, 150))
souris1 = pygame.transform.scale(pygame.image.load("souris1.png"), (600, 300))
souris2 = pygame.transform.scale(pygame.image.load("souris2.png"), (600, 300))
patte = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("patte.png"), (200, 100)), -45)
bombe = pygame.transform.scale(pygame.image.load("bombe.png"), (200, 100))
bubulle = pygame.transform.scale(pygame.image.load("bulle.png"), (200, 100))
commode = pygame.transform.scale(pygame.image.load("commode.png"), (300, 150))
barriere = pygame.transform.scale(pygame.image.load("barriere.png"), (350, 175))
masque = pygame.image.load("none.png")
#choisit le chat de base
chat, chat_x, chat_y = pygame.transform.scale(pygame.image.load(f"orp.png"), (400, 350)), 200, 200
#gère les souris/bombes etc pour le mini jeu 1
souris_liste, bombe_liste, compteur_animation, nombre_souris, nombre_bombes, vitesse, intervalle_apparition, souris_attrapees, dernier_temps_augmentation, dernier_temps_souris, dernier_temps_bombe, patte_affichee = [], [], 0, 2, 2, 2, 3000, 0, pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks(), None
#variable pour l'augmentation de l'énergie quand le chat dort
derniere_aug = pygame.time.get_ticks()
#variable pour le saut du chat et la barrière dans le mini jeu 2
vitesse_y, gravité, saut_force, sol, est_sautant, chat_rect, barriere_x, barrieres_passees, vitesse_barriere, dernier_temps_vitesse = 0, 0.5, -14, 210, False, pygame.Rect(75, 210, 100, 100), 800, 0, randint(-17, -7), pygame.time.get_ticks()
#gère la personnalisation
etat = {"lunettes": "o", "noeud": "r", "chaussettes": "p"}
def maj_chat():
    global chat
    lunettes = etat["lunettes"]
    noeud = etat["noeud"]
    chaussettes = etat["chaussettes"]
    chat = pygame.transform.scale(pygame.image.load(f"{lunettes}{noeud}{chaussettes}.png"), (800 - 400, 600 - 250))
#gère les besoins du chat : affichage de la barre colorée, diminution etc
besoins, intervalle_besoins, dernier_temps_besoins = {"Faim": 80, "Soif": 90, "Énergie": 60, "Hygiène": 70, "Bonheur": 85}, 50000, pygame.time.get_ticks()
def couleur_besoin(valeur):
    couleurs = [(80, (0, 255, 0)), (60, (173, 255, 47)), (40, (255, 255, 0)), (20, (255, 165, 0)), (0, (255, 0, 0))]
    for limite, couleur in couleurs:
        if valeur >= limite:
            return couleur
def barre_besoin(x, y, valeur, texte):
    largeur, hauteur = 100, 10
    largeur_remplie = (valeur / 100) * largeur
    pygame.draw.rect(fenetre, (0, 0, 0), (x-2, y-2, largeur+4, hauteur+4))
    pygame.draw.rect(fenetre, couleur_besoin(valeur), (x, y, largeur_remplie, hauteur))
    fenetre.blit(pygame.font.Font(None, 26).render(f"{texte}: {valeur}%", True, (255, 255, 255)), (x + largeur // 2 - pygame.font.Font(None, 26).render(f"{texte}: {valeur}%", True, (255, 255, 255)).get_width() // 2, y - 25))
def reduire_besoins():
    for i in besoins :
        besoins[i] = max(0, besoins[i] - 1)
#gère le timer et l'affichage du coeur
temps_sur_chat, affiche_coeur, temps_debut_affichage_coeur = None, False, None
#gère les pièces et l'inventaire
pieces, inventaire, index_objet, deplacerobjet, objet_x, objet_y = 50, [], 0, False, 0, 520
#variables pour le savon/douche et les bulles
douche_x, douche_y, savon_x, savon_y, deplacerdouche, deplacersavon, bulles = 625, 475, -75, 480, False, False, []
#boucle principale
while True :
    #position de la souris pour des interactions
    x_souris, y_souris = pygame.mouse.get_pos()
    #personnalisation du chat
    if jeu == 0:
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(chat, (chat_x, chat_y))
        fenetre.blit(pygame.font.Font(None, 100).render("Personnalisez votre", True, (255, 105, 180)), (50, 10))
        fenetre.blit(pygame.font.Font(None, 100).render("chat !", True, (255, 105, 180)), (300, 75))
        elements = [(p, (620, 400)), (o, (10, 200)), (n, (620, 250)), (c, (620, 500)), (f, (10, 400)), (r, (620, 150)), (l, (10, 300))]
        for nom, position in elements:
            fenetre.blit(nom, position)
        fenetre.blit(pygame.font.Font(None, 26).render("Lunettes :", True, (255, 255, 255)), (40, 175))
        fenetre.blit(pygame.font.Font(None, 26).render("Noeud :", True, (255, 255, 255)), (660, 125))
        fenetre.blit(pygame.font.Font(None, 26).render("Chaussettes :", True, (255, 255, 255)), (630, 375))
        fenetre.blit(pygame.font.Font(None, 26).render("Appuyer sur ESPACE pour valider", True, (255, 255, 255)), (250, 560))
        #evenements
        for event in pygame.event.get():
            #pour quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN :
                #touche espace : changement d'ecran de jeu
                if event.key == pygame.K_SPACE :
                    jeu = 5
            #bouton de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #vérifie si un bouton est cliqué
                if 10 < x < 10 + l.get_width() and 300 < y < 300 + l.get_height():
                    etat["lunettes"] = "l"
                elif 10 < x < 10 + f.get_width() and 400 < y < 400 + f.get_height():
                    etat["lunettes"] = "f"
                elif 10 < x < 10 + o.get_width() and 200 < y < 200 + o.get_height():
                    etat["lunettes"] = "o"
                elif 620 < x < 620 + n.get_width() and 250 < y < 250 + n.get_height():
                    etat["noeud"] = "n"
                elif 620 < x < 620 + r.get_width() and 150 < y < 150 + r.get_height():
                    etat["noeud"] = "r"
                elif 620 < x < 620 + c.get_width() and 500 < y < 500 + c.get_height():
                    etat["chaussettes"] = "c"
                elif 620 < x < 620 + p.get_width() and 400 < y < 400 + p.get_height():
                    etat["chaussettes"] = "p"
                #met à jour l'apparence du chat
                maj_chat()
    #cuisine
    elif jeu == 1 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(chat, (chat_x, chat_y))
        pygame.draw.rect(fenetre, (255, 255, 255), (730, 513, 37, 17))
        fenetre.blit(shop, (600, 450))
        cuisine = pygame.font.Font(None, 36).render("CUISINE", True, (255, 105, 180))
        fenetre.blit(cuisine, (350, 560))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Pièces : {pieces}", True, (255, 255, 255)), (700, 7))
        fenetre.blit(piece, (610, -25))
        fenetre.blit(fgauche, (-50, 265))
        fenetre.blit(fdroite, (650, 265))
        fenetre.blit(pygame.transform.scale(fgauche, (100, 50)), (-25, 550))
        fenetre.blit(pygame.transform.scale(fdroite, (100, 50)), (125, 550))
        barre_besoin(50, 70, besoins["Faim"], "FAIM")
        barre_besoin(200, 70, besoins["Soif"], "SOIF")
        barre_besoin(350, 70, besoins["Énergie"], "ÉNERGIE")
        barre_besoin(500, 70, besoins["Hygiène"], "HYGIENE")
        barre_besoin(650, 70, besoins["Bonheur"], "BONHEUR")
        #gère temps et affichage coeur
        temps_actuel = pygame.time.get_ticks()
        if chat_x < x_souris < chat_x + chat.get_width() and chat_y < y_souris < chat_y + chat.get_height():
            if temps_sur_chat is None:
                temps_sur_chat = temps_actuel
            elif temps_actuel - temps_sur_chat >= 2000 and not affiche_coeur:
                affiche_coeur = True
                temps_debut_affichage_coeur = temps_actuel
        else:
            temps_sur_chat = None
        if affiche_coeur:
            fenetre.blit(coeur, (chat_x + chat.get_width() // 2 - coeur.get_width() // 2, chat_y - coeur.get_height()))
            if temps_actuel - temps_debut_affichage_coeur >= 2000:
                affiche_coeur = False
                temps_debut_affichage_coeur = None
            pygame.display.flip()
        #diminution des besoins
        temps_actuel2 = pygame.time.get_ticks()
        if temps_actuel2 - dernier_temps_besoins >= intervalle_besoins :
            reduire_besoins()
            dernier_temps_besoins = temps_actuel2
        #gère l'affichage de l'inventaire
        if inventaire:
            objet_actuel = inventaire[index_objet]
            objet_image = eval(objet_actuel)
            fenetre.blit(pygame.transform.scale(objet_image, (200, 100)), (objet_x, objet_y))
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jeu = 6
                if event.key == pygame.K_SPACE:
                    jeu = 2
                #faire défiler l'inventaire
                if event.key == pygame.K_q and inventaire :
                    index_objet = (index_objet - 1) % len(inventaire)
                if event.key == pygame.K_d and inventaire :
                    index_objet = (index_objet + 1) % len(inventaire)
                #faire défiler les salles
                if event.key == pygame.K_RIGHT:
                    jeu = 3
                if event.key == pygame.K_LEFT:
                    jeu = 4
            #bouton souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #le chat fait miaou
                if chat_x < x < chat_x + chat.get_width() and chat_y < y < chat_y + chat.get_height():
                    miaou.play()
                #pour appuyer sur les boutons, le magasin et les flèches pour changer de salle/d'objet d'inventaire
                if 600 < x < 600 + shop.get_width() and 450 < y < 450 + shop.get_height():
                    jeu = 2
                elif 650 < x < 650 + fdroite.get_width() and 265 < y < 265 + fdroite.get_height():
                    jeu = 3
                elif -50 < x < -50 + fgauche.get_width() and 265 < y < 265 + fgauche.get_height():
                    jeu = 4
                elif -25 < x < -25 + pygame.transform.scale(fgauche, (100, 50)).get_width() and 550 < y < 550 + pygame.transform.scale(fgauche, (100, 50)).get_height() and inventaire :
                    index_objet = (index_objet - 1) % len(inventaire)
                elif 125 < x < 125 + pygame.transform.scale(fdroite, (100, 50)).get_width() and 550 < y < 550 + pygame.transform.scale(fdroite, (100, 50)).get_height() and inventaire :
                    index_objet = (index_objet + 1) % len(inventaire)
                #pour déplacer l'objet de l'inventaire
                elif inventaire:
                    if objet_x < x < objet_x + objet_image.get_width() and objet_y < y < objet_y + objet_image.get_height():
                        deplacerobjet = True
            #pour déplacer l'objet de l'inventaire
            if event.type == pygame.MOUSEMOTION and deplacerobjet == True :
                objet_x = x_souris - 100
                objet_y = y_souris - 50
            #pour relâcher l'objet de l'inventaire et le remettre à sa position initiale
            if event.type == pygame.MOUSEBUTTONUP :
                if 225 < x_souris < 475 and 250 < y_souris < 375:
                    inventaire.remove(objet_actuel)
                    deplacerobjet, objet_x, objet_y = False, 0, 520
                    if objet_actuel == "eau" or objet_actuel == "lait":
                        besoins["Soif"] += 30
                        if besoins["Soif"] > 100:
                            besoins["Soif"] = 100
                    else :
                        besoins["Faim"] += 30
                        if besoins["Faim"] > 100:
                            besoins["Faim"] = 100
                else:
                    deplacerobjet, objet_x, objet_y = False, 0, 520
    #magasin
    elif jeu == 2 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill((195, 230, 252))
        fenetre.blit(fleche, (-50, -15))
        fenetre.blit(pygame.font.Font(None, 100).render("MAGASIN", True, (255, 105, 180)), (225, 20))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Pièces : {pieces}", True, (255, 105, 180)), (700, 7))
        fenetre.blit(piece, (610, -25))
        items = [("1 : Eau", eau, (-100, 100), (220, 150)),("2 : Lait", lait, (250, 100), (570, 150)),("4 : Croquettes", croquettes, (250, 250), (570, 300)),("5 : Pâtée", patee, (-100, 400), (220, 450)),("3 : Poulet", poulet, (-100, 250), (220, 300)),("6 : Poisson", poisson, (250, 400), (570, 450))]
        for name, image, pos_image, pos_texte in items:
            fenetre.blit(image, pos_image)
            fenetre.blit(pygame.font.Font(None, 36).render(name, True, (255, 105, 180)), pos_texte)
            fenetre.blit(pygame.font.Font(None, 26).render("30%", True, (0, 0, 0)), (pos_texte[0], pos_texte[1] + 40))
            fenetre.blit(pygame.font.Font(None, 26).render("10 pièces", True, (0, 0, 0)), (pos_texte[0], pos_texte[1] + 65))
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jeu = 1
                #pour acheter les objets avec le clavier et pas la souris
                if event.key == pygame.K_1:
                    inventaire.append("eau")
                    pieces -= 10
                if event.key == pygame.K_2:
                    inventaire.append("lait")
                    pieces -= 10
                if event.key == pygame.K_3:
                    inventaire.append("poulet")
                    pieces -= 10
                if event.key == pygame.K_4:
                    inventaire.append("croquettes")
                    pieces -= 10
                if event.key == pygame.K_5:
                    inventaire.append("patee")
                    pieces -= 10
                if event.key == pygame.K_6:
                    inventaire.append("poisson")
                    pieces -= 10
            #bouton souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if -50 < x < -50 + fleche.get_width() and -15 < y < -15 + fleche.get_height():
                    jeu = 1
                #gère l'achat d'objets
                if -100 < x < -100 + eau.get_width() and 100 < y < 100 + eau.get_height():
                    if pieces >= 10 :
                        inventaire.append("eau")
                        pieces -= 10
                if 250 < x < 250 + lait.get_width() and 100 < y < 100 + lait.get_height():
                    if pieces >= 10 :
                        inventaire.append("lait")
                        pieces -= 10
                if -100 < x < -100 + poulet.get_width() and 250 < y < 250 + poulet.get_height():
                    if pieces >= 10 :
                        inventaire.append("poulet")
                        pieces -= 10
                if 250 < x < 250 + croquettes.get_width() and 250 < y < 250 + croquettes.get_height():
                    if pieces >= 10 :
                        inventaire.append("croquettes")
                        pieces -= 10
                if 250 < x < 250 + poisson.get_width() and 400 < y < 400 + poisson.get_height():
                    if pieces >= 10 :
                        inventaire.append("poisson")
                        pieces -= 10
                if -100 < x < -100 + patee.get_width() and 400 < y < 400 + patee.get_height():
                    if pieces >= 10 :
                        inventaire.append("patee")
                        pieces -= 10
    #salle de jeux
    elif jeu == 3 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(chat, (chat_x, chat_y))
        chat = pygame.transform.scale(chat, (800 - 400, 600 - 250))
        fenetre.blit(pygame.font.Font(None, 36).render("SALLE DE JEUX", True, (255, 105, 180)), (300, 560))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Pièces : {pieces}", True, (255, 255, 255)), (700, 7))
        fenetre.blit(piece, (610, -25))
        fenetre.blit(fgauche, (-50, 265))
        fenetre.blit(fdroite, (650, 265))
        fenetre.blit(manette, (615, 490))
        barre_besoin(50, 70, besoins["Faim"], "FAIM")
        barre_besoin(200, 70, besoins["Soif"], "SOIF")
        barre_besoin(350, 70, besoins["Énergie"], "ÉNERGIE")
        barre_besoin(500, 70, besoins["Hygiène"], "HYGIENE")
        barre_besoin(650, 70, besoins["Bonheur"], "BONHEUR")
        #gère temps et affichage coeur
        temps_actuel = pygame.time.get_ticks()
        if chat_x < x_souris < chat_x + chat.get_width() and chat_y < y_souris < chat_y + chat.get_height():
            if temps_sur_chat is None:
                temps_sur_chat = temps_actuel
            elif temps_actuel - temps_sur_chat >= 2000 and not affiche_coeur:
                affiche_coeur = True
                temps_debut_affichage_coeur = temps_actuel
        else:
            temps_sur_chat = None
        if affiche_coeur:
            fenetre.blit(coeur, (chat_x + chat.get_width() // 2 - coeur.get_width() // 2, chat_y - coeur.get_height()))
            if temps_actuel - temps_debut_affichage_coeur >= 2000:
                affiche_coeur = False
                temps_debut_affichage_coeur = None
            pygame.display.flip()
        #diminution des besoins
        temps_actuel2 = pygame.time.get_ticks()
        if temps_actuel2 - dernier_temps_besoins >= intervalle_besoins :
            reduire_besoins()
            dernier_temps_besoins = temps_actuel2
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                #pour appuyer sur les touches, les crédits, les salles et le menu des mini jeux
                if event.key == pygame.K_ESCAPE:
                    jeu = 6
                if event.key == pygame.K_RIGHT:
                    jeu = 5
                if event.key == pygame.K_LEFT:
                    jeu = 1
                if event.key == pygame.K_SPACE:
                    jeu = 9
            #les boutons, les flèches pour changer de salle et le bouton des mini jeux
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 650 < x < 650 + fdroite.get_width() and 265 < y < 265 + fdroite.get_height():
                    jeu = 5
                if -50 < x < -50 + fgauche.get_width() and 265 < y < 265 + fgauche.get_height():
                    jeu = 1
                if 615 < x < 615 + manette.get_width() and 490 < y < 490 + manette.get_height():
                    jeu = 9
                #miaou
                if chat_x < x < chat_x + chat.get_width() and chat_y < y < chat_y + chat.get_height():
                    miaou.play()
    #salle de bains
    elif jeu == 4 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(chat, (chat_x, chat_y))
        fenetre.blit(pygame.font.Font(None, 36).render("SALLE DE BAINS", True, (255, 105, 180)), (300, 560))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Pièces : {pieces}", True, (255, 255, 255)), (700, 7))
        fenetre.blit(piece, (610, -25))
        fenetre.blit(fgauche, (-50, 265))
        fenetre.blit(fdroite, (650, 265))
        fenetre.blit(savon, (savon_x, savon_y))
        fenetre.blit(douche, (douche_x, douche_y))
        for bulle in bulles:
            fenetre.blit(bubulle, (bulle["x"], bulle["y"]))
        barre_besoin(50, 70, besoins["Faim"], "FAIM")
        barre_besoin(200, 70, besoins["Soif"], "SOIF")
        barre_besoin(350, 70, besoins["Énergie"], "ÉNERGIE")
        barre_besoin(500, 70, besoins["Hygiène"], "HYGIENE")
        barre_besoin(650, 70, besoins["Bonheur"], "BONHEUR")
        #gère temps et affichage coeur
        if deplacersavon == False and deplacerdouche == False :
            temps_actuel = pygame.time.get_ticks()
            if chat_x < x_souris < chat_x + chat.get_width() and chat_y < y_souris < chat_y + chat.get_height():
                if temps_sur_chat is None:
                    temps_sur_chat = temps_actuel
                elif temps_actuel - temps_sur_chat >= 2000 and not affiche_coeur:
                    affiche_coeur = True
                    temps_debut_affichage_coeur = temps_actuel
            else:
                temps_sur_chat = None
            if affiche_coeur:
                fenetre.blit(coeur, (chat_x + chat.get_width() // 2 - coeur.get_width() // 2, chat_y - coeur.get_height()))
                if temps_actuel - temps_debut_affichage_coeur >= 2000:
                    affiche_coeur = False
                    temps_debut_affichage_coeur = None
                pygame.display.flip()
        #diminution des besoins
        temps_actuel2 = pygame.time.get_ticks()
        if temps_actuel2 - dernier_temps_besoins >= intervalle_besoins :
            reduire_besoins()
            dernier_temps_besoins = temps_actuel2
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jeu = 6
                if event.key == pygame.K_RIGHT:
                    jeu = 1
                if event.key == pygame.K_LEFT:
                    jeu = 5
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #miaou
                if chat_x < x < chat_x + chat.get_width() and chat_y < y < chat_y + chat.get_height():
                    miaou.play()
                #les boutons, flèches et savon + douche
                if 650 < x < 650 + fdroite.get_width() and 265 < y < 265 + fdroite.get_height():
                    jeu = 1
                if -50 < x < -50 + fgauche.get_width() and 265 < y < 265 + fgauche.get_height():
                    jeu = 5
                if -75 < x < -75 + savon.get_width() and 480 < y < 480 + savon.get_height():
                    deplacersavon = True
                if 625 < x < 625 + douche.get_width() and 475 < y < 475 + douche.get_height():
                    deplacerdouche = True
            #pour déplacer le savon
            if event.type == pygame.MOUSEMOTION and deplacersavon == True :
                savon_x = x_souris - 125
                savon_y = y_souris - 75
                if chat_x < savon_x < chat_x + chat.get_width() and chat_y < savon_y < chat_y + chat.get_height():
                    bulles.append({"x": savon_x + randint(-20, 20), "y": savon_y + randint(-20, 20), "temps": pygame.time.get_ticks()})
                    #augmente l'hygiène
                    if besoins["Hygiène"] < 100:
                        besoins["Hygiène"] += 1
            #pour déplacer la douche
            if event.type == pygame.MOUSEMOTION and deplacerdouche == True :
                douche_x = x_souris - 125
                douche_y = y_souris - 75
                bulles = [b for b in bulles if not (douche_x < b["x"] + 10 < douche_x + 100 and douche_y < b["y"] + 10 < douche_y + 100)]
            #relâche le savon et la douche en les remettant à leur position initiale
            if event.type == pygame.MOUSEBUTTONUP :
                deplacersavon, deplacerdouche, savon_x, savon_y, douche_x, douche_y = False, False, -75, 480, 625, 475
    #chambre
    elif jeu == 5 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(chat, (chat_x, chat_y))
        fenetre.blit(pygame.font.Font(None, 36).render("CHAMBRE", True, (255, 105, 180)), (350, 560))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Pièces : {pieces}", True, (255, 255, 255)), (700, 7))
        fenetre.blit(piece, (610, -25))
        fenetre.blit(fgauche, (-50, 265))
        fenetre.blit(fdroite, (650, 265))
        fenetre.blit(lampe, (625, 475))
        fenetre.blit(commode, (-75, 475))
        fenetre.blit(masque, (-50, 80))
        barre_besoin(50, 70, besoins["Faim"], "FAIM")
        barre_besoin(200, 70, besoins["Soif"], "SOIF")
        barre_besoin(350, 70, besoins["Énergie"], "ÉNERGIE")
        barre_besoin(500, 70, besoins["Hygiène"], "HYGIENE")
        barre_besoin(650, 70, besoins["Bonheur"], "BONHEUR")
        #gère temps et affichage coeur
        temps_actuel = pygame.time.get_ticks()
        if chat_x < x_souris < chat_x + chat.get_width() and chat_y < y_souris < chat_y + chat.get_height():
            if temps_sur_chat is None:
                temps_sur_chat = temps_actuel
            elif temps_actuel - temps_sur_chat >= 2000 and not affiche_coeur:
                affiche_coeur = True
                temps_debut_affichage_coeur = temps_actuel
        else:
            temps_sur_chat = None
        if affiche_coeur:
            fenetre.blit(coeur, (chat_x + chat.get_width() // 2 - coeur.get_width() // 2, chat_y - coeur.get_height()))
            if temps_actuel - temps_debut_affichage_coeur >= 2000:
                affiche_coeur = False
                temps_debut_affichage_coeur = None
            pygame.display.flip()
        #diminution des besoins
        temps_actuel2 = pygame.time.get_ticks()
        if temps_actuel2 - dernier_temps_besoins >= intervalle_besoins :
            reduire_besoins()
            dernier_temps_besoins = temps_actuel2
        #evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #clavier
            if event.type == pygame.KEYDOWN:
                #revient à la personalisation et réinitialise les variables
                if event.key == pygame.K_BACKSPACE:
                    jeu = 0
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
                if event.key == pygame.K_ESCAPE:
                    #affiche les crédits et réinitialise la couleur de fond et le masque
                    jeu = 6
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
                #pour gérer la lampe avec la touche espace
                if event.key == pygame.K_SPACE:
                    if Couleur_fond == (135, 206, 250):
                        Couleur_fond = (81, 123, 150)
                        masque = pygame.transform.scale(pygame.image.load("masque.png"), (800, 400))
                    elif Couleur_fond == (81, 123, 150):
                        Couleur_fond = (135, 206, 250)
                        masque = pygame.image.load("none.png")
                #changer de salle en réinitialisant les variables
                if event.key == pygame.K_RIGHT:
                    jeu = 4
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
                if event.key == pygame.K_LEFT:
                    jeu = 3
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #jouer le son miaou quand le chat est cliqué
                if chat_x < x < chat_x + chat.get_width() and chat_y < y < chat_y + chat.get_height():
                    miaou.play()
                #quand on appuie sur les flèches pour changer de pièce, réinitialise le masque et la couleur de fond
                if 650 < x < 650 + fdroite.get_width() and 265 < y < 265 + fdroite.get_height():
                    jeu = 4
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
                if -50 < x < -50 + fgauche.get_width() and 265 < y < 265 + fgauche.get_height():
                    jeu = 3
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
                #pour éteindre/allumer la lumière et faire dormir/réveiller le chat avec son masque
                if 625 < x < 625 + lampe.get_width() and 475 < y < 475 + lampe.get_height():
                    if Couleur_fond == (135, 206, 250):
                        Couleur_fond = (81, 123, 150)
                        masque = pygame.transform.scale(pygame.image.load("masque.png"), (800, 400))
                    elif Couleur_fond == (81, 123, 150):
                        Couleur_fond = (135, 206, 250)
                        masque = pygame.image.load("none.png")
                #pour aller dans la commode et retourner à la personnalisation du chat
                if -75 < x < -75 + commode.get_width() and 475 < y < 475 + commode.get_height():
                    jeu = 0
                    Couleur_fond = (135, 206, 250)
                    masque = pygame.image.load("none.png")
        if Couleur_fond == (81, 123, 150):
            #affichage du texte ZZZ
            fenetre.blit(pygame.font.Font(None, 100).render("Z", True, (255, 255, 255)), (475, 175))
            fenetre.blit(pygame.font.Font(None, 75).render("Z", True, (255, 255, 255)), (530, 145))
            fenetre.blit(pygame.font.Font(None, 50).render("Z", True, (255, 255, 255)), (570, 115))
            #augmentation du besoin énergie
            temps_actuel4 = pygame.time.get_ticks()
            if temps_actuel4 - derniere_aug >= 3000 and besoins["Énergie"] < 100:
                besoins["Énergie"] += 1
                derniere_aug = temps_actuel4
    #mini jeu 1 : attrape souris
    elif jeu == 7 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        pygame.draw.rect(fenetre, (205, 133, 63), (0, 150, 800, 75))
        pygame.draw.rect(fenetre, (205, 133, 63), (0, 300, 800, 75))
        pygame.draw.rect(fenetre, (205, 133, 63), (0, 450, 800, 75))
        pygame.draw.rect(fenetre, (0, 255, 0), (0, 150, 800, 10))
        pygame.draw.rect(fenetre, (0, 255, 0), (0, 300, 800, 10))
        pygame.draw.rect(fenetre, (0, 255, 0), (0, 450, 800, 10))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Souris : {souris_attrapees}", True, (255, 255, 255)), (10, 10))
        fenetre.blit(pygame.font.Font(None, 100).render("Attrapez les souris !", True, (255, 105, 180)), (50, 30))
        fenetre.blit(pygame.transform.scale(chat, (100, 100)), (350, 500))
        #gere les souris/bombes, les mouvements etc
        temps_actuel3 = pygame.time.get_ticks()
        #ajoute des souris
        if temps_actuel3 - dernier_temps_souris > intervalle_apparition and len(souris_liste) < nombre_souris:
            souris_liste.append({"x": choice([-250, 800 - 250]), "y": choice([-10, 140, 290]), "vitesse": vitesse, "direction": choice(["droite", "gauche"]), "image": souris1})
            dernier_temps_souris = temps_actuel3
        #ajoute des bombes
        if temps_actuel3 - dernier_temps_bombe > intervalle_apparition and len(bombe_liste) < nombre_bombes:
            bombe_liste.append({"x": choice([-250, 800]), "y": choice([75, 225, 375]), "vitesse": vitesse, "direction": choice(["droite", "gauche"]), "image": pygame.transform.scale(pygame.image.load("bombe.png").convert_alpha(), (200, 100))})
            dernier_temps_bombe = temps_actuel3
        #augmente le nombre de souris et de bombes toutes les 10 sec (5 max en même temps) + leur vitesse + réduit l'intervalle d'apparition des souris => complique le jeu avec le temps
        if temps_actuel3 - dernier_temps_augmentation > 10000:
            if nombre_souris < 5:
                nombre_souris += 1
            if nombre_bombes < 5 :
                nombre_bombes += 1
            if vitesse < 5:
                vitesse += 1
            if intervalle_apparition > 500 :
                intervalle_apparition -= 500
            dernier_temps_augmentation = temps_actuel3
        #gère les souris
        compteur_animation += 1
        if compteur_animation % 10 == 0:
            #animation de marche
            for souris in souris_liste:
                souris["image"] = souris1 if souris["image"] == souris2 else souris2
        #affiche la souris et la fait avancer
        for souris in souris_liste:
            if souris["direction"] == "droite":
                souris["x"] += souris["vitesse"]
                souris_image_affichee = souris["image"]
            else:
                souris["x"] -= souris["vitesse"]
                souris_image_affichee = pygame.transform.flip(souris["image"], True, False)
            #fait réapparaître une souris si elle atteint le bord sur une ligne aléatoire
            if souris["x"] > 800-250:
                souris["direction"] = "gauche"
                souris["y"] = choice([-10, 140, 290])
            elif souris["x"] < -250:
                souris["direction"] = "droite"
                souris["y"] = choice([-10, 140, 290])
            fenetre.blit(souris_image_affichee, (souris["x"], souris["y"]))
        #gère les bombes de la même manière que les souris mais sans animation
        for bombe in bombe_liste:
            if bombe["direction"] == "droite":
                bombe["x"] += bombe["vitesse"]
            else:
                bombe["x"] -= bombe["vitesse"]
            if bombe["x"] > 800:
                bombe["direction"] = "gauche"
                bombe["y"] = choice([75, 225, 375])
            elif bombe["x"] < -250:
                bombe["direction"] = "droite"
                bombe["y"] = choice([75, 225, 375])
            fenetre.blit(bombe["image"], (bombe["x"], bombe["y"]))
        #affiche la patte quand on clique sur une souris
        if patte_affichee:
            fenetre.blit(patte, (patte_affichee["x"], patte_affichee["y"]))
            if pygame.time.get_ticks() - patte_affichee["temps"] > 2000:
                patte_affichee = None
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #detecte la souris et la fait disparaître si on clique dessus
                for souris in souris_liste:
                    souris_rect = pygame.Rect(souris["x"]+250, souris["y"]+125, 100, 50)
                    if souris_rect.collidepoint(x, y):
                        patte_affichee = {"x": souris["x"]+200, "y": souris["y"]+50, "temps": pygame.time.get_ticks()}
                        souris_liste.remove(souris)
                        souris_attrapees += 1
                #détecte la bombe et affiche l'écran game over
                for bombe in bombe_liste:
                    bombe_rect = pygame.Rect(bombe["x"]+40, bombe["y"]+25, 100, 50)
                    if bombe_rect.collidepoint(x, y):
                        #réinitialise les variables
                        jeu, pieces, souris_liste, bombe_liste, compteur_animation, nombre_souris, nombre_bombes, vitesse, intervalle_apparition, dernier_temps_augmentation, dernier_temps_souris, dernier_temps_bombe, souris_attrapees = 10, pieces + souris_attrapees // 3, [], [], 0, 2, 2, 2, 3000, pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks(), 0
                        #augmente le bonheur
                        besoins["Bonheur"] += 20
                        if besoins["Bonheur"] > 100 :
                            besoins["Bonheur"] = 100
    #mini jeu 2 : course d'obstacles
    elif jeu == 8 :
        temps_actuel5 = pygame.time.get_ticks()
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(pygame.font.Font(None, 100).render("Sautez !", True, (255, 105, 180)), (250, 10))
        pygame.draw.rect(fenetre, (205, 133, 63), (0, 300, 800, 300))
        pygame.draw.rect(fenetre, (0, 255, 0), (0, 300, 800, 10))
        fenetre.blit(pygame.transform.flip(pygame.transform.scale(chat, (100, 100)), True, False), chat_rect)
        fenetre.blit(barriere, (barriere_x, 195))
        fenetre.blit(pygame.font.Font(None, 26).render(f"Barrières : {barrieres_passees}", True, (255, 255, 255)), (10, 10))
        #faire reculer la barrière
        barriere_x += vitesse_barriere
        if barriere_x < -200 :
            barriere_x = 800
            barrieres_passees += 1
            vitesse_barriere = randint(-17, -7)
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #gère le saut
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not est_sautant:
                    vitesse_y = saut_force
                    est_sautant = True
        if est_sautant:
            vitesse_y += gravité
            chat_rect.y += vitesse_y
        #pour que le personnage reste sur le sol
        if chat_rect.y >= sol:
            chat_rect.y = sol
            est_sautant = False
            vitesse_y = 0
        #gère la collision entre le chat et la barrière
        barriere_rect = pygame.Rect(barriere_x + 120, 260, barriere.get_width() - 150, barriere.get_height())
        if chat_rect.colliderect(barriere_rect):
            #affiche l'écran game over et réinitialise les variables
            jeu = 10
            vitesse_y, gravité, saut_force, sol, est_sautant, chat_rect, barriere_x, barrieres_passees, vitesse_barriere, dernier_temps_vitesse, pieces = 0, 0.5, -14, 210, False, pygame.Rect(75, 210, 100, 100), 800, 0, randint(-17, -7), pygame.time.get_ticks(), pieces + barrieres_passees // 3
            #augmente le bonheur
            besoins["Bonheur"] += 20
            if besoins["Bonheur"] > 100 :
                besoins["Bonheur"] = 100
    #menu mini jeux
    elif jeu == 9 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill((195, 230, 252))
        pygame.draw.rect(fenetre, Couleur_fond, (150, 200, 150, 150))
        pygame.draw.rect(fenetre, Couleur_fond, (500, 200, 150, 150))
        pygame.draw.rect(fenetre, (205, 133, 63), (150, 300, 150, 50))
        pygame.draw.rect(fenetre, (0, 255, 0), (150, 300, 150, 10))
        pygame.draw.rect(fenetre, (205, 133, 63), (500, 300, 150, 50))
        pygame.draw.rect(fenetre, (0, 255, 0), (500, 300, 150, 10))
        pygame.draw.rect(fenetre, (0, 0, 0), (150, 200, 150, 150), 5)
        pygame.draw.rect(fenetre, (0, 0, 0), (500, 200, 150, 150), 5)
        fenetre.blit(pygame.transform.scale(barriere, (200, 100)), (515, 240))
        fenetre.blit(pygame.transform.flip(pygame.transform.scale(chat, (60, 60)), True, False), (515, 250))
        fenetre.blit(pygame.font.Font(None, 36).render("1 : Attrape-Souris", True, (255, 105, 180)), (125, 365))
        fenetre.blit(pygame.font.Font(None, 36).render("2 : Course d'obstacles", True, (255, 105, 180)), (460, 365))
        fenetre.blit(pygame.font.Font(None, 100).render("Mini jeux", True, (255, 105, 180)), (250, 10))
        fenetre.blit(fleche, (-50, -15))
        fenetre.blit(souris1, (-75, 135))
        fenetre.blit(patte, (120, 180))
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #touche pour revenir en arrière ou cliquer sur les mini jeux
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jeu = 3
                if event.key == pygame.K_1:
                    jeu = 7
                if event.key == pygame.K_2:
                    jeu = 8
            #bouton souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #la fleche pour revenir en arriere
                if -50 < x < -50 + fleche.get_width() and -15 < y < -15 + fleche.get_height():
                    jeu = 3
                #jouer aux mini jeux
                if 150 < x < 150 + 150 and 200 < y < 200 + 150 :
                    jeu = 7
                if 500 < x < 500 + 150 and 200 < y < 200 + 150 :
                    jeu = 8
    #crédits de fin
    elif jeu == 6 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill(Couleur_fond)
        fenetre.blit(pygame.font.Font(None, 100).render("Merci d'avoir joué !", True, (255, 105, 180)), (75, 20))
        fenetre.blit(pygame.font.Font(None, 36).render("Codeuse :", True, (255, 255, 255)), (110, 120))
        fenetre.blit(pygame.font.Font(None, 36).render("Justine", True, (255, 255, 255)), (120, 160))
        fenetre.blit(pygame.font.Font(None, 36).render("Relecteurs :", True, (255, 255, 255)), (800 - 350, 120))
        fenetre.blit(pygame.font.Font(None, 36).render("Arthur, Jade, Alexandre, Clara", True, (255, 255, 255)), (800 - 420, 160))
        fenetre.blit(pygame.font.Font(None, 36).render("Inspiré des jeux Tamagotchi", True, (255, 255, 255)), (800 // 2 - pygame.font.Font(None, 36).render("Inspiré des jeux Tamagotchi", True, (255, 255, 255)).get_width() // 2, 240))
        fenetre.blit(pygame.font.Font(None, 36).render("(mais rendu coquette parce que c'est plus joli)", True, (255, 255, 255)), (800 // 2 - pygame.font.Font(None, 36).render("(mais rendu coquette parce que c'est plus joli)", True, (255, 255, 255)).get_width() // 2, 280))
        fenetre.blit(pygame.font.Font(None, 36).render("Sons :", True, (255, 255, 255)), (135, 360))
        fenetre.blit(pygame.font.Font(None, 36).render("Trouvés sur Zedge", True, (255, 255, 255)), (70, 400))
        fenetre.blit(pygame.font.Font(None, 36).render("Musique :", True, (255, 255, 255)), (800 - 350, 360))
        fenetre.blit(pygame.font.Font(None, 36).render("Bubblegum Kéké, par Kéké Laglisse", True, (255, 255, 255)), (800 - 460, 400))
        fenetre.blit(pygame.font.Font(None, 36).render("Aucun chat n'a été blessé durant ce jeu.", True, (255, 255, 255)), (800 // 2 - pygame.font.Font(None, 36).render("Aucun chat n'a été blessé durant ce jeu.", True, (255, 255, 255)).get_width() // 2, 480))
        fenetre.blit(pygame.font.Font(None, 36).render("Appuyer sur ECHAP pour quitter", True, (255, 255, 255)), (800 // 2 - pygame.font.Font(None, 36).render("Appuyer sur ECHAP pour quitter", True, (255, 255, 255)).get_width() // 2, 520))
        #evenements
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #quitter
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    #game over mini jeux
    elif jeu == 10 :
        #création de la fenêtre, les couleurs/textes images etc
        fenetre.fill((195, 230, 252))
        fenetre.blit(pygame.font.Font(None, 100).render("GAME OVER !", True, (255, 105, 180)), (150, 200))
        fenetre.blit(fleche, (-50, -15))
        for event in pygame.event.get():
            #quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #touche pour revenir au menu des mini jeux
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jeu = 9
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                #revenir au menu
                if -50 < x < -50 + fleche.get_width() and -15 < y < -15 + fleche.get_height():
                    jeu = 9
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(60)