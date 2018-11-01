import time
import pandas as pd
import numpy as np
from detectors import *
import re
import os



#Misc
def get_row_values(i,df,column_names):
    column_names = list(self.df.columns.values)
    temp_list = []
    for column in column_names:
        value = et.at[i,column] # The value at the current cell
        temp_list.append(value)

    return temp_list

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def get_subject_nr(subject_path): # Return the subject number from the file name
    return int(''.join(filter(str.isdigit, subject_path)))


def get_subjects(): # Gets a list where every element is the subject beh and their et data
    fullList = os.listdir()
    
    subject_numbers = {}
    subject_pairs = []

    for v in fullList:
        if "subject" in v:
            try:
                nr = get_subject_nr(v)
                subject_numbers[v]=nr
            except ValueError:
                print("ERROR ! Check if you have any file named subject without number")
                
                
    for key, value in subject_numbers.items():
        for key2,value2 in subject_numbers.items(): #Loop though the dictionary
            if key != key2: # If key are named differently
                if value == value2:#If they have the same value
                    if (key2,key) not in subject_pairs:
                        subject_pairs.append((key,key2))
                        #print((key,key2)) 
                        
            
    
                       #print(key,key2)
    return subject_pairs

#Fix functions
def replace_line(subject_path,badIndex): #Replace or remove the bad line of the file using the index
    
    #First open the current bad file and search for the error line
    f=open(subject_path,"r")

    data=f.readlines() 
    badLine = data[badIndex-1]
    del f
    
    if "gamble" in badLine: #If that bad line contains gamble then try to replace
        print("REPLACING")
        template = "    "+"\t"+"gamble"
        data[badIndex-1] = template
        with open(subject_path, 'w') as fileG:
            fileG.writelines(data)
            del fileG

    else: # If is not gamble then remove it
        print("REMOVING")
        template = "    "											
        data[badIndex-1] = template
        with open(subject_path, 'w') as fileB:
            fileB.writelines(data)
            del fileB
    

def get_badIndex(e): # Get the index as integer from error
    result = [f for f in re.split("[^0-9]", str(e)) if f != ''] 
    return (max(map(int, result)))


        
def check_et(et_path,subject_nr): # This function will verify the et file for any problems
    temp = False 
    while temp == False: # Continuosly try to read the file, if worked then stop otherwise try to fix it
        try:
            et = pd.read_csv(et_path,sep="\t",skiprows=17)
            temp = True
        except pd.errors.ParserError as e:
            print(e)
            print("Subject %d has a bad line, trying to fix."%subject_nr)
            badIndex = get_badIndex(e) # Get the index of where the error was
            replace_line(et_path,badIndex) # Replace the error line with good or bad
            temp = False
    return et

def get_fixations(df): #GEt the fixations for the given dataframe
    
    dfListX = df["GazePointX"].tolist()
    dfListY = df["GazePointY"].tolist()
    dfListT = df["TimeStamp"].tolist()
    
    dfListX =list(map(float, dfListX))
    
    dfListY =list(map(float, dfListY))
    dfListT =list(map(float, dfListT))

    
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

def get_AOIs(fixations,x_loc):
    AOI_p = []
    AOI_x = []
    AOI_q = []
    AOI_y = []
    for f in fixations:
            endx = f[3]
            endy = f[4]
            duration = f[2]
            
            #AOI 1 coordonates
            a1x_up = 944
            a1y_up = 524
            a1x_low = 656
            a1y_low = 236
            
            #AOI 2 coordonates
            a2x_up = 1264
            a2y_up = 524
            a2x_low = 976
            a2y_low = 236
            #AOI 3 coordonates
            a3x_up = 944
            a3y_up = 844
            a3x_low = 656
            a3y_low = 556
            #AOI 4 coordonates
            a4x_up = 1264
            a4y_up = 844
            a4x_low = 976
            a4y_low = 556
            
            
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
        #
    AOIs = get_AOI_MT(AOI_p,AOI_q,AOI_x,AOI_y)
    return AOIs
                    
        
                    
#Classes       
class Subject:
    def __init__(self,et_file_path,beh_file_path):
        self.et = et_file_path
        self.beh = beh_file_path
        self.subject_nr = get_subject_nr(et_file_path)
        self.read_clean_files()

    
    def read_clean_files(self):
        #Load and create the dataframes
        self.et = check_et(self.et,self.subject_nr) #Clean et of any possible errors and return the dataframe - et had problems with the file
        self.beh = pd.read_csv(self.beh)
        self.beh = self.beh.loc[:,["CBcond","Gamble","domain","X_location","risk_selected","response_time"]]

    def get_trials(self):
        #Loop though the indexes and take only the indexes the start and end gamble
        trials = []
        trials_indexes = [] # Here we store the tuples with the start-end indexes
        ph = 0 #A place holder for start-gamble index
        
        temp_values = []
        ####
        column_names = list(self.et.columns.values) #Check later!!!!!!!!
        self.et = self.et.loc[:,["TimeStamp","Event","GazePointX","GazePointY"]]
        #####
        for i in self.et.index:          
            #row_values = get_row_values(i,self.et,column_names)      
            val = self.et.at[i,"Event"] # The value at the current cell
            if "gamble" in str(val): 
                temp_values.append(val)
                if ph != 0:   # if ph !=0 then ph is start-gamble
                    trials_indexes.append((ph,i)) #Append the ph and the current index
                    ph = 0 #Reset
                else: # If ph is 0 then take the index of start-gamble
                    ph = i 
                    
        if len(trials_indexes) < 150:
            print("Subject nr",self.subject_nr)
            find_bad(temp_values)           
        #print(self.subject_nr,len(trials_indexes))           
        for trial_index in trials_indexes:
            trials.append(pd.DataFrame(self.et.iloc[(trial_index[0]+1):trial_index[1]]))
            
        return trials
 
    

    def get_beh_data(self,current_trial_index):
        x_loc = self.beh.at[current_trial_index,"X_location"]
        response_time = self.beh.at[current_trial_index,"response_time"]
        domain = self.beh.at[current_trial_index,"domain"]
        gamble_nr = self.beh.at[current_trial_index,"Gamble"]   
        risk = self.beh.at[current_trial_index,"risk_selected"]
        return x_loc,response_time,domain,gamble_nr,risk
        
    def get_output(self):# this should be main method to return the dataframe for this current subject with all of his trials processed
        
        
        trials = self.get_trials()
        print(len(trials))
        subject_table = []
        for i,trial in enumerate(trials):
            beh_data = self.get_beh_data(i)
            fixations = get_fixations(trial)
            AOIs = get_AOIs(fixations,beh_data[0])       
            
            
            row = [self.subject_nr] + [beh_data[3]] + [beh_data[2]] + AOIs + [beh_data[4]]+[beh_data[1]]
            
            subject_table.append(row)
            
        return subject_table
            

def find_bad(bList):
    print(len(bList))
    sM = [] 
    for v in bList:
        sM.append(get_subject_nr(v))
        
    for n in sM:
        cr = sM.count(n)
        if cr < 4:
            print(n)
        
        
        




def main():

    # Get the list of subjects from the current folder
    subject_list = get_subjects()
    finalDf = pd.DataFrame() 

    #subject = Subject('subject-16_TOBII_output.tsv','subject-16.csv')
    #subject_raw = subject.get_output()
    #subject = pd.DataFrame(subject_raw)
    #subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
    
    
    #Loop though the list of subjects to create the subjects
    for subject_files in subject_list:
        #print(subject_files[1],subject_files[0])
        subject = Subject(subject_files[1],subject_files[0])
        subject_raw = subject.get_output()
        subject = pd.DataFrame(subject_raw)
        subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
        finalDf = pd.concat([finalDf, subject])
    

    return finalDf




#Start the program
start = time.time() 


FinalOutput = main()

#Export the dataset
FinalOutput.to_csv("Final-Output.csv", index = False)

end = time.time()  
print("Program ended and it took: ",end-start)


