import time
import pandas as pd
import numpy as np
from detectors import *




start = time.time() 

#Load and create the dataframes
et = pd.read_csv("eye_tracking_data.csv")
beh = pd.read_csv("behavioural_data.csv")
op = pd.DataFrame()
    
#Slice it and take what we need and then clean it
beh = beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected","response_time"]]
et = et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]
    
#et = et.drop(et[(et.GazePointX < 0) & (et.GazePointY < 0)].index)
    
et = et[~(et['GazePointY'] < 0)]
et = et[~(et['GazePointX'] < 0)]
et = et.reset_index(drop=True)
    

    
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def get_subject_nr(subject_path):
    return int(''.join(filter(str.isdigit, subject_path)))





def get_fixations(df): #GEt the fixations for the given dataframe
    dfListX = df["GazePointX"].tolist()
    dfListY = df["GazePointY"].tolist()
    dfListT = df["TimeStamp"].tolist()
    
    results = fixation_detection(dfListX, dfListY, dfListT, missing=0.0, maxdist=25, mindur=16.7)
    fixations = results[1]

    return fixations


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

def get_trials_indexes(df):
    #Loop though the indexes and take only the indexes the start and end gamble
    trials = [] # Here we store the tuples with the start-end indexes
    ph = 0 #A place holder for start-gamble index
    for i in df.index:
        val = et.at[i,"Event"] # The value at the current cell
        if "gamble" in str(val):       
            if ph != 0:   # if ph !=0 then ph is start-gamble
                trials.append((ph,i)) #Append the ph and the current index
                ph = 0 #Reset
            else: # If ph is 0 then take the index of start-gamble
                ph = i 
    return trials

def get_trial_from_indexes(f):
    
    first_gamble_index = f[0]+1 # take the first tuple value - start-gamble
    last_gamble_index = (f[1]) # take the second tuple value - end gamble
    return pd.DataFrame(et.iloc[first_gamble_index:last_gamble_index])
 


    



def main():  
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
    trials = get_trials_indexes(et)
    for f in trials: 
        #Using the tuple, use start index and end index to create a trial
        op =  get_trial_from_indexes(f)
        
        #Get a list of fixations of the current  trial
        fixations = get_fixations(op) 

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
        subject_nr = 15
                
        AOIs = get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y)
        
        result = [subject_nr] + [gamble_nr] + [domain] + AOIs + [risk]+[response_time]
        subject_values.append(result)
        c += 1

    
    
    return subject_values #result
    #Subject finished


    



#Main     
op = main()

subject_15 = pd.DataFrame(op)
subject_15.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]



#Export the dataset
subject_15.to_csv("Subject-AOIs.csv", index = False)


end = time.time()  
print("Program ended and it took: ",end-start)


