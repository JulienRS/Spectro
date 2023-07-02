# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:11:26 2022

@author: Julien-IBPC
"""

t = []
tt = []
s = ['D','^',100,'|','D',100,'D',100,'D',200,'D','|','D',100,'D',200]
i = 0

while i <= len(s):
    if (s[i] != '|'):
        t.append(s[i])
        i += 1
    else:
        break
    
print(i)
i += 1

while i <= len(s):
    if (s[i] != '|'):
        tt.append(s[i])
        i += 1
    else:
        break