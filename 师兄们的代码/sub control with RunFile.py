# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 09:47:57 2020

@author: ppms
"""

from sqm import *
import multiprocessing as mp
import os
import time
import re
import numpy as np


ppms=PPMS()
vna=VNA()
k6221=K6221()
sr830=SR830()

#vna.set_on_off('on')
#vna.set_span(fcent=11.6e9,fspan=0.2e9,power=0)
#vna.fmr_init(points=1601,freq_start=1e9,freq_stop=20e9,power=-25,IF=1e3,sweep_time=0)
#vna.auto_scale()
#s21=vna.ReadLine(1)
#s=s21.split(',')
#print s[3]
#vna.set_on_off('off')

'''
### SET K6221
Is=0         ### in A
Ie=-200e-6
Iac=10e-6
k6221.set_DCoffset(Is)
#k6221.set_ACamp(Iac)
'''

##### FOR DIFFERENT MAGNETIC FIELD DETECTION ######

TempPoints=[4]
FreqPoints=np.arange(1,20,1)
#FreqPoints=[11,12,13,14,15,16,]
HPoints=[1200,2300]
print(FreqPoints)

######   set PPMS  ######
#ppms.setField(0,100,0,stable=0)
#ppms.setTemperature(20,2)
#time.sleep(600)

Temp=4  # in K
H=0  # in Oe
#ppms.setTemperature(Temp,2)
#time.sleep(100)
ppms.setField(H,100,0,stable=0)
#time.sleep(60)

######   set VNA  ######
fres=1   #GHz
fspan=0.2e9
power=0
vna.set_on_off('on')
vna.set_span(fcent=fres*1e9,fspan=0.2e9,power=-25,points=201,ave=16,IF=10e3,sweep_time=0)
vna.auto_scale()
vna.auto_scale()

#######  set K6221, current in mA  ######
Is=-500e-6
Ie=500e-6
Istep=10e-6
di=5e-6

#######  set SR830  ######
sr830.ClearBuffer()

real_plot_another_process(plot_row_number=1,columns_list=[])
for Hs in HPoints:
    FilePath='E:\\Cai Ranran\\FMR driven Josephson Effect\\Nb(100)-Py(30)-Nb(100)\\s2\\20201028-FMR driven\\4K\\'+str(Hs)+'Oe\\step 1G'
    if not os.path.exists(FilePath):
        os.makedirs(FilePath)
        
    ppms.setField(Hs,100,0,stable=0)
    print(('magnetic field is '+str(Hs)+'Oe'))
    time.sleep(100)
    i=0
    for freq in FreqPoints:
        #for P in PowPoints:
        i=i+1
        #filename=str(i)+'- '+str(Temp)+'K '+str(H)+'Oe '+str(fres)+'GHz_0.2G '+str(P)+'dBm_dvdi.txt'  
        filename=str(i)+'- '+str(Temp)+'K '+str(Hs)+'Oe '+str(freq)+'GHz_1G 0dBm_dvdi.txt' 
        fp=os.path.join(FilePath,filename)
        vna.set_span(fcent=freq*1e9,fspan=fspan,power=power,points=201,ave=16,IF=10e3,sweep_time=0)
        #    vna.set_span(fcent=fres*1e9,fspan=fspan,power=P,points=201,ave=16,IF=10e3,sweep_time=0)
        #    vna.set_span(fcent=fres*1e9,fspan=fspan,power=P)
        vna.auto_scale()
        vna.auto_scale()
        print(('the RF set as: '+str(freq)+'G_'+str(fspan*1e-9)+'G_0dbm'))
        #    print('the RF set as: '+str(fres)+'G_'+str(fspan*1e-9)+'G_'+str(P)+'dbm')
        k6221.set_DCoffset(Is)   # in A
        print(('wait some time for more stable. '+time.ctime()))
        time.sleep(100)
        k6221.sweep_offset(pathfilename=fp,Istart=Is,Iend=Ie,ramp=Istep,dI=di)  
        time.sleep(100) 
    
print(('the measuremnent is over '+ time.ctime()))
vna.set_on_off('off')

ppms.setField(0,100,0,stable=0)
ppms.setTemperature(20,2)
#time.sleep(600)
'''

###### FOR JUST dV VS dI without microwave ######

TempPoints=[4]
FieldPoints=[0,400,1200,1600,2300]

print(FieldPoints)

######   set PPMS  ######

Temp=4  # in K
H=0 # in Oe
ppms.setTemperature(Temp,2)
time.sleep(300)
ppms.setField(H,100,0,stable=0)
time.sleep(10)


#######  set K6221, current in A  ######
Is=-600e-6
Ie=600e-6
Istep=10e-6
di=5e-6

#######  set SR830  ######
sr830.ClearBuffer()



real_plot_another_process(plot_row_number=1,columns_list=[])

i=0
for H in FieldPoints:
#for T in TempPoints:
    FilePath='E:\\Cai Ranran\\FMR driven Josephson Effect\\Nb(100)-Py(30)-Nb(100)\\s2\\20201028-FMR driven\\4K\\NO RF'
    if not os.path.exists(FilePath):
        
        os.makedirs(FilePath)
    ppms.setField(H,100,0,stable=0)
    time.sleep(60)
        
    i=i+1
    filename=str(i)+'- '+str(Temp)+'K '+str(H)+'Oe NO RF_dvdi.txt' 
    fp=os.path.join(FilePath,filename)

    k6221.set_DCoffset(Is)   # in A
    print('wait some time for more stable. '+time.ctime())
    time.sleep(10)
    k6221.sweep_offset(pathfilename=fp,Istart=Is,Iend=Ie,ramp=Istep,dI=di)  
    time.sleep(100) 

print('the measuremnent is over '+ time.ctime())
'''
