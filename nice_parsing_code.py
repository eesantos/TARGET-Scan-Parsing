# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:55:38 2019

@author: rober
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_excel('vertical_poition_ms.xlsx')   #importing dataframe

cols = df.columns.tolist()
# -----------------------------------------
#  convert df to a numpy array of times
#  and a numpy array of values
# -----------------------------------------
num_cols = int(len(df.columns))
even_cols = [x for x in range(num_cols) if x % 2 == 0]
odd_cols = [x for x in range(num_cols) if x % 2 == 1]

times_df = df.iloc[:,even_cols]
readings_df = df.iloc[:,odd_cols]

times_ar = np.transpose(times_df.to_numpy())
readings_ar = np.transpose(readings_df.to_numpy())

print(times_ar)
#print(readings_ar)
#np.save('test.npy', times_ar) # saving as numpy array

# -----------------------------------------
#  time normalization
# -----------------------------------------
base_ar = times_ar[:1,].tolist()[0]                     # assign the set of times that we compare everything to

for i in range(1,len(times_ar)):                        # looping through all the other sets of times
    index = 0                                           # set index to first time in set
    compare_ar = times_ar[i:(i+1)].tolist()[0]          # getting the next set of times  
    values_ar = readings_ar[i:(i+1)].tolist()[0] 
    while(index < len(base_ar)):                        # loop through each value in the times
        if (index == len(compare_ar)):                  # if compare list is shorter than base insert a zero end
            compare_ar.append(0)
            values_ar.append(0)
            index = index + 1
        elif (base_ar[index] < compare_ar[index] - 10):      # if compare list skips insert a zero
            compare_ar.insert(index, 0)
            values_ar.insert(index,0)
            index = index + 1
        elif (base_ar[index] > compare_ar[index] + 10):      # if base list skips delete time from compare list
            compare_ar.pop(index)
            values_ar.pop(index)
        else:                                           # the two times match
            index = index + 1
    compare_ar = compare_ar[:len(base_ar)]              # remove extra values from compare
    values_ar = values_ar[:len(base_ar)]
    times_ar[i:(i+1)] = compare_ar                      # puts the new times back into the times array
    readings_ar[i:(i+1)] = values_ar

times_ar = np.nan_to_num(times_ar)            # convers NANs to zero
tr_times_ar = np.transpose(times_ar)
tr_readings_ar = np.transpose(readings_ar)

print('check: how many zeros')
count = 0
for i in range(0,len(tr_times_ar)):  
    if (np.any(tr_times_ar[i:(i+1)]  == 0)):
        count = count + 1

print (count) 
print( tr_times_ar.shape)               # shape before zeros are deleted
print( tr_readings_ar.shape)

i = 0
while (i < tr_times_ar.shape[0]):                       # loop through rows
    if (np.any(tr_times_ar[i:(i+1)]  == 0)):            # if row contains zero delete
        tr_times_ar = np.delete(tr_times_ar,i,0)
        tr_readings_ar = np.delete(tr_readings_ar,i,0)
    else:                                               # if not, go to next row
        i = i+1

print( tr_times_ar.shape)
print( tr_readings_ar.shape)

times_ar = np.transpose(tr_times_ar)
readings_ar = np.transpose(tr_readings_ar) 

final_ar = readings_ar

for i in even_cols:
    index = int(i/2)
    insert_ar = times_ar[index:(index+1)].tolist()[0]
    final_ar = np.insert(final_ar, i, insert_ar, axis = 0)

final_ar = np.transpose(final_ar)

df = pd.DataFrame(data=final_ar,                #reverting back to dataframe - defining column labels
                  columns=cols)  

print(df)

#df.to_excel('final_vertical_position.xlsx')