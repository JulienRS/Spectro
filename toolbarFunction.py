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
def actionLoadExperiment(self):
    # Read and save the name of opened file
    dialog = QFileDialog()
    experiment_filename = dialog.getOpenFileName()
    self.loaded_filename = experiment_filename[0]
######################################################################################################################
######################################################################################################################
 
def actionLoadUserParameter(self):
    # Read and save the name of opened file
    dialog = QFileDialog()
    userParameter = dialog.getOpenFileName(filter = 'parameter_*.bin')
    self.loadedUserParameter = userParameter[0]
    p1 = self.loadedUserParameter.find('_')
    p2 = self.loadedUserParameter.find('.')
    self.lineEditDisplayCurrentUser.setText(self.loadedUserParameter[p1+1:p2])
    self.lineEditDisplayCurrentUser.setReadOnly(True)