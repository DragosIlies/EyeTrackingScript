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
beh = beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected"]]
et = et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]

et = et.drop(et[(et.GazePointX < 0) & (et.GazePointY < 0)].index)
et = et.reset_index(drop=True)



def get_fixations(df):
    dfListX = df["GazePointX"].tolist()
    dfListY = df["GazePointY"].tolist()
    dfListT = df["TimeStamp"].tolist()
    
    results = fixation_detection(dfListX, dfListY, dfListT, missing=0.0, maxdist=25, mindur=16.7)
    fixations = results[1]
    return fixations
    
    
    
    

def get_gambles():
    test = []
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
        op = pd.DataFrame(et.iloc[first__gamble_index:last_gamble_index])
        
    ###############################
    
    
    
    ##############################
    
    
    
    
    
    #############################
        #print(op.at[first__gamble_index,"Event"])
        fixations = get_fixations(op) # The fixations for the particular trial
        
        
        test.append(fixations)

    
    return test #Return the database with all the gambles

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
    
       
rez = get_gambles()

AOI_X = 0
AOI_Y = 0
AOI_P = []
AOI_Q = 0

#Loop though the trials
for t in rez:
    #Loop though the fixations
    print("New trial")
    print(" ")
    print("Fixations")
    print(" ")
    for f in t:
        endx = f[3]
        endy = f[4]
        duration = f[2]
        
        if 900 <= endx <= 1100:
            if 400 <= endy <= 500:
                AOI_P.append(duration)
                
        
        print(f[3],f[4])
    
    print(" ")
    


print(mean(AOI_P))

end = time.time()  
print("Program ended and it took: ",end-start)
#Export the dataset
#op.to_csv("output_file.csv",index = True)





