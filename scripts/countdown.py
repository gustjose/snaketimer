from PyQt5.QtCore import QTimer
from scripts.support import convert_ct
from scripts.notification import alert

class Countdown:
    def __init__(self, label, timer, alert):
        self.label = label
        self.alert = alert
        self.total_seconds = 0
        self.timer = timer
        self.timer.timeout.connect(self.update_timer_label)

    def update_timer_label(self):
        self.label.setText(convert_ct(self.total_seconds))
        if self.total_seconds > 0:
            self.total_seconds -= 1
        else:
            if self.alert: alert()
            self.timer.stop()

    def start_timer(self, tempo):
        if tempo:
            self.temp1 = int(tempo)
            self.total_seconds = self.temp1
            self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self, tempo):
        self.timer.stop()
        self.total_seconds = 0
        self.label.setText(tempo)
