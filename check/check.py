#!/usr/bin/env python

import datetime
import sys
import os
import os.path
import math
import numpy as np

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

if(sys.argv[0] == "check.py"):
    working_path = "./"
else:
    working_path = sys.argv[0].rsplit('/',1)[0] + '/'

now = datetime.datetime.today()
data_path_file = open(working_path+"data_path_dollar","r")
path=data_path_file.read().rstrip("\n")

doll_rate_file=open(path+now.strftime("%Y%m%d"))

line=doll_rate_file.readline()
doll_rate_bid={}
doll_rate_ask={}
doll_bid_hour_unit_data=[]
doll_ask_hour_unit_data=[]
doll_bid_hour_to_now_data=[]
doll_ask_hour_to_now_data=[]
while line:

    doll_rate_time=line.split(':')[0].split('m')[0]+'m'
    doll_rate_bid[doll_rate_time]=float(line.split(':')[2])
    doll_rate_ask[doll_rate_time]=float(line.split(':')[4])
    line=doll_rate_file.readline()

if len(doll_rate_bid) < 60 :
    print("few data")
    sys.exit(1)

dollar_file = open(working_path+'../dollar','r')
line = dollar_file.readline()
while line:
    my_dollar = float(line.split(',')[1])
    temp = line.split(',')[2]
    if temp.find('@')> -1 :
        last_deal_rate_dollar = float(temp.split('@')[1])
    line=dollar_file.readline()
now_hour = int(now.strftime("%H"))
now_minute = int(now.strftime("%M"))
for i in range(0,60):
    temp = str(int(now_hour)-1)+"h"+str(i).zfill(2)+"m"
    doll_bid_hour_unit_data.append(doll_rate_bid[temp])
    doll_ask_hour_unit_data.append(doll_rate_ask[temp])

for i in range(now_minute+1,60):
    temp = str(int(now_hour)-1)+"h"+str(i).zfill(2)+"m"
    doll_bid_hour_to_now_data.append(doll_rate_bid[temp])
    doll_ask_hour_to_now_data.append(doll_rate_ask[temp])
for i in range(0,now_minute+1):
    temp = str(int(now_hour))+"h"+str(i).zfill(2)+"m"
    doll_bid_hour_to_now_data.append(doll_rate_bid[temp])
    doll_ask_hour_to_now_data.append(doll_rate_ask[temp])

#"""
doll_bid_hour_unit_data = zero_bury(doll_bid_hour_unit_data,doll_bid_hour_unit_data)
doll_ask_hour_unit_data = zero_bury(doll_ask_hour_unit_data,doll_ask_hour_unit_data)
doll_bid_hour_to_now_data = zero_bury(doll_bid_hour_to_now_data,doll_bid_hour_to_now_data)
doll_ask_hour_to_now_data = zero_bury(doll_ask_hour_to_now_data,doll_ask_hour_to_now_data)
#"""

#print(doll_bid_hour_unit_data)

rate_path_file=open(working_path+"../rate_path_dollar","r")
path=rate_path_file.read().rstrip("\n")
doll_bid_file=open(path+"doll-bid","r")
doll_ask_file=open(path+"doll-ask","r")
doll_bid_now=float(doll_bid_file.read().rstrip("\n"))
doll_ask_now=float(doll_ask_file.read().rstrip("\n"))

#---------------------------------------------------------
#buy check
#---------------------------------------------------------
#least squares method(linear function approximation)
#using ask data
#y=ax+b

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
#---------------------------------------------------------
#sell check
#---------------------------------------------------------
if my_dollar == 0.0 :
    print("can't sell dollar")
    sys.exit(1)
if last_deal_rate_dollar - doll_bid_now > 0.20:
    print("sell doll 1000 reason 1") # loss cut
    sys.exit(1)
elif doll_bid_now - last_deal_rate_dollar > 0.10:
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
#---------------------------------------------------------
