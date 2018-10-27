# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 13:59:00 2018

@author: D
"""



class Trial():
    def __init__(self,start_index,end_index,et):
        self.trial_df = create_df(start_index,end_index,et)
        
    def create_df(start_index,end_index,et):
        return pd.DataFrame(et.iloc[(start_index+1):end_index])