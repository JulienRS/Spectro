#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

import sys

import pickle

class PopUpPivotal(QDialog):
    
        def __init__(self, parent = None):
            super().__init__()
            uic.loadUi(__file__.split('.py')[0] + '.ui', self)
        
            self.pushButtonPivotal.clicked.connect(self.onPushButtonPivotal) 
            
            
        def onPushButtonPivotal(self, filename):
            
            # with open(filename,'rb') as file:
            #     data = pickle.load(file)
                
                print('ok')
                self.close()
