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
import ast

# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211216(Nb-Py(30)-Nb-JJ device)\power=1dBm'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211219(CrO2 150nm)\Third measure after make waveguide angle\[01-1]'
folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20220520(CrO2 200nm)\[010]\PNA-40GHz'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211219(CrO2 150nm)\[010]\Detailed T'
# folder = 'C:\\Users\\aoubl\\Desktop\\FMR'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20210813-YBCO(sample-2021-08-11)'
files = os.listdir(folder)

files = []
all_files = os.listdir(folder)
for file in all_files:
    if os.path.splitext(file)[1] == '.txt':
        files.append(file)

# folder_back = 'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211219(CrO2 150nm)\back-signal'
# files_back = os.listdir(folder_back)

file_form = 'Ist_T=ValueK_-5dBm_H=15000Oe_S21.txt'
# file_back_form = 'Ist_T=ValueK_-5dBm_H=10000Oe_S21.txt'

T = []
for i in files:
    T.append(ast.literal_eval(re.findall(r'(\d+\.?\d*)K', i)[0]))
T.sort(reverse=True)
T_new = T.copy()

jud = 1
if jud == 0:
    print('You are using file\'s Temperature')
    choose_T = T[0]
    T = np.delete(T, 0)
elif jud == 1:
    print('You are using inputed Temperature')
    choose_T = str(input())
print('You are process ' + choose_T + 'K\'s data')

order = str(T_new.index(float(choose_T)) + 1)

filename = file_form.replace('Value', choose_T).replace('I', order)
data_measure = sqa.fmr_load_data(folder + '\\' + filename)


'''
#构造一个origin表格=========================================================================
table_lineshape_fit = sqa.origin_creat_table(f'{choose_T}K')
longname_unit_comment1 = [['sysmetrical height', '', ''],
                          ['resonance field', '', ''],
                          ['half linewidth', '', ''],
                          ['asysmetrical height', '', ''],
                          ['linear slope', '', ''], ['constant', '', '']]
#============================================================================================
'''
# filebackname = file_back_form.replace('Value', str(choose_T)).replace('I', order)
# data_back = sqa.fmr_load_data(folder_back + '\\' + filebackname)

n = 0
result = []
#Here is to choose the range of Frequency
#===============================================================
fre_range = [25E9, 40E9]
columns = data_measure.columns[:]
lowest_fre = float(columns[0])
delta_fre = float(columns[1]) - float(columns[0])
if fre_range[0] < lowest_fre:
    fre_range[0] = lowest_fre
#cutoff frequency用来在cut_fre之前取更多的频率点，便于作图
cut_fre = 13E9

low_index = int((fre_range[0] - lowest_fre) / delta_fre)
cut_index = int((cut_fre - lowest_fre) / delta_fre)

top_index = int((fre_range[-1] - lowest_fre) / delta_fre) + 1

More = 0
if fre_range[0] >= cut_fre:
    More = 0
if More == 1:
    choose_fre_before_cut = columns[low_index:cut_index:1]
    choose_fre_after_cut = columns[cut_index:top_index:2]
    choose_fre = np.append(choose_fre_before_cut, choose_fre_after_cut)
else:
    choose_fre = columns[low_index:top_index:2]

#================================================================

for i in choose_fre:
    frequency = float(i[1:])
    figure_path = folder + '\\' + filename.replace(
        '.txt', '-freq' + str(float(i[1:]) / 1e9) + 'GHz with_substract.png')
    a = sqa.fmr_select_frequency(data_measure, frequency)
    if a.index.values[-1] >= 10000:
        if frequency < float(choose_fre[-1]) / 2:
            a_range = a.head(int(len(a) / 2))
        else:
            a_range = a
    else:
        a_range = a
    absorb = a_range.values
    # b=sqa.fmr_select_frequency(data_back,frequency)
    # b=b.drop(b.tail(len(b)-len(a)).index)
    # a_new = a.values-b.values

    # a_new=sqa.substrate_background_from_one_curve(a.index.values,a.values)
    plt.title(f'The frequency now is {frequency/1e9} GHz')

    fitting_para = sqa.fit_one_curve(a_range.index.values, absorb)

    #print parameters
    print([n, 0], frequency)
    n = n + 1
    if sum(abs(fitting_para)) != 0:
        sqa.origin_get_array(table_lineshape_fit,
                             np.array(frequency, ndmin=2),
                             position=[n, 0],
                             longname_unit_comment=[['frequency(Hz)', '', '']])
        sqa.origin_get_array(table_lineshape_fit,
                             np.array(fitting_para, ndmin=2),
                             position=[n, 1],
                             longname_unit_comment=longname_unit_comment1)
        result.append([frequency] + fitting_para.tolist())
