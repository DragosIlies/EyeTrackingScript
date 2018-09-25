import time
import pandas as pd
import numpy as np
from detectors import *

    
#Load and create the dataframes
et = pd.read_csv("eye_tracking_data.csv")
beh = pd.read_csv("behavioural_data.csv")
op = pd.DataFrame()

#Slice it and take what we need
beh = beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected"]]
et = et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]



def get_gambles():
    trials = [] # Here we store the tuples
    ph = 0 #A place holder for start-gamble index
    op = pd.DataFrame() 
    #Loop though the indexes and take only the indexes the start and end gamble 
    for i in et.index:
        val = et.at[i,"Event"] # The value at the current cell
        if "gamble" in str(val):       
            if ph != 0:   # if ph !=0 then ph is start-gamble
                trials.append((ph,i)) #Append the ph and the current index
                ph = 0 #Reset
            else: # If ph is 0 then take the index of start-gamble
                ph = i 
                
    #loop through the gambles indexes pairs and add them to a data            
    for f in trials: 
        first__gamble_index = f[0]+1 # take the first tuple value - start-gamble
        last_gamble_index = (f[1]) # take the second tuple value - end gamble
        op = op.append(et.iloc[first__gamble_index:last_gamble_index]) 
        
    op = op.drop(op[(op.GazePointX < 0) & (op.GazePointY < 0)].index)
    
    return op #Return the database with all the gambles


    
start = time.time()           
op = get_gambles()
end = time.time()  

#Export the dataset
op.to_csv("output_file.csv",index = True)





