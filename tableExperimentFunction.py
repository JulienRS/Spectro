# -*- coding: utf-8 -*-

import sys
import os
import time

from PyQt5 import uic, QtCore, QtGui

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pickle
import numpy as np


######################################################################################################################           
######################################################################################################################        
##### Creation of Experiment and Calculation table   #################################################################         
def createTable(self,data):
    # Determination of experiment's number and calculation's number in opened file    
    self.nbExperiment = 0
    self.nbCalculation = 0
    data_calculation = []
    data_experiment = []

    
    for i in range (0,len(data)):
        if data[i].get('type') == 'Calculation':
            self.nbCalculation = self.nbCalculation + 1
            data_calculation.append(data[i])
            
        if data[i].get('type') == 'Experiment':
            self.nbExperiment = self.nbExperiment + 1
            data_experiment.append(data[i])
            

    # Creation of Experiment table
    if self.nbExperiment < 10:
        self.tableWidgetExperiment.setRowCount(1)
        self.tableWidgetExperiment.setColumnCount(self.nbExperiment)
        
    else:
        nb_exp_str = str(self.nbExperiment)
        if nb_exp_str[-1] == 0:    
            index_nb_exp = int(nb_exp_str[:-1])
        else:
            index_nb_exp = int(nb_exp_str[:-1])+1

        self.tableWidgetExperiment.setColumnCount(10)
        self.tableWidgetExperiment.setRowCount(index_nb_exp)
        
    # Creation of Calculation table   
    if self.nbCalculation < 10:
        self.tableWidgetCalculation.setRowCount(1)
        self.tableWidgetCalculation.setColumnCount(self.nbCalculation)
        
    else:
        nb_calc_str = str(self.nbCalculation)
        if nb_calc_str[-1] == 0:    
            index_nb_calc = int(nb_calc_str[:-1])
        else:
            index_nb_calc = int(nb_calc_str[:-1])+1

        self.tableWidgetCalculation.setColumnCount(10)
        self.tableWidgetCalculation.setRowCount(index_nb_calc)
        
        
    # Filling the tables         
    i_exp = 1
    for j in range(0,self.tableWidgetExperiment.rowCount()):
        for k in range(0,self.tableWidgetExperiment.columnCount()):
            if i_exp > self.nbExperiment:
                break
            else:
                item = QTableWidgetItem(str(i_exp))
                item.setBackground(QtGui.QColor(210, 210, 210))
                self.tableWidgetExperiment.setItem(j,k,item)
                i_exp = i_exp + 1
                
    self.tableWidgetExperiment.resizeColumnsToContents()
    self.tableWidgetExperiment.resizeRowsToContents()
    
    i_calc = 1
    for j in range(0,self.tableWidgetCalculation.rowCount()):
        for k in range(0,self.tableWidgetCalculation.columnCount()):
            if i_calc > self.nbCalculation:
                break
            else:
                if data_calculation[i_calc - 1 ].get("operation") == "pivotal":
                    item = QTableWidgetItem(str(i_calc))
                    item.setBackground(QtGui.QColor(255, 240, 190))
                    self.tableWidgetCalculation.setItem(j,k,item)
                    i_calc = i_calc + 1
                    
                elif data_calculation[i_calc - 1].get("operation") == "difference" or data_calculation[i_calc - 1].get("operation") == "addition":
                    item = QTableWidgetItem(str(i_calc))
                    item.setBackground(QtGui.QColor(190, 230, 255))
                    self.tableWidgetCalculation.setItem(j,k,item)
                    i_calc = i_calc + 1
                    
                elif data_calculation[i_calc - 1].get("operation") == "division" or data_calculation[i_calc - 1].get("operation") == "multiplication":
                    item = QTableWidgetItem(str(i_calc))
                    item.setBackground(QtGui.QColor(255, 220, 250))
                    self.tableWidgetCalculation.setItem(j,k,item)
                    i_calc = i_calc + 1
                
    self.tableWidgetCalculation.resizeColumnsToContents()
    self.tableWidgetCalculation.resizeRowsToContents()
######################################################################################################################
######################################################################################################################
     