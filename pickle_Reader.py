from sys import argv
import cPickle as pickle

file = argv[1]
fd = open(file,"rb")
x = pickle.load(fd)
fd.close()
print x


