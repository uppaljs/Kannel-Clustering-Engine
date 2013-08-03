import KCSMonitorUtils
import os
import signal
import time 
import threading
"""
	This code will satle till get one of those signals :
1. sig HUP reload  Qlist from shared memory
2. sig user1
"""
class React():
	def __init__(self):
		""" Method inside this class are sorted by pre-action and post-action """
	def escaleUP(self): 
		""" #Start new node from template and ##return its IP """
		from boto import ec2
		conn = ec2.connection.EC2Connection(aws_access_key_id="AKIAI6TGU5J3XBGFECKQ", aws_secret_access_key="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")
		print "( MEngine ) { escaleUP() } [ INFO ] We know using AWS API version : ", conn.APIVersion
		reservations = ec2conn.get_all_instances()
		instances = [i for r in reservations for i in r.instances]
		for i in instances :
			### All this code must changed to be load from template instead start static nodes
			if i.__dict__['tags']['Name'][:5] == 'node' :  # 'key_name': u'FARM-xxxx'
		# return IP addr of the new node
				pass

	def migrateBB(self, BB , node): 
		"""#Add iptables rule ##Modify /etc/hosts ###Stop this BB at the GW and Start it  at the new node""" 
		pass
	def getBackBB(self) : 
		""" Revert all actions toked by migrateBB"""
		pass
	def escaleDOWN(self,node):
		pass
	def try_to_start_link(self,link):
		pass
	
		

def signal_hundler(sig , stack):
	import cPickle as pickle
	if sig == signal.SIGHUP : # Handle down link problem
		print "( MEngine ) ( WARNING ) Get links that listed to queue messages "
		with open("/dev/shm/QList.pickle",'r') as f :
			QList = pickle.load(f)
		print QList
		for link in QList :
			print "Deploying monitoring agent for link -> " , link
			monitor_link_thread = threading.Thread(target=KCSMonitorUtils.monitorLink,args=(link,)) 
			monitor_link_thread.daemon = True
			monitor_link_thread.start()
def getRoute(self,link):
	rt = configobj.ConfigObj('/dev/shm/RT')
        if rt.has_key(link) :
        	return rt[link]
	else : return '_Q' 

signal.signal(signal.SIGHUP, signal_hundler)
signal.signal(signal.SIGUSR1, signal_hundler)


print "Starting MEngine @ pid : ", os.getpid(),":"
with open("/dev/shm/MEngine.pid","wb") as f :
	f.write(str(os.getpid()))

print "\twaiting action signals"
while True:
	time.sleep(60)
	print "( MEngine ) [ INFO ] waiting signal ...."
	# Checking system resources for monitor trigger ( we will dir(trigger_class) and execute all methods inside it
	import cPickle as pickle
	f = open('/dev/shm/QList2.pickle', 'rb')
	try : 
		QList2 = pickle.load(f)
	except : 
		print "Q List 2 seems empty"
		QList2 = set()
	f.close()
	if KCSMonitorUtils.monitorLinksQueue() :
		for link in KCSMonitorUtils.monitorLinksQueue() and link not in QList2 :
			reactor = React()
			node = reactor.escaleUP()
			BB = getRoute(link)
			if BB == '_Q' :
				print "( MEngine ) [ ERROR ] Can not find BB for : ", link
				continue 
			reactor.migrateBB(BB, node)
                        monitor_node_thread = threading.Thread(target=KCSMonitorUtils.monitorNode,args=(node,link))
                        monitor_node_thread.daemon = True
                        monitor_node_thread.start()

