#!/usr/bin/env python

import datetime
import sys
import os.path

class Fx:
    def __init__(self,yen,doller):
        
        self.c_place = 1
        self.yen = 0
        self.doller = 0
        
        now = datetime.datetime.today()
        yen_file = open('./yen','a+')
        if os.path.getsize("./yen") == 0:
            yen_file.write("{0},{1}".format(now.strftime("%Y/%m/%d %H:%M:%S"),yen))
        doller_file = open('doller','a+')
        line = doller_file.readlines()
        if os.path.getsize("./doller") == 0:
            doller_file.write("{0},{1}".format(now.strftime("%Y/%m/%d %H:%M:%S"),doller))

        yen_file.seek(0)
        line=yen_file.readline()
        while line:
            self.yen = int(line.split(',')[self.c_place])
            line=yen_file.readline()
        
        doller_file.seek(0)
        line=doller_file.readline()
        while line:
            self.doller = int(line.split(',')[self.c_place])
            line=doller_file.readline()
        
        print("yen={0}".format(self.yen))
        print("doller={0}".format(self.doller))

        yen_file.close()
        doller_file.close()

p=Fx(2000000,0)
