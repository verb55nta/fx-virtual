#!/usr/bin/env python

import datetime
import sys
import os
import os.path
import math
import numpy as np

#print(sys.argv[0])

if(sys.argv[0] == "fx-virtual.py"):
    working_path = "./"
else:
    working_path = sys.argv[0].rsplit('/',1)[0] + '/'

now = datetime.datetime.today()
data_path_file = open(working_path+"data_path_dollar","r")
path=data_path_file.read().rstrip("\n")
#print(path)
#print(now.strftime("%Y%m%d"))
doll_rate_file=open(path+now.strftime("%Y%m%d"))
#print(doll_rate_file.read())
line=doll_rate_file.readline()
doll_rate_bid={}
doll_rate_ask={}
doll_bid_hour_unit_data=[]
doll_ask_hour_unit_data=[]
doll_bid_hour_to_now_data=[]
doll_ask_hour_to_now_data=[]
while line:
    #doll_rate_time.append(line.split(':')[0])
    doll_rate_time=line.split(':')[0].split('m')[0]+'m'
    #doll_rate_bid.append(float(line.split(':')[2]))
    doll_rate_bid[doll_rate_time]=float(line.split(':')[2])
    doll_rate_ask[doll_rate_time]=float(line.split(':')[4])
    #doll_rate_ask.append(float(line.split(':')[4]))
    line=doll_rate_file.readline()
#print(doll_rate_bid)
#print(doll_rate_ask)
#print("doll_rate_bid:")
#print(len(doll_rate_bid))
#print("doll_rate_ask:")
#print(len(doll_rate_ask))
#x=[1,2,3,4,5]



if len(doll_rate_bid) < 60 :
    print("few data")
    sys.exit(1)
#print("Hello World")



dollar_file = open(working_path+'../dollar','r')
line = dollar_file.readline()
while line:
    my_dollar = float(line.split(',')[1])
    temp = line.split(',')[2]
    #print(len(temp))
    if temp.find('@')> -1 :
        last_deal_rate_dollar = float(temp.split('@')[1])
        #print(last_deal_rate_dollar)
    #else:
        #print("not str after @")
    line=dollar_file.readline()
#print(my_dollar)
if my_dollar != 0.0 :
    print("already buying dollar")
    sys.exit(1)

#print(now.strftime("%H"+"h"+"%M"+"m"+"%S"+"s"))
#print(now.strftime("%H"+"h"+"%M"+"m"))
#print(doll_rate_time[len(doll_rate_time)-1])
now_hour = int(now.strftime("%H"))
now_minute = int(now.strftime("%M"))
#print(now_hour)
#print(now_minute)
for i in range(0,60):
    #print(str(int(now.strftime("%H"))-1)+"h"+str(i).zfill(2)+"m")
    temp = str(int(now_hour)-1)+"h"+str(i).zfill(2)+"m"
    #print(temp)
    #print(doll_rate_bid[temp])
    #print(doll_rate_ask[temp])
    doll_bid_hour_unit_data.append(doll_rate_bid[temp])
    doll_ask_hour_unit_data.append(doll_rate_ask[temp])
#print(doll_bid_hour_unit_data)
#print(doll_ask_hour_unit_data)
for i in range(now_minute+1,60):
    temp = str(int(now_hour)-1)+"h"+str(i).zfill(2)+"m"
    doll_bid_hour_to_now_data.append(doll_rate_bid[temp])
    doll_ask_hour_to_now_data.append(doll_rate_ask[temp])
for i in range(0,now_minute+1):
    temp = str(int(now_hour))+"h"+str(i).zfill(2)+"m"
    doll_bid_hour_to_now_data.append(doll_rate_bid[temp])
    doll_ask_hour_to_now_data.append(doll_rate_ask[temp])
#print(doll_bid_hour_to_now_data)
#print(doll_ask_hour_to_now_data)
#print(len(doll_bid_hour_unit_data))
#print(len(doll_ask_hour_unit_data))
#print(len(doll_bid_hour_to_now_data))
#print(len(doll_ask_hour_to_now_data))
#doll_bid_hour_unit_div = doll_bid_hour_unit_data[len(doll_bid_hour_unit_data)-1] - doll_bid_hour_unit_data[0]
#doll_bid_hour_to_now_div = doll_bid_hour_to_now_data[len(doll_bid_hour_unit_data)-1] - doll_bid_hour_to_now_data[0]
#print(doll_bid_hour_unit_div)
#print(doll_bid_hour_to_now_div)



rate_path_file=open(working_path+"../rate_path_dollar","r")
path=rate_path_file.read().rstrip("\n")
#print(path)
doll_bid_file=open(path+"doll-bid","r")
doll_ask_file=open(path+"doll-ask","r")
doll_bid_now=float(doll_bid_file.read().rstrip("\n"))
doll_ask_now=float(doll_ask_file.read().rstrip("\n"))
#print(doll_bid_now)
#print(doll_ask_now)

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
#print(doll_ask_hour_unit_a)
#print(doll_ask_hour_unit_b)
A = np.array([x,np.ones(len(x))])
A = A.T
doll_ask_hour_to_now_a,doll_ask_hour_to_now_b = np.linalg.lstsq(A,doll_ask_hour_to_now_data)[0]
#print(doll_ask_hour_to_now_a)
#print(doll_ask_hour_to_now_b)
if doll_ask_hour_unit_a < 0 and doll_ask_hour_to_now_a >0 :
    print("buy doll 1000")
    sys.exit(1)
#---------------------------------------------------------
#sell check
#---------------------------------------------------------
#print(last_deal_rate_dollar)
if my_dollar == 0.0 :
    print("can't sell dollar")
    sys.exit(1)
if last_deal_rate_dollar - doll_bid_now > 0.20:
    print("sell doll 1000") # loss cut
    sys.exit(1)
if doll_bid_now - last_deal_rate_dollar > 0.10:
    print("sell doll 1000") # gain cut
    sys.exit(1)
if last_deal_rate_dollar - doll_bid_now > 0.10 and doll_ask_hour_unit_a > doll_ask_hour_to_now_a:
    print("sell doll 1000") # low judge
    sys.exit(1)
if doll_bid_now - last_deal_rate_dollar > 0.10 and doll_ask_hour_to_now_a > doll_ask_hour_unit_a:
    print("sell doll 1000") # high judge
    sys.exit(1)
#---------------------------------------------------------
