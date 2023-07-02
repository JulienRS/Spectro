# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:56:42 2021

@author: Julien
"""

import pickle

sequence = []
sequence.append({"Name" : "Sequence Baseline 100ms", "Sequence" : "10(100msD)"})
sequence.append({"Name" : "Sequence Flash laser", "Sequence" : "4(100msD)A140usC500usD1msD2msD5msD10msD"})

with open('sequence_tester.bin', 'wb') as file_temp:
    pickle.dump(sequence, file_temp, pickle.HIGHEST_PROTOCOL)