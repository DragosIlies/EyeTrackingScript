class Trial:
    def __init__(self,trial_start_index,trial_end_index,beh_dataframe,subject_nr,current_trial_nr):
        self.index_start = trial_start_index
        self.index_end = trial_end_index
        self.beh = beh_dataframe
        self.subject_nr = subject_nr
        self.current_trial_nr = current_trial_nr

    def get_trial_from_indexes(self):
        first_gamble_index = self.index_start+1 # take the first tuple value - start-gamble
        last_gamble_index = self.index_end # take the second tuple value - end gamble
        return pd.DataFrame(et.iloc[first_gamble_index:last_gamble_index])

    def get_beh_data(self):
        x_loc = self.beh.at[self.current_trial_nr,"X_location"]
        response_time = self.beh.at[self.current_trial_nr,"response_time"]
        domain = self.beh.at[self.current_trial_nr,"domain"]
        gamble_nr = self.beh.at[self.current_trial_nr,"Gamble"]   
        risk = self.beh.at[self.current_trial_nr,"risk_selected"]
        return x_loc,response_time,domain,gamble_nr,risk

        


