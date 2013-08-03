AppRoot='/home/ec2-user/Devel/Cequens-Kannel-Cluster-Solution/'
cd $AppRoot
. KCManager/functions.sh
usage()
{
	echo "Bad cmd args"
}
case $1 in 
	--show-run)
	;;
	--start)
		# Add check to verify $2
		start $2
	;;
	--stop)
	;;
	--auto|--start-kannel)
	;;
	--monitor)
	;;
	*)
		usage 
		exit 111
	;;
esac
