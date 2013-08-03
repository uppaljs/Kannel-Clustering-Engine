import ConfigParser


cnf = ConfigParser.RawConfigParser()
cnf.add_section('ports')
cnf.set('ports' , 'core-admin-port' , '2' )
with  open('../runTime/itr','wb') as f :
	cnf.write(f)
if not f.closed : f.close()
print "Byvyyyy"
