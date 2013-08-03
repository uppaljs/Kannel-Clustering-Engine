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


std::string initialize()
{


}
//std::string 
void enqueue (std::string  msg)
{
   activemq::library::ActiveMQCPP::initializeLibrary();
   ActiveMQSender *sr_sender;
   /*sr_sender = new ActiveMQSender("localhost",
                                    "61612",
                                    "FOO.BAR");
  */
  sr_sender = ActiveMQSender("192.168.0.108", "61616", "TEST") ;
  printf("You want to enqueue message %s\n ", msg.c_str());
  puts((sr_sender == NULL)?"Not initialized":"Should initialized properly\n");
  puts("Before Inserting Data at the queue");
  
  sr_sender->Insert(msg.c_str());
  usleep(5000000);
  puts("EEnnddd");
 //  return  ((std::string)"Enqueue : " + msg)  ;
 activemq::library::ActiveMQCPP::shutdownLibrary();
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
