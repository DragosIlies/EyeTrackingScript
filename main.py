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
    for i in et.index:
        val = et.at[i,"Event"]
        if "gamble" in str(val):       
            if ph != 0:   
                trials.append((ph,i))
                ph = 0 
            else:
                ph = i 
                
    for f in trials:
        first__gamble_index = f[0]+1 # take the first tuple value - start-gamble
        last_gamble_index = (f[1]) # take the second tuple value - end gamble
        op = op.append(et.iloc[first__gamble_index:last_gamble_index]) 
        
    op = op.drop(op[(op.GazePointX < 0) & (op.GazePointY < 0)].index)
    
    return op
    
    




 
start = time.time()           

op = get_gambles()


end = time.time()
print(end - start)

opListX = op["GazePointX"].tolist()
opListY = op["GazePointY"].tolist()
opListT = op["TimeStamp"].tolist()


results = fixation_detection(opListX, opListY, opListT, missing=0.0, maxdist=25, mindur=20)
fixations = results[1]






