class A:
	""" definition of the Class foo class"""
	def __init__(self,arg):
		print "Start class A with arg : " + arg
	def byby(self):
		print "End ...."


if __name__ == "__main__" :
	print "STarting the new program"
	a = A('test class')
	a.byby()
	print "Finish the programm ."
