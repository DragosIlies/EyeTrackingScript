import time
import pandas as pd
import numpy as np
from detectors import *
import re
import os




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
            
def replace_line2(subject_path,badIndex,subject_nr): #Replace or remove the bad line of the file using the index
    
    
    print("Subuject is: ",subject_nr)
    #First open the current bad file and search for the error line
    f=open(subject_path,"r")

    data=f.readlines() 
    badLine = data[badIndex-1]
    #rint("Bubu: ",badLine)
    #print("Bubu 2: ",data[badIndex])
    
    del f
    
    if "carrot" in badLine: #If that bad line contains gamble then try to replace
        print("REPLACING")
        template = "    "+"\t"+"gamble"
        data[badIndex-1] = template
        
        with open(subject_path, 'w') as fileG:
            fileG.writelines(data)
            del fileG
    #### CARE MODIFIED QUICK
    else: # If is not gamble then remove it
        print("REMOVING")
        template = "    "+"\t"+"gamble"+"\t"
        template2 = "    "										
        data[badIndex-1] = template2
        #data[badIndex] = template2
        print("New line is :",data[badIndex-1])
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
            print("Subject %d has a bad line, trying to fix."%subject_nr)
            badIndex = get_badIndex(e) # Get the index of where the error was
            replace_line(et_path,badIndex) # Replace the error line with good or bad
            temp = False
    return et

def create_df(head,body):
    subject = pd.DataFrame(body)
    subject.columns = head
    
    return subject
def main():

    # Get the list of subjects from the current folder
    subject_list = get_subjects()
    finalDf = pd.DataFrame() 

    #subject = Subject('subject-16_TOBII_output.tsv','subject-16.csv')
    #subject_raw = subject.get_output()
    #subject = pd.DataFrame(subject_raw)
    #subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
    
    badS = []
    badHead = []
    #Loop though the list of subjects to create the subjects
    for subject_files in subject_list:
        subject_nr = get_subject_nr(subject_files[1])
        et = check_et(subject_files[1],subject_nr)
        for i in et.index:  
            val = et.at[i,"PupilSizeLeft"] # The value at the current cell
            print(val)
            if "gamble" in str(val):
                badS.append([subject_nr,i])

                '''
                print(val,i)
                replace_line2(subject_files[1],(i+19),subject_nr)
                val = 0
                print("Modified")
                '''
                
        #print(subject_files[1],subject_files[0])
    return create_df(["Subject nr","Bad index"],badS)
        





#Start the program
start = time.time() 


FinalOutput = main()


end = time.time()  
print("Program ended and it took: ",end-start)


