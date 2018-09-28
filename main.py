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

et = et.drop(et[(et.GazePointX < 0) & (et.GazePointY < 0)].index)
et = et.reset_index(drop=True)



def get_fixations(df): #GEt the fixations for the given dataframe
    dfListX = df["GazePointX"].tolist()
    dfListY = df["GazePointY"].tolist()
    dfListT = df["TimeStamp"].tolist()
    
    results = fixation_detection(dfListX, dfListY, dfListT, missing=0.0, maxdist=25, mindur=16.7)
    fixations = results[1]

    return fixations


def get_AOI_MT(AOI_P,AOI_Q,AOI_X,AOI_Y): #Return the processed AOIs 
    #calculate the means
    p_Meanfix = mean(AOI_P)  
    q_Meanfix = mean(AOI_Q)
    x_Meanfix = mean(AOI_X)
    y_Meanfix = mean(AOI_Y) 
    
    
    #calculate the length
    p_TotalFix = len(AOI_P)
    q_TotalFix = len(AOI_Q)
    x_TotalFix = len(AOI_X)
    y_TotalFix = len(AOI_Y)
    
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
    AOI_P = []
    AOI_Q = []
    AOI_X = []
    AOI_Y = []

    
    #loop through the gambles indexes pairs and add them to a data       
    trials = get_trials_indexes(et)
    for f in trials: 
        #Using the tuple, use start index and end index to create a trial
        op =  get_trial_from_indexes(f)
        
        #Get a list of fixations of the current  trial

        fixations = get_fixations(op) 


        #Loop though the fixations
        for f in fixations:
            endx = f[3]
            endy = f[4]
            duration = f[2]
            
            # Determine in which AOI should the fixation be
            if 800  <= endx <= 1000 and 400 <= endy <= 600: # AOI P
                AOI_P.append(duration)
            elif 800 <= endx <= 1000 and 400 <= endy <= 600: # AOI Q*
                AOI_Q.append(duration)
            elif 800 <= endx <= 1000 and 600 <= endy <= 800: # AOI X
                AOI_X.append(duration)
            elif 800 <= endx <= 1000 and 600 <= endy <= 800: # AOI Y*
                AOI_Y.append(duration)

    #When we processed all the fixations then get the meansfix and totalfix for all
                                                                # the AOIs
    result = get_AOI_MT(AOI_P,AOI_Q,AOI_X,AOI_Y)
    
    return result
    #Subject finished


    



#Main       
result = main()

subject_15 = pd.DataFrame([result])
subject_15.columns = ["p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix"]

end = time.time()  
print("Program ended and it took: ",end-start)

#Export the dataset
subject_15.to_csv("Subject-AOIs.csv", index = False)





