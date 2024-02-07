import pygame
import threading
import yaml
import pynotifier
from pynotifier.backends import platform

# Carregando os valores do arquivo YAML
with open('data/config-user.yaml', 'r') as file:
    configUser = yaml.safe_load(file)

def play_alert_sound():
    pygame.init()
    pygame.mixer.music.load(f"./assets/sound/{configUser['Pomodoro']['filealert']}")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)

def alert():
    sound_thread = threading.Thread(target=play_alert_sound)
    sound_thread.start()

def notify(title: str, message: str):
    c = pynotifier.NotificationClient()
    c.register_backend(platform.Backend())

    notification = pynotifier.Notification(
        title=title,
        message=message,
        icon_path="assets/img/icon.ico",
        duration=20,
        keep_alive=True,
        threaded=True
    )

    c.notify_all(notification)