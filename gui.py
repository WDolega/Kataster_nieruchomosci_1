from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QGridLayout, QPlainTextEdit, QPushButton, QMessageBox, QMainWindow, \
    QApplication, QFileDialog, QDesktopWidget
import kataster


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.file_name = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.oldPos = self.pos()
        self.setStyleSheet('background-color: rgb(26, 25, 25);')
        self.textArea = QPlainTextEdit()
        self.textArea.setReadOnly(True)
        self.textArea.setStyleSheet("border: 3px solid rgb(255,215,0); background-color: rgb(26,25,25); color:white")
        # self.textArea.setStyleSheet('border: 3px solid red; background-image: url(grey.png)')
        self.textArea.verticalScrollBar().setStyleSheet('background: rgb(255,215,0); width: 20px')
        self.textArea.setFont(QtGui.QFont('Courier', 10))
        self.icon = QLabel()
        self.pix = QPixmap('house2.png')
        self.icon.setPixmap(self.pix)
        self.icon.setMaximumSize(25, 25)
        self.icon.setScaledContents(True)
        self.title = QLabel('ZSK - Walidator kodów EGiB')
        self.title.setStyleSheet("background-color: rgb(26,25,25); color:white; font: bold")
        self.title.setFont(QtGui.QFont('Courier', 13))
        self.title.setMinimumWidth(600)
        minimize_btn = QPushButton('_', self)
        end_btn = QPushButton('X', self)
        load_btn = QPushButton('Wczytaj plik', self)
        codes_btn = QPushButton('Wszystkie kody', self)
        corrects_btn = QPushButton('Poprawne kody', self)
        incorrects_btn = QPushButton('Niepoprawne kody', self)
        save_btn = QPushButton('Zapisz dane', self)
        clear_btn = QPushButton('Wyczyść', self)
        end_btn.resize(end_btn.sizeHint())
        minimize_btn.setMinimumSize(40, 20)
        end_btn.setMinimumSize(40, 20)
        load_btn.setMinimumSize(180, 35)
        codes_btn.setMinimumSize(180, 35)
        corrects_btn.setMinimumSize(180, 35)
        incorrects_btn.setMinimumSize(180, 35)
        save_btn.setMinimumSize(180, 35)
        clear_btn.setMinimumSize(180, 35)
        # load_btn.setMaximumWidth(245)
        # save_btn.setMaximumWidth(245)
        # clear_btn.setMaximumWidth(245)
        # end_btn.setMaximumWidth(245)
        minimize_btn.setFont(QtGui.QFont('Arial', 13))
        end_btn.setFont(QtGui.QFont('Arial', 13))
        codes_btn.setFont(QtGui.QFont('Courier', 13))
        incorrects_btn.setFont(QtGui.QFont('Courier', 13))
        load_btn.setFont(QtGui.QFont('Courier', 13))
        save_btn.setFont(QtGui.QFont('Courier', 13))
        clear_btn.setFont(QtGui.QFont('Courier', 13))
        corrects_btn.setFont(QtGui.QFont('Courier', 13))
        minimize_btn.setStyleSheet('QPushButton{color:white; font:bold}'
                                   'QPushButton:pressed{background-color: rgb(53, 53, 54)}'
                                   'QPushButton:hover{background-color: rgb(38,38,38)}')
        end_btn.setStyleSheet('QPushButton{color:white; font:bold}'
                                   'QPushButton:pressed{background-color: rgb(212, 55, 73)}'
                                   'QPushButton:hover{background-color: rgb(212, 55, 73)}')
        style = 'QPushButton{border:2px solid rgb(255,215,0); background-color:rgb(26,25,25);color:white; font:bold}'\
                'QPushButton:pressed{background-color: rgb(53, 53, 54)}' \
                'QPushButton:hover{background-color: rgb(38,38,38)}'
        load_btn.setStyleSheet(style)
        codes_btn.setStyleSheet(style)
        corrects_btn.setStyleSheet(style)
        incorrects_btn.setStyleSheet(style)
        save_btn.setStyleSheet(style)
        clear_btn.setStyleSheet(style)
        layout = QGridLayout()
        layout.setVerticalSpacing(20)
        layout.addWidget(self.icon, 0, 0, 1, 1)
        layout.addWidget(self.title, 0, 1, 1, 9)
        layout.addWidget(minimize_btn, 0, 10, 1, 1)
        layout.addWidget(end_btn, 0, 11, 1, 1)
        layout.addWidget(load_btn, 1, 8, 1, 4)
        layout.addWidget(codes_btn, 2, 8, 1, 4)
        layout.addWidget(corrects_btn, 3, 8, 1, 4)
        layout.addWidget(incorrects_btn, 4, 8, 1, 4)
        layout.addWidget(save_btn, 5, 8, 1, 4)
        layout.addWidget(clear_btn, 6, 8, 1, 4)
        layout.addWidget(self.textArea, 1, 0, 7, 8)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        minimize_btn.clicked.connect(self.minimize_window)
        load_btn.clicked.connect(self.open_file)
        codes_btn.clicked.connect(self.set_text)
        corrects_btn.clicked.connect(self.set_text)
        incorrects_btn.clicked.connect(self.set_text)
        save_btn.clicked.connect(self.save_file)
        clear_btn.clicked.connect(self.clear_wind)
        end_btn.clicked.connect(self.end)
        self.setGeometry(300, 100, 700, 900)
        # self.setFont(myFont)
        self.setCentralWidget(widget)
        self.setWindowIcon(QIcon('pw.png'))
        self.setWindowTitle('ZSK - Walidator kodów EGiB')
        self.show()

    def minimize_window(self):
        self.showMinimized()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def msg_box(self, text, info, msg_type):
        msg = QMessageBox(self)
        msg.setWindowTitle('Komunikat')
        msg.setStyleSheet("QMessageBox{background-color: rgb(26,25,25); color: white; font: bold; width: 500px;}"
                          "QLabel{background:transparent; color:#fff; width: 300px}"
                          "QPushButton{border:1.5px solid rgb(255,215,0);background-color:rgb(26,25,25);color: white;"
                          " width: 100px; height: 25px; font:bold; }")
        msg.setText(f'    {text}   \n\n    {info}')
        if msg_type == 'crit-error':
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Critical)
        if msg_type == 'error':
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Warning)
        if msg_type == 'info':
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setIcon(QMessageBox.Information)
        if msg_type == 'question':
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setIcon(QMessageBox.Question)
        msg.show()
        return msg

    def end(self):
        self.close()

    def open_file(self):
        try:
            file_dialog = QFileDialog()
            path = str(file_dialog.getOpenFileName(filter="Text files (*.txt)")[0])
        except (FileNotFoundError, OSError):
            pass
        else:
            self.file_name = path

    def set_text(self):
        send = self.sender()
        try:
            # pre_codes = kataster.open_file(self.file_name)
            codes, corrects, incorrects = kataster.open_file3(self.file_name)
        except (NameError, TypeError, FileNotFoundError):
            self.msg_box('Błąd!', 'Wczytaj plik', 'error')
        except (UnicodeDecodeError, ValueError):
            self.msg_box('Błąd!', 'Wczytaj poprawny plik', 'crit-error')
            # QMessageBox.critical(self, 'Błąd!', 'Wczytaj poprawny plik!', QMessageBox.Ok, QMessageBox.Ok)
        else:
            # correct, incorrect = kataster.validator(pre_codes)
            if send.text() == 'Wszystkie kody':
                self.textArea.clear()
                for code in codes:
                    self.textArea.appendPlainText(str(code))
                # self.textArea.appendPlainText('Liczba poprawnych kodów: ' + str(len(correct)))
            if send.text() == 'Poprawne kody':
                self.textArea.clear()
                for code in corrects:
                    self.textArea.appendPlainText(str(code))
                self.textArea.appendPlainText('Liczba poprawnych kodów: ' + str(len(corrects)))
            if send.text() == 'Niepoprawne kody':
                self.textArea.clear()
                for code in incorrects:
                    self.textArea.appendPlainText(str(code))
                self.textArea.appendPlainText('Liczba niepoprawnych kodów: ' + str(len(incorrects)))

    def closeEvent(self, event):
        odp = self.msg_box('\n Czy na pewno chcesz zamknąć aplikację?', '', 'question')
        odp = odp.exec()
        if odp == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clear_wind(self):
        self.textArea.clear()

    def save_file(self):
        if self.textArea.toPlainText():
            try:
                name = QFileDialog.getSaveFileName(self, '/', '*.txt')[0]
                save = open(name, 'w')
            except FileNotFoundError:
                pass
            else:
                save.writelines(self.textArea.toPlainText())
                save.close()
                self.msg_box('Dane zostały poprawnie zapisane!', '', 'info')
        else:
            self.msg_box('Brak informacji do zapisu!', '', 'error')
