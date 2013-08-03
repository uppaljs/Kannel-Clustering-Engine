import time
import sys

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message

    def on_message(self, headers, message):
        print 'received a message %s' % message

import stomp
conn = stomp.Connection([("stomp://localhost",61612)])
conn.set_listener('', MyListener())
conn.start()
conn.connect()

conn.subscribe(destination='/queue/test', ack='auto')

conn.send(' '.join(sys.argv[1:]), destination='/queue/test')

time.sleep(2)
conn.disconnect()
