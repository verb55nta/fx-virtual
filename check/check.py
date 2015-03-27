#!/usr/bin/env python

import datetime
import sys
import os
import os.path
import math

now = datetime.datetime.today()
data_path_file = open("./data_path_doller","r")
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
print(len(doll_rate_bid))
#print("doll_rate_ask:")
print(len(doll_rate_ask))
