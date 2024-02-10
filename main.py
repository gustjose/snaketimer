import sys, shutil
from tinydb import TinyDB, Query
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo, QTimer
from assets.interface import Ui_MainWindow
import scripts, os

current_dir = os.path.dirname(os.path.abspath(__file__))

app = QtWidgets.QApplication(sys.argv)
tray_icon = QSystemTrayIcon(QIcon(os.path.join(current_dir, 'assets', 'img', 'icon.ico')), parent=None)

tray_icon.setToolTip('Snaketimer')

config_file_path = os.path.join(current_dir, 'data', 'config-user.json')

db = TinyDB(config_file_path, indent=4, ensure_ascii=False)
busca = Query()

dataUser = {
'alert': db.get(busca.type == 'alerta')['status'],
'autoplay': db.get(busca.type == 'autoplay')['status'],
'filealert': db.get(busca.type == 'sound')['filename'],
'long_break': db.get(busca.type == 'long-break')['tempo'],
'short_break': db.get(busca.type == 'short-break')['tempo'],
'pomodoro': db.get(busca.type == 'pomodoro')['tempo']
}


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_cronometro.clicked.connect(self.set_current_index_0)
        self.btn_pomodoro.clicked.connect(self.set_current_index_2)
        self.btn_regressivo.clicked.connect(self.set_current_index_3)
        self.btn_pm_config.clicked.connect(self.set_current_index_4)
        self.btn_info.clicked.connect(self.set_current_index_1)

        self.btn_pm_salvar.clicked.connect(self.alterar_config)

        self.pushButton_2.clicked.connect(self.sound_fname)

        self.label_2.setText(db.get(busca.type == 'sound')['filename'])

        self.timer = QTimer(self)
        self.stopwatch = scripts.Stopwatch(self.lb_st_contador, self.timer)

        self.btn_st_start.clicked.connect(self.stopwatch.start_timer)
        self.btn_st_stop.clicked.connect(self.stopwatch.stop_timer)
        self.btn_st_reset.clicked.connect(self.stopwatch.reset_timer)
        self.timer.timeout.connect(self.stopwatch.update_timer_label)

        self.timer_countdown = QTimer(self)
        self.countdown = scripts.Countdown(self.lb_ct_contador, self.timer_countdown, dataUser['alert'], dataUser['filealert'])

        self.btn_ct_start.clicked.connect(self.start_countdown)
        self.btn_ct_stop.clicked.connect(self.countdown.stop_timer)
        self.btn_ct_reset.clicked.connect(self.reset_countdown)
        self.btn_ct_save.clicked.connect(self.alterar_config_ct)

        self.lb_pm_contador.setText(scripts.convert_time(dataUser['pomodoro']))
        self.spinBox_pm.setValue(dataUser['pomodoro'])
        self.spinBox_lb.setValue(dataUser['long_break'])
        self.spinBox_sb.setValue(dataUser['short_break'])
        self.checkBox_alert.setChecked(dataUser['alert'])
        self.checkBox_autoplay.setChecked(dataUser['autoplay'])

        self.timer_pomodoro = QTimer(self)
        self.pomodoro = scripts.Pomodoro(self.lb_pm_contador, self.timer_pomodoro, dataUser)
        # Atualiza os valores na classe Pomodoro
        self.update_pomodoro_values()

        self.btn_pm_p1.clicked.connect(lambda: self.pomodoro.trocar_pomodoro(dataUser['pomodoro']))
        self.btn_pm_p2.clicked.connect(lambda: self.pomodoro.trocar_pomodoro(dataUser['short_break']))
        self.btn_pm_p3.clicked.connect(lambda: self.pomodoro.trocar_pomodoro(dataUser['long_break']))
        self.btn_pm_start.clicked.connect(self.start_pomodoro)
        self.pushButton.clicked.connect(self.pomodoro.stop_timer)
        self.btn_pm_reset.clicked.connect(self.pomodoro.reset_timer)

    def set_current_index_0(self):
        self.stackedWidget.setCurrentIndex(0)

    def set_current_index_1(self):
        self.stackedWidget.setCurrentIndex(1)

    def set_current_index_2(self):
        self.stackedWidget.setCurrentIndex(2)

    def set_current_index_3(self):
        self.stackedWidget.setCurrentIndex(3)

    def set_current_index_4(self):
        self.stackedWidget.setCurrentIndex(4)

    def update_pomodoro_values(self):
        # Atualiza os valores na classe Pomodoro com os valores atuais do dataUser
        self.pomodoro.update_values(dataUser)

    def sound_fname(self):
        filelocalname, _ = QFileDialog.getOpenFileName(self, 'Open file', os.path.join(current_dir, 'assets', 'sound'),"Sound files (*.mp3 *.wav)")

        if filelocalname:  # Verifica se o usuário selecionou um arquivo
            fname = QFileInfo(filelocalname).fileName()
            target_path = os.path.join(current_dir, 'assets', 'sound')

            # Verifica se o arquivo já existe no diretório de destino
            if os.path.exists(os.path.join(target_path, fname)):
                db.update({'filename': fname}, busca.type == 'sound')
                self.label_2.setText(fname)
            else:
                # Copia o arquivo para o diretório de destino
                shutil.copy(filelocalname, target_path)
                db.update({'filename': fname}, busca.type == 'sound')
                dataUser.update({'filealert': fname})
                self.label_2.setText(fname)
        else:
            QMessageBox.warning(self, "No File Selected", "No file selected.")


    def start_countdown(self):
        self.countdown.start_timer(scripts.convert_to_seconds(self.lb_ct_contador.text()))

    def reset_countdown(self):
        self.countdown.reset_timer(scripts.convert_time(int(self.spinBox_ct.text())))

    def alterar_config_ct(self):
        self.lb_ct_contador.setText(scripts.convert_time(int(self.spinBox_ct.text())))

    def start_pomodoro(self):
        self.pomodoro.start_timer(scripts.convert_to_seconds(self.lb_pm_contador.text()))

    def alterar_config(self):
        pomodoro_value = int(self.spinBox_pm.text())
        sb_value = int(self.spinBox_sb.text())
        lb_value = int(self.spinBox_lb.text())
        cb_alert_value = self.checkBox_alert.isChecked()
        cb_autoplay_value = self.checkBox_autoplay.isChecked()

        try:
            db.update({'tempo': pomodoro_value}, busca.type == 'pomodoro')
            self.lb_pm_contador.setText(scripts.convert_time(pomodoro_value))
            db.update({'tempo': sb_value}, busca.type == 'short-break')
            db.update({'tempo': lb_value}, busca.type == 'long-break')
            db.update({'status': cb_alert_value}, busca.type == 'alerta')
            db.update({'status': cb_autoplay_value}, busca.type == 'autoplay')

            self.spinBox_pm.setValue(pomodoro_value)
            self.spinBox_lb.setValue(lb_value)
            self.spinBox_sb.setValue(sb_value)

            
            dataUser.update({
                'alert': cb_alert_value,
                'autoplay': cb_autoplay_value,
                'long_break': lb_value,
                'short_break': sb_value,
                'pomodoro': pomodoro_value
            })

            self.update_pomodoro_values()
            QMessageBox.information(self, "Update data", "Saved successfully!")

        except ValueError as e:
            QMessageBox.warning(self, "Value Error", f"Invalid value: {e}")
        except Exception as erro:
            QMessageBox.warning(self, "Attention!", f"Error: {erro}")

if __name__ == "__main__":
    tray_icon.show()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
