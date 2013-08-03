#!/usr/bin/python

"""
<smscs><count>87</count>
        <smsc>
                <name>SMPP:213.158.112.40:3333/3333:egNhtdy1:SMPP</name>
                <id>link60</id>
                <status>online 7762s</status>
                <received>0</received>
                <sent>0</sent>
                <failed>0</failed>
                <queued>0</queued>
        </smsc>
<smsc>
                <name>SMPP:212.118.129.59:10003/10003:Bulk77977:77977</name>
                <id>stc3</id>
                <status>online 7762s</status>
                <received>1135</received>
                <sent>2197</sent>
                <failed>54</failed>
                <queued>0</queued>
        </smsc>
"""

def monitorLinksQueue() :
   import urllib2
   from os import path,listdir,environ
   import configobj,re
   with open('/dev/shm/smsc_pool') as f :
		   smsc_pool = f.read()
   smsc_pool = smsc_pool.rstrip()
   if path.exists(environ['KCROOT'] + "/" + smsc_pool):
	   smsc_pool = environ['KCROOT'] + "/" + smsc_pool
   else : 
	if not path.exists(smsc_pool):
		   print "( KCMonitorUtils ) { monitorLinksQueue() } [ Error ] Could not find smsc_pool !!"
		   import sys
	   	   sys.exit(100)
   threshold = configobj.ConfigObj(environ['KCROOT'] + "/config/app.conf")['kannels']['links-threshold']
   print "( KCMonitorUtils ) { monitorLinksQueue() } [ INFO ] threshold value configured to be  " , threshold
### Remove this value it just for test.
   q = []
   smscsQList = {}
   for smsc in listdir(smsc_pool):
	smsc =smsc.replace('.links','')
	pat = re.compile("admin-port = (\d+)")
	with open(environ['KCROOT'] + "/runTime/" + smsc +".conf") as f :
		data = f.read()
	port = pat.findall(data)[0]
	URL = "http://"+smsc+":"+port+"/status.xml?password=xXxXxXx"
	file = urllib2.urlopen(URL)
	import xml.etree.ElementTree as ET
	tree = ET.parse(file)
	root = tree.getroot()
	smscsTag = root.findall('smscs')
	smscs = smscsTag.pop()
	for smscItem in smscs.getiterator() :
		if smscItem.tag == 'id' : 
			linkName = smscItem.text
			if not smscsQList.has_key(linkName) : 
				smscsQList[linkName] = 0
	    	if smscItem.tag == 'queued' : smscsQList[linkName] += int(smscItem.text)
   
   q += filter( lambda link: smscsQList[link] > threshold   ,smscsQList)
   if not len(q) > 0 : return [] 
   print "Links that trigger the Queue limit are : " ,  smscsQList
   print "Adding them to list "
   f = open('/dev/shm/QList2.pickle', 'wb')
   import cPickle as pickle
   try :
	QList2 = pickle.load(f)
   except IOError:
	QList2 = set()
   QList2.add(tuple(q))
   pickle.dump(QList2,f,-1)
   f.close()
   return q
""" 
The below code should moved to MEngine.React
	f = open('/dev/shm/Qlist2.pickler','rw')
	import marshal
	Qset = marsharl.load(f)
	Q.set.add(q)
	marshal.dump(Qset,f)
	f.close()
"""

def monitorLink(link):
	print "Start monitoring link ({0})".format(link)
	from urllib2 import urlopen
	import configobj
	import time 
	status = ''
	while not status  == 'Sent.':
		rt = configobj.ConfigObj('/dev/shm/RT')
		if rt.has_key(link) :
                	_rt = rt[link]
			try :
				fd = urlopen("http://" + _rt + "/cgi-bin/sendsms?username=nemra1&password=koko88&smsc=ignore&from=cithosting&to=201000310352&text=cithosting15&coding=0" )
				status = fd.read()[0:5] 
				print status
				fd.close()
			except: 
				print "( ",link ," ) Still Down :("
				time.sleep(3)
		else:
			print "( Alert ) Unknown link ! >> " + link
			return
	try :
		import cPickle as pickle
		f = open('/dev/shm/QList.pickle', 'r') 
		QList = pickle.load(f)	; print QList
		QList.remove(link) ; print QList
		f.close()
		f = open('/dev/shm/QList.pickle', 'w')
		pickle.dump(QList, f, -1)
		print "( monitorLink() )( Congratulations ) Link {0} is up now ;)".format(link)
		f.close()
		from os import environ
		import configobj
		QD = configobj.ConfigObj( environ['KCROOT'] + '/config/app.conf' )['application']['q-driver']
		from sys import path
		path.append( environ['KCROOT'])
                from Gateway import QEngine
                QE = QEngine.QEngine(QD)
		print "Start dequeuing msgs"
		QE.dequeue(link)

	except  :
		print "Exception @ last try @ monitorLink"
		import sys
		print sys.exc_info()


if __name__ == "__main__" :
	# Send Heart beat to all components
	pass
