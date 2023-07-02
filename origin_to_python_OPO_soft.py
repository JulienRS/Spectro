import pickle

with open("BF4_F34+_spectre-bleu.txt", "rb") as file:
    
    x = list()
    y_1 = list()
    y_2 = list()
    y_3 = list()
    y_4 = list()
    y_5 = list()
    y_6 = list()
    y_7 = list()
    y_8 = list()
    
    for line in file:
        data = line.split()
        x.append(int(data[0]))
        
        d_1 = data[1].decode()  
        d_1 = d_1.replace(",",".")
        y_1.append(float(d_1))
        
        d_2 = data[2].decode()  
        d_2 = d_2.replace(",",".")
        y_2.append(float(d_2))

        d_3 = data[3].decode()  
        d_3 = d_3.replace(",",".")
        y_3.append(float(d_3))
        
        d_4 = data[4].decode()  
        d_4 = d_4.replace(",",".")
        y_4.append(float(d_4))
        
        d_5 = data[5].decode()  
        d_5 = d_5.replace(",",".")
        y_5.append(float(d_5))
        
        d_6 = data[6].decode()  
        d_6 = d_6.replace(",",".")
        y_6.append(float(d_6))
        
        d_7 = data[7].decode()  
        d_7 = d_7.replace(",",".")
        y_7.append(float(d_7))
        
        d_8 = data[8].decode()  
        d_8 = d_8.replace(",",".")
        y_8.append(float(d_8))
        
        
exp_temp_1 = {"operation" : "raw" , "type" : "Experiment", "number" : "1", "comment" : "1", "wavelength" : 520, "time" : x, "data": y_1}
exp_temp_2 = {"operation" : "raw" , "type" : "Experiment", "number" : "2", "comment" : "2", "wavelength" : 520, "time" : x, "data": y_2}
exp_temp_3 = {"operation" : "raw" , "type" : "Experiment", "number" : "3", "comment" : "3", "wavelength" : 520, "time" : x, "data": y_3}
exp_temp_4 = {"operation" : "raw" , "type" : "Experiment", "number" : "4", "comment" : "4", "wavelength" : 520, "time" : x, "data": y_4}
exp_temp_5 = {"operation" : "raw" , "type" : "Experiment", "number" : "5", "comment" : "5", "wavelength" : 520, "time" : x, "data": y_5}
exp_temp_6 = {"operation" : "raw" , "type" : "Experiment", "number" : "6", "comment" : "6", "wavelength" : 520, "time" : x, "data": y_6}
exp_temp_7 = {"operation" : "raw" , "type" : "Experiment", "number" : "7", "comment" : "7", "wavelength" : 520, "time" : x, "data": y_7}
exp_temp_8 = {"operation" : "raw" , "type" : "Experiment", "number" : "8", "comment" : "8", "wavelength" : 520, "time" : x, "data": y_8}

data_final = [exp_temp_1,exp_temp_2,exp_temp_3,exp_temp_4,exp_temp_5,exp_temp_6,exp_temp_7,exp_temp_8]

with open('spectre_OPO_1.bin', 'wb') as file_temp:
    pickle.dump(data_final, file_temp, pickle.HIGHEST_PROTOCOL)
    
with open('spectre_OPO_1.bin','rb') as file:
    donnees = pickle.load(file)
    
d = len(donnees)    
print(d)