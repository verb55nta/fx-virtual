#!/bin/sh
#tmp=`python simulate.py z:/chart/dollar-yen/data/20150409 no both 10 1000.0 100 -50`
#echo $tmp
#tmp2=`python simulate.py z:/chart/dollar-yen/data/20150410 no both 10 1000.0 100 -50`
#echo $tmp2
#tmp=$((tmp2-$tmp))
#echo $tmp
tmp=0
sum=0
for l in `seq -10 -10 -100`
do
    #echo $file
    for j in `seq 10 1 30`
    do
	for k in `seq 10 10 150`
	do
	    sum=0
	    #echo "time-length:$j,gain-lim:$k,loss-lim:$l"
	    for i in `seq 1 1 10` #file-day
	    do
		file=$(printf 201504%02d $i)
		#echo "file:$file"
		tmp=`python simulate.py z:/chart/dollar-yen/data/$file no both $j 1000.0 $k -50`
		#echo $tmp
		sum=$(($sum + $tmp))		    		
	    done
	    echo "time-length:$j,gain-lim:$k,loss-lim:$l=>sum:$sum"
	done
    done
done


