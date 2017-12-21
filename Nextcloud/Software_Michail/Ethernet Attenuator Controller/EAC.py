#This Program is a controller for the JDSU Attenuator via computer using the Prologix ETHERNET GPIB#


import Attenuator  #script to communitcate with the Attenuator#

#Things that need to be imported for the GUI#
import sys
from PySide.QtGui import *
from ui_mainWindow import Ui_MainWindow
from ui_connect import Ui_Dialog


print("Start up..")
d = Attenuator.Attenuator()

#Main window class#
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ip = connect.textEdit.toPlainText()
        d.open(ip)
        self.setupUi(self)
        self.textEdit.clear()
        self.textEdit.insertPlainText(ip)
        self.assignWidgets()
        self.refresh()

    def assignWidgets(self):
        self.checkBox.stateChanged.connect(self.block)
        self.spinBox.valueChanged.connect(self.changeWVL)
        self.doubleSpinBox.valueChanged.connect(self.changeATT)
        self.pushButton.clicked.connect(self.Apply)

    def block(self):
        if self.checkBox.isChecked() == True:
            d.write('D 1')
        else:
            d.write('D 0')

    def changeATT(self):
        d.setAtt(self.doubleSpinBox.value())

    def changeWVL(self):
        d.setWVL(self.spinBox.value())
        self.doubleSpinBox.setValue(d.getAtt())

    def refresh(self):
        att = d.getAtt()
        wvl = d.getWVL()
        minwvl, maxwvl = d.getWVLbound()
        D = d.ask('D?')
        print('%f %f %f %f %s' % (att, wvl, minwvl, maxwvl, D))

        self.spinBox.setMinimum(minwvl)
        self.spinBox.setMaximum(maxwvl)
        self.spinBox.setValue(wvl)
        if D == '1':
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)

    def Apply(self):
        d.open(self.textEdit.toPlainText())
        self.refresh()

#IP window class#
class Connect(QDialog, Ui_Dialog):
    def __init__(self):
        super(Connect, self).__init__()
        self.setupUi(self)
        self.assignWidgets()

    def assignWidgets(self):
        self.pushButton.clicked.connect(start)

#Close IP window and open main program#
def start():
    global mainWin
    print("Connecting")
    mainWin = MainWindow()
    connect.close()
    mainWin.show()
    print("Connected !")

#Setup GUI and open IP window#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    connect = Connect()
    connect.show()
    print("Started up!")
    ret = app.exec_()
    sys.exit(ret)