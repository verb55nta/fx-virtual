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
doll_bid_10m_unit_data=[]
doll_ask_10m_unit_data=[]
doll_bid_10m_to_now_data=[]
doll_ask_10m_to_now_data=[]
my_yen = 2000000
if sys.argv[2] == "yes":
    my_dollar=1000.0
else:
    my_dollar=0.0

while line:

    doll_rate_time=line.split(':')[0].split('m')[0]+'m'
    doll_rate_bid[doll_rate_time]=float(line.split(':')[2])
    doll_rate_ask[doll_rate_time]=float(line.split(':')[4])
    line=doll_rate_file.readline()

for i in range(0,len(doll_rate_bid) - 10 + 1):
    if int(i%10) == 0:
        doll_bid_10m_unit_data=[]
        doll_ask_10m_unit_data=[]
        for j in range(0,10):
            temp = str(int(i/60))+"h"+str(int((i%60)+j)).zfill(2)+"m"
            doll_bid_10m_unit_data.append(doll_rate_bid[temp])
            doll_ask_10m_unit_data.append(doll_rate_ask[temp])
    for j in range(0,10):
        if (i%60)+j >= 60:
            temp = str(int(i/60)+1)+"h"+str(int((i%60)+j)-60).zfill(2)+"m"
        else:
            temp = str(int(i/60))+"h"+str(int((i%60)+j)).zfill(2)+"m"
        doll_bid_10m_to_now_data.append(doll_rate_bid[temp])
        doll_ask_10m_to_now_data.append(doll_rate_ask[temp])
    
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
    for i in range(0,len(doll_ask_10m_to_now_data)):
        x.append(i)
    A = np.array([x,np.ones(len(x))])
    A = A.T
    doll_ask_10m_unit_a,doll_ask_10m_unit_b = np.linalg.lstsq(A,doll_ask_10m_unit_data)[0]
    A = np.array([x,np.ones(len(x))])
    A = A.T
    doll_ask_10m_to_now_a,doll_ask_10m_to_now_b = np.linalg.lstsq(A,doll_ask_10m_to_now_data)[0]

    if sys.argv[3] == "buy":

        if doll_ask_10m_unit_a < 0 and doll_ask_10m_to_now_a >0 :
            print("{0}:buy doll 1000 reason 0".format(temp))
        else:
            print("{0}:dummy".format(temp))

    elif sys.argv[3] == "sell":
        
        if last_deal_rate_dollar - doll_bid_now > 0.20:
            print("sell doll 1000 reason 1") # loss cut
        elif doll_bid_now - last_deal_rate_dollar > 0.05:
            print("sell doll 1000 reason 2") # gain cut
        elif last_deal_rate_dollar - doll_bid_now > 0.10 and doll_ask_hour_unit_a > doll_ask_hour_to_now_a:
            print("sell doll 1000 reason 3") # low judge
        elif doll_bid_now - last_deal_rate_dollar > 0.10 and doll_ask_hour_to_now_a > doll_ask_hour_unit_a:
            print("sell doll 1000 reason 4") # high judge
        else :
            print("dummy")
        
    elif sys.argv[3] == "both":
        #print(temp)
        if my_dollar > 0.0 :
            dummy=0
            #print("already sell dollar")
        elif doll_ask_10m_unit_a < 0 and doll_ask_10m_to_now_a >0 :
            print(temp)
            print("buy doll 1000 reason 0")
            print("doll-ask:{0}".format(doll_ask_now))
            my_yen -= doll_ask_now * 1000
            my_dollar=1000.0
            print("yen:{0}".format(my_yen))
            last_deal_rate_dollar = doll_ask_now
        if my_dollar == 0.0 :
            dummy=0
            #print("can't sell dollar")
        elif last_deal_rate_dollar - doll_bid_now > 0.20:
            print(temp)
            print("sell doll 1000 reason 1") # loss cut
            print("doll-bid:{0}".format(doll_bid_now))
            my_yen += doll_bid_now * 1000
            my_dollar = 0.0
            print("yen:{0}".format(my_yen))
        elif doll_bid_now - last_deal_rate_dollar > 0.05:
            print(temp)
            print("sell doll 1000 reason 2") # gain cut
            print("doll-bid:{0}".format(doll_bid_now))
            my_yen += doll_bid_now * 1000
            my_dollar = 0.0
            print("yen:{0}".format(my_yen))
        elif last_deal_rate_dollar - doll_bid_now > 0.10 and doll_ask_10m_unit_a > doll_ask_10m_to_now_a:
            print(temp)
            print("sell doll 1000 reason 3") # low judge
            print("doll-bid:{0}".format(doll_bid_now))
            my_yen += doll_bid_now * 1000
            my_dollar = 0.0
            print("yen:{0}".format(my_yen))
        elif doll_bid_now - last_deal_rate_dollar > 0.10 and doll_ask_10m_to_now_a > doll_ask_10m_unit_a:
            print(temp)
            print("sell doll 1000 reason 4") # high judge
            print("doll-bid:{0}".format(doll_bid_now))
            my_yen += doll_bid_now * 1000
            my_dollar = 0.0
            print("yen:{0}".format(my_yen))
        #else :
            #print("dummy")
    #---------------------------------------------------------
    #simulate end
    #---------------------------------------------------------
    
    doll_bid_10m_to_now_data=[]
    doll_ask_10m_to_now_data=[]


#print(doll_bid_hour_unit_data)

#---------------------------------------------------------
#buy check
#---------------------------------------------------------
#least squares method(linear function approximation)
#using ask data
#y=ax+b
"""
x=[]
for i in range(0,60):
    x.append(i)
A = np.array([x,np.ones(len(x))])
A = A.T
doll_ask_hour_unit_a,doll_ask_hour_unit_b = np.linalg.lstsq(A,doll_ask_hour_unit_data)[0]
A = np.array([x,np.ones(len(x))])
A = A.T
doll_ask_hour_to_now_a,doll_ask_hour_to_now_b = np.linalg.lstsq(A,doll_ask_hour_to_now_data)[0]
if my_dollar > 0.0 :
    dummy=0
elif doll_ask_hour_unit_a < 0 and doll_ask_hour_to_now_a >0 :
    print("buy doll 1000 reason 0")
    sys.exit(1)
"""
#---------------------------------------------------------
#sell check
#---------------------------------------------------------
"""
if my_dollar == 0.0 :
    print("can't sell dollar")
    sys.exit(1)
if last_deal_rate_dollar - doll_bid_now > 0.20:
    print("sell doll 1000 reason 1") # loss cut
    sys.exit(1)
elif doll_bid_now - last_deal_rate_dollar > 0.05:
    print("sell doll 1000 reason 2") # gain cut
    sys.exit(1)
elif last_deal_rate_dollar - doll_bid_now > 0.10 and doll_ask_hour_unit_a > doll_ask_hour_to_now_a:
    print("sell doll 1000 reason 3") # low judge
    sys.exit(1)
elif doll_bid_now - last_deal_rate_dollar > 0.10 and doll_ask_hour_to_now_a > doll_ask_hour_unit_a:
    print("sell doll 1000 reason 4") # high judge
    sys.exit(1)
else :
    print("dummy")
"""
#---------------------------------------------------------
