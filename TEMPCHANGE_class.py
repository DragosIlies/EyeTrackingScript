class Subject:
    def __init__(self,et_file,beh_file):
        self.et = et_file
        self.beh = beh_file
        self.subject_nr = get_subject_nr(et_file)
        self.read_files()

    
    def read_clean_files(self):
        #Try to make sure that that files are good!!!
        #Load and create the dataframes
        #Slice and take only what you need

    def get_list_trials(self):
        #get_trials_indexes 
        #Creaza o lista de seturi unde un set are valori - start si sfarsit indice pentru un trial - un set din lista reprezinta in trial (trebuie sa fie 150 de trials)

    def get_trial_from_indexes(self):
        #return a trial

    def get_beh_data(self,current_trial_index):
        x_loc = self.beh.at[current_trial_index,"X_location"]
        response_time = self.beh.at[current_trial_index,"response_time"]
        domain = self.beh.at[current_trial_index,"domain"]
        gamble_nr = self.beh.at[current_trial_index,"Gamble"]   
        risk = self.beh.at[current_trial_index,"risk_selected"]
        return x_loc,response_time,domain,gamble_nr,risk
        
    def get_ouput(self):# this should be main method to return the dataframe for this current subject with all of his trials processed



ex = Subject(5,6)

ex.get_f()