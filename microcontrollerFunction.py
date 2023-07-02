# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 10:52:53 2021

@author: Julien
"""

import serial
import time
import numpy as np

from struct import *

def sendSequenceToMC(sequence, mc, NbAcqu, TimeBetweenAcqu):

    sequence = sequence.replace(" ","")
    
    new_sequence = []
    
    for i in range(len(sequence)):
        if sequence[i] == "s":
            if sequence[i-1] == 'm':
                new_sequence.append(sequence[:i] + sequence[i+1:])
            elif sequence[i-1] == 'M':
                new_sequence.append(sequence[:i] + sequence[i+1:])
            elif sequence[i-1] == 'u':
                new_sequence.append(sequence[:i] + sequence[i+1:])
            elif sequence[i-1] == 'µ':
                new_sequence.append(sequence[:i] + sequence[i+1:])
            elif sequence[i-1] == 'U':
                new_sequence.append(sequence[:i] + sequence[i+1:])
            else:
                new_sequence.append(sequence[:i] + "S" + sequence[i+1:])
                
    sequence = sequence.replace("s","")
    sequence = sequence + '1'
    
    posInt = []
    posChar = []        
    
    for i in range(len(sequence)):
        idx = sequence[i]
        try:
            int(idx)
        except ValueError:
            posChar.append(i)
        else:
            posInt.append(i)
    
    listInt = []
    strInt = ""
    for i in range(len(sequence)):
        idx = sequence[i]
        try:
            int(idx)
        except ValueError:
            listInt.append(strInt)
            strInt = ""
            pass
        else:
            strInt = strInt + idx
    
    listChar = []
    strChar = ""
    for i in range(len(sequence)):
        idx = sequence[i]
        try:
            int(idx)
        except ValueError:
            strChar = strChar + idx
            pass
        else:
            listChar.append(strChar)
            strChar = ""
    
    listInt = [i for i in listInt if i != '']
    listChar = [i for i in listChar if i != '']
    
    listInt = [int(i) for i in listInt]
    
    ### !! Milliseconds based !! ###
    listTime = []
    for i in range(len(listChar)):
        if listChar[i][0] == 'm':
            listTime.append(1)
        elif listChar[i][0] == 'M':
            listTime.append(1)
        elif listChar[i][0] == 'u':
            listTime.append(1e-03)
        elif listChar[i][0] == 'µ':
            listTime.append(1e-03)
        elif listChar[i][0] == 'U':
            listTime.append(1e-03)
        elif listChar[i][0] == 'n':
            listTime.append(1e-03)
        elif listChar[i][0] == 'N':
            listTime.append(1e-03)
        else:
            pass
    
            
    listExpPts = np.multiply(listInt,listTime)
    listExpPtsFloat = []
    for i in range(len(listExpPts)):
        listExpPtsFloat.append(float(listExpPts[i]))
    
    for i in range(len(listChar)):
        listChar[i] = listChar[i][1:]
    
    listFin = []
    listFin.append(str(NbAcqu))
    listFin.append('|')
    listFin.append(str(TimeBetweenAcqu))
    listFin.append('|')
    
    for i in range(len(listExpPts)):
        listFin.append('&')
        listFin.append(str(listExpPtsFloat[i]))
        listFin.append('^')
        listFin.append(listChar[i])
        
    print(listFin)
  
    for j in range(len(listFin)):
        mc.write(listFin[j].encode())
    mc.write('\n'.encode())
    
    return listFin