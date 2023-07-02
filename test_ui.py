# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from qtwidgets import Toggle, AnimatedToggle

class Ui_Dialog(QDialog):
    def __init__(self):
        Dialog.setObjectName("Dialog")
        Dialog.resize(717, 246)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 561, 161))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(11, 11, 121, 16))
        self.label.setObjectName("label")
        self.lineEditExperimentNumberNormalization = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditExperimentNumberNormalization.setGeometry(QtCore.QRect(150, 10, 133, 20))
        self.lineEditExperimentNumberNormalization.setObjectName("lineEditExperimentNumberNormalization")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(12, 61, 77, 16))
        self.label_2.setObjectName("label_2")
        self.lineEditConstanteNormalization = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditConstanteNormalization.setEnabled(True)
        self.lineEditConstanteNormalization.setGeometry(QtCore.QRect(95, 61, 81, 20))
        self.lineEditConstanteNormalization.setText("")
        self.lineEditConstanteNormalization.setDragEnabled(False)
        self.lineEditConstanteNormalization.setReadOnly(True)
        self.lineEditConstanteNormalization.setObjectName("lineEditConstanteNormalization")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(234, 61, 93, 16))
        self.label_3.setObjectName("label_3")
        self.lineEditAnotherExperimentNormalization = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditAnotherExperimentNormalization.setEnabled(True)
        self.lineEditAnotherExperimentNormalization.setGeometry(QtCore.QRect(333, 61, 61, 20))
        self.lineEditAnotherExperimentNormalization.setText("")
        self.lineEditAnotherExperimentNormalization.setReadOnly(True)
        self.lineEditAnotherExperimentNormalization.setObjectName("lineEditAnotherExperimentNormalization")
        self.pushButtonMultiply = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonMultiply.setGeometry(QtCore.QRect(70, 100, 75, 23))
        self.pushButtonMultiply.setObjectName("pushButtonMultiply")
        self.checkBoxConstante = Toggle(self.groupBox)
        self.checkBoxConstante.setEnabled(True)
        self.checkBoxConstante.setGeometry(QtCore.QRect(12, 38, 121, 17))
        self.checkBoxConstante.setObjectName("checkBoxConstante")
        self.checkBoxAnotherExperiment = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxAnotherExperiment.setGeometry(QtCore.QRect(234, 38, 181, 17))
        self.checkBoxAnotherExperiment.setObjectName("checkBoxAnotherExperiment")
        self.pushButtonDivision = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonDivision.setGeometry(QtCore.QRect(310, 100, 75, 23))
        self.pushButtonDivision.setObjectName("pushButtonDivision")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Experiment number"))
        self.label_2.setText(_translate("Dialog", "Constant value:"))
        self.label_3.setText(_translate("Dialog", "Experiment number"))
        self.pushButtonMultiply.setText(_translate("Dialog", "Multiply"))
        self.checkBoxConstante.setText(_translate("Dialog", "With constante"))
        self.checkBoxAnotherExperiment.setText(_translate("Dialog", "With another experiment"))
        self.pushButtonDivision.setText(_translate("Dialog", "Divide"))

### Code minimal pour afficher l'interface graphique        
if __name__.endswith('__main__'):
    
    if not QApplication.instance():
        MainApp = QApplication(sys.argv)
    else :
        MainApp = QApplication.instance()
     
mainWindow = Ui_Dialog()
mainWindow.show()

rc = MainApp.exec_()
sys.exit(rc)