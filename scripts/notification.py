import pygame
import threading
import pynotifier
from pynotifier.backends import platform
import os

current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def play_alert_sound(filename):
    pygame.init()

    sound_path = os.path.join(current_dir, 'assets', 'sound', filename)
    
    # Verifica se o arquivo de som existe
    if os.path.exists(sound_path):
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)
    else:
        pygame.mixer.music.load(os.path.join(current_dir, 'assets', 'sound', 'beep.mp3'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)


def alert(filename):
    sound_thread = threading.Thread(target=play_alert_sound(filename))
    sound_thread.start()

def notify(title: str, message: str):
    c = pynotifier.NotificationClient()
    c.register_backend(platform.Backend())

    notification = pynotifier.Notification(
        title=title,
        message=message,
        icon_path=os.path.join(current_dir, 'assets', 'img', 'icon.ico'),
        duration=20,
        keep_alive=True,
        threaded=True
    )

    c.notify_all(notification)