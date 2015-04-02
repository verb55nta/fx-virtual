#!/usr/bin/env python

import datetime
import sys
import os
import os.path
import math

if(sys.argv[0] == "fx-virtual.py"):
    working_path = "./"
else:
    working_path = sys.argv[0].rsplit('/',1)[0] + '/'

class Fx:
    #------------------------------
    def __init__(self,yen,dollar):
        
        self.__c_place = 1
        self.__yen = 0
        self.__dollar = 0.0
        
        #print(sys.argv[0].rsplit('/',1)[0])
        #print(sys.argv[0].rsplit('/',1)[1])

        #print(working_path)
        
        now = datetime.datetime.today()
        yen_file = open(working_path+"yen",'a+')
        if os.path.getsize(working_path+"yen") == 0:
            yen_file.write("{0},{1},{2}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"),yen,"init"))
        dollar_file = open(working_path+"dollar",'a+')
        line = dollar_file.readlines()
        if os.path.getsize(working_path+"dollar") == 0:
            dollar_file.write("{0},{1},{2}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"),dollar,"init"))

        yen_file.seek(0)
        line=yen_file.readline()
        while line:
            self.__yen = int(line.split(',')[self.__c_place])
            line=yen_file.readline()
        
        dollar_file.seek(0)
        line=dollar_file.readline()
        while line:
            self.__dollar = float(line.split(',')[self.__c_place])
            line=dollar_file.readline()
        
        #print("yen={0}".format(self.__yen))
        #print("dollar={0}".format(self.__dollar))
        

        yen_file.close()
        dollar_file.close()

    def Read_rate(self):
        rate_path_file=open(working_path+"rate_path_dollar","r")
        path=rate_path_file.read().rstrip("\n")
        #print(path)
        doll_bid_file=open(path+"doll-bid","r")
        doll_ask_file=open(path+"doll-ask","r")
        self.__doll_bid=float(doll_bid_file.read().rstrip("\n"))
        self.__doll_ask=float(doll_ask_file.read().rstrip("\n"))
        #print(doll_bid)
        #print(doll_ask)
    #------------------------------
    def init_doll_yen(self):
        self.__yen = 2000000
        self.__dollar = 0
    #------------------------------
    def print_now_yen(self):
        print(self.__yen)
    def print_now_dollar(self):
        print(self.__dollar)
    def print_now_doll_bid(self):
        print(self.__doll_bid)
    def print_now_doll_ask(self):
        print(self.__doll_ask)
    #------------------------------
    def buy_doll(self,dollar):
        self.__yen -= math.ceil(self.__doll_ask * dollar)
        self.__dollar += dollar
        #print("dummy")
        
    def sell_doll(self,dollar):
        self.__yen += math.floor(self.__doll_bid * dollar)
        self.__dollar -= dollar
        #print("dummy")
    #------------------------------
    def save_money_status(self,status):
        if(status=="buy-doll"):
            buf = str(status)+"@"+str(self.__doll_ask)
        elif(status=="sell-doll"):
            buf = str(status)+"@"+str(self.__doll_bid)
        else:
            buf = status
        now = datetime.datetime.today()
        yen_file = open(working_path+"yen",'a+')
        yen_file.write("{0},{1},{2}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"),self.__yen,buf))
        dollar_file = open(working_path+"dollar",'a+')
        dollar_file.write("{0},{1},{2}\n".format(now.strftime("%Y/%m/%d %H:%M:%S"),self.__dollar,buf))
        
#initialize start
p=Fx(2000000,0.0)
p.Read_rate()
#initialize end

#p.save_money_status()
#print(sys.argv)
if len(sys.argv) > 1:
    if sys.argv[1] == "reset":
        p.init_doll_yen()
        p.save_money_status("reset")
        print("reset")
        sys.exit(0)
    if sys.argv[1] == "print":
        if sys.argv[2] == "yen":
            p.print_now_yen()
        elif sys.argv[2] == "doll":
            p.print_now_dollar()
        elif sys.argv[2] == "doll-bid":
            p.print_now_doll_bid()
        elif sys.argv[2] == "doll-ask":
            p.print_now_doll_ask()
        else:
            print("dummy")
    elif sys.argv[1] == "buy":
        if sys.argv[2] == "doll":
            p.buy_doll(float(sys.argv[3]))
            p.save_money_status("buy-doll")
    elif sys.argv[1] == "sell":
        if sys.argv[2] == "doll":
            p.sell_doll(float(sys.argv[3]))
            p.save_money_status("sell-doll")
    else:
        print("Wrong arg")
else:
    print("no arg(initializing is done)")
