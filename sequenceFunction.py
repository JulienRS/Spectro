# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 10:20:00 2021

@author: Julien-IBPC
"""

def ReadSequence(sequence):  
    sequence = ' ' + sequence               ### !! must have space character in the begining !!
    
###### Analyze the presence of bracket ######################################################################################
#############################################################################################################################
    idx_find_left_bracket = 0
    i_left = 0
    i_left_list = []
    
    idx_find_right_bracket = 0
    i_right = 0
    i_right_list = []
    
    while idx_find_left_bracket < len(sequence):
        idx_find_left_bracket = sequence.find('(', idx_find_left_bracket)
        if idx_find_left_bracket == -1:
            break
        i_left_list.append(idx_find_left_bracket)
        i_left += 1
        idx_find_left_bracket += 1 
            
    while idx_find_right_bracket < len(sequence):
        idx_find_right_bracket = sequence.find(')', idx_find_right_bracket)
        if idx_find_right_bracket == -1:
            break
        i_right_list.append(idx_find_right_bracket)
        i_right += 1
        idx_find_right_bracket += 1 
        
    idxSubSeqBracket = []
    if i_left != i_right:
        bracketMissing = True
    else:
        bracketMissing = False
        for i in range(0,len(i_left_list)):
            j = i_left_list[i] - 1
            while j >= 0:
                try:
                    idx = int(sequence[j])
                except ValueError:
                    idxSubSeqBracket.append(j)
                    break
                else:
                    j -= 1
                    
    subSeqBracket = []
    for i in range(0,len(i_left_list)):
        if idxSubSeqBracket == []:
            break
        else:
            subSeqBracket.append(sequence[idxSubSeqBracket[i]+1:i_right_list[i]+1])
            
    subSeqBracketD = []
    for i in range(0,len(subSeqBracket)):
        if subSeqBracket[i][-2] == ('D' or 'd'):
            subSeqBracketD.append(subSeqBracket[i])
        else:
            subSeqBracketD.append(subSeqBracket[i][:-1] + 'D)')
            
    subSeqBracketDev = []
    for i in range(0,len(subSeqBracketD)):
        bracketPos = subSeqBracketD[i].find('(')
        multiplicator = int(subSeqBracketD[i][0:bracketPos])
        subSeqBracketDev.append(subSeqBracketD[i][bracketPos+1:-1]*multiplicator)
        
    subSeqNonBracket = []
    for i in range(0,len(idxSubSeqBracket)-1):
        # if subSeqNonBracket != []:
        #     print('There are no instructions outside bracket')
        # else:
        subSeqNonBracket.append(sequence[i_right_list[i]+1:idxSubSeqBracket[i+1]+1])
    
######### Replace bracketed part in original sequence by the developed part #################################
############################################################################################################# 
    fullSeq = []
    for i in range(0,len(subSeqBracket)):
        sequence = sequence.replace(subSeqBracket[i], subSeqBracketDev[i])
        fullSeq = sequence
        
    return fullSeq, bracketMissing
##########################################################################################################################
##########################################################################################################################