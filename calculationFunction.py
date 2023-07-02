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


def normalization(self,dictNormalization):
    data_experiment = []
    
    # if 'constante' = empty str => it's a normalization with another experiment
    if dictNormalization.get('constante') == '':
        nbSelectedExperimentNormalization = int(dictNormalization.get('experiment'))
        nbSelectedAnotherExperiment = int(dictNormalization.get('anotherExperiment'))
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
            
        indexCalculation = 1
        for i in range (0,len(data)):
            if data[i].get('type') == 'Calculation':
                indexCalculation = indexCalculation + 1
            
        for i in range(0,len(data)):
            if data[i].get('type') == 'Experiment':
                data_experiment.append(data[i])
            else:
                pass
            
        if dictNormalization.get('type') == 'division':
            referenceExperiment = data_experiment[nbSelectedExperimentNormalization-1].get('data')
            experimentToNormalize = data_experiment[nbSelectedAnotherExperiment-1].get('data')
            x = data_experiment[nbSelectedExperimentNormalization-1].get('time')
            division = np.divide(referenceExperiment,experimentToNormalize)
            
            calc = {"operation" : "division", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": division}
            data.append(calc)
            
        elif dictNormalization.get('type') == 'multiplication':
            referenceExperiment = data_experiment[nbSelectedExperimentNormalization-1].get('data')
            experimentToMultiply = data_experiment[nbSelectedAnotherExperiment-1].get('data')
            x = data_experiment[nbSelectedExperimentNormalization-1].get('time')
            multiplication = np.multiply(referenceExperiment,experimentToMultiply)
            
            calc = {"operation" : "multiplication", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": multiplication}
            data.append(calc)

        
    # if 'anotherExperiment = empty str => it's a diff or add with a constante
    if dictNormalization.get('anotherExperiment') == '':
        nbSelectedExperimentNormalization = int(dictNormalization.get('experiment'))
        selectedConstante = float(dictNormalization.get('constante'))
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
            
        indexCalculation = 1
        for i in range (0,len(data)):
            if data[i].get('type') == 'Calculation':
                indexCalculation = indexCalculation + 1
            
        for i in range(0,len(data)):
            if data[i].get('type') == 'Experiment':
                data_experiment.append(data[i])
            else:
                pass
            
        if dictNormalization.get('type') == 'division':
            referenceExperiment = data_experiment[nbSelectedExperimentNormalization-1].get('data')
            x = data_experiment[nbSelectedExperimentNormalization-1].get('time')
            division = np.divide(referenceExperiment,selectedConstante)
            
            calc = {"operation" : "division", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": division}
            data.append(calc)
            
        elif dictNormalization.get('type') == 'multiplication':
            referenceExperiment = data_experiment[nbSelectedExperimentNormalization-1].get('data')
            x = data_experiment[nbSelectedExperimentNormalization-1].get('time')
            multiplication = np.multiply(referenceExperiment,selectedConstante)
            
            calc = {"operation" : "multiplication", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": multiplication}
            data.append(calc)
            
                
    return calc

##########################################################################################################
##########################################################################################################

def diffOrAdd(self, dictDiffOrAdd):
    data_experiment = []
        
    # if 'constante' = empty str => it's a diff or add with another experiment
    if dictDiffOrAdd.get('constante') == '':
        nbSelectedExperimentDiffOrAdd = int(dictDiffOrAdd.get('experiment'))
        nbSelectedAnotherExperiment = int(dictDiffOrAdd.get('anotherExperiment'))
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
            
        indexCalculation = 1
        for i in range (0,len(data)):
            if data[i].get('type') == 'Calculation':
                indexCalculation = indexCalculation + 1
            
        for i in range(0,len(data)):
            if data[i].get('type') == 'Experiment':
                data_experiment.append(data[i])
            else:
                pass
            
        if dictDiffOrAdd.get('type') == 'difference':
            referenceExperiment = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('data')
            experimentToSubstract = data_experiment[nbSelectedAnotherExperiment-1].get('data')
            x = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('time')
            substraction = np.subtract(referenceExperiment,experimentToSubstract)
            
            calc = {"operation" : "difference", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": substraction}
            data.append(calc)
            
        elif dictDiffOrAdd.get('type') == 'addition':
            referenceExperiment = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('data')
            experimentToSumUp = data_experiment[nbSelectedAnotherExperiment-1].get('data')
            x = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('time')
            addition = np.add(referenceExperiment,experimentToSumUp)
            
            calc = {"operation" : "addition", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": addition}
            data.append(calc)
            

        
    # if 'anotherExperiment = empty str => it's a diff or add with a constante
    if dictDiffOrAdd.get('anotherExperiment') == '':
        nbSelectedExperimentDiffOrAdd = int(dictDiffOrAdd.get('experiment'))
        selectedConstante = int(dictDiffOrAdd.get('constante'))
        
        with open(self.loaded_filename, 'rb') as file:
            data = pickle.load(file)
            
        indexCalculation = 1
        for i in range (0,len(data)):
            if data[i].get('type') == 'Calculation':
                indexCalculation = indexCalculation + 1
            
        for i in range(0,len(data)):
            if data[i].get('type') == 'Experiment':
                data_experiment.append(data[i])
            else:
                pass
            
        if dictDiffOrAdd.get('type') == 'difference':
            referenceExperiment = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('data')
            x = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('time')
            substraction = np.subtract(referenceExperiment,selectedConstante)
            
            calc = {"operation" : "difference", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": substraction}
            data.append(calc)

            
        elif dictDiffOrAdd.get('type') == 'addition':
            referenceExperiment = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('data')
            x = data_experiment[nbSelectedExperimentDiffOrAdd-1].get('time')
            addition = np.add(referenceExperiment,selectedConstante)
            
            calc = {"operation" : "addition", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Difference', "wavelength" : 520, "time" : x, "data": addition}
            data.append(calc)

    return calc

##########################################################################################################
##########################################################################################################
def pivotal(self, list_piv):
    selected_experiment_pivotal = list_piv[0]
    yPivotal = []
    
    with open(self.loaded_filename,'rb') as file:
        data = pickle.load(file)
        
    indexCalculation = 1
    for i in range (0,len(data)):
        if data[i].get('type') == 'Calculation':
            indexCalculation = indexCalculation + 1
            
        
    x = data[int(selected_experiment_pivotal)].get('time')
    y = data[int(selected_experiment_pivotal)].get('data')
    
    pt_1 = list_piv[1]-1
    pt_2 = list_piv[2]-1
    
    a = (y[pt_2]-y[pt_1])/(x[pt_2]-x[pt_1])
    b = y[pt_1]-a*x[pt_1]
    
    
    for i in range(0,len(x)):
        linearReg = a*x[i]+b         
        yPivotal.append((y[i]-linearReg))
    
    calc = {"operation" : "pivotal", "type" : "Calculation", "number" : str(indexCalculation), "comment" : 'test Pivotal', "wavelength" : 520, "time" : x, "data": yPivotal}
    data.append(calc)

    return calc