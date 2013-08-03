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
### Remove this value it just for test.
   threshold = -1
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
                if smscItem.tag == 'queued' : 
			smscsQList[linkName] += int(smscItem.text)

   q += filter( lambda link: smscsQList[link] > threshold   ,smscsQList)
   print smscsQList
   print "Links that trigger the Queue limit are : " ,  q



monitorLinksQueue()
