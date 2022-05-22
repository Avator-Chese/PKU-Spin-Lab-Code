# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 19:50:43 2016

@author: ppms
"""


from sqm import *
import multiprocessing as mp
import os
import time
import re
import numpy as np


'''
#Four Point IV measurement 2002 2400
ppms=PPMS()
TemperaturePoint=[2]

for Temp in TemperaturePoint:
    ppms.SetPPMSTemp(Temp)
    time.sleep(20)

    print 'wait 600s to let the temperature more stalbe'

    FileName='FourPointPtCalibrationOnPunkWait600STemp'+str(Temp)+'KIV'+'.txt'    
    FourPointIVCurev(os.path.join(FilePath,FileName)) 
'''

'''
#Spin Pumping 
folder='E:\\YYY\\20180505\\BiSe-LCO\\#1' #.replace('\\','\\')  # take care not \  should be /
#NamePrefix='test90_3'
#var=[300,275,250,225,200,175,150,125,100,75,50,25,10]
#var=[10]#25,50,75,100,125,150,175,200,225,250,275,300]
var=[8E9,7E9,6E9,5E9,4E9,3E9]
#var=[-2.5,-5,-7.5,-10,-12.5,-15,-17.5,-20]
frequency=7
temperature=50
#refreq=17.777

unit='Hz'
amplifier=1
#temperature=[300]
ppms=PPMS()
#figure=plt.figure()
i=0
#k2002=K2002()
sr830=SR830()
modulation_freq=sr830.get_freq()
#k2400=K2400()
vna=VNA()
vna.set_on_off('on')
#var.reverse()
vna.spin_pumping_init(power=-25,freq_cent=frequency*1e9)
real_plot_another_process(plot_row_number=2)
NameSuffix=str(modulation_freq)+'Hz_@0dBm_50K_AC'#+'modul_freq'+modulation_freq
for temp in var:
    i=i+1
    print temp,unit   
    ppms.setTemperature(temperature)
    #time.sleep(600)
    #k2400.k2400.write(':sour:volt '+str(temp))
    #time.sleep(600)
    print 'temperature is ok, please wait 5 mins for more stable',time.ctime()
    vna.SetFreqCenter(temp)
    time.sleep(100)
#    time.sleep(0)
    #axes=plt.subplot(4,4,i)
    #axes.set_title(str(temp)+unit)  
    #time.sleep(600)
    vna.set_power(0)
    time.sleep(200)
#    SpinPumingDC2002(filename=os.path.join(folder,str(temp)+unit+'_'+NameSuffix+'_'+str(i)+'.txt'),StartMag=2000,Rate=8,amplifier=amplifier)
#    SpinPumingDC2002(filename=os.path.join(folder,str(temp)+unit+'_'+NameSuffix+'_'+str(i)+'.txt'),StartMag=-2000,Rate=8,amplifier=amplifier)
    SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+'_'+NameSuffix+'_'+str(i)+'.txt'),StartMag=5000,StopMag=0,Rate=5,amplifier=amplifier)
    SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+'_'+NameSuffix+'_'+str(i)+'.txt'),StartMag=-5000,StopMag=-0,Rate=5,amplifier=amplifier)
    ppms.setField(0,100,0,stable=0)  # set magnetic field persistent
    vna.set_power(-25)
vna.set_power(-25)
vna.set_on_off('off')
#ppms.setTemperature(300)
'''


'''
#Four Point IV measurement 2002 2400__set V

ppms=PPMS()

#TemperaturePoint=[10,20,30,40,50,60,70,80,90,100,125,150,175,200,225,250,275,300]
TemperaturePoint=[300]
#TemperaturePoint=[10.8,10.6,10.4,10.2,10,11.8,11.5,11.2,11]
fp='E:\\YYY\\20170930\\10-15-10 RT'
IV_info='I79_V108'
f=open(os.path.join(fp,IV_info+'R_setV_5mV.txt'),'a')
f.write('Temperature(k),Resistance\n')
real_plot_another_process()
for Temp in TemperaturePoint:    

    ppms.setTemperature(Temp,2)
    time.sleep(500)
    
    print 'wait 500s to let the temperature more stalbe',time.ctime()

    FileName=''+str(Temp)+'K_'+IV_info+'.txt'    
    StartV=-5e-3
    EndV=5e-3
    step=5e-4
    
    R=FourPointIVCurveSetV(os.path.join(fp,FileName),StartV=0,EndV=StartV,StepV=-1*step)
    f.write(str(Temp)+','+str(R)+'\n')
    R=FourPointIVCurveSetV(os.path.join(fp,FileName),StartV=StartV,EndV=EndV,StepV=step)
    f.write(str(Temp)+','+str(R)+'\n')
    R=FourPointIVCurveSetV(os.path.join(fp,FileName),StartV=EndV,EndV=0,StepV=-1*step)
    f.write(str(Temp)+','+str(R)+'\n')
       
f.close()
#ppms.setTemperature(20)
'''



'''
#Four Point IV measurement 2002 2400__SET I

ppms=PPMS()

#TemperaturePoint=[20,25,30,35,40,50,60,70,80,90,100,125,150,175,200,225,250,275,300]
#TemperaturePoint=[300,275,250,225,200,175,150,125,100,90,80,70,60,50,40,35,30,25,20,10]#,19,18,17,16,15,14.5,14,13.5,13,12.8,12.5,12,11.5,11]
TemperaturePoint=[300]
fp='E:\\YYY\\20171220\\R-T\\Nb-Py-Nb\\3nm'
IV_info='I107_V89'
f=open(os.path.join(fp,IV_info+'_2mA.txt'),'a')
f.write('Temperature(k),Resistance\n')
real_plot_another_process()
for Temp in TemperaturePoint: 
    
    if Temp>15:
        speed=15
        setI=2e-3
    elif Temp<15:
        speed=2
        setI=10e-6
        
    ppms.setTemperature(Temp,speed)
    time.sleep(5)
    
    print 'wait 1200s to let the temperature more stalbe',time.ctime()

    FileName=''+str(Temp)+'K_'+IV_info+'.txt'    
    StartI=-setI
    EndI=setI
    step=setI/10
    
    R=FourPointIVCurveSetI(os.path.join(fp,FileName),StartI=0,EndI=StartI,StepI=-1*step)
    f.write(str(Temp)+','+str(R)+'\n')
    R=FourPointIVCurveSetI(os.path.join(fp,FileName),StartI=StartI,EndI=EndI,StepI=step)
    f.write(str(Temp)+','+str(R)+'\n')
    R=FourPointIVCurveSetI(os.path.join(fp,FileName),StartI=EndI,EndI=0,StepI=-1*step)
    f.write(str(Temp)+','+str(R)+'\n')
       
f.close()
#ppms.setTemperature(20)
'''

'''
#time.sleep(1200)   # wait for 20mins 
#print 'wait 1200s to let the temperature more stalbe',time.ctime()
#four point sweep T

endT=20
rate=1      # k/min
setI=1e-6   # A
SweepTMeasureR('E:\\YYY\\20170930\\10-15-10 RT\\20K--2K.txt',endT,rate,setI)
'''


'''
# Two Point IV measurement 2400 only
FilePath='E:\\Cai Ranran\\FMR driven Josephson Effect\\20200801-Py 20nm\\silver2 T-dep'                                                            
ppms=PPMS()
k2400=K2400()
TemperaturePoint=[188]
#TemperaturePoint=[10]
#skype=Skype()
#TemperaturePoint=[300]
real_plot_another_process(plot_row_number=2)
filenumber='I1314V1314_R-Nb'
for Temp in TemperaturePoint:
    ppms.setTemperature(Temp)
    print 'wait 120s to let the temperature more stalbe' 
    time.sleep(2)
    FileName=filenumber+'.txt'
    R=k2400.IVCurve_sourceV(os.path.join(FilePath,FileName),StartV=-2e-1,EndV=2e-1,StepV=1e-2)
    f1=open(os.path.join(FilePath,filenumber+'0.2V'+'.txt'),'a')
    f1.write(str(Temp)+','+str(R)+'\n')
    f1.close()
'''


'''
#sweep T get R 2400
ppms=PPMS()
k2400=K2400()
temp_des=20
ppms.setTemperature(temp_des,rate=10,stable=0)
#time.sleep(1800)
#ppms.SetPPMSTemp(300,Rate=2,stable=0)
Temp=ppms.getPPMSStatus()[0]
print Temp
filename='E:\\Qi\\TI YIG\\4 0.25\\Resistance\\temperature dependence 2\\RT_2terminal'
f=open(filename,'a')
global COLUMNS,DATA
COLUMNS='T,R\n'
f.write(COLUMNS)
f.close()
real_plot_another_process(plot_row_number=3,columns_list=[])
while not abs(float(Temp)-temp_des)<0.1:
    #k2400.k2400.write(':sour:volt '+str(0.001))
    #time.sleep(1)
    R=k2400.k2400.query(':measure:res?').split(',')[2]
    time.sleep(0.4)
    #k2400.k2400.write(':sour:volt '+str(0))
    #R=float(VIpoint[0])/float(VIpoint[1])
    Temp=ppms.getPPMSStatus()[0]
    DATA=str(Temp)+','+str(R)+'\n'
    f=open(filename,'a')
    f.write(DATA)
    f.close()
    print 'Temperature is '+str(Temp)+'k'+'Resistance is '+str(R)+'ohm'

#ppms.setTemperature(300,rate=10,stable=1)
'''




'''
# T dependence of S21 and impedence

FilePath='E:\\Qi\\Prf Wang Nanlin\\LaAgSb\\Sample on waveguide tight loose'
ppms=PPMS()
vna=VNA()
TemperaturePoint=[10,15,20,30,40,50,60,70,80,90,100,125,150,175,200,225,250,275,300]

TemperaturePoint2=[TemperaturePoint[-i-1] for i in range(len(TemperaturePoint))]
f1=open(os.path.join(FilePath,'S21.txt'),'a')
f2=open(os.path.join(FilePath,'R1.txt'),'a')
f3=open(os.path.join(FilePath,'R2.txt'),'a')
freq=vna.GetFreq()
f1.write('freq,'+freq)
f2.write('freq,'+freq)
f3.write('freq,'+freq)
f1.close()
f2.close()
f3.close()
for Temp in TemperaturePoint:
    ppms.setTemperature(Temp)
    print 'wait 600s to let the temperature more stalbe'
    time.sleep(600)
    f1=open(os.path.join(FilePath,'S21.txt'),'a')
    f2=open(os.path.join(FilePath,'R1.txt'),'a')
    f3=open(os.path.join(FilePath,'R2.txt'),'a')
    s21=vna.ReadLine(1)
    R=vna.ReadLine(2).split(',')
    R1=','.join([R[i*2] for i in range(1601)])
    R2=','.join([R[i*2+1] for i in range(1601)])
    
    f1.write(str(Temp)+','+s21)
    f2.write(str(Temp)+','+R1+'\n')
    f3.write(str(Temp)+','+R1+'\n')
    
    f1.close()
    f2.close()
    f3.close()
      
    
    print Temp
'''

'''
# Four-point contact to detect R-H curve via K6221-2182A delta mode

ppms=PPMS()
k6221=K6221()

init_H=-2000
en,d_H=2000
H_ramp=20
I_resource=1e-3
delta_count='INF'

FilePath='E:\\YYY\\20190604\\TIG\\2nd TIG-Au-TIG\\R-T\\30-8-15'
if not os.path.exists(FilePath):
    os.makedirs(FilePath)
filename='30-8-15 '+ str(init_H)+'Oe to '+str(end_H)+'Oe '+str(H_ramp)+'Oe-s '+'I='+str(I_resource*1e6)+'uA 0degree'+'.txt'
fp=os.path.join(FilePath,filename)

k6221.ARM_Delta(I_resource,delay=0.002,delta_count='INF')
real_plot_another_process(plot_row_number=1,columns_list=[])
time.sleep(5)
#k6221.R_text_init(fp)
k6221.Delta_R_H(fp,init_H,end_H,H_ramp)

'''
'''
# Four-point contact to detect R-T curve via K6221-2182A delta mode

ppms=PPMS()
k6221=K6221()

init_T=300
set_T=10
T_ramp=5
I_resource=1e-3
delta_count='INF'
H=20

FilePath='E:\\YYY\\20190604\\TIG\\2nd TIG-Au-TIG\\R-T\\60-12-15'
if not os.path.exists(FilePath):
    os.makedirs(FilePath)
filename='60-12-15 '+ str(init_T)+'K to '+str(set_T)+'K '+str(T_ramp)+'K-min '+'I='+str(I_resource*1e6)+'uA H='+str(H)+'Oe.txt'
fp=os.path.join(FilePath,filename)

k6221.ARM_Delta(I_resource,delay=0.002,delta_count='INF')
real_plot_another_process(plot_row_number=1,columns_list=[])
time.sleep(5)
#k6221.R_T_text_init(fp)
k6221.Delta_R_T(fp,set_T,T_ramp)
'''


#FMR --sweep magnetic field using VNA E5071C
'''
FilePath='E:\\GLL\\Data\\FMR-data\\20211218(CrO2 100nm)\\45 degree test\\VNA-20GHz'
#FilePath='E:\\YYY\\SFS\\Nb-Py\\S5097\\Py-8nm\\20201227-trilayer'
#make it if path does not exist\
if not os.path.exists(FilePath):
    os.makedirs(FilePath)
ppms=PPMS() 
vna=VNA()
IP_H=5000
Power=-5
H_step=10

step=0.25
Start=1
Fre_Start=Start*1e9
Stop=20
Fre_Stop=Stop*1e9
Points=(Stop-Start)/step+1
       
vna.set_on_off('on')
vna.fmr_init(points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=Power,IF=1e3)
vna.auto_scale()

#TemperaturePoint=[200,100,50,25,15,10,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3,10,9,8.5,8,7.5,7,6.5,6,5.5,5,4.5,4,3.5,3] 
#TemperaturePoint=[300,250,200,150,100,75,50,25,10,4,2]
TemperaturePoint=[300]
#TemperaturePoint=[320,340,360,380,400]  
#TemperaturePoint=[300,100,50,10,9,8,7,6.5,6,5.5,5,4.5,4,3.5,3] 
#fpoints=[3,201]
#Powerpoints=[-5]

               ### in-plane magnetic field
i=0
ppms.setField(0,150,0,stable=0)
#time.sleep(600)
real_plot_another_process(plot_row_number=3,columns_list=[])
#Temp=5
for Temp in TemperaturePoint:
#for fps in fpoints:
# for ps in Powerpoints:
    i=i+1 
    filename=str(i)+'st_T='+str(Temp)+'K_'+str(Power)+'dBm_H='+str(IP_H)+'Oe_S21.txt'
#    filename=str(i)+'st_T=5K_'+str(ps)+'dBm_H='+str(IP_H)+'Oe_S21.txt'
    fp=os.path.join(FilePath,filename)
#    ppms.setField(15000,150,0,stable=0)
    if Temp<10:
        TIME=600
        rate=2
        vna.fmr_init(points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=Power,IF=1e3)
#        vna.fmr_init(points=fps,freq_start=16.9e9,freq_stop=17.1e9,power=-25,IF=1e3)
        vna.auto_scale()
    elif Temp>=10:
        TIME=100
#        TIME=10
        rate=10
        vna.fmr_init(points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=Power,IF=1e3)
#        vna.fmr_init(points=fps,freq_start=9.9e9,freq_stop=10.1e9,power=-25,IF=1e3)
#        vna.fmr_init(points=191,freq_start=1e9,freq_stop=20e9,power=-25,IF=1e3)
        vna.auto_scale()
    ppms.setTemperature(Temp,rate)
    print('wait some mins to let the temperature more stalbe'+time.ctime())
    time.sleep(TIME)
#    vna.set_power(Power)
    vna.set_power(Power)
    vna.auto_scale()
    vna.auto_scale()
    time.sleep(240)
    vna.fmr_measure(fp,IP_H,H_step)#(MAGNETIC FIELD, SPEED)
#    vna.fmr_measure(fp,-3000,8)
    ppms.setField(0,150,0,stable=0)  # set magnetic field persistent
    time.sleep(300)

#time.sleep(30)
#vna.set_TriggerMode(mode='HOLD')
vna.set_on_off('off')
#ppms.setTemperature(10,2)
#time.sleep(120) 
#print('the measurement is over, '+time.ctime())
#ppms.setTemperature(300,10)
#mail
'''



'''

ppms=PPMS()
vna=VNA()
vna.set_on_off('on')
vna.set_span(fcent=11.6e9,fspan=0.2e9,power=0)
#vna.fmr_init(points=1601,freq_start=1e9,freq_stop=20e9,power=-25,IF=1e3,sweep_time=0)
vna.auto_scale()
#s21=vna.ReadLine(1)
#s=s21.split(',')
#print s[3]
#vna.set_on_off('off')
'''
'''
ppms=PPMS()
vna=VNA()
H=0
ppms.setField(H,100,0,stable=0)
time.sleep(20)

fres=10   #GHz
fspan=0.2e9
power=0
vna.set_on_off('on')
vna.set_span(fcent=fres*1e9,fspan=0.2e9,power=-25,points=201,ave=16,IF=10e3,sweep_time=0)
vna.auto_scale()
vna.auto_scale()

#vna.set_on_off('off')
'''

'''
#K6221-sin_wave-offset mode + SR830 to detect the dV - dI for Josephson coupling
ppms=PPMS()
vna=VNA()
k6221=K6221()
sr830=SR830()

TempPoints=[6]
FreqPoints=np.arange(6,10.2,0.2)
#FreqPoints=[4,10,11,16,17]
FieldPonits=[0]
#PowPoints=[5,3,1,0,-1,-3,-5,-10,-15,-20,-25]
print(FreqPoints)

######   set PPMS  ######
#ppms.setField(0,100,0,stable=0)
#ppms.setTemperature(20,2)
#time.sleep(600)

Temp=4  # in K
H=400 # in Oe
#ppms.setTemperature(Temp,2)
#time.sleep(10)
ppms.setField(H,100,0,stable=0)
time.sleep(9)

######   set VNA  ######
vna=VNA()
fres=10   #GHz
fspan=0.2e9
power=0
vna.set_on_off('on')
vna.set_span(fcent=fres*1e9,fspan=0.2e9,power=-25,points=201,ave=16,IF=10e3,sweep_time=0)
vna.auto_scale()
vna.auto_scale()
#vna.set_on_off('off')
#######  set K6221, current in mA  ######

Is=-2000e-6
Ie=2000e-6
Istep=10e-6
di=5e-6

#######  set SR830  ######
sr830.ClearBuffer()

FilePath='E:\\GLL\\Data\\Transport-measure\\20211207(Nb-Py(5-3)-Nb)\\Shapiro dV-dI'
if not os.path.exists(FilePath):
    os.makedirs(FilePath)

real_plot_another_process(plot_row_number=1,columns_list=[])

i=0
for freq in FreqPoints:
#for P in PowPoints:
    i=i+1
#    filename=str(i)+'- '+str(Temp)+'K '+str(H)+'Oe '+str(fres)+'GHz_0.2G '+str(P)+'dBm_dvdi.txt'  
    filename=str(i)+'- '+str(Temp)+'K '+str(H)+'Oe '+str(freq)+'GHz_0.2G 0dBm_dvdi.txt' 
    fp=os.path.join(FilePath,filename)
#    vna.set_span(fcent=freq*1e9,fspan=fspan,power=power,points=201,ave=16,IF=10e3,sweep_time=0)
#    vna.set_span(fcent=fres*1e9,fspan=fspan,power=P,points=201,ave=16,IF=10e3,sweep_time=0)
#    vna.set_span(fcent=fres*1e9,fspan=fspan,power=P)
#    vna.auto_scale()
#    vna.auto_scale()
    print('the RF set as: '+str(freq)+'G_'+str(fspan*1e-9)+'G_0dbm')
#    print('the RF set as: '+str(fres)+'G_'+str(fspan*1e-9)+'G_'+str(P)+'dbm')
    k6221.set_DCoffset(Is)   # in A
    print('wait some time for more stable. '+time.ctime())
    time.sleep(6)
    k6221.sweep_offset(pathfilename=fp,Istart=Is,Iend=Ie,ramp=Istep,dI=di)  
    time.sleep(200) 

print('the measuremnent is over '+ time.ctime())
#vna.set_on_off('off')
'''

#pna=PNA()
#
#pna.set_trigger('CONT')
#pna.set_on_off('on')
#step=0.25
#Start=1
#Fre_Start=Start*1e9
#Stop=40
#Fre_Stop=Stop*1e9
#Measure_Type='S21'
#Points=(Stop-Start)/step+1
#pna.fmr_init(measure_type=Measure_Type,points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=-25,IF=1e3)
#pna.set_on_off('off')
#pna.set_trigger('single')
#pna.set_on_off('off')

#FMR --sweep magnetic field using PNA N5234B
#set path, frequency, power,field, sweep field step, wait time, etc.

FilePath='E:\\GLL\\Data\\FMR-data\\20220520(CrO2 150nm-2)\\[010]\\PNA-40GHz'
#make it if path does not exist\
if not os.path.exists(FilePath):
    os.makedirs(FilePath)
ppms=PPMS() 
pna=PNA()
Measure_Type='S21'

#pna.fmr_init(points=117,freq_start=1e9,freq_stop=30e9,power=-25,IF=1e3)
#pna.fmr_init(points=79,freq_start=1e9,freq_stop=40e9,power=-25,IF=1e3)
#TemperaturePoint=[300,250,200,150,100,75,50,40,30,25,20,15,10,8,4,2]
TemperaturePoint=[30,20]    
Power=-5

H_initial=0
H_sweep=15000          # unit in Oe
H_step=10        # Oe/s, if H< 1.0T. STEP~8 Oe/s, otherwise 10 Oe/s
step=0.25

Start=1
Fre_Start=Start*1e9
Stop=40
Fre_Stop=Stop*1e9

Points=(Stop-Start)/step+1
ppms.setField(H_initial,150,0,stable=0)
pna.set_trigger('CONT')
pna.set_on_off('on')
pna.fmr_init(measure_type=Measure_Type,points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=-25,IF=1e3)
#sp.Popen(args=['python.exe','E:\\Qi\\labview\\Python\\real_plot.py',fp,[]],stdout=sp.PIPE,stderr=sp.PIPE)
real_plot_another_process(plot_row_number=3,columns_list=[])


i=5
for Temp in TemperaturePoint:
    i=i+1 
    filename=str(i)+'st_T='+str(Temp)+'K_'+str(Power)+'dBm_H='+str(H_sweep)+'Oe_S21.txt'
    fp=os.path.join(FilePath,filename)
#    ppms.setField(15000,150,0,stable=0)
    if Temp<10:
        TIME=1200
        rate=2
        pna.fmr_init(measure_type=Measure_Type,points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=-25,IF=1e3)
#        pna.fmr_init(points=117,freq_start=1e9,freq_stop=30e9,power=-25,IF=1e3)
#        pna.fmr_init(points=391,freq_start=1e9,freq_stop=40e9,power=-25,IF=1e3)
    elif Temp>=10:
        TIME=300
        rate=10
        pna.fmr_init(measure_type=Measure_Type,points=Points,freq_start=Fre_Start,freq_stop=Fre_Stop,power=-25,IF=1e3)
#        pna.fmr_init(points=117,freq_start=1e9,freq_stop=30e9,power=-25,IF=1e3)
#        pna.fmr_init(points=79,freq_start=1e9,freq_stop=40e9,power=-25,IF=1e3)
    ppms.setTemperature(Temp,rate)
    #pna.set_power(Temp)
    #pna.set_IF(Temp)
    print('wait some mins to let the temperature more stalbe',time.ctime())
    time.sleep(TIME)
    pna.set_power(Power)
    time.sleep(200)
    pna.fmr_measure(fp,H_sweep,H_step)#(MAGNETIC FIELD, SPEED)  
#    pna.fmr_measure(fp,10000,10) #H Kening Cr2O3 0 Field 500OE Field
#    pna.fmr_measure(fp,-3000,8)
    ppms.setField(0,150,0,stable=0)  # set magnetic field persistent
#    ppms.setTemperature(200,10)#zero field warm-up and  field cool-down
    time.sleep(20)
#    ppms.setField(10000,150,0,stable=0)
#    time.sleep(100)
    #pna.fmr_measure(fp,-8000,10)
time.sleep(30)
pna.set_trigger('single')
pna.set_on_off('off')

ppms.setTemperature(300,10)
#ppms.setTemperature(10,2)
#ppms.setTemperature(10,10)
#ppms.setTemperature(10,2)
#time.sleep(300)
#ppms.setTemperature(300,10)

#mail



'''
#FMR --fixed field, sweep frequency
FilePath='E:\\Cai Ranran\\FMR driven Josephson Effect\\Nb(100)-Py(5)-Nb(100)\\20200818_S2\\20200901\\FMR'
ppms=PPMS() 
vna=VNA()
vna.set_on_off('on')
vna.fmr_init(points=1601,freq_start=1e9,freq_stop=20e9,power=-10,IF=1e3,ave=16)
TemperaturePoint=[5]#,300,200,200,100,50,50,10,10]
#TemperaturePoint=[15,10,8,7.7,7.6,7.1,6.5,4.2]
fieldPoint=[2000]
power=0
col=''
data=''
i=0
#j=0
#sp.Popen(args=['python.exe','E:\\Qi\\labview\\Python\\real_plot.py',fp,[]],stdout=sp.PIPE,stderr=sp.PIPE)
#real_plot_another_process(plot_row_number=3,columns_list=[])

for Temp in TemperaturePoint:
    i=i+1
    filename=str(i)+'st_T='+str(Temp)+'K_'+str(power)+'dBm_S21.txt'
    fp=os.path.join(FilePath,filename)
    if Temp<10:
        rate=2
    elif Temp>=10:
        rate=15
       
    vna.fmr_text_init(fp)
    for field in fieldPoint:
        time.sleep(20)
        vna.set_on_off('off')
        ppms.setTemperature(Temp,rate)
        print 'wait 10 mins to let the temperature more stalbe',time.ctime()
        time.sleep(50)
#        filename=str(j)+'st_'+str(field)+'Oe_T='+str(Temp)+'K_'+str(power)+'dBm_S21.txt'
#        fp=os.path.join(FilePath,filename)
        
        ppms.setField(field,150)
#        ppms.setField(field,150,0,stable=0)
        time.sleep(20)
#        print field_realtime
        vna.set_on_off('on')
        vna.auto_scale()
#        time.sleep(30)
        vna.fmr_init(points=1601,freq_start=1e9,freq_stop=20e9,power=0,IF=1e3,ave=16,sweep_time=1)
        vna.auto_scale()
        time.sleep(20)
#        vna.fmr_measure(fp,field,5)
#        vna.fmr_text_init(fp)
#        data_last=data
        s21=vna.ReadLine(1)
        s21_realtime=float(s21[0].index)
        data=str(s21_realtime)+','+s21[1:-1]
        f1=open(fp,'a')
        f1.write(data)             
        f1.close()
        
        print field_realtime
        time.sleep(3)
        ppms.setField(0,150,0,stable=0)
        time.sleep(10)
        field_realtime=float(ppms.getField()[0])
        print field_realtime
        
#        vna.fmr_init(points=1601,freq_start=1e9,freq_stop=20e9,power=-20,IF=1e3,ave=16)
        if field>1:
            ppms.setTemperature(10,2)
            time.sleep(60)
        
#    f1=open(fp,'a')
#    f1.write(data)             
#    f1.close()
    time.sleep(3)
   
    #vna.set_power(Temp)
    #vna.set_IF(Temp)    
   
#    vna.fmr_measure(fp,10,5)
#    ppms.setField(0,100,0,stable=0)  # set magnetic field persistent
    #vna.fmr_measure(fp,-2000,10)
    #vna.fmr_measure(fp,-8000,10)
#ppms.setTemperature(10,2)
'''

'''
#  SWeep T, MR, microwave on AC
folder='E:\\Qi\\MR calibration\\device 3\\second' #.replace('\\','\\')  # take care not \  should be /
#NamePrefix='test90_3'
var=[-1.5e-3,1.5e-3]
amplifier=1
current_source=-1e-8
#var.reverse()
unit='k'
#amplifier=100
#temperature=[300]
ppms=PPMS()
#figure=plt.figure()
i=0
#sr830=SR830()
#modulation_freq=sr830.get_freq()
k2400=K2400()
k2002=K2002()
vna=VNA()
vna.spin_pumping_init(power=0,freq_cent=8e9)
real_plot_another_process(plot_row_number=2)
NameSuffix='0dbm300k8G'+'Hz'#+'modul_freq'+modulation_freq
for temp in var:
    i=i+1
    print temp,unit   
    #ppms.setTemperature(temp)
    
    #time.sleep(600)
    #k2400.k2400.write(':sour:volt '+str(temp))
    #vna.set_power(temp)
    print 'temperature is ok, please wait some time untill it is stable',time.ctime()
    #vna.SetFreqCenter(temp)
    #time.sleep(1200)
    #time.sleep(300)
    #axes=plt.subplot(4,4,i)
    #axes.set_title(str(temp)+unit)  
    #time.sleep(600)
    k2400.k2400.write(':sour:curr '+ str(temp))
    time.sleep(600)
    SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=3000,Rate=5,amplifier=amplifier)
    SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=-3000,Rate=5,amplifier=amplifier)
    #MR_2400_2002(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=1200,StopMag=-1200,Rate=5,current_source=current_source,amplifier=amplifier)
    #MR_2400_2002(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=-2000,StopMag=-0,Rate=5,current_source=1e-5)
vna.set_power(-40)
k2400.k2400.write(':sour:curr '+ str(0))
#ppms.setTemperature(100)
#ppms.setTemperature(300)
'''


'''
#  SWeep T, MR  microwvave off , DC
folder='E:\\Qi\\TI YIG\\x0.7\\Hall' #.replace('\\','\\')  # take care not \  should be /
#NamePrefix='test90_3'
var=[300]#[-10e-3,-5e-3,-1e-3,-5e-4,0,5e-4,1e-3,5e-3,10e-3]`
amplifier=1
current_source=5e-6
#var.reverse()
unit='k'
#amplifier=100
#temperature=[300]
ppms=PPMS()
#figure=plt.figure()
i=0
#sr830=SR830()
#modulation_freq=sr830.get_freq()
k2400=K2400()
k2002=K2002()
#vna=VNA()
#vna.spin_pumping_init(power=-15,freq_cent=5e9)
real_plot_another_process(plot_row_number=2)
NameSuffix='5uAI8_13V7_11'#+'modul_freq'+modulation_freq
for temp in var:
    i=i+1
    print temp,unit   
    #ppms.setTemperature(temp)
    
    #time.sleep(600)
    #k2400.k2400.write(':sour:volt '+str(temp))
    #vna.set_power(temp)
    print 'temperature is ok, please wait some time untill it is stable',time.ctime()
    #vna.SetFreqCenter(temp)
    #time.sleep(1200)
    #time.sleep(300)
    #axes=plt.subplot(4,4,i)
    #axes.set_title(str(temp)+unit)  
    #time.sleep(600)
    #k2400.k2400.write(':sour:curr '+ str(temp))
    #time.sleep(600)
    #SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=1500,Rate=15,amplifier=amplifier)
    #SpinPumingSR830(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'.txt'),StartMag=-1500,Rate=15,amplifier=amplifier)
    MR_2400_2002(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'up.txt'),StartMag=-15000,StopMag=15000,Rate=50,current_source=current_source,amplifier=amplifier)
    MR_2400_2002(filename=os.path.join(folder,str(temp)+unit+NameSuffix+'down.txt'),StartMag=15000,StopMag=-15000,Rate=50,current_source=current_source,amplifier=amplifier)
#vna.set_power(-40)
k2400.k2400.write(':sour:curr '+ str(0))
ppms.setField(0)
'''