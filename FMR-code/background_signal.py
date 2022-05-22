import numpy as np
import pandas as pd
import re
import os
import sys
import matplotlib.pyplot as plt
import sys
# sys.path.append('E:\\python\\python FMR_analyse\\FMR__Songqi')
import sqa
import statsmodels.api as sm

folder = 'D:\\ShareCache\\郭亮亮_2101110192\\科研\All-Data\\FMR\\PPMS-data\\20210925(sample-no-patterned)'
files = os.listdir(folder)

folder_back = 'D:\\ShareCache\\郭亮亮_2101110192\\科研\\All-Data\\FMR\\PPMS-data\\FMR-background-signal'
files_back=os.listdir(folder_back)

file_form = 'Ist_T=ValueK_-5dBm_H=10000Oe_S21.txt'

T=[]
for i in files:
    T.append(int(re.findall(r'(\d+)K',i)[0]))
T.sort(reverse=True)
T_new=T.copy()

jud = 1
if jud == 0:
    print('You are using file\'s Temperature')
    choose_T = T[0]
    T = np.delete(T, 0)
elif jud == 1:
    print('You are using inputed Temperature')
    choose_T = int(input())
print('You are process ' + str(choose_T) + 'K\'s data')

order=str(T_new.index(choose_T)+1)
filename=file_form.replace('Value',str(choose_T)).replace('I',order)

data_measure=sqa.fmr_load_data(folder+'\\'+filename)
data_back=sqa.fmr_load_data(folder_back+'\\'+filename)

n = 0
result = []
#Here is to choose the range of Frequency
#===============================================================
fre_range = [0E9, 20E9]
columns = data_measure.columns[:]
lowest_fre = float(columns[0])
delta_fre = float(columns[1]) - float(columns[0])
if fre_range[0] < lowest_fre:
    fre_range[0] = lowest_fre
low_index = int((fre_range[0] - lowest_fre) / delta_fre)
top_index = int((fre_range[-1] - lowest_fre) / delta_fre) + 1
choose_fre = columns[low_index:top_index]
#================================================================
for i in choose_fre:
    frequency = float(i[1:])
    figure_path = folder + '\\' + filename.replace(
        '.txt', '-freq' + str(float(i[1:]) / 1e9) + 'GHz with_substract.png')
    a = sqa.fmr_select_frequency(data_measure,
                                 frequency) 
    b= sqa.fmr_select_frequency(data_back, frequency)
    b[5000:]=0
    a_new=a.values-b.values
    plt.title(f'The frequency now is {frequency/1e9} GHz')

    fitting_para = sqa.fit_one_curve(a.index.values, a_new)
