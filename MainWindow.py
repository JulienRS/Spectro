#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys
import os
import time

# Lib for communication with arduino/esp #####################################
import serial   
##############################################################################

#### Lib for USB1808X ADC communication ######################################
from builtins import *  # @UnusedWildImport

from ctypes import cast, POINTER, c_ushort

from mcculw import ul
from mcculw.enums import (InterfaceType, ScanOptions, Status, FunctionType, ChannelType,
                          ULRange, DigitalPortType, TriggerSensitivity,
                          TriggerEvent, TriggerSource)
from mcculw.ul import ULError
from mcculw.device_info import DaqDeviceInfo

##############################################################################

from PyQt5 import uic, QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pickle as pickle
import numpy as np

### Import pyqtgraph for displaying graph #####################################
import pyqtgraph as pg

### Import external built-in function #########################################
import sequenceFunction
import toolbarFunction
import tableExperimentFunction
import calculationFunction
import microcontrollerFunction
import ADCScanFunction_analog

class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
    
        ### Conversion from .ui (from QtDesigner) to .py  
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('MainWindow.ui', self) # Load the .ui file
        
        
        #### Opening port of ESP 32 for acquisition control ############################
        
        self.mc = serial.Serial(port='COM10', baudrate=115200, timeout=0.1)
        time.sleep(2)
        
        ################################################################################
        
        #### Opening USB1808X ADC for Analog to Digital Conversion #####################
        # ul.ignore_instacal()
        # dev_id_list = None
        # self.board_num = 0
        # devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        # if not devices:
        #     raise Exception('Error: No DAQ devices found')
    
        # print('Found', len(devices), 'DAQ device(s):')
        # for device in devices:
        #     print('  ', device.product_name, ' (', device.unique_id, ') - ',
        #           'Device ID = ', device.product_id, sep='')
    
        # device = devices[0]
        # if dev_id_list:
        #     device = next((device for device in devices
        #                    if device.product_id in dev_id_list), None)
        #     if not device:
        #         err_str = 'Error: No DAQ device found in device ID list: '
        #         err_str += ','.join(str(dev_id) for dev_id in dev_id_list)
        #         raise Exception(err_str)
    
        # # Add the first DAQ device to the UL with the specified board number
        # ul.create_daq_device(self.board_num, device)


        ################################################################################
        self.loadedUserParameter = None
        self.loaded_filename = None
        
        ################################################################################ 
        ### Action link to toolbar menu
        self.actionLoad.triggered.connect(self.onPushActionLoadExperiment)
        self.actionChooseUserParameter.triggered.connect(self.onPushActionLoadUserParameter)
        self.actionQuit.triggered.connect(self.onPushActionQuitWindow)
        

        ### Connection of differents clickable events from main window ####################
        
        ### Buttons linked to Experiment Control ##########################################
        self.pushButtonSingleShot.clicked.connect(self.onPushButtonSingleShot)
        self.pushButtonRepeat10Hz.clicked.connect(self.onPushButtonRepeat10Hz)
        self.pushButtonShutterClosed.clicked.connect(self.onPushButtonShutterClosed)
        self.pushButtonLaserControl.clicked.connect(self.onPushButtonLaserControl)
        self.pushButtonSequence.clicked.connect(self.onPushButtonSequence)
        self.pushButtonStartAcquisition.clicked.connect(self.onPushButtonStartAcquisition)
        ##################################################################################
        
        ### Boutons linked to Calculation Tools ######################################
        self.pushButtonNormalization.clicked.connect(self.onPushButtonNormalization)
        self.pushButtonClearPlot.clicked.connect(self.onPushButtonClearPlot)
        self.pushButtonDiffOrAdd.clicked.connect(self.onPushButtonDiffOrAdd)
        self.pushButtonPivotal.clicked.connect(self.onPushButtonPivotal)
        ###################################################################################
        
                
        ### Boutons link to QTableWidget des donnees #####################################
        self.tableWidgetExperiment.cellClicked.connect(self.plotExperiment)
        self.tableWidgetExperiment.cellClicked.connect(self.displayMetaData)
        
        self.tableWidgetCalculation.cellClicked.connect(self.plotExperiment)
        self.tableWidgetCalculation.cellClicked.connect(self.displayMetaData)
######################################################################################################################
######################################################################################################################        
        # self.pushButtonRepeat10Hz.toggle()

################ Action linked to toolbar menu #######################################################################
######################################################################################################################        
    def onPushActionLoadExperiment(self):
        toolbarFunction.actionLoadExperiment(self)
        
        with open(self.loaded_filename,'rb') as file:
            data = pickle.load(file)
        
        tableExperimentFunction.createTable(self,data)
        
######################################################################################################################
 
    def onPushActionLoadUserParameter(self):
        toolbarFunction.actionLoadUserParameter(self)
######################################################################################################################

    def onPushActionQuitWindow(self):
        self.mc.close()
        self.close()
######################################################################################################################
######################################################################################################################        


################ Action linked to Experiment Control #######################################################################
######################################################################################################################        
    def onPushButtonSingleShot(self):   
        self.mc.write('#'.encode())
        self.mc.write('\n'.encode()) 
######################################################################################################################
        
    def onPushButtonRepeat10Hz(self): 
        if self.pushButtonRepeat10Hz.isChecked():
                self.mc.write('@'.encode())
                self.mc.write('\n'.encode())
        else :
            for i in range(1000):
                if self.pushButtonRepeat10Hz.isChecked() == False:
                    break
                else:
                    print('ok1')



######################################################################################################################
    def onPushButtonShutterClosed(self):   
        self.close() 
        
######################################################################################################################    
    def onPushButtonLaserControl(self):   
        self.mc.close()
        self.close()
        
######################################################################################################################
    @QtCore.pyqtSlot()        
    def onPushButtonSequence(self):
        if self.loadedUserParameter == None:
            self.errorLoadedUsernameWindow = PopUpUserParameterNotLoad()
            self.errorLoadedUsernameWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.errorLoadedUsernameWindow.show()
        if self.loaded_filename == None:
            self.errorLoadedExperimentWindow = PopUpExperimentNotLoad()
            self.errorLoadedExperimentWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.errorLoadedExperimentWindow.show()               
        else:   
            self.sequenceWindow = PopUpSequence(self.loadedUserParameter)
            self.sequenceWindow.fermeturePopUpSequence.connect(self.loadSequence)
            self.sequenceWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.sequenceWindow.show() 
              
    @QtCore.pyqtSlot(dict)    
    def loadSequence(self, dict_sequence):
        self.sequenceToUse = dict_sequence.get("Sequence")
        self.numberOfAcquisition = dict_sequence.get("Number of acquisition")
        self.timeBetweenAcquisition = dict_sequence.get("Time between acquisition")
        self.fullSeq, self.bracketMissing = sequenceFunction.ReadSequence(self.sequenceToUse)
        
        if self.bracketMissing == True:
            self.errorBracketMissingWindow = PopUpBracketError()
            self.errorBracketMissingWindow.setWindowModality(QtCore.Qt.ApplicationModal)
            self.errorBracketMissingWindow.show()
        else:
            print('ok2')
    
######################################################################################################################
    def onPushButtonStartAcquisition(self):   ### Declenche une mesure avec la sequence chargee
           
        self.typeSeq = microcontrollerFunction.sendSequenceToMC(self.fullSeq, self.mc, self.numberOfAcquisition, self.timeBetweenAcquisition)
        ADCScanFunction_analog.ADCScanFunction(self.mc) 
######################################################################################################################
######################################################################################################################
        
    def onPushButtonClearPlot(self):   ### Efface les graph affiches
        self.displayGraph.clear()

        
######################################################################################################################
######################################################################################################################        
    @QtCore.pyqtSlot()    
    def onPushButtonCreateUser(self):
        self.createUsernameWindow = PopUpUsername()
        self.createUsernameWindow.fermeturePopUpUsername.connect(self.createUsername)
        self.createUsernameWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.createUsernameWindow.show()          
        
    @QtCore.pyqtSlot(str)
    def createUsername(self,usernameCreated):
        sequence = []
        sequence.append({"Name" : "Sequence Baseline 100ms", "Sequence" : "10(100msD)"})
        sequence.append({"Name" : "Sequence Flash laser", "Sequence" : "4(100msD)A140usC500usD1msD2msD5msD10msD"})
        
        with open('sequence_' + usernameCreated + '.bin', 'wb') as file_temp:
            pickle.dump(sequence, file_temp, pickle.HIGHEST_PROTOCOL)
        
        self.loadedUserParameter = usernameCreated
        self.lineEditDisplayCurrentUser.setText(self.loadedUserParameter)
        self.lineEditDisplayCurrentUser.setReadOnly(True)
######################################################################################################################
######################################################################################################################


######################################################################################################################
#################### Normalization part ############################################################################## 
    @QtCore.pyqtSlot()
    def onPushButtonNormalization(self):
        self.normalizationWindow = PopUpNormalization()
        self.normalizationWindow.fermeturePopUpNormalization.connect(self.normalization)
        self.normalizationWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.normalizationWindow.show()     
        
    @QtCore.pyqtSlot(dict)    
    def normalization(self, dictNormalization):
        self.calc = calculationFunction.normalization(self, dictNormalization)
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
        
        data.append(self.calc)
        
        with open(self.loaded_filename, 'wb') as file_temp:
            pickle.dump(data, file_temp, pickle.HIGHEST_PROTOCOL)       
        
        tableExperimentFunction.createTable(self,data)
######################################################################################################################
######################################################################################################################


######################################################################################################################
#################### Diff or Add part ################################################################################
    @QtCore.pyqtSlot()        
    def onPushButtonDiffOrAdd(self):   ### Procedure pour effectuer une difference entre deux courbes ou entre une courbe et une valeur fixe
        self.diffOrAddWindow = PopUpDiffOrAdd()
        # In case of "fermetureDifference()" received from self.PopUpDifference => execute difference 
        self.diffOrAddWindow.fermeturePopUpDiffOrAdd.connect(self.diffOrAdd)
        self.diffOrAddWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.diffOrAddWindow.show()   
        
    @QtCore.pyqtSlot(dict)    
    def diffOrAdd(self, dictDiffOrAdd):
        self.calc = calculationFunction.diffOrAdd(self, dictDiffOrAdd)
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
        
        data.append(self.calc)
        
        with open(self.loaded_filename, 'wb') as file_temp:
            pickle.dump(data, file_temp, pickle.HIGHEST_PROTOCOL)       
        
        tableExperimentFunction.createTable(self,data)
######################################################################################################################
######################################################################################################################
        
        
######################################################################################################################
#################### Pivotal part ####################################################################################        
    @QtCore.pyqtSlot()        
    def onPushButtonPivotal(self):   ### Procedure to rotate a curve between two points (linear regression to have both points at zero)
        self.pivotalWindow = PopUpPivotal()
        # In case of "fermeturePivotal()" received from self.PopUpPivotal => execute pivotal 
        self.pivotalWindow.fermeturePopUpPivotal.connect(self.pivotal)
        self.pivotalWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pivotalWindow.show()   
                   
    @QtCore.pyqtSlot(list)    
    def pivotal(self, list_piv):
        self.calc = calculationFunction.pivotal(self, list_piv)
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
        
        data.append(self.calc)
        
        with open(self.loaded_filename, 'wb') as file_temp:
            pickle.dump(data, file_temp, pickle.HIGHEST_PROTOCOL)       
        
        tableExperimentFunction.createTable(self,data)
######################################################################################################################
######################################################################################################################

######################################################################################################################
######################################################################################################################
    def displayMetaData(self):
        # Determine which table (Experiment or Calculation) is sending an event
        sender = self.sender().objectName()
        
        if sender == 'tableWidgetExperiment':
            selected_experiment = self.tableWidgetExperiment.selectedItems()   # Number of the selected experiment
            selected_experiment_convert = selected_experiment[0].text()
            senderType = 'Experiment'
            
        else:
            selected_experiment = self.tableWidgetCalculation.selectedItems()   # Number of the selected experiment
            selected_experiment_convert = selected_experiment[0].text()
            senderType = 'Calculation'

        with open(self.loaded_filename,'rb') as file:
            data = pickle.load(file)
            
        # Searching selectionned data
        i = 0
        while i <= len(data):
            if data[i].get('type') == senderType and data[i].get('number') == selected_experiment_convert:
                wl = data[i].get('wavelength')
                comment = data[i].get('comment')
                break
            else:
                i = i+1
        
        self.textEditDisplayMetadata.setPlainText(comment+'\n'+str(wl))
######################################################################################################################
######################################################################################################################       

######################################################################################################################
######################################################################################################################        
    def plotExperiment(self):
        # Determine which table (Experiment or Calculation) is sending an event
        sender = self.sender().objectName()
        
        if sender == 'tableWidgetExperiment':
            selected_experiment = self.tableWidgetExperiment.selectedItems()   # Number of the selected experiment
            selected_experiment_convert = selected_experiment[0].text()
            senderType = 'Experiment'
            
        else:
            selected_experiment = self.tableWidgetCalculation.selectedItems()   # Number of the selected experiment
            selected_experiment_convert = selected_experiment[0].text()
            senderType = 'Calculation'
        
        # Open data file
        with open(self.loaded_filename,'rb') as file:
            data = pickle.load(file)
        
        # Searching selectionned data
        i = 0 
        while i <= len(data):
            if data[i].get('type') == senderType and data[i].get('number') == selected_experiment_convert:
                x = data[i].get('time')
                y = data[i].get('data')
                break
            else:
                i = i+1
        
        C = pg.hsvColor(time.time()/5%1, alpha=.5)
        pen = pg.mkPen(color = C, width = 2)
    
        self.displayGraph.plot(x, y, pen = pen, symbol = 'x', symbolPen = pen, clear = False)
######################################################################################################################
######################################################################################################################  
    
    
######################################################################################################################
################ Definition of differents classes ####################################################################

######################################################################################################################
################ Pivotal Class #######################################################################################
class PopUpPivotal(QDialog):
    
    fermeturePopUpPivotal = QtCore.pyqtSignal(list)
    
    def __init__(self, parent = MainWindow):
            super(PopUpPivotal, self).__init__() # Call the inherited classes __init__ method
            uic.loadUi('PopUpPivotal.ui', self) # Load the .ui file   

            self.pushButtonPivotal.clicked.connect(self.onPushButtonPivotal) 
            
    @QtCore.pyqtSlot()        
    def onPushButtonPivotal(self):
        self.experimentList = []
        
        self.experimentNumber = self.lineEditExperimentNumber.text()
        self.experimentNumber = int(self.experimentNumber)
        
        self.firstPoint = self.lineEditFirstPoint.text()
        self.firstPoint = int(self.firstPoint)
        
        self.secondPoint = self.lineEditSecondPoint.text()
        self.secondPoint = int(self.secondPoint)
        
        self.experimentList.append(self.experimentNumber)
        self.experimentList.append(self.firstPoint)
        self.experimentList.append(self.secondPoint)
        
        # Emet un signal de fermeture fenetre Pivotal
        self.fermeturePopUpPivotal.emit(self.experimentList)
        # fermer la fenêtre
        self.close()
######################################################################################################################
######################################################################################################################

######################################################################################################################
###################### Difference or Addition class ##################################################################
class PopUpDiffOrAdd(QDialog):
    fermeturePopUpDiffOrAdd = QtCore.pyqtSignal(dict)
    def __init__(self, parent = MainWindow):
            super(PopUpDiffOrAdd, self).__init__() # Call the inherited classes __init__ method
            uic.loadUi('PopUpDiffOrAdd.ui', self) # Load the .ui file   

            self.pushButtonAddition.clicked.connect(self.onPushButtonAddition)
            self.pushButtonDifference.clicked.connect(self.onPushButtonDifference) 
            self.checkBoxAnotherExperiment.stateChanged.connect(self.checkBoxState)
            self.checkBoxConstante.stateChanged.connect(self.checkBoxState)
            
    @QtCore.pyqtSlot()        
    def onPushButtonAddition(self):
        self.experimentDictDiffOrAdd = {}
        self.experimentDictDiffOrAdd['type'] = 'addition'
        self.experimentDictDiffOrAdd['experiment'] = self.lineEditExperimentNumberDifference.text()
        self.experimentDictDiffOrAdd['constante'] = self.lineEditConstante.text()
        self.experimentDictDiffOrAdd['anotherExperiment'] = self.lineEditAnotherExperiment.text()
        
        # Close signal emitted for diffOrAdd window
        self.fermeturePopUpDiffOrAdd.emit(self.experimentDictDiffOrAdd)
        self.close()
    
    @QtCore.pyqtSlot()        
    def onPushButtonDifference(self):
        self.experimentDictDiffOrAdd = {}
        self.experimentDictDiffOrAdd['type'] = 'difference'
        self.experimentDictDiffOrAdd['experiment'] = self.lineEditExperimentNumberDifference.text()
        self.experimentDictDiffOrAdd['constante'] = self.lineEditConstante.text()
        self.experimentDictDiffOrAdd['anotherExperiment'] = self.lineEditAnotherExperiment.text()
        
        # Close signal emitted for diffOrAdd window
        self.fermeturePopUpDiffOrAdd.emit(self.experimentDictDiffOrAdd)
        self.close()
        
    def checkBoxState(self): 
        if self.checkBoxConstante.checkState() == 2 and self.checkBoxAnotherExperiment.checkState() == 0:
            self.lineEditConstante.setReadOnly(False)
            self.lineEditAnotherExperiment.setReadOnly(True)
            
        elif self.checkBoxConstante.checkState() == 0 and self.checkBoxAnotherExperiment.checkState() == 2:
            self.lineEditConstante.setReadOnly(True)
            self.lineEditAnotherExperiment.setReadOnly(False)
            
        elif self.checkBoxConstante.checkState() == 0 and self.checkBoxAnotherExperiment.checkState() == 0:
            self.lineEditConstante.setReadOnly(True)
            self.lineEditAnotherExperiment.setReadOnly(True)
        
        elif self.checkBoxConstante.checkState() == 2 and self.checkBoxAnotherExperiment.checkState() == 2:
            self.lineEditConstante.setReadOnly(True)
            self.lineEditAnotherExperiment.setReadOnly(True) 
######################################################################################################################
######################################################################################################################    

######################################################################################################################
################ Pivotal Class #######################################################################################
class PopUpNormalization(QDialog):
    
    fermeturePopUpNormalization = QtCore.pyqtSignal(dict)
    
    def __init__(self, parent = MainWindow):
            super(PopUpNormalization, self).__init__() # Call the inherited classes __init__ method
            uic.loadUi('PopUpNormalization.ui', self) # Load the .ui file   

            toggle_1 = Toggle()
            toggle_2 = AnimatedToggle(
                checked_color="#FFB000",
                pulse_checked_color="#44FFB000"
            )
    
            container = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(toggle_1)
            layout.addWidget(toggle_2)
            container.setLayout(layout)
    

            self.pushButtonMultiply.clicked.connect(self.onPushButtonMultiply)
            self.pushButtonDivision.clicked.connect(self.onPushButtonDivision) 
            self.checkBoxAnotherExperiment.stateChanged.connect(self.checkBoxState)
            self.checkBoxConstante.stateChanged.connect(self.checkBoxState)
            
    @QtCore.pyqtSlot()        
    def onPushButtonMultiply(self):
        self.experimentDictNormalization = {}
        self.experimentDictNormalization['type'] = 'multiplication'
        self.experimentDictNormalization['experiment'] = self.lineEditExperimentNumberNormalization.text()
        self.experimentDictNormalization['constante'] = self.lineEditConstanteNormalization.text()
        self.experimentDictNormalization['anotherExperiment'] = self.lineEditAnotherExperimentNormalization.text()
        
        # Close signal emitted for diffOrAdd window
        self.fermeturePopUpNormalization.emit(self.experimentDictNormalization)
        self.close()
    
    @QtCore.pyqtSlot()        
    def onPushButtonDivision(self):
        self.experimentDictNormalization = {}
        self.experimentDictNormalization['type'] = 'difference'
        self.experimentDictNormalization['experiment'] = self.lineEditExperimentNumberNormalization.text()
        self.experimentDictNormalization['constante'] = self.lineEditConstanteNormalization.text()
        self.experimentDictNormalization['anotherExperiment'] = self.lineEditAnotherExperimentNormalization.text()
        
        # Close signal emitted for diffOrAdd window
        self.fermeturePopUpNormalization.emit(self.experimentDictNormalization)
        self.close()
        
    def checkBoxState(self): 
        if self.checkBoxConstante.checkState() == 2 and self.checkBoxAnotherExperiment.checkState() == 0:
            self.lineEditConstanteNormalization.setReadOnly(False)
            self.lineEditAnotherExperimentNormalization.setReadOnly(True)
            
        elif self.checkBoxConstante.checkState() == 0 and self.checkBoxAnotherExperiment.checkState() == 2:
            self.lineEditConstanteNormalization.setReadOnly(True)
            self.lineEditAnotherExperimentNormalization.setReadOnly(False)
            
        elif self.checkBoxConstante.checkState() == 0 and self.checkBoxAnotherExperiment.checkState() == 0:
            self.lineEditConstanteNormalization.setReadOnly(True)
            self.lineEditAnotherExperimentNormalization.setReadOnly(True)
        
        elif self.checkBoxConstante.checkState() == 2 and self.checkBoxAnotherExperiment.checkState() == 2:
            self.lineEditConstanteNormalization.setReadOnly(True)
            self.lineEditAnotherExperimentNormalization.setReadOnly(True) 
######################################################################################################################
######################################################################################################################


######################################################################################################################
################################### Username Class ###################################################################
class PopUpUsername(QDialog):
    
    fermeturePopUpUsername = QtCore.pyqtSignal(str)
    
    def __init__(self ,parent = MainWindow):
        super(PopUpUsername, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('PopUpUsername.ui', self) # Load the .ui file
        
        self.pushButtonOkUsername.clicked.connect(self.onPushButtonOkUsername)
        self.pushButtonCancelUsername.clicked.connect(self.onPushButtonCancelUsername)

    @QtCore.pyqtSlot()
    def onPushButtonOkUsername(self):
        self.usernameCreated = self.lineEditCreateUsername.text()
        self.fermeturePopUpUsername.emit(self.usernameCreated)
        self.close()
        
    def onPushButtonCancelUsername(self):
        self.close()
######################################################################################################################
######################################################################################################################


######################################################################################################################
################ Sequence Class ######################################################################################
class PopUpSequence(QDialog):
    
    fermeturePopUpSequence = QtCore.pyqtSignal(dict)
    
    def __init__(self, loadedUserParameter,parent = MainWindow):
        super(PopUpSequence, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('PopUpSequence.ui', self) # Load the .ui file  
        
        self.loadedUserParameter = loadedUserParameter

        self.pushButtonLoadSequence.clicked.connect(self.onPushButtonLoadSequence) 
        self.pushButtonAddSequence.clicked.connect(self.onPushButtonAddSequence)
        self.listWidgetSequence.itemClicked.connect(self.onPushListSequence)
        PopUpSequence.createListSequence(self)
            
    @QtCore.pyqtSlot()        
    def onPushButtonLoadSequence(self):
        self.sequenceDict = {}
        
        self.sequenceDict["Sequence"] = self.textEditCurrentSequence.toPlainText()
        self.sequenceDict["Number of acquisition"] = int(self.lineEditNumberOfAcquisition.text())
        self.sequenceDict["Acquisition to supress"] = int(self.lineEditAcquisitionToSupress.text())
        self.sequenceDict["Time between acquisition"] = int(self.lineEditTimeBetweenAcquisition.text())
        self.sequenceDict["Average type"] = self.comboBoxAverage.currentText()
        self.sequenceDict["Baseline type"] = self.comboBoxBaselineCorrection.currentText()
        self.sequenceDict["First point baseline"] = int(self.lineEditFirstPointBaseline.text())
        self.sequenceDict["Second point baseline"] = int(self.lineEditSecondPointBaseline.text())
        self.sequenceDict["Third point baseline"] = int(self.lineEditThirdPointBaseline.text())
        self.sequenceDict["Fourth point baseline"] = int(self.lineEditFourthPointBaseline.text())
        
        # Emet un signal de fermeture fenetre Sequence
        self.fermeturePopUpSequence.emit(self.sequenceDict)
        # fermer la fenêtre
        self.close()
        
    def onPushButtonAddSequence(self):
        with open(self.loadedUserParameter,'rb') as file:
            data = pickle.load(file)
            
        name = self.lineEditNameSequence.text()
        sequence = self.textEditCurrentSequence.toPlainText()

        seq = {"Name": name, "Sequence": sequence}
        data.append(seq)
 
        with open(self.loadedUserParameter,'wb') as file_temp:
            pickle.dump(data, file_temp, pickle.HIGHEST_PROTOCOL)
            
        PopUpSequence.createListSequence(self)
        
    def onPushListSequence(self):
        sequenceSelected = self.listWidgetSequence.currentItem().text()
        
        with open(self.loadedUserParameter,'rb') as file:
            data = pickle.load(file)
            
        listSelected = list(filter(lambda item: item['Name'] == sequenceSelected, data))
        sequenceToDisplay = listSelected[0].get("Sequence")
        
        self.textEditCurrentSequence.setText(sequenceToDisplay)
######################################################################################################################
######################################################################################################################  

        
        
############ Function that create list of sequence ##############################################################
#################################################################################################################
    def createListSequence(self):
        # Open file
        with open(self.loadedUserParameter,'rb') as file:
            data = pickle.load(file)
            
        self.listWidgetSequence.clear()
        for i in range(0,len(data)):
            self.listWidgetSequence.addItem(data[i].get("Name"))    
######################################################################################################################
######################################################################################################################

############ Classes for PopUp Error Window #####################################################################
#################################################################################################################
class PopUpUserParameterNotLoad(QDialog): 
    
    def __init__(self,parent = MainWindow):
        super(PopUpUserParameterNotLoad, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('PopUpUserParameterNotLoad.ui', self) # Load the .ui file
        
        self.pushButtonPopUpUserParameterNotLoad.clicked.connect(self.onPushButtonPopUpUserParameterNotLoad)
        
    def onPushButtonPopUpUserParameterNotLoad(self):
        self.close()
######################################################################################################################
######################################################################################################################


############ Classes for PopUp Error Window #####################################################################
#################################################################################################################
class PopUpExperimentNotLoad(QDialog): 
    
    def __init__(self,parent = MainWindow):
        super(PopUpExperimentNotLoad, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('PopUpExperimentNotLoad.ui', self) # Load the .ui file
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.pushButtonPopUpExperimentNotLoad.clicked.connect(self.onPushButtonPopUpExperimentNotLoad)
        
    def onPushButtonPopUpExperimentNotLoad(self):
        self.close()
######################################################################################################################
######################################################################################################################

############ Classes for PopUp Error Window #####################################################################
#################################################################################################################
class PopUpBracketError(QDialog): 
    
    def __init__(self,parent = MainWindow):
        super(PopUpBracketError, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('PopUpBracketError.ui', self) # Load the .ui file
        self.setWindowFlag(Qt.FramelessWindowHint)
        
        self.pushButtonBracketMissing.clicked.connect(self.onPushButtonBracketMissing)
        
    def onPushButtonBracketMissing(self):
        self.close()
######################################################################################################################
######################################################################################################################


### Code minimal pour afficher l'interface graphique        
if __name__.endswith('__main__'):
    
    if not QApplication.instance():
        MainApp = QApplication(sys.argv)
    else :
        MainApp = QApplication.instance()
     
mainWindow = MainWindow()
mainWindow.show()

rc = MainApp.exec_()
sys.exit(rc)
##################################