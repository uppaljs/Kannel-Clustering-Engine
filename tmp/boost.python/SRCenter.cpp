#include <cstdio>
#include <cstring>          // Needed for str*()
#include "ActiveMQSender.h"
#include <string>
#include <unistd.h>

#define BUF_SIZE 40000

class AMQ
{
private :
	ActiveMQSender* sr_sender;
	std::string ip ;
	std::string port;
	std::string Qname;

public :
	AMQ( std::string ip,  std::string port, std::string Qname )
        : ip(ip), port(port), Qname(Qname)
	{
		std::cout << "Constructor" << std::endl;
		sr_sender = new ActiveMQSender(ip, port, Qname);
	}
	~AMQ()
	{
		std::cout << "Destructor" << std::endl;
		delete sr_sender;
	}

	void  enqueue(std::string msg)
	{
	    	std::cout << "Inside enqueue" << std::endl;
	    	sr_sender->Insert(msg.c_str());
		std::cout << "End enqueeu" << std::endl;
	}
	void dequeue()
	{
	}

};

int main(int argc, char **argv)
{
	std::cout << "ZZZZZZZZZZZZZZZZeft" << std::endl;
	activemq::library::ActiveMQCPP::initializeLibrary();
	AMQ x("localhost","61612","FOO.BAR");
	x.enqueue("TeSt");
	usleep(5000000);
	//activemq::library::ActiveMQCPP::shutdownLibrary();
	return 0;
}

