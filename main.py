import sys, shutil
from tinydb import TinyDB, Query
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
from assets.interface import Ui_MainWindow
from time import sleep
from threading import Thread
import scripts

app = QtWidgets.QApplication(sys.argv)
tray_icon = QSystemTrayIcon(QIcon('assets\img\icon.ico'), parent=None)
tray_icon.setToolTip('Snaketimer')

db = TinyDB('db.json', indent=4, ensure_ascii=False)
busca = Query()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_cronometro.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_pomodoro.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_regressivo.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.btn_pm_config.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.btn_info.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.btn_st_start.clicked.connect(lambda: Thread(target=start_timer, args=(self.lb_st_contador.text(),)).start())
        self.btn_st_stop.clicked.connect(lambda: stop_timer())
        self.btn_st_reset.clicked.connect(lambda: reset_timer())
        self.btn_pm_salvar.clicked.connect(lambda: alterar_config())

        self.btn_pm_start.clicked.connect(lambda: Thread(target=start_pm, args=(self.lb_pm_contador.text(),)).start())
        self.pushButton.clicked.connect(lambda: stop_pm())
        self.btn_pm_reset.clicked.connect(lambda: reset_pm())
        self.btn_pm_p1.clicked.connect(lambda: btn_pm_pomodoro())
        self.btn_pm_p2.clicked.connect(lambda: btn_pm_shortbreak())
        self.btn_pm_p3.clicked.connect(lambda: btn_pm_longbreak())
        self.btn_pm_p3.clicked.connect(lambda: btn_pm_longbreak())
        self.pushButton_2.clicked.connect(lambda: sound_fname())

        self.btn_ct_save.clicked.connect(lambda: alterar_config_ct())
        self.btn_ct_start.clicked.connect(lambda: Thread(target=start_ct, args=(self.lb_ct_contador.text(),)).start())
        self.btn_ct_stop.clicked.connect(lambda: stop_ct())
        self.btn_ct_reset.clicked.connect(lambda: reset_ct())

        self.label_2.setText(db.get(busca.type == 'sound')['filename'])
        def sound_fname():
            filelocalname = QFileDialog.getOpenFileName(self, 'Open file','./assets/sound',"Sound files (*.mp3 *.wav)")
            fname = QFileInfo(filelocalname[0]).fileName()

            shutil.copy(filelocalname[0], './assets/sound')
            db.update({'filename': fname}, busca.type == 'sound')
            
            self.label_2.setText(fname)

    
###################### STOPWATCH #########################################################################################

        iniciador = False

        def reset_timer():
            global iniciador
            iniciador = False
            sleep(0.8)
            self.lb_st_contador.setText("00:00:00")


        def stop_timer():

            global iniciador
            iniciador = False
            self.btn_st_start.setEnabled(True)

        def start_timer(contador):

            reset_pm()
            reset_ct1()

            self.btn_st_start.setEnabled(False)

            global iniciador
            iniciador = True
            h,m,s = map(int, contador.split(":"))
            total_segundos = h * 3600 + m * 60 + s

            while iniciador is True:
                total_segundos += 1
                sleep(1)
                self.lb_st_contador.setText(scripts.convert_ct(total_segundos))
            else:
                self.lb_st_contador.setText(scripts.convert_ct(total_segundos - 1))
                self.btn_st_start.setEnabled(True)


###################### POMODORO #########################################################################################

        global ativo_timer
        global n_repeticao

        self.lb_pm_contador.setText(scripts.convert_time(db.get(busca.type == 'pomodoro')['tempo']))
        self.spinBox_pm.setValue(db.get(busca.type == 'pomodoro')['tempo'])
        self.spinBox_lb.setValue(db.get(busca.type == 'long-break')['tempo'])
        self.spinBox_sb.setValue(db.get(busca.type == 'short-break')['tempo'])

        self.checkBox_alert.setChecked(db.get(busca.type == 'alerta')['status'])
        self.checkBox_autoplay.setChecked(db.get(busca.type == 'autoplay')['status'])

        ativo_timer = 0
        n_repeticao = 0

        #CONFIG
        def alterar_config():
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

                self.spinBox_pm.setValue(db.get(busca.type == 'pomodoro')['tempo'])
                self.spinBox_lb.setValue(db.get(busca.type == 'long-break')['tempo'])
                self.spinBox_sb.setValue(db.get(busca.type == 'short-break')['tempo'])

                QMessageBox.information(self, "Update data", "Saved successfully.")
            except Exception as erro:
                QMessageBox.warning(self, "Attention!", f"Erro: {erro.__cause__}")
        
        #TIMER
        def stop_pm():

            global iniciador2
            iniciador2 = False
            self.btn_pm_start.setEnabled(True)
        
        def reset_pm():
            global iniciador2
            global ativo_timer

            iniciador2 = False
            sleep(1)

            if ativo_timer != 0:
                self.lb_pm_contador.setText(scripts.convert_time(ativo_timer))
            else:
                self.lb_pm_contador.setText(scripts.convert_time(db.get(busca.type == 'pomodoro')['tempo']))
        
        def start_pm(contador):

            global n_repeticao

            reset_timer()
            reset_ct1()

            self.btn_pm_start.setEnabled(False)

            global iniciador2
            iniciador2 = True
            h,m,s = map(int, contador.split(":"))
            total_segundos = h * 3600 + m * 60 + s

            while iniciador2 is True:
                if total_segundos > 0:
                    total_segundos -= 1
                    sleep(1)
                    self.lb_pm_contador.setText(scripts.convert_ct(total_segundos))
                else:
                    if db.get(busca.type == 'autoplay')['status'] is True:
                        if n_repeticao <= 3:
                            n_repeticao += 1
                            Thread(target=sb_start).start()
                        else:
                            Thread(target=lb_start).start()
                        break
                    else:
                        if db.get(busca.type == 'alerta')['status'] is True:
                            scripts.alert()
                            tray_icon.showMessage('Pomodoro', 'The time is over!', QSystemTrayIcon.Information, 5000)
                            self.btn_pm_start.setEnabled(True)
                            break
                    self.btn_pm_start.setEnabled(True)
                    break
            else:
                self.lb_pm_contador.setText(scripts.convert_ct(total_segundos + 1))
                self.btn_pm_start.setEnabled(True)

        def sb_start():

            tempo_sb = db.get(busca.type == 'short-break')['tempo']
            text_pm = scripts.convert_time(db.get(busca.type == 'pomodoro')['tempo'])
            text_sb = scripts.convert_time(tempo_sb)
            self.lb_pm_contador.setText(text_sb)
            self.btn_pm_start.setEnabled(False)

            global iniciador2
            iniciador2 = True

            h,m,s = map(int, text_sb.split(":"))
            total_segundos = h * 3600 + m * 60 + s

            while iniciador2 is True:
                if total_segundos > 0:
                    total_segundos -= 1
                    sleep(1)
                    self.lb_pm_contador.setText(scripts.convert_ct(total_segundos))
                else:
                    break
            else:
                self.lb_pm_contador.setText(scripts.convert_ct(total_segundos + 1))
                self.btn_pm_start.setEnabled(True)
            Thread(target=start_pm, args=(text_pm,)).start()

        def lb_start():
            tempo_sb = db.get(busca.type == 'long-break')['tempo']
            text_pm = scripts.convert_time(db.get(busca.type == 'pomodoro')['tempo'])
            text_sb = scripts.convert_time(tempo_sb)
            self.lb_pm_contador.setText(text_sb)
            self.btn_pm_start.setEnabled(False)

            global iniciador2, n_repeticao
            iniciador2 = True

            h,m,s = map(int, text_sb.split(":"))
            total_segundos = h * 3600 + m * 60 + s

            while iniciador2 is True:
                if total_segundos > 0:
                    total_segundos -= 1
                    sleep(1)
                    self.lb_pm_contador.setText(scripts.convert_ct(total_segundos))
                else:
                    n_repeticao = 0
                    break
            
            self.btn_pm_start.setEnabled(True)
            if db.get(busca.type == 'alerta')['status'] is True:
                scripts.alert()
                tray_icon.showMessage('Pomodoro', 'The time is over!', QSystemTrayIcon.Information, 5000)

        def btn_pm_pomodoro():

            global ativo_timer
            
            stop_pm()
            sleep(0.65)
            self.lb_pm_contador.setText(scripts.convert_time(db.get(busca.type == 'pomodoro')['tempo']))
            ativo_timer = db.get(busca.type == 'pomodoro')['tempo']
            self.spinBox_pm.setValue(db.get(busca.type == 'pomodoro')['tempo'])

        def btn_pm_shortbreak():

            global ativo_timer

            stop_pm()
            sleep(0.65)
            self.lb_pm_contador.setText(scripts.convert_time(db.get(busca.type == 'short-break')['tempo']))
            ativo_timer = db.get(busca.type == 'short-break')['tempo']
            self.spinBox_sb.setValue(db.get(busca.type == 'short-break')['tempo'])
        
        def btn_pm_longbreak():

            global ativo_timer

            stop_pm()
            sleep(0.65)
            self.lb_pm_contador.setText(scripts.convert_time(db.get(busca.type == 'long-break')['tempo']))
            ativo_timer = db.get(busca.type == 'long-break')['tempo']
            self.spinBox_lb.setValue(db.get(busca.type == 'long-break')['tempo'])

###################### COUNTDOWN #########################################################################################

        global ativo_ct
        ativo_ct = 0

        #CONFIG
        def alterar_config_ct():
            global iniciador3
            iniciador3 = False
            sleep(0.8)
            self.lb_ct_contador.setText(scripts.convert_time(int(self.spinBox_ct.text())))

        def reset_ct1():
            global iniciador3
            iniciador3 = False
            self.btn_ct_start.setEnabled(True)
        
        def reset_ct():
            global iniciador3
            iniciador3 = False
            sleep(0.8)
            self.lb_ct_contador.setText(scripts.convert_time(int(self.spinBox_ct.text())))
            self.btn_ct_start.setEnabled(True)

        def stop_ct():

            global iniciador3
            iniciador3 = False
            self.btn_ct_start.setEnabled(True)
        
        def start_ct(contador):

            reset_timer()
            reset_pm()

            self.btn_ct_start.setEnabled(False)

            global iniciador3
            iniciador3 = True
            h,m,s = map(int, contador.split(":"))
            total_segundos = h * 3600 + m * 60 + s

            while iniciador3 is True:
                if total_segundos > 0:
                    total_segundos -= 1
                    sleep(1)
                    self.lb_ct_contador.setText(scripts.convert_ct(total_segundos))
                else:
                    if db.get(busca.type == 'alerta')['status'] is True:
                        scripts.alert()
                        tray_icon.showMessage('Countdown', 'The time is over!', QSystemTrayIcon.Information, 5000)
                        break
                    break
            else:
                self.lb_ct_contador.setText(scripts.convert_ct(total_segundos + 1))
                self.btn_ct_start.setEnabled(True)
        

tray_icon.show()
window = MainWindow()
window.show()
app.exec()