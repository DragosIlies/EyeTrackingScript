import time
import pandas as pd
import numpy as np
from detectors import *
import re
import os

import os
import linecache


start = time.time() 



def get_badIndex(e):
    result = [f for f in re.split("[^0-9]", str(e)) if f != ''] 
    return (max(map(int, result)))

def replace_line(subject_path,badIndex):
    f=open(subject_path)

    data=f.readlines()
    badLine = data[badIndex-1]
    
    
    
    
    
    
    if "gamble" in badLine:
        #print("REPLACING")
        template = "    "+"\t"+"gamble"
        data[badIndex-1] = template
        with open(subject_path, 'w') as file:
            file.writelines(data)
    else:
        #print("REMOVING")
        template = "    "											
        data[badIndex-1] = template
        with open(subject_path, 'w') as file:
            file.writelines(data)
    del f
    
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def get_subject_nr(subject_path):
    return int(''.join(filter(str.isdigit, subject_path)))


def read_dataframe(subject_path):
    et = pd.DataFrame()
    temp = False
    while temp == False:
        try:
            #print("Trying to read file")
            et = pd.read_csv(subject_path,sep="\t",skiprows=17)
            temp = True

        except pd.errors.ParserError as e:
            #print("Got an error: ",e)
             #get the index
            badIndex = get_badIndex(e)
            replace_line(subject_path,badIndex)
            temp = False
    return et


    

def get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y): #Return the processed AOIs 
    #calculate the means
    p_Meanfix = mean(AOI_p)  
    q_Meanfix = mean(AOI_q)
    x_Meanfix = mean(AOI_x)
    y_Meanfix = mean(AOI_y) 
    
    
    #calculate the length
    p_TotalFix = len(AOI_p)
    q_TotalFix = len(AOI_q)
    x_TotalFix = len(AOI_x)
    y_TotalFix = len(AOI_y)
    
    return [p_Meanfix,q_Meanfix,x_Meanfix,y_Meanfix,p_TotalFix,q_TotalFix,x_TotalFix,y_TotalFix]


def main(et_path,beh_path):
    
    subject_nr = get_subject_nr(beh_path)
    et=read_dataframe(et_path)
    
        
        
    #print("Finished with subject:",subject_nr)
    beh = pd.read_csv(beh_path)
    op = pd.DataFrame()
        
    #Slice it and take what we need and then clean it
    beh = beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected","response_time"]]
    et = et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]
        
    #et = et.drop(et[(et.GazePointX < 0) & (et.GazePointY < 0)].index)

    #print("Finished cleaning")
 
    #Where we store the fixations
    AOI_p = []
    AOI_q = []
    AOI_x = []
    AOI_y = []
    #Use c to take the current stuff we need at the current row
    c = 0
    #Where we store the dataframe of the subject
    subject_values = []

    
    #loop through the gambles indexes pairs and add them to a data     
    #Loop though the indexes and take only the indexes the start and end gamble
    trials = [] # Here we store the tuples with the start-end indexes
    ph = 0 #A place holder for start-gamble index
    #print("Starting to create the trials")
    for i in et.index:
        val = et.at[i,"Event"] # The value at the current cell
        if "gamble" in str(val):       
            if ph != 0:   # if ph !=0 then ph is start-gamble
                trials.append((ph,i)) #Append the ph and the current index
                ph = 0 #Reset
            else: # If ph is 0 then take the index of start-gamble
                ph = i 
    trials = trials
    #print("got the trials")
    #print(len(trials))
    for f in trials: 
        AOI_p = []
        AOI_q = []
        AOI_x = []
        AOI_y = []
        
        #Using the tuple, use start index and end index to create a trial
        
        first_gamble_index = f[0]+1 # take the first tuple value - start-gamble
        last_gamble_index = (f[1]) # take the second tuple value - end gamble
        op =  pd.DataFrame(et.iloc[first_gamble_index:last_gamble_index])
        
        #Get a list of fixations of the current  trial
        dfListX = op["GazePointX"].tolist()
        dfListY = op["GazePointY"].tolist()
        dfListT = op["TimeStamp"].tolist()
        #print("Subject is:",subject_nr)
        dfListX =list(map(float, dfListX))
        dfListY =list(map(float, dfListY))
        dfListT =list(map(float, dfListT))

        #print("wanna calculate fixations")
        #print(list(map(float, dfListX)))
        #print(dfListY)
        #print(dfListT)
            
            
        
        results = fixation_detection(dfListX, dfListY, dfListT, missing=0.0, maxdist=25, mindur=16.7)
        #print("Finished fixations")
        
        fixations = results[1]
        for b in fixations:
            #print(b[3],b[4])
            if b[3] < 0 or b[4] < 0:
               # print("Deleted one")
                fixations.remove(b)
        fixations = fixations 

        x_loc = beh.at[c,"X_location"]
        #Loop though the fixations
        for f in fixations:
            endx = f[3]
            endy = f[4]
            duration = f[2]
            
            #AOI 1 coordonates
            a1x_up = 880
            a1y_up = 428
            a1x_low = 720
            a1y_low = 332
            
            #AOI 2 coordonates
            a2x_up = 1200
            a2y_up = 748
            a2x_low = 1040
            a2y_low = 332
            #AOI 3 coordonates
            a3x_up = 880
            a3y_up = 748
            a3x_low = 720
            a3y_low = 652
            #AOI 4 coordonates
            a4x_up = 1200
            a4y_up = 748
            a4x_low = 1040
            a4y_low = 652

            
            # Determine in which AOI should the fixation be
            if a1x_low  <= endx <= a1x_up and a1y_low <= endy <= a1y_up: # AOI 1
                if x_loc == 1:
                    AOI_p.append(duration)
                    #Add to AOI_p 
                elif x_loc == 2:
                    AOI_x.append(duration)
                    #add to AOI_x 
                elif x_loc == 3:
                    AOI_q.append(duration)
                    #add to AOI Q 
                elif x_loc == 4:
                    AOI_y.append(duration)
                    #add to AOI y 
                
   
            elif a2x_low  <= endx <= a2x_up and a2y_low <= endy <= a2y_up: # AOI 2*
                if x_loc == 1:
                    AOI_x.append(duration)
                    #add to aoi x 
                elif x_loc == 2:
                    AOI_p.append(duration)
                    #add to aoi p 
                elif x_loc == 3:
                    AOI_y.append(duration)
                    #add to aoi y 
                elif x_loc == 4:
                    AOI_q.append(duration)
                    #add to q AOI

            elif a3x_low  <= endx <= a3x_up and a3y_low <= endy <= a3y_up: # AOI 3
                if x_loc == 1:
                    AOI_q.append(duration)
                    #add to aoi q 
                elif x_loc == 2:
                    AOI_y.append(duration)
                    #add to y
                elif x_loc == 3:
                    AOI_p.append(duration)
                    #add to p
                elif x_loc == 4:
                    AOI_x.append(duration)
                    #add to x

            elif a4x_low  <= endx <= a4x_up and a4y_low <= endy <= a4y_up: # AOI 4*
                if x_loc == 1:
                    AOI_y.append(duration)
                    #add to y
                elif x_loc == 2:
                    AOI_q.append(duration)
                    #add to q
                elif x_loc == 3:
                    AOI_x.append(duration)
                    #add to x
                elif x_loc == 4:
                    AOI_p.append(duration)
                    #add to p
        response_time = beh.at[c,"response_time"]
        domain = beh.at[c,"domain"]
        gamble_nr = beh.at[c,"Gamble"]   
        risk = beh.at[c,"risk_selected"]
        
                
        AOIs = get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y)
        
        result = [subject_nr] + [gamble_nr] + [domain] + AOIs + [risk]+[response_time]
        subject_values.append(result)
        c += 1

    
    
    return subject_values #result
    #Subject finished


def get_subjects():
    fullList = os.listdir()
    subject_numbers = {}
    subject_pairs = []

    for v in fullList:
        if "subject" in v:
            #print("Taking")
            nr = get_subject_nr(v)
            subject_numbers[v]=nr
            
    for key, value in subject_numbers.items():
        for key2,value2 in subject_numbers.items(): #Loop though the dictionary
            if key != key2: # If key are named differently
                if value == value2:#If they have the same value
                    if (key2,key) not in subject_pairs:
                        subject_pairs.append((key,key2))
                        #print(key,key2)
    return subject_pairs
        



#Main
'''
finalDf = pd.DataFrame()
op = main("subject-3_TOBII_output.tsv","subject-3.csv")
#print(op)
subject = pd.DataFrame(op)
subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
finalDf = pd.concat([finalDf, subject])
'''
  
v = get_subjects()
finalDf = pd.DataFrame() 
for s in v:
    et_path =s[1]
    beh_path =s[0]
    
    op = main(et_path,beh_path)
    
    subject = pd.DataFrame(op)
    subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
    
    finalDf = pd.concat([finalDf, subject])

print("Finished with the program")

#Export the dataset
finalDf.to_csv("All-Subjects-AOIs_FIX1.csv", index = False)


end = time.time()  
print("Program ended and it took: ",end-start)


