def source():
	return range(1,1000)
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

import Queue 
import threading
q = Queue.Queue()
for i in range(3):
     t = threading.Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()       # block until all tasks are done
