
class proxy :
	def __init__(self,buff):
		self.Q = buff
		self.QList = set()
		self.QList2 = set()
		QD = configobj.ConfigObj( 'config/app.conf' )['application']['q-driver']
		from Gateway import QEngine
		self.QE = QEngine.QEngine(QD)
		from lockfile import FileLock
		#self.flock = FileLock('/dev/shm/QList.pickle')
		from os import getpid , getppid
		print "Starting proxy instance: " , getpid() , "From parent: " , getppid()
		import signal
		# get pid of monitorLink
	def getRoute(self,link):
		rt = configobj.ConfigObj('/dev/shm/RT')
		if rt.has_key(link) :
			return rt[link]
		else :
			return '_Q'
	def getQList(self):
		return self.QList.union(self.QList2)
	def send(self,sms):
		_rt = self.getRoute(sms['link'])
		# Send normally as we found a link to route .
		if not  _rt == '_Q' :
	#		print " urllib2.urlopen(http://"+ _rt + sms['uri']
			try :
				fd = urllib2.urlopen("http://" + _rt + sms['uri'])
				if fd.read()[0:5] == 'Sent.' :
					self.Q.task_done()	
					fd.close()
					return
				""" Should not ever enter this code above return to first except """
				print "(Alert!) => {0} is not sending !! <<Should not Enter here>>".format(sms['link'])
				self.QList.add(sms['link'])
				self.QE.enqueue(sms)
				#if self.flock.is_locked and self.flock.i_am_locking() : 
				#	self.flock.release()
				#self.flock.acquire()
				import cPickle as pickle
				with  open('/dev/shm/QList.pickle', 'wb' ) as f :
                                        pickle.dump(self.QList, f, -1)
                                        f.close()
				with open('/dev/shm/MEngine.pid','r') as f:
					ME_PID = f.read()
				from os import kill
				print "Firing signal to MEngine. @ PID: " , ME_PID
				kill(int(ME_PID),1)
				#self.flock.release()
			except urllib2.URLError , e:
                                print "(Alert!) Link {0} is not Reachable !!".format(sms['link'])
                                """ Fire a signal to trigger 1. monIF , 2.  """
                                self.QList.add(sms['link'])
                                self.QE.enqueue(sms)
                                #if self.flock.is_locked and self.flock.i_am_locking() :
                                #       self.flock.release()
                                #self.flock.acquire()
                                import cPickle as pickle
				with  open('/dev/shm/QList.pickle', 'wb' ) as f :
					pickle.dump(self.QList, f, -1)
                                	f.close()
                                #self.flock.release()
                                with open('/dev/shm/MEngine.pid','r') as f:
                                        ME_PID = f.read()
                                from os import kill
                                print "Firing signal to MEngine. @ PID: " , ME_PID
                                kill(int(ME_PID),1)
			finally : print "( GW ) ( proxy ) [ LOG ] Request : \n\t" , sms['link'], "=>" , sms['uri'][60:150] , "Done. "
	
		else : print "Unkown link {" + sms['link'] +"} !!"
	
	def callback(self,condition,msg):
		import cPickle as pickle
		print msg
		from os import getpid
		with open('/dev/shm/GW_PROXY_CALLBACK.pid','wb') as fd :
			fd.write(str(getpid()))
		while True :
			if self.Q.empty(): pass
				#condition.acquire()
				#condition.wait()
				#condition.release()
			sms = self.Q.get()
			if sms['link'] not in ( 'link1','ignore')  and  sms['link'] not in self.QList and sms['link'] not in self.QList2:
				self.send(sms)
				continue
			if sms['link'] in self.QList:
                                self.QE.enqueue(sms)
				"""CCCCC"""
				print self.QList
				print "Queued . for => "  + sms['link'] + " <= because of fail in sending or entering a transint stat."
                                f = open('/dev/shm/QList.pickle', 'rb')
                                try : 
					self.QList = pickle.load(f)
				except :
					self.QList = set() 
				f.close()
				continue 
			if sms['link'] in self.QList2: 
				self.QE.enqueue(sms)
				print "=> " + sms['link'] + " Enqueueing because it match some restriction policy"
				try :
					f = open('/dev/shm/QList2.pickle', 'rb')
				except IOError:
					f = open('/dev/shm/QList2.pickle', 'wb') 
				self.QList2 = pickle.load(f)
				f.close()

import socket, select
import Queue
import threading
import urllib2
import configobj
from sys import path
from os import environ,getpid
path.append(environ['KCROOT'])
# This test reveal very impressive reslult so plz proceeed with it
# src http://scotdoyle.com/python-epoll-howto.html


"""
TODOs
-----
   1. at sigTerm save the queue to presistent storage then die.
"""
QList = set() # Down Links Q
sms = {}
Q = Queue.Queue()  # Memory Q between accept socket and send to kannel.
condition = threading.Condition()
p = proxy(buff=Q)
print "Start service listener @ PID : " , getpid()
with open('/dev/shm/GW_SVC_LISTENER.pid','wb') as fd :
	fd.write(str(getpid()))
send_thread = threading.Thread(target=p.callback , args=(condition,"Starting Memory deqeue callback\n\n\tBOOT DONE.\n") )
send_thread.daemon = True
send_thread.start()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(200)
serversocket.setblocking(0)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
	connections = {}; requests = {}; responses = {}
	while True:
		events = epoll.poll(-1)
		for fileno, event in events:
			# Just accept a client connections with unblocking manar and register there handler for epoll in and put them in a connections ,request and response queues.
			if fileno == serversocket.fileno():
				connection, address = serversocket.accept()
				connection.setblocking(0)
				epoll.register(connection.fileno(), select.EPOLLIN)
				connections[connection.fileno()] = connection
				requests[connection.fileno()] = b''
				responses[connection.fileno()] = b''
			elif event & select.EPOLLIN:
				requests[fileno] += connections[fileno].recv(2048)
				#connections[fileno].send(responses[fileno])
				sms['uri'] = requests[fileno].split()[1] 
				sms['link'] = str(requests[fileno])[58:69].split('&')[0]
				#condition.acquire()
				Q.put(sms)
				if not  sms['link'] in p.getQList() : 
					responses[fileno]=b"Sent."
				else :
					responses[fileno]=b"Queued."	
				epoll.modify(fileno, select.EPOLLOUT)
				#condition.notifyAll()
				#condition.release()
			elif event & select.EPOLLOUT:
				byteswritten = connections[fileno].send(responses[fileno])
				responses[fileno] = responses[fileno][byteswritten:]
				if len(responses[fileno]) == 0:
					epoll.modify(fileno, 0)
					connections[fileno].shutdown(socket.SHUT_RDWR)
			elif event & select.EPOLLHUP:
				epoll.unregister(fileno)
				connections[fileno].close()
				del connections[fileno]
finally:
	epoll.unregister(serversocket.fileno())
	epoll.close()
	serversocket.close()
	send_thread.join()
	print "ByBy .................."
	# send all Q data to QEngine . and free all Qlists
	

