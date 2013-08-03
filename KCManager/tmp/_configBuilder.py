#!/usr/bin/python
import sys
from sys import argv,exit,exc_info
import ConfigParser


class ConfigBuilder :
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
	def saveIterator():
		pass
	def load_AppConfig():
	AppRoot='/home/ec2-user/Devel/Cequens-Kannel-Cluster-Solution/'
	f = open(AppRoot + 'config/app.conf','r')
	cnf = ConfigParser.RawConfigParser()
	cnf.readfp(f)
	f.close()
#        AppConfig['log-dir'] = cnf.get("kannels","log-dir")
#        AppConfig['store-dir'] = cnf.get("kannels","store-dir")
        return { 'log-dir' : cnf.get("kannels","log-dir") , 'store-dir' : cnf.get("kannels","store-dir") }

def editContab_to_remove_oldDLR():
        pass
def getDB():
        return "pass"

def load_Iterator():
	f = open(AppRoot + 'runTime/itr','r')
	cnf = ConfigParser.RawConfigParser()
        cnf.readfp(f)
        f.close()
	
        return  {  'core' : {'admin-port' : cnf.get("ports","core-admin-port") ,'smsbox-port' : cnf.get("ports","core-smsbox-port")} , 'smsbox' : { 'sendsms-port' : cnf.get("ports","sendsms-port")} }

def createConfig():
        core_log = AppConfig['log-dir'] + kannel + '-core.Log'
        core_access_log = AppConfig['log-dir'] + kannel + '-core-access.log'
        store_file = AppConfig['store-dir'] + kannel + '.store'
        sb_log = AppConfig['log-dir'] + kannel + '-smsbox-Log'
        sb_access_log = AppConfig['log-dir'] + kannel + '-smsbox-access.log'
        f = open('common.conf','r')
        cnf = f.read().format(Iterator['core']['admin-port'] , Iterator['core']['smsbox-port'] , core_log , core_access_log , store_file , Iterator['smsbox']['sendsms-port'] , sb_log , sb_access_log , kannel ,kannel)
        Iterator['core']['admin-port']# += 1
        Iterator['core']['smsbox-port']# += 1
        Iterator['smsbox']['sendsms-port']# += 1
        f.close()
	#rt =  <<<<<<<<<<<<<<<<<<<<<<<<<<
	
        try:
                x = AppRoot + 'runTime/'  + kannel + '.conf'
                f2 = open(x , 'w+')
		f2.write(cnf)
                if not f2.closed : f2.close()
        except IOError as e :
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                sys.exit(12)


def finish():
        sys.exit(0)
"""
        # delete Iterator file`
        #
        # Save %Config in ???? to generate the rtable from  .

"""
def main(kannel):
	if kannel == 'Done...' :
		finish()
        config = {}
        Iterator = {}
        AppConfig = {}
        RTable = {}
        AppConfig = load_AppConfig()
        Iterator = load_Iterator()

        try :
                createConfig()
                saveIterator()
        except IOError as e :
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except:
                print "Unexpected error:", sys.exc_info()[0]
                sys.exit(1)

if __name__=="__main__" :
	if argv[1] == 'Done...' :
		finish()
	print "Before main"
	main(argv[1])
	sys.exit(0)


