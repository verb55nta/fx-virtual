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
doll_rate_bid=[]
doll_rate_ask=[]
while line:
    doll_rate_bid.append(float(line.split(':')[2]))
    doll_rate_ask.append(float(line.split(':')[4]))
    line=doll_rate_file.readline()
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

#---------------------------------------------------------
#sell check
#---------------------------------------------------------



#---------------------------------------------------------
