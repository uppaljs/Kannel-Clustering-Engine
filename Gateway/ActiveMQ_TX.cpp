#include <cstdio>
#include <cstring>          // Needed for str*()
#include "ActiveMQSender.h"
#include "Logger.h"
#include "command_line_args.h" // COMMAND_LINE_ARGS
#include <string>
#include <unistd.h>
#include <sys/time.h>
#include <typeinfo>
COMMAND_LINE_ARGS command_line_args;
void print_info(void)
{
#ifdef WIN32
    system("cls"); // clear screen
#else
    system("clear");
#endif
    FORCE_TRACE(1, "*********************************************************");
    FORCE_TRACE(1, "*        ActiveMQ sender Copyright(C) CEQUENS           *");
    FORCE_TRACE(1, "*********************************************************");
    FORCE_TRACE(1, "Active MQ IP    : %s"  , command_line_args.activemq_ip);
    FORCE_TRACE(1, "Active MQ Port  : %s"  , command_line_args.activemq_port);
    FORCE_TRACE(1, "Active MQ Name  : %s\n", command_line_args.activemq_name);
    FORCE_TRACE(1, "Trace Level     : %d\n", command_line_args.trace_level);
    FORCE_TRACE(1, "Start TimeStamp : %s"  , command_line_args.start_timestamp);
    FORCE_TRACE(1, "*********************************************************");
}

#define BUF_SIZE 4000
/*class SHABANA_AMQ
{
private:
ActiveMQSender          *sr_sender;
public:
    SHABANA_AMQ(std::string ip, std::string port, std::string qname)
    {
        activemq::library::ActiveMQCPP::initializeLibrary();
        sr_sender = new ActiveMQSender(ip,
                                       port,
                                       qname);
    }
    ~SHABANA_AMQ()
    {
        delete sr_sender;
        activemq::library::ActiveMQCPP::shutdownLibrary();
    }
    void Insert(std::string str)
    {
        sr_sender->Insert(str);
    }
};
*/
int main(int argc, char *argv[])
{
    setvbuf(stderr, NULL, _IONBF, 0); //TO Flush O/P directly to log file
    parseargs(&command_line_args, argc, argv);
    getcdate(command_line_args.start_timestamp);
    LoggerSetup(command_line_args.start_timestamp);
    print_info();
    FORCE_TRACE(1, "Initialize ActiveMQ");
    char buffer[BUF_SIZE] ;
    std::string a ;
    int count = 0;
    FILE* fp = popen("tail -f -n1 /tmp/activemq_spool" , "r") ;
    char *msg,*link ;
    std::map<std::string ,ActiveMQSender*> Link_Q_Map ;
    while( fgets(buffer, BUF_SIZE, fp) != NULL  )
    {
	Link_Q_Map[std::string("_X")] = new ActiveMQSender("localhost", "61612", "X" );
	link = strtok(buffer, "|");
	msg =  strtok(NULL, "|");
	std::string LINK(link) ;
	std::cout << LINK << std::endl << msg << std::endl ;
	if( Link_Q_Map.find(LINK) == Link_Q_Map.end() ){ 
		std::cout<< "Inside IF" << std::endl  ;
		activemq::library::ActiveMQCPP::initializeLibrary();
		std::string IP(argv[1]) ; 
		std::string PORT(argv[2]); 

		std::cout << IP << "," << PORT << "," << LINK  << std::endl ;
		std::cout<< "XXXXX" << std::endl;
       		Link_Q_Map[LINK] = new ActiveMQSender("localhost", "61612", "test" );
		//sleep(2);
		std::cout<< "After try to connect and before insert."  ;
		std::cout << LINK << "," << msg << std::endl ;
		if (Link_Q_Map.find(LINK) == Link_Q_Map.end() ) std::cout << " Not Found. " << std::endl ;
		(Link_Q_Map[LINK])->Insert("static string") ;
		 std::cout << "\n Done." << std::endl ;
	}




        Link_Q_Map[link]->Insert(msg);
        fprintf(stderr, "(%d) Insert msg (%s) at link [%s] : %s\n",++count ,msg);
    }
    FORCE_TRACE(1, "ShutDown");
    FORCE_TRACE(1, "shutdown ActiveMQ");
    //activemq::library::ActiveMQCPP::shutdownLibrary();
    LoggerClose();
    return 0;
}

