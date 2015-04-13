#!/usr/bin/env python3

import datetime
import sys
import os
import os.path
import math
import numpy as np

#sys.argv[1]:file
#sys.argv[2]:dollar exist or not
#sys.argv[3]:buy or sell or both
#sys.argv[4]:time length of data
#sys.argv[5]:dollar_unit
#sys.argv[6]:day_gain_lim
#sys.argv[7]:day_loss_lim

"""
if len(sys.argv) - 1 < 7:
    print("few arg")
    sys.exit(1)
"""

def print_debug(flag,buf):
    if flag == 1 :
        print(buf)

debug_flag=0

def zero_bury(y,x):
    last_non_zero_index=-1
    for i in range(0,len(y)):
        if(y[i] != 0):
            if last_non_zero_index+1 != i:
                if last_non_zero_index == -1 :
                    for j in range(last_non_zero_index+1,i):
                        x[j] = x[i]
                else:
                    for j in range(last_non_zero_index+1,i):
                        x[j] = (x[last_non_zero_index] + x[i])/2
            last_nonzero_number=y[i]
            last_non_zero_index=i
    if last_non_zero_index+1 != len(y):
        for j in range(last_non_zero_index+1,len(y)):
            x[j] = x[last_non_zero_index]
        last_non_zero_index=len(y)-1
    return x

doll_rate_file=open(sys.argv[1])

line=doll_rate_file.readline()
doll_rate_bid={}
doll_rate_ask={}
tmp_doll_bid_unit_data=[]
tmp_doll_ask_unit_data=[]
doll_bid_unit_data={}
doll_ask_unit_data={}
doll_bid_unit_a={}
doll_ask_unit_a={}
doll_bid_unit_b={}
doll_ask_unit_b={}
doll_bid_to_now_data={}
doll_ask_to_now_data={}

x=[]

time_size=int(sys.argv[2])
init_yen = 2000000
#day_gain_lim = int(sys.argv[6])
#day_loss_lim = int(sys.argv[7])
#dollar_unit = float(sys.argv[5])

loss_cut=0
gain_cut=0
loss_cut_and_average_up=0
gain_cut_and_average_sown=0

my_yen = 2000000
"""
if sys.argv[2] == "yes":
    my_dollar=dollar_unit
else:
    my_dollar=0.0
"""

"""
ttttt={}
temp=[]
temp.append(1)
temp.append(2)
temp.append(3)
print(temp)
ttttt["123"]=temp
print(ttttt)
"""

while line:

    doll_rate_time=line.split(':')[0].split('m')[0]+'m'
    doll_rate_bid[doll_rate_time]=float(line.split(':')[2])
    doll_rate_ask[doll_rate_time]=float(line.split(':')[4])
    line=doll_rate_file.readline()


for i in range(0,time_size):
        x.append(i)

for i in range(0,len(doll_rate_bid) - time_size + 1): # "i" is the index of current time
    if int(i%time_size) == 0:
        for j in range(0,time_size):

            temp = str(int((i+j)/60))+"h"+str(int(((i+j)%60))).zfill(2)+"m"
            tmp_doll_bid_unit_data.append(doll_rate_bid[temp])
            tmp_doll_ask_unit_data.append(doll_rate_ask[temp])

        temp2 = str(int((i+0)/60))+"h"+str(int(((i+0)%60))).zfill(2)+"m-"+str(int((i+time_size)/60))+"h"+str(int(((i+time_size)%60))).zfill(2)+"m"
        doll_bid_unit_data[temp2]=tmp_doll_bid_unit_data
        doll_ask_unit_data[temp2]=tmp_doll_ask_unit_data
        tmp_doll_bid_unit_data=[]
        tmp_doll_ask_unit_data=[]

#print(doll_bid_unit_data)

"""
    for j in range(0,time_size):
        if ((i+j)%60) >= 60:
            temp = str(int((i+j)/60)+1)+"h"+str(int(((i+j)%60))-60).zfill(2)+"m"
        else:
            temp = str(int((i+j)/60))+"h"+str(int(((i+j)%60))).zfill(2)+"m"
        doll_bid_10m_to_now_data.append(doll_rate_bid[temp])
        doll_ask_10m_to_now_data.append(doll_rate_ask[temp])
"""

"""
for i in range(0,len(doll_rate_bid) - time_size + 1):
    #---------------------------------------------------------
    #simulate start
    #---------------------------------------------------------
    
    doll_bid_10m_unit_data = zero_bury(doll_bid_10m_unit_data,doll_bid_10m_unit_data)
    doll_ask_10m_unit_data = zero_bury(doll_ask_10m_unit_data,doll_ask_10m_unit_data)
    doll_bid_10m_to_now_data = zero_bury(doll_bid_10m_to_now_data,doll_bid_10m_to_now_data)
    doll_ask_10m_to_now_data = zero_bury(doll_ask_10m_to_now_data,doll_ask_10m_to_now_data)
    
    doll_bid_now = doll_bid_10m_to_now_data[len(doll_bid_10m_to_now_data) - 1]
    doll_ask_now = doll_ask_10m_to_now_data[len(doll_ask_10m_to_now_data) - 1]
        
    x=[]
    for j in range(0,len(doll_ask_10m_to_now_data)):
        x.append(j)
    A = np.array([x,np.ones(len(x))])
    A = A.T
    doll_ask_10m_unit_a,doll_ask_10m_unit_b = np.linalg.lstsq(A,doll_ask_10m_unit_data)[0]
    A = np.array([x,np.ones(len(x))])
    A = A.T
    doll_ask_10m_to_now_a,doll_ask_10m_to_now_b = np.linalg.lstsq(A,doll_ask_10m_to_now_data)[0]

    if sys.argv[3] == "both":
        if my_dollar > 0.0 :
            dummy=0
        elif my_yen - init_yen > day_gain_lim:
            dummy=0
        elif my_yen - init_yen < day_loss_lim:
            dummy=0
        elif doll_ask_10m_unit_a < 0 and doll_ask_10m_to_now_a >0 :
            reason=0
            my_yen -= doll_ask_now * dollar_unit
            my_dollar=dollar_unit
            last_deal_rate_dollar = doll_ask_now
            print_debug(debug_flag,"{0} buy doll 1000 reason {1} doll-ask:{2} yen:{3}".format(temp,reason,doll_ask_now,my_yen))

        if my_dollar == 0.0 :
            dummy=0
        elif last_deal_rate_dollar - doll_bid_now > 0.30:
            reason=1
            my_yen += doll_bid_now * dollar_unit
            my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(temp,reason,doll_bid_now,my_yen))
        elif doll_bid_now - last_deal_rate_dollar > 0.10:
            reason=2
            my_yen += doll_bid_now * dollar_unit
            my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(temp,reason,doll_bid_now,my_yen))
        elif last_deal_rate_dollar - doll_bid_now > 0.20 and doll_ask_10m_unit_a > doll_ask_10m_to_now_a:
            reason=3
            my_yen += doll_bid_now * dollar_unit
            my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(temp,reason,doll_bid_now,my_yen))
        elif doll_bid_now - last_deal_rate_dollar > 0.05 and doll_ask_10m_to_now_a > doll_ask_10m_unit_a:
            reason=4
            my_yen += doll_bid_now * dollar_unit
            my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(temp,reason,doll_bid_now,my_yen))
        elif my_dollar > 0.0 and i == len(doll_rate_bid) - time_size:
            reason=5
            my_yen += doll_bid_now * dollar_unit
            my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(temp,reason,doll_bid_now,my_yen))
    #---------------------------------------------------------
    #simulate end
    #---------------------------------------------------------

    doll_bid_10m_to_now_data=[]
    doll_ask_10m_to_now_data=[]
"""
