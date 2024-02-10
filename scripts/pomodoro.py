from PyQt5.QtCore import QTimer
from scripts.support import convert_ct, convert_time
from scripts.notification import alert, notify

class Pomodoro:
    def __init__(self, label, timer, data):
        self.label = label
        self.timer = timer
        self.data = data
        self.alert = data['alert']
        self.total_seconds = 0
        self.timer.timeout.connect(self.update_timer_label)

        self.state = 'pomodoro'  # Estado inicial é pomodoro
        self.cycles_completed = 0  # Número de ciclos completos

        self.filealert = data['filealert']
        self.autoplay = data['autoplay']
        self.pomodoro_duration = data['pomodoro'] * 60
        self.short_break_duration = data['short_break'] * 60
        self.long_break_duration = data['long_break'] * 60

    def update_timer_label(self):
        self.label.setText(convert_ct(self.total_seconds))
        if self.total_seconds > 0:
            self.total_seconds -= 1
        else:
            if self.autoplay:
                if self.cycles_completed <= 4:
                    self.handle_state_transition()
                else:
                    self.cycles_completed = 0
                    self.timer.stop()
                    if self.alert: alert(self.filealert)
            else:
                self.timer.stop()
    
    def start_timer(self, tempo):
        if tempo:
            self.temp1 = int(tempo)
            self.total_seconds = self.temp1
            self.timer.start(1000)

    def handle_state_transition(self):
        if self.state == 'pomodoro' and self.cycles_completed <= 4:
            self.start_short_break()
            notify('Attention', f'{self.cycles_completed + 1}° study completed. Time for a quick break.')
        elif self.state == 'short_break' and self.cycles_completed <= 4:
            self.cycles_completed += 1
            notify('Attention', 'Hora de voltar a estudar! :)')
            self.start_pomodoro()
        else:
            notify('Congratulations!', 'You have completed the complete study cycle, time for a long rest.')
            self.start_long_break()

    def start_pomodoro(self):
        self.state = 'pomodoro'
        self.total_seconds = self.pomodoro_duration
        self.timer.start(1000)

    def start_short_break(self):
        self.state = 'short_break'
        self.total_seconds = self.short_break_duration
        self.timer.start(1000)

    def start_long_break(self):
        self.state = 'long_break'
        self.total_seconds = self.long_break_duration
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.cycles_completed = 0

        if self.autoplay:
            self.state = 'pomodoro'
            self.total_seconds = self.pomodoro_duration
            self.label.setText(convert_ct(self.total_seconds))
        else:
            if self.state == 'pomodoro':
                self.total_seconds = self.pomodoro_duration
                self.label.setText(convert_ct(self.total_seconds))
            elif self.state == 'short_break':
                self.total_seconds = self.short_break_duration
                self.label.setText(convert_ct(self.total_seconds))
            elif self.state == 'long_break':
                self.total_seconds = self.long_break_duration
                self.label.setText(convert_ct(self.total_seconds))
    
    def trocar_pomodoro(self, tempo):
        self.timer.stop()
        if tempo:
            time = convert_time(tempo)
            self.label.setText(time)
            self.temp = time

            if tempo == self.data['pomodoro']:
                self.state = 'pomodoro'
            elif tempo == self.data['short_break']:
                self.state = 'short_break'
            elif tempo == self.data['long_break']:
                self.state = 'long_break'
        
    def update_values(self, dataUser):
        self.data = dataUser
        self.alert = dataUser['alert']
        self.filealert = dataUser['filealert']
        self.autoplay = dataUser['autoplay']
        self.pomodoro_duration = dataUser['pomodoro'] * 60
        self.short_break_duration = dataUser['short_break'] * 60
        self.long_break_duration = dataUser['long_break'] * 60
