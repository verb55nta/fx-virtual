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
print(doll_rate_file.read())
