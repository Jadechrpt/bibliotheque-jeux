import pygame 
pygame.mixer.init()
class SoundManager: 
    def __init__(self): 
        self.sounds = {
            'click': pygame.mixer.Sound("PygameAssets-main/sounds/click.ogg"),
            
            'meteorite': pygame.mixer.Sound("PygameAssets-main/sounds/meteorite.ogg"),
            'tir': pygame.mixer.Sound("PygameAssets-main/sounds/tir.ogg"),
            "chat":pygame.mixer.Sound("PygameAssets-main/sounds/chat.ogg"),
            'game_over': pygame.mixer.Sound("PygameAssets-main/sounds/game_over.ogg"),
            "alienbark": pygame.mixer.Sound("PygameAssets-main/sounds/alienbark.ogg"),
            "alienbark": pygame.mixer.Sound("PygameAssets-main/sounds/alienbark.ogg"),
            "projectile": pygame.mixer.Sound("PygameAssets-main/sounds/projectile.ogg"),
            "degat": pygame.mixer.Sound("PygameAssets-main/sounds/degat.ogg"),
            "turtle": pygame.mixer.Sound("PygameAssets-main/sounds/turtle.ogg"),

        }
        self.sound_continue={
            "bg": pygame.mixer.Sound("PygameAssets-main/sounds/bg.ogg"),
            "bienvenu": pygame.mixer.Sound("PygameAssets-main/sounds/bienvenu.ogg"),
            
        }
        self.current_bg = None 
        self.game_over_played=False
     #methode pour jouer la musique choisi   
    def play(self, name, volume=1.0):
        
        ajustement_volume = max(0.0, min(volume * 0.3, 1.0))  # Réduction supplémentaire
        self.volume_reglage(name, ajustement_volume)  # Appliquer le volume ajusté
        if name in self.sounds:
            self.sounds[name].play()
        elif name in self.sound_continue:
            if self.current_bg == name:  
                return
            self.stop_all()  # S'assure qu'on arrête la précédente avant
            self.current_bg = name
          
            self.sound_continue[name].play(loops=-1)  # Musique en boucle
    
    def stop_all(self):    
        """Arrête tous les sons de fond."""
        for sound in self.sound_continue.values():
            sound.stop()
        self.current_bg = None
        self.game_over_played = False  
    
    #regle le volume ne fonction du son chosii entre 0.0 et 1.0
    def volume_reglage(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        elif name in self.sound_continue:
            self.sound_continue[name].set_volume(volume)