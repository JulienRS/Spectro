#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 14:06:42 2021

@author: Julien-IBPC
"""

import numpy as np

import pickle


data_final = [] ### Creation d'une liste pour stocker l'ensemble des experiences

time_temp = []  ### Fichier temporaire pour stocker les temps d'acquisitions de la sequence
data_temp = []  ### Fichier temporaire pour stocker les donnees acquises
exp_temp = {}   ### Fichier temporaire pour stocker le dictionnaire regroupant donnees et metadonnees de l'experience

n = 300
comment = "test_experience"
wavelength = 520

### Boucle pour generer n experience
for i in range (1,n+1):
    ### Boucle pour stocker temps et donnees de maniere temporaire
    time_temp = []  ### Fichier temporaire pour stocker les temps d'acquisitions de la sequence
    data_temp = []  ### Fichier temporaire pour stocker les donnees acquises
    for j in range(0,20):
        time_temp.append(j*100)
        data_temp.append(2.5*j * (np.random.randint(10)))
        
    
    exp_temp_1 = {"type" : "Experiment", "number" : str(i), "comment" : 'test'+str(i), "wavelength" : wavelength, "time" : time_temp, "data": data_temp}
    exp_temp_2 = {"type" : "Calculation", "number" : str(i), "comment" : 'test'+str(i), "wavelength" : wavelength, "time" : time_temp, "data": data_temp}
    data_final.append(exp_temp_1)
    data_final.append(exp_temp_2)

with open('file_test_pickle_1.bin', 'wb') as file_temp:
    pickle.dump(data_final, file_temp, pickle.HIGHEST_PROTOCOL)
    
with open('file_test_pickle_1.bin','rb') as file:
    donnees = pickle.load(file)
    
d = len(donnees)    
print(d)