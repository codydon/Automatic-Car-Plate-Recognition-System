from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import sys
import autoplate as main

class AutoPlate(main.Ui_MainWindow, QtWidgets.QMainWindow):
        def __init__(self):
                super(AutoPlate,self).__init__()
                #setting up the first window
                self.setupUi(self)


#APP LAUNCH
if __name__ == "__main__":
        #create an application
        app = QtWidgets.QApplication(sys.argv)
        w = AutoPlate()
        #show the window and start the app
        w.show()
        app.exec_()
