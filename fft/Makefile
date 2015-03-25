# Makefile 3

# マクロ定義部
CC      = /opt/centos/devtoolset-1.1/root/usr/bin/g++
#CC      = g++
#OBJS    = sub1.o sub2.o
OBJS = *.o
LDLIBS = -lm -lfftw3
CFLAGS = -Wall -std=c++11
#CFLAGS = -Wall


# 生成規則部
a.out: $(OBJS)                 
	$(CC) -o $@ $(OBJS) $(LDLIBS)   

.cpp.o:
	$(CC) -c $< $(CFLAGS)

clean:
	rm *~ *.o a.out

#sub1.o: header.h
#sub2.o: header.h
