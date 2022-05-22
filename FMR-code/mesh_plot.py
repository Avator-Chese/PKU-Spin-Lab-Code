from matplotlib.font_manager import FontProperties
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
import fnmatch
#This one is used to compared if the FMR works well
# folder = 'D:\\ShareCache\\郭亮亮_2101110192\\科研\\All-Data\\FMR\\PPMS-data\\20210814-Si-Py(sample-2021-08-11)'




# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211219(CrO2 150nm)\New measure after make angle\[011]\PNA-40GHz'
folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20220520(CrO2 150nm-2)\[010]\PNA-40GHz'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20211219(CrO2 150nm)\[010]\PNA-40GHz'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20220115(CoFeB of Zhu with higher power)\Sample-Y13\PNA'
# folder = r'D:\ShareCache\郭亮亮_2101110192\科研\All-Data\FMR\PPMS-data\20220114(CoFeB for Zhu CAS)\Sample-YI3\PNA'

files=os.listdir(folder)

files=[]
all_files = os.listdir(folder)
for file in all_files:
    if os.path.splitext(file)[1]=='.txt':
        files.append(file)


file_form = 'Ist_T=ValueK_-5dBm_H=15000Oe_S21.txt'
T = []
for i in files:
    T.append(ast.literal_eval(re.findall(r'(\d+\.?\d*)K', i)[0]))
T.sort(reverse=True)
T_new = T.copy()
print(T_new)



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
data = sqa.fmr_load_data(folder + '\\' + filename)

# data=data.head(int(len(data)*1/6))

sqa.fmr_mesh_dataframe(data)

# data.to_excel(r'D:\ShareCache\郭亮亮_2101110192\科研\Projects\1.xlsx')
plt.title(f'The temperature is {choose_T} K')


# plt.xticks(fontproperties="Arial",size=14)
# plt.yticks(fontProperties='Arial',size=14)
# from matplotlib.pyplot import MultipleLocator

# ax=plt.gca()
# ax.xaxis.set_major_locator(MultipleLocator(4000))

# plt.tick_params(axis='both', labelsize=14, length=7)
# plt.savefig(r'D:\ShareCache\郭亮亮_2101110192\科研\Projects\FMR.png',
#             format='png',
#             dpi=1200)
plt.show()