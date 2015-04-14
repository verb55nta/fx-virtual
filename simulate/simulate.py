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
#-------------------------------------------------------------------
# define function
#-------------------------------------------------------------------
def print_debug(flag,buf):
    if flag == 1 :
        print(buf)

debug_flag=1



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

#-------------------------------------------------------------------
# define function end
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# define arrays and so on
#-------------------------------------------------------------------





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
tmp_doll_bid_to_now_data=[]
tmp_doll_ask_to_now_data=[]
doll_bid_to_now_data={}
doll_ask_to_now_data={}
doll_bid_to_now_a={}
doll_ask_to_now_a={}
doll_bid_to_now_b={}
doll_ask_to_now_b={}

x=[]


#-------------------------------------------------------------------
# define arrays and so on ends
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# init values
#-------------------------------------------------------------------

doll_rate_file=open(sys.argv[1])
time_size=int(sys.argv[2]) #magic number

my_yen = 2000000 # magic number
my_dollar = 0.0 # magic number
day_gain_lim = 10000 #magic number
day_loss_lim = -10000 #magic number

loss_cut=0.30 #magic number
gain_cut=0.10 #magic number
loss_cut_and_average_up=0.20 #magic number
gain_cut_and_average_down=0.05 #magic number

init_yen = my_yen
init_dollar = my_dollar

dollar_unit = 1000

zero_flag=0

#-------------------------------------------------------------------
# init values ends
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# read from file
#-------------------------------------------------------------------

line=doll_rate_file.readline()
while line:

    doll_rate_time=line.split(':')[0].split('m')[0]+'m'
    doll_rate_bid[doll_rate_time]=float(line.split(':')[2])
    doll_rate_ask[doll_rate_time]=float(line.split(':')[4])
    line=doll_rate_file.readline()

#-------------------------------------------------------------------
# read from file ends
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# value setup
#-------------------------------------------------------------------

for i in range(0,time_size):
    x.append(i)

for i in range(0,len(doll_rate_bid) - time_size ): # "i" is the index of current time
    if int(i%time_size) == 0:

        for j in range(0,time_size):

            temp = str(int((i+j)/60))+"h"+str(int(((i+j)%60))).zfill(2)+"m"
            if(doll_rate_bid[temp] == 0 or doll_rate_ask[temp] == 0):
                zero_flag=1
                print_debug(debug_flag,"unit-warning:zero detected in {0}".format(temp))
            tmp_doll_bid_unit_data.append(doll_rate_bid[temp])
            tmp_doll_ask_unit_data.append(doll_rate_ask[temp])
        if zero_flag == 1:
            tmp_doll_bid_unit_data = zero_bury(tmp_doll_bid_unit_data,tmp_doll_bid_unit_data)
            tmp_doll_ask_unit_data = zero_bury(tmp_doll_ask_unit_data,tmp_doll_ask_unit_data)
            zero_flag=0

        temp2 = str(i//time_size*time_size // 60)+"h" + str(i//time_size*time_size % 60)+"m-"+str((i//time_size*time_size +time_size - 1)// 60)+"h" + str((i//time_size*time_size +time_size - 1)% 60)+"m"    
        doll_bid_unit_data[temp2]=tmp_doll_bid_unit_data
        doll_ask_unit_data[temp2]=tmp_doll_ask_unit_data
        tmp_doll_bid_unit_data=[]
        tmp_doll_ask_unit_data=[]
        A = np.array([x,np.ones(len(x))])
        A = A.T
        tmp_doll_bid_unit_a,tmp_doll_bid_unit_b = np.linalg.lstsq(A,doll_bid_unit_data[temp2])[0]
        doll_bid_unit_a[temp2]=tmp_doll_bid_unit_a
        doll_bid_unit_b[temp2]=tmp_doll_bid_unit_b
        tmp_doll_ask_unit_a,tmp_doll_ask_unit_b = np.linalg.lstsq(A,doll_ask_unit_data[temp2])[0]
        doll_ask_unit_a[temp2]=tmp_doll_ask_unit_a
        doll_ask_unit_b[temp2]=tmp_doll_ask_unit_b


    for j in range(0,time_size):

        temp = str(int((i+j)/60))+"h"+str(int(((i+j)%60))).zfill(2)+"m"
        if(doll_rate_bid[temp] == 0 or doll_rate_ask[temp] == 0):
            zero_flag=1
            print_debug(debug_flag,"to-now-warning:zero detected in {0}".format(temp))
        tmp_doll_bid_to_now_data.append(doll_rate_bid[temp])
        tmp_doll_ask_to_now_data.append(doll_rate_ask[temp])

    if zero_flag == 1:
        tmp_doll_bid_to_now_data = zero_bury(tmp_doll_bid_to_now_data,tmp_doll_bid_to_now_data)
        tmp_doll_ask_to_now_data = zero_bury(tmp_doll_ask_to_now_data,tmp_doll_ask_to_now_data)
        zero_flag=0        
    temp2 = str(i // 60)+"h" + str(i % 60)+"m-"+str((i+time_size - 1)// 60)+"h" + str((i+time_size - 1)% 60)+"m"
    doll_bid_to_now_data[temp2]=tmp_doll_bid_to_now_data
    doll_ask_to_now_data[temp2]=tmp_doll_ask_to_now_data
    tmp_doll_bid_to_now_data=[]
    tmp_doll_ask_to_now_data=[]
    A = np.array([x,np.ones(len(x))])
    A = A.T
    tmp_doll_bid_to_now_a,tmp_doll_bid_to_now_b = np.linalg.lstsq(A,doll_bid_to_now_data[temp2])[0]
    doll_bid_to_now_a[temp2]=tmp_doll_bid_to_now_a
    doll_bid_to_now_b[temp2]=tmp_doll_bid_to_now_b
    tmp_doll_ask_to_now_a,tmp_doll_ask_to_now_b = np.linalg.lstsq(A,doll_ask_to_now_data[temp2])[0]
    doll_ask_to_now_a[temp2]=tmp_doll_ask_to_now_a
    doll_ask_to_now_b[temp2]=tmp_doll_ask_to_now_b

#-------------------------------------------------------------------
# value setup ends
#-------------------------------------------------------------------

#---------------------------------------------------------
#simulate base define end
#---------------------------------------------------------
"""
time_size=int(sys.argv[2]) #magic number

my_yen = 2000000 # magic number
my_dollar = 0.0 # magic number
day_gain_lim = 10000 #magic number
day_loss_lim = -10000 #magic number

loss_cut=0.30 #magic number
gain_cut=0.10 #magic number
loss_cut_and_average_up=0.20 #magic number
gain_cut_and_average_down=0.05 #magic number
"""

def simulate_base(l_time_size,l_my_yen,l_my_dollar,l_day_gain_lim,l_day_loss_lim,l_loss_cut,l_gain_cut,l_loss_cut_and_average_up,l_gain_cut_and_average_down):
    for i in range(0,len(doll_rate_bid) - l_time_size):
        
        now_time = str(int((i+l_time_size)/60))+"h"+str(int(((i+l_time_size)%60))).zfill(2)+"m"
        now_time_unit = str(i // 60)+"h" + str(i % 60)+"m-"+str((i+l_time_size - 1)// 60)+"h" + str((i+l_time_size - 1)% 60)+"m"
        unit_time = str(i//l_time_size*l_time_size // 60)+"h" + str(i//l_time_size*l_time_size % 60)+"m-"+str((i//l_time_size*l_time_size +l_time_size - 1)// 60)+"h" + str((i//l_time_size*l_time_size +l_time_size - 1)% 60)+"m"
        doll_bid_now = doll_rate_bid[now_time]
        doll_ask_now = doll_rate_ask[now_time]
        
        l_my_dollar,l_my_yen
       
        if l_my_dollar > 0.0 :
            dummy=0
        elif l_my_yen - init_yen > l_day_gain_lim:
            dummy=0
        elif l_my_yen - init_yen < l_day_loss_lim:
            dummy=0
        elif doll_ask_unit_a[unit_time] < 0 and doll_ask_to_now_a[now_time_unit] >0 :
            reason=0
            l_my_yen -= doll_ask_now * dollar_unit
            l_my_dollar=dollar_unit
            last_deal_rate_dollar = doll_ask_now
            print_debug(debug_flag,"{0} buy doll 1000 reason {1} doll-ask:{2} yen:{3}".format(now_time,reason,doll_ask_now,l_my_yen))
            
        if l_my_dollar == 0.0 :
            dummy=0
        elif last_deal_rate_dollar - doll_bid_now > l_loss_cut:
            reason=1
            l_my_yen += doll_bid_now * dollar_unit
            l_my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(now_time,reason,doll_bid_now,l_my_yen))
        elif doll_bid_now - last_deal_rate_dollar > l_gain_cut:
            reason=2
            l_my_yen += doll_bid_now * dollar_unit
            l_my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(now_time,reason,doll_bid_now,l_my_yen))
        elif last_deal_rate_dollar - doll_bid_now > l_loss_cut_and_average_up and doll_ask_unit_a[unit_time] > doll_ask_to_now_a[now_time_unit]:
            reason=3
            l_my_yen += doll_bid_now * dollar_unit
            l_my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(now_time,reason,doll_bid_now,l_my_yen))
        elif doll_bid_now - last_deal_rate_dollar > l_gain_cut_and_average_down and doll_ask_to_now_a[now_time_unit] > doll_ask_unit_a[unit_time]:
            reason=4
            l_my_yen += doll_bid_now * dollar_unit
            l_my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(now_time,reason,doll_bid_now,l_my_yen))
        elif l_my_dollar > 0.0 and i == len(doll_rate_bid) - l_time_size - 1:
            reason=5
            l_my_yen += doll_bid_now * dollar_unit
            l_my_dollar = 0.0
            print_debug(debug_flag,"{0} sell doll 1000 reason {1} doll-bid:{2} yen:{3}".format(now_time,reason,doll_bid_now,l_my_yen))
#---------------------------------------------------------
#simulate base define end
#---------------------------------------------------------
            

#---------------------------------------------------------
#simulate start
#---------------------------------------------------------
simulate_base(time_size,my_yen,my_dollar,day_gain_lim,day_loss_lim,loss_cut,gain_cut,loss_cut_and_average_up,gain_cut_and_average_down)
#---------------------------------------------------------
#simulate end
#---------------------------------------------------------
