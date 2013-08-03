//  Copyright Joel de Guzman 2002-2004. Distributed under the Boost
//  Software License, Version 1.0. (See accompanying file LICENSE_1_0.txt
//  or copy at http://www.boost.org/LICENSE_1_0.txt)
//  Hello World Example from the tutorial
//  [Joel de Guzman 10/9/2002]

#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <string>
#include <stdlib.h>
#include "ActiveMQSender.h"
#include <unistd.h>
#include <cstdio>
#include <cstring>          // Needed for str*()
#include "ActiveMQSender.h"
#include "Logger.h"
#include "command_line_args.h" // COMMAND_LINE_ARGS
#include <string>
#include <unistd.h>

std::string initialize()
{


}
//std::string 
void enqueue (std::string  msg)
{
	// #################################################
COMMAND_LINE_ARGS command_line_args;
#define BUF_SIZE 4000

ActiveMQSender          *sr_sender;
    setvbuf(stderr, NULL, _IONBF, 0); //TO Flush O/P directly to log file
    parseargs(&command_line_args, argc, argv);
    getcdate(command_line_args.start_timestamp);
    LoggerSetup(command_line_args.start_timestamp);
    print_info();
    FORCE_TRACE(1, "Initialize ActiveMQ");
    activemq::library::ActiveMQCPP::initializeLibrary();
    sr_sender = new ActiveMQSender(command_line_args.activemq_ip,
                                    command_line_args.activemq_port,
                                    command_line_args.activemq_name);
    char buffer = "Hellow , world : this is my first message ." ;
    int count = 0;
        sr_sender->Insert(buffer);
        fprintf(stderr, "(%d) Submit Response : %s\n",++count ,buffer);
    usleep(5000000);
    FORCE_TRACE(1, "ShutDown");
    delete sr_sender;
    FORCE_TRACE(1, "shutdown ActiveMQ");
    activemq::library::ActiveMQCPP::shutdownLibrary();
    LoggerClose();
}
	
	
	// ##################################################
}

std::string dequeue(std::string msg, std::string link)
{

   return  ((std::string)"Dequeu : " + msg + " FROM Link : " + link )  ;
}
/*

BOOST_PYTHON_MODULE(ActiveMQ)
{
    using namespace boost::python;
    def("Enqueue", enqueue);
    def("Dequeue",dequeue);
}

*/

int main () { enqueue("TEeeSsTt\0"); return 0 ; }
