import time
import pandas as pd
import numpy as np
from detectors import *
import re
import os
from Classes import Trial,Subject


def get_subject_nr(subject_path): # Return the subject number from the file name(string)
    return int(''.join(filter(str.isdigit, subject_path)))


def get_subjects(): # Gets a list where every element is the subject beh and their et data
    
    fullList = os.listdir() # Get all the files in the current folder
    
    subject_numbers = {}
    subject_pairs = []

    # Loop though the files and take the ones with subject along with the subject number
    for file in fullList:
        if "subject" in file:
            try:
                nr = get_subject_nr(file) # Get the subject number
                subject_numbers[file]=nr # Add the file and it's number to the dictionary
            except ValueError:
                print("ERROR ! Check if you have any file named subject without number")
                
    #Combine the subject beh and et data by finding the common subject number
    
    for file,number in subject_numbers.items(): # Nested loop to compare each file betwwen them and append the ones with same object number
        for file_2,number_2 in subject_numbers.items():
            if file != file_2: # If key are named differently
                if number == number_2:#If they have the same value
                    if (file_2,file) not in subject_pairs:
                        subject_pairs.append((file,file_2)) # Append the files with same subject number

    return subject_pairs


def main():

    # Get the list of subjects from the current folder
    subject_list = get_subjects()
    final_output = pd.DataFrame() 

    
    #Loop though the list of subjects to create the subjects
    for subject_files in subject_list:
        subject = Subject(subject_files[1],subject_files[0],get_subject_nr(subject_files[1])) #Create the subject object with the et and beh files
        subject_raw = subject.get_output()   # Get a table with all the information from the table
        # Create an empty table using pandas and set the column names
        subject = pd.DataFrame(subject_raw) 
        subject.columns = ["Subject","Gamble","Domain","p_Meanfix","q_Meanfix","x_Meanfix","y_Meanfix","p_TotalFix","q_TotalFix","x_TotalFix","y_TotalFix","risk_selected","response_time"]
        #Add the new table with the old one by combining them using pandas
        final_output = pd.concat([final_output, subject])
    

    return final_output # Return the main table output




#Start the program
start = time.time() 


FinalOutput = main()

#Export the table to a csv file
FinalOutput.to_csv("Final-Output.csv", index = False)

end = time.time()  
print("Program ended and it took: ",end-start)


