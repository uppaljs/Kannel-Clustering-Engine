#!/usr/bin/python
import sys,os
from os import environ
from sys import argv,exit,exc_info
import configobj
import commands

class ConfigBuild :
	""" 
	Decription :
	This scribt just take the kannel name form KCmgr --start code and build its config at runTime config dir



	Replacable items 
	0#admin-port = $admin-port
	1#smsbox-port = $smsbox-port
	2#log-file = $LOGDIR/$KANNEL_NAME_CORE.log
	3#access-log = $LOGDIR/$KANNEL_NAME_Core-access.log
	4#store-location = $STOREDIR/$KANNEL_NAME.store
	5#sendsms-port = $sendsms_port
	6#log-file = $LOGDIR/KANNEL_NAME_SB.log"
	7#access-log = $LOGDIR/KANNEL_NAME_SB-access.log"
	8#database = $KANNEL_NAME
	9#include = $KANNEL_NAME
	"""
	"""
	self.AppRoot='/home/ec2-user/Devel/Cequens-Kannel-Cluster-Solution/'
        self.config = {}
        self.Iterator = {}
        self.AppConfig = {}
        self.RTable = {}
	"""
	def __init__(self, kannel = 'Done...'):
		pass
	def save_Iterator(self ,ca ,cs ,ss):
		cnf = configobj.ConfigObj(self.AppConfig['AppRoot'] + '/runTime/itr')
                cnf['ports']['core-admin-port'] = ca 
		cnf['ports']['core-smsbox-port'] = cs 
		cnf['ports']['sendsms-port']  = ss 
		cnf.write()

	def load_AppConfig(self):
		cnf = configobj.ConfigObj(os.environ['KCROOT'] + '/config/app.conf')
	        return { 'log-dir' : cnf['kannels']['log-dir'] , 'store-dir' : cnf['kannels']['store-dir'] , 'AppRoot' : os.environ['KCROOT'] } ### AppRoot is a bug with this code

	def editContab_to_remove_oldDLR(self):
        	pass
	def getDB(self):
        	return "pass"

	def load_Iterator(self):
		cnf = configobj.ConfigObj(self.AppConfig['AppRoot'] + '/runTime/itr')
        	return  {  'core' : {'admin-port' : cnf["ports"]["core-admin-port"] ,'smsbox-port' : cnf["ports"]["core-smsbox-port"]} , 'smsbox' : { 'sendsms-port' : cnf["ports"]["sendsms-port"]}  }

	def createConfig(self):
		""" This build :
			 1) kannel conf file,
			 2) Iterator state file, 
			 3) Routing Table ( link mapper )
			 4) /etc/hosts
		 """
		"""1) kannel config file"""
        	core_log = self.AppConfig['log-dir'] + self.kannel + '-core.Log'
	        core_access_log = self.AppConfig['log-dir'] + self.kannel + '-core-access.log'
        	store_file = self.AppConfig['store-dir'] + self.kannel + '.store'
	        sb_log = self.AppConfig['log-dir'] + self.kannel + '-smsbox.Log'
        	sb_access_log = self.AppConfig['log-dir'] + self.kannel + '-smsbox-access.log'
	        f = open(os.environ['KCROOT'] + '/config/common.conf','r')
        	cnf = f.read().format(self.Iterator['core']['admin-port'] , self.Iterator['core']['smsbox-port'] , core_log , core_access_log , store_file , self.Iterator['smsbox']['sendsms-port'] , sb_log , sb_access_log , self.kannel , self.AppConfig['AppRoot'] + "/" + self.smsc_pool_dir + "/" + self.kannel)
	        core_admin_port = int(self.Iterator['core']['admin-port']) + 1  
        	core_smsbox_port = int(self.Iterator['core']['smsbox-port']) + 1
        	smsbox_sendsms_port = int(self.Iterator['smsbox']['sendsms-port']) + 1
		"""2) Iterator state save"""
		self.save_Iterator(core_admin_port ,core_smsbox_port ,smsbox_sendsms_port)
        	f.close()
	#rt =  <<<<<<<<<<<<<<<<<<<<<<<<<<
	        try:
        	        x = self.AppConfig['AppRoot'] + '/runTime/'  + self.kannel + '.conf'
                	f2 = open(x , 'w+')
			f2.write(cnf)
        	        if not f2.closed : f2.close()
	        except IOError as e :
        	        print "CreateConfig() I/O error({0}): {1}".format(e.errno, e.strerror)
                	sys.exit(12)
		"""3) Routing table 
			Relation hint : ref value sendsms-port
			core-admin-port = sendsms-port - 1000 << most interesting one >>
			core-smsbox-port = sendsms-port - 500
		   And Should be at this form
			RTable['Link_Name']["{0}:{1}".foramt(kannel ,self.Iterator['smsbox']['sendsms-port']) ]
			RTable['stc'][KSA_Stc:2010]
		   And /etc/hosts will be at this iteration "127.0.0.1   localhost localhost.localdomain KSA_Stc"
		   Or at upnormal cases :                    1.2.3.4	KSA_Stc 
		"""
		rt = configobj.ConfigObj('/dev/shm/RT')
		for smsc in self.getSMSCsFromProvider():
			rt[smsc] = "{0}:{1}".format(self.kannel,self.Iterator['smsbox']['sendsms-port'])
			rt.write()
		print "\tLink map created"
		"""4) /etc/hosts"""
		f = open('/tmp/hosts','r')
		# TODO : Check if it have routing to other node or not 
		header = f.read()
		body = header
		body += "127.0.0.1   " 	+ self.kannel + '\n'
		f = open('/tmp/hosts','w+')
		f.write(body)
		f.close()
		print "\tRouting table : add route configured " , self.kannel

	def getSMSCsFromProvider(self):
		# Read /dev/shm/smsc_pool file to get smsc pool dir
		smsc_pool_dir = self.smsc_pool_dir
		# Process the file and return array of each link name
		CMD = 'grep  ^smsc-id '+smsc_pool_dir+'/'+self.kannel+'.links | sed \'s/smsc-id//\' | sed \'s/"//g\' | sed \'s/=//g\'  | sed \'s/ //g\' ' 
		x = commands.getoutput(CMD)
		return set(x.splitlines())

	def finish(self):
		commands.getoutput('sudo cp /tmp/hosts /etc/hosts ')
        	sys.exit(0)
	
	def build(self,kannel):
		if kannel == 'Done...' :
			finish()
                else :
                	try:
                        	os.environ['KCROOT']
		        except :
                	        print "Please set os.environ['KCROOT'] "
                		self.finish()
                f = open('/dev/shm/smsc_pool')
                self.smsc_pool_dir = f.read().rstrip().lstrip()
                f.close()
                self.AppConfig = self.load_AppConfig()
                self.Iterator = self.load_Iterator()
                self.kannel = kannel
                self.createConfig()
		sys.exit(0)

	def test(self):
		print "Call build in method inside ConfigBuild .. success"


if __name__=="__main__" :
	print sys.argv[1]
	if sys.argv[1] == 'Done...' :
		sys.exit(0)
	cnfb = ConfigBuild()
	cnfb.build(sys.argv[1])
	cnfb.finish()
	sys.exit(0)

