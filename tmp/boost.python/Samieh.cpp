#include <cstdio>
#include <cstring>          // Needed for str*()
#include "ActiveMQSender.h"
#include "Logger.h"
#include "command_line_args.h" // COMMAND_LINE_ARGS
#include <string>
#include <unistd.h>
COMMAND_LINE_ARGS command_line_args;
void print_info(void)
{
#ifdef WIN32
    system("cls"); // clear screen
#else
    system("clear");
#endif
    FORCE_TRACE(1, "*********************************************************");
    FORCE_TRACE(1, "*        SR Center v1.0 rev36  Copyright(C) CEQUENS     *");
    FORCE_TRACE(1, "*********************************************************");
    FORCE_TRACE(1, "Active MQ IP    : %s"  , command_line_args.activemq_ip);
    FORCE_TRACE(1, "Active MQ Port  : %s"  , command_line_args.activemq_port);
    FORCE_TRACE(1, "Active MQ Name  : %s\n", command_line_args.activemq_name);
    FORCE_TRACE(1, "Trace Level     : %d\n", command_line_args.trace_level);
    FORCE_TRACE(1, "Start TimeStamp : %s"  , command_line_args.start_timestamp);
    FORCE_TRACE(1, "*********************************************************");
}

#define BUF_SIZE 4000
class SHABANA_AMQ
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
int main(int argc, char *argv[])
{
    setvbuf(stderr, NULL, _IONBF, 0); //TO Flush O/P directly to log file
    parseargs(&command_line_args, argc, argv);
    getcdate(command_line_args.start_timestamp);
    LoggerSetup(command_line_args.start_timestamp);
    print_info();
    FORCE_TRACE(1, "Initialize ActiveMQ");
    //activemq::library::ActiveMQCPP::initializeLibrary();
    SHABANA_AMQ *shosho = new SHABANA_AMQ(command_line_args.activemq_ip,
                                          command_line_args.activemq_port,
                                          command_line_args.activemq_name);

    char buffer[BUF_SIZE] ;
    int count = 0;
    FILE* fp = popen("tail /var/log/secure" , "r") ;
    while( fgets(buffer, BUF_SIZE, fp) != NULL  )
    {
        shosho->Insert(buffer);
        fprintf(stderr, "(%d) Submit Response : %s\n",++count ,buffer);
        fflush(stdin);
    }
    FORCE_TRACE(1, "ShutDown");
    delete shosho;
    FORCE_TRACE(1, "shutdown ActiveMQ");
    //activemq::library::ActiveMQCPP::shutdownLibrary();
    LoggerClose();
    return 0;
}

