#!/bin/sh

start()
{
# Init data
echo $KCROOT
AppRoot=$KCROOT
smscPool=$1
#Cleanm startup
clean_startup
#Create config data , conf files and RT and hosts 
echo $smscPool > /dev/shm/smsc_pool
for i in `ls $1`
do 
	kannel_name=`echo $i | sed 's/.links//'` 
	python $AppRoot/KCManager/configBuilder.py  $kannel_name
done 

python $AppRoot/KCManager/configBuilder.py Done...
sudo cp /tmp/hosts /etc/hosts 
#End config mgr stage



#Start kannels
cd $AppRoot/runTime
pwd
echo "Start BBs loop"
for i in `ls *.conf`
do
	echo -e "\tStarting bearerbox $i"	
	bearerbox  $i 2> /dev/null &
done 

sleep 3
echo "Starting SMs loop"
for i in `ls *.conf`
do
	echo -e "\tStarting smsbox $i"
	smsbox $i 2> /dev/null &
done 
#Start proxy service 
cd ..
echo "Start service listener =>  GW ProxyEngine and GW QEngine"
python Gateway/MEngine.py &
python Gateway/proxy.py
sleep 1 

#Start Monitoring services .
}

clean_startup()
{
	# revert to the start up 
		#1 iterator
		#rm -f $AppRoot/runTime/itr #>> /dev/null
		cat $AppRoot/config/init_itr > $AppRoot/runTime/itr
		#2 host file
		sudo echo > /tmp/hosts 
		sudo cp $AppRoot/config/init_etc_hosts /etc/hosts
		sudo cp $AppRoot/config/init_etc_hosts /tmp/hosts
		#3 RAM Desk
		#4 runTimeConfig
		rm -f $AppRoot/runTime/*.conf
		#5 flush routing table and process old rtable_dump
		mv /dev/shm/RT /dev/shm/RT.previous
}
