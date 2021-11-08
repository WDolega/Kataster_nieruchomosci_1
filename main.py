import sys
from PyQt5.QtWidgets import QApplication
import gui
import kataster


if __name__ == '__main__':
    # file = 'D:\projekty\python\kataster_1\Kontury_eksport_dz.txt'
    # kataster.validator(kataster.open_file(file))
    # kataster.open_file3('D:\projekty\python\kataster_1\Kontury_eksport_dz.txt')
    app = QApplication(sys.argv)
    w = gui.MainWindow()
    app.exec_()