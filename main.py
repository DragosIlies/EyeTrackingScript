import time
import pandas as pd
import numpy as np
from detectors import *



start = time.time() 
    

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#Load and create the dataframes
et = pd.read_csv("eye_tracking_data.csv")
beh = pd.read_csv("behavioural_data.csv")
op = pd.DataFrame()

#Slice it and take what we need and then clean it
beh = beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected"]]
et = et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]

#et = et.drop(et[(et.GazePointX < 0) & (et.GazePointY < 0)].index)

et = et[~(et['GazePointY'] < 0)]
et = et[~(et['GazePointX'] < 0)]
et = et.reset_index(drop=True)



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
    AOI_p = []
    AOI_q = []
    AOI_x = []
    AOI_y = []
    c = 0
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
            
            # Determine in which AOI should the fixation be
            if 800  <= endx <= 1000 and 400 <= endy <= 600: # AOI 1
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
                
   
            elif 800 <= endx <= 1000 and 400 <= endy <= 600: # AOI 2*
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

            elif 800 <= endx <= 1000 and 600 <= endy <= 800: # AOI 3
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

            elif 800 <= endx <= 1000 and 600 <= endy <= 800: # AOI 4*
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
        
        domain = beh.at[c,"domain"]
        gamble_nr = beh.at[c,"Gamble"]   
        risk = beh.at[c,"risk_selected"]
        subject = 15
                
        AOIs = get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y)
        result = [subject] + [gamble_nr] + [domain] + AOIs + [risk]
        subject_values.append(result)
        c += 1

    
    
    return subject_values #result
    #Subject finished


    



#Main     
op = main()

subject_15 = pd.DataFrame(op)
subject_15.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected"]

end = time.time()  
print("Program ended and it took: ",end-start)

#Export the dataset
subject_15.to_csv("Subject-AOIs.csv", index = False)





