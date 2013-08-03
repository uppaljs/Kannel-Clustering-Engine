

class QEngine :
	def __init__(self,qd='FS') : 
		driver = {'FS'   : self.fs,
                	   'SQS' : self.sqs,
	                   'AMQ' : self.amq }
		self.q = driver[qd]()
	def enqueue(self,obj):
		self.q.enqueue(obj)
	def dequeue(self,link):
		self.q.dequeue(link)
		
	class fs :
		def __init__(self):
			print "We now using FileSystem Queueing Engine @ runtime/FSQ.\n"
			from os import path,listdir,environ
			import configobj
			if path.exists(environ['KCROOT'] + '/runTime/FSQ') :
				self.basedir = environ['KCROOT'] + '/runTime/FSQ/'
			else :
				print "Exit ALL system because path not exist"
		def enqueue(self,obj):
			from datetime import datetime
			fileName = self.basedir + datetime.now().strftime("%Y%m%d-%H%M%S.%f." ) + obj['link']
			with open( fileName , 'wb') as f:
				f.write(obj['uri'])
		def dequeue(self,link):
			from os import path,chdir,listdir,remove,environ
			import urllib2
			import configobj
			chdir(self.basedir)
			for file in listdir('.'):
				if path.splitext(file)[1] == '.'+link : 
					print "Dequeueing -> ", file
					f = open(file,'rb')
					uri = f.read()
					f.close()
					#link = path.splitext(file)[1]
				        rt = configobj.ConfigObj('/dev/shm/RT')
                			_rt = ""
					if rt.has_key(link) :
		                        	_rt = rt[link]
						#print _rt
					fd = urllib2.urlopen("http://" + _rt + uri)
	                                if fd.read()[0:5] == 'Sent.' :
						remove(file)
					fd.close()
				else : 
						pass

	class sqs:
		def __init__(self):
			print "We now using Amazon SQS Queueing Engine .\n"
                def enqueue(self,obj):
                        print "We now using SQS enqueueing "
                def dequeue(self,link):
                        print "We now using SQS dequeueing"

	class amq:
		def __init__(self):
			print "We now using Apache AMQ Queueing Engine @ /tmp/activemq_spool .\n"
			# start activeMQ_TX

                def enqueue(self,obj):
                        print "We now using AMQ enqueueing "
			# add messages per line at /tmp/activemq_spool
			with open('/tmp/activemq_spool','ap') as fd :
				fd.write(obj['link']+"::"+obj['sms']
			
                def dequeue(self,link):
                        print "We now using AMQ dequeueing"
			# Start activeMQ_RX


if __name__=="__main__" :
	QE = QEngine('SQS')
	QE.enqueue('ss')
	QE.dequeue()
