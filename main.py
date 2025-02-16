import pygame
import math
from game import Game, GameOver  
from player import Player

#définir une horloge
clock= pygame.time.Clock()
FPS= 60

#creer la fenetre
pygame.display.set_caption("cat_ennemie")
screen = pygame.display.set_mode((1000,700))
menu = "bienvenue"


background = pygame.image.load("PygameAssets-main/bg.jpeg").convert_alpha()
background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))


#charger la banniere du jeu
banner = pygame.image.load("PygameAssets-main/banner.png")
banner = pygame.transform.scale(banner, (800,300))#redimensioner l'image
banner_rect = banner.get_rect()#plus simple pour repositionner l'image
banner_rect.center = (screen.get_width() // 2, screen.get_height() // 3)

police = pygame.font.Font(None, 40)

#charger le boutin "jouer"
play_button= pygame.image.load("PygameAssets-main/button.png")
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect= play_button.get_rect()
play_button_rect.center = (screen.get_width() // 2, screen.get_height() // 1.5)

# Charger le bouton "Réglages"
settings_button = pygame.image.load("PygameAssets-main/button.png")
settings_button = pygame.transform.scale(settings_button, (300, 100))
settings_button_rect = settings_button.get_rect(center=(screen.get_width() // 2, 600))
back_button = pygame.image.load("PygameAssets-main/button.png")
back_button = pygame.transform.scale(back_button, (200, 80))
back_button_rect = back_button.get_rect(center=(screen.get_width() // 2, 600))

#3 bpoutons de niveaux
level1_button = pygame.image.load("PygameAssets-main/button.png")
level1_button = pygame.transform.scale(level1_button, (300, 100))
level1_button_rect = level1_button.get_rect()
level1_button_rect.x = math.ceil(screen.get_width() / 3.33)
level1_button_rect.y = 200  # Position verticale pour Niveau 1

level2_button = pygame.image.load("PygameAssets-main/button.png")
level2_button = pygame.transform.scale(level2_button, (300, 100))
level2_button_rect = level2_button.get_rect()
level2_button_rect.x = math.ceil(screen.get_width() / 3.33)
level2_button_rect.y = 350  # Position verticale pour Niveau 2

level3_button = pygame.image.load("PygameAssets-main/button.png")
level3_button = pygame.transform.scale(level3_button, (300, 100))
level3_button_rect = level3_button.get_rect()
level3_button_rect.x = math.ceil(screen.get_width() / 3.33)
level3_button_rect.y = 500  # Position verticale pour Niveau 3

def afficher_boutons_niveaux(screen):
    screen.blit(level1_button, level1_button_rect)
    screen.blit(level2_button, level2_button_rect)
    screen.blit(level3_button, level3_button_rect)

#focntion pour afficher les regles dans un rectangle arrondie avec une ombre t legerement trasnparent 
def afficher_regles(screen, police):
    
    regles =  [
    "RÈGLES DU JEU :",
    "Déplacement : <- ->  |  Saut : ^  |  Attaque : Z (boule de feu)",
    "Ennemis : contact = dégâts  |  Chien = tire des projectiles",
    "Bonus : Étoile = boost temporaire  |  Malus : Poison = ralentit",
    " ", 
    "A TOI DE JOUER !"

    ]


    largeur_rect = screen.get_width() // 1.15
    hauteur_rect = 250
    x_rect = (screen.get_width() - largeur_rect) // 2
    y_rect = 150
    couleur_fond = (30, 30, 60, 180)  
    ombre_rect = pygame.Rect(x_rect + 5, y_rect + 5, largeur_rect, hauteur_rect)
    pygame.draw.rect(screen, (10, 10, 30), ombre_rect, border_radius=20)  
    surface_regles = pygame.Surface((largeur_rect, hauteur_rect), pygame.SRCALPHA)
    pygame.draw.rect(surface_regles, couleur_fond, (0, 0, largeur_rect, hauteur_rect), border_radius=20)
    screen.blit(surface_regles, (x_rect, y_rect))
    pygame.draw.rect(screen, (200, 200, 255), (x_rect, y_rect, largeur_rect, hauteur_rect), 3, border_radius=20)
    y_texte = y_rect + 20 
    for ligne in regles:
        texte = police.render(ligne, True, (255, 255, 255))  # Texte blanc pour le contraste
        x_texte = x_rect + (largeur_rect - texte.get_width()) // 2  # Centrer le texte
        screen.blit(texte, (x_texte, y_texte))
        y_texte += texte.get_height() + 10  # Espacement entre lignes





def niveau_clique(event, game):
    #choix du niveau
    if level1_button_rect.collidepoint(event.pos):
        print("Niveau 1 sélectionné")
        game.start(1)
        return "in_game"

    elif level2_button_rect.collidepoint(event.pos):
        print("Niveau 2 sélectionné")
        game.start(2)
        return "in_game"

    elif level3_button_rect.collidepoint(event.pos):
        print("Niveau 3 sélectionné")
        game.start(3)
        return "in_game"
def afficher_game_over(screen, game):
    """
    Affiche l'écran Game Over, le texte et le bouton "Rejouer".
    Gère l'événement de clic sur "Rejouer" pour retourner au menu principal.
    """
    # Créer un objet GameOver pour gérer l'affichage
    game_over_screen = GameOver(screen, game)
    game_over_screen.display()  # Afficher l'écran Game Over
    
    # Gérer l'événement du bouton "Rejouer"
    new_menu = game_over_screen.handle_events()  # Récupérer l'événement du bouton Rejouer
    
    if new_menu:  # Si un nouveau menu est retourné (lorsque le bouton "Rejouer" est cliqué)
        return new_menu  # Retourner "bienvenue" pour revenir au menu principal
    
    return None  # Aucun changement, garder le menu actuel
clock = pygame.time.Clock()
# charger le jeu
game= Game(screen)

running= True
game_over_played = False 
#boucle tant que running==True
while running:
    
    print("menu =", menu)
    print("game_over_val =", game.game_over_val)

    #arriere plan
    screen.blit(background, (0, 0))
    
    delta_time = clock.tick(45) / 1000.0    # Temps écoulé en secondes
     #verifier si le jeu a commencézzzzzzzzzz
    

    
    # main.py

    if game.game_over_val :
        if menu != "game_over":
            menu = "game_over"  # Modifier l'état du menu pour afficher l'écran Game Over

        # Arrêter tous les sons avant de jouer le son de Game Over
            game.sound_manager.stop_all()  # Arrêter tous les sons en cours
        
        # Ne jouer le son Game Over qu'une seule fois
         # S'assurer qu'il ne joue qu'une seule fois
        game_over_screen = GameOver(screen, game)
        # Afficher l'écran "Game Over"
         # Afficher l'écran Game Over
        game_over_screen.display()
        
        # Gérer les événements du bouton "Rejouer"
        new_menu = game_over_screen.handle_events()  # Récupérer l'événement du bouton Rejouer
        if new_menu:  # Si un nouveau menu est retourné (lorsque le bouton "Rejouer" est cliqué)
            menu = new_menu  
           


        
 # Appeler la méthode qui retourne la nouvelle valeur de menu

    elif game.start_party:
        # Le jeu commence, appliquer la gravité et mettre à jour l'état du jeu
        game.player.apply_gravity()
        game.update(screen)
    else:
        # Si le jeu n'a pas encore commencé, afficher les menus
        if menu == "bienvenue":
            # Afficher l'écran de bienvenue
            screen.blit(play_button, play_button_rect)
            screen.blit(banner, banner_rect)
            screen.blit(settings_button, settings_button_rect)
        elif menu == "level_select":
            # Afficher les boutons de sélection des niveaux
            afficher_boutons_niveaux(screen)
        elif menu == "reglages":
            afficher_regles(screen,police)
            screen.blit(back_button, back_button_rect)
    
    
    
    
    pygame.display.flip()
    
    if menu in ["bienvenue", "level_select"]:
        if not game.game_over_val:  # S'assurer que la partie n'est pas encore en Game Over
            game_over_played = False
        game.sound_manager.play("bienvenu",0.2)  # Musique du menu
    elif menu == "in_game":
        game.sound_manager.play("bg",0.2) # Musique du jeu
    elif menu=="game_over": 
        if not game_over_played:  
            game.sound_manager.play("tir",0.3)
            game_over_played=True
        
    
      
    # fenetre ferméez
    for event in pygame.event.get():
        #verif fermeture
        if event.type== pygame.QUIT:
            running=False
            pygame.quit()
            print("fenetrre fermée")

        # detecter si touche appuyé
        elif event.type== pygame.KEYDOWN:

            #enregistrer la ouche dans le dictionnaire
            game.pressed[event.key]=True
            
            if event.key == pygame.K_z:  # Touche Z
                if game.start_party:
                    game.player.launch_projectile()  # Lancer un projectile
                # detecter si toucvhe espace appuyée pour projectile
            elif event.key == pygame.K_SPACE and not game.start_party:
                if menu == "level_select":
                    menu = niveau_clique(event, game)
                    

            elif event.key == pygame.K_UP:  # Flèche haut
                if game.start_party:
                    game.player.jump()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key]=False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Clic détecté :", event.pos)
            if menu =="bienvenue": #si la banierre est affichée
                
                #vérifier si le joueur a appuyé sur le bouton "jouer"
                if play_button_rect.collidepoint(event.pos):
                    game.sound_manager.play("click",0.5)
                    menu = "level_select"
                elif settings_button_rect.collidepoint(event.pos):
                    menu = "reglages"
                #gerer les nievau
            elif menu == "level_select":
                menu = niveau_clique(event, game)
            elif menu == "reglages" and back_button_rect.collidepoint(event.pos):
                game.sound_manager.play("click",0.5)
                menu = "bienvenue"
    #fixer le nombre de fps a l'ohorloge
    clock.tick(FPS)




    
