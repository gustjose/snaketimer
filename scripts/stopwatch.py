from PyQt5.QtCore import QTimer
from .support import convert_ct

class Stopwatch:
    def __init__(self, label, timer):
        self.timer = timer
        self.label = label
        self.total_seconds = 0

    def update_timer_label(self):
        # Atualize o rótulo do temporizador a cada timeout do QTimer
        self.label.setText(convert_ct(self.total_seconds))
        self.total_seconds += 1
    
    def start_timer(self):
        # Comece a contagem do temporizador
        self.timer.start(1000)

    def stop_timer(self):
        # Pare a contagem do temporizador
        self.timer.stop()

    def reset_timer(self):
        # Resete a contagem do temporizador
        self.timer.stop()
        self.total_segundos = 0
        self.label.setText("00:00:00")