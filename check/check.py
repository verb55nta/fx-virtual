#!/usr/bin/env python

import datetime
import sys
import os
import os.path
import math

now = datetime.datetime.today()
data_path_file = open("./data_path_dollar","r")
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
if len(doll_rate_bid) < 60 :
    print("few data")
    sys.exit(1)
#print("Hello World")

#buy check
#---------------------------------------------------------

dollar_file = open('../dollar','r')
line = dollar_file.readline()
while line:
    my_dollar = float(line.split(',')[1])
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

#---------------------------------------------------------
#sell check
#---------------------------------------------------------
if my_dollar == 0.0 :
    print("can't sell dollar")
    sys.exit(1)


#---------------------------------------------------------
