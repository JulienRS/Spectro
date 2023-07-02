#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 12:44:26 2021

@author: Julien-IBPC
"""

from PyQt5.QtWidgets import QWidget, QTableWidget, QFileDialog
from PyQt5 import uic

class PlotExperimentOPO(QWidget):
    
        def __init__(self, parent = None):
            super().__init__()
            uic.loadUi(__file__.split('.py')[0] + '.ui', self)
        
            self.pushButtonPlotExperiment.clicked.connect(self.onPushButtonPlotExperiment) 
            
            
        def onPushButtonPlotExperiment(self, filename):
            with open(filename,'rb') as file:
                donnees = pickle.load(file)