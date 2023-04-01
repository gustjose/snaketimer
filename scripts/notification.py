from tinydb import TinyDB, Query
from playsound import playsound

db = TinyDB('db.json', indent=4)
busca = Query()

def alert():
    alert_name = db.get(busca.type == 'sound')['filename']
    playsound(f'./assets/sound/{alert_name}', block=False)