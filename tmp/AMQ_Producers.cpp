#include <cstdio>
#include <cstring>          // Needed for str*()
#include "ActiveMQSender.h"
#include <string>
#include <unistd.h>

class activemq (int argc, char **argv)
{
    activemq::library::ActiveMQCPP::initializeLibrary();
    return 0;

    sr_sender = new ActiveMQSender(activemq_ip,
			       activemq_port,
                               activemq_name);
    sr_sender->Insert(buffer);
    fprintf(stderr, "(%d) Submit Response : %s\n",++count ,buffer);

}
