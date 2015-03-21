#!/usr/bin/env python

import datetime
import sys

def fx_init():
    now = datetime.datetime.today()
    
    
    yen_file = open('yen','a+')
    line = yen_file.readline()
    if line == "":
        yen_file.write("{0},1000000".format(now.strftime("%Y/%m/%d %H:%M:%S")))
    doller_file = open('doller','a+')
    line = doller_file.readline()
    if line == "":
            doller_file.write("{0},0".format(now.strftime("%Y/%m/%d %H:%M:%S")))
            
    yen_file.close()
    doller_file.close()

fx_init()
