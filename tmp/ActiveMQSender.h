#ifndef ACTIVEMQ_DYNAMIC_SENDER_H_
#define ACTIVEMQ_DYNAMIC_SENDER_H_
#include <string>
#include <list>
#include <activemq/core/ActiveMQConnectionFactory.h>
#include <activemq/library/ActiveMQCPP.h>
#ifdef WIN32
#include <windows.h>
#include <process.h>        // Needed for _beginthread() and _endthread()
#else
#include <pthread.h>
#include <semaphore.h>
#endif
class ActiveMQDynamicSender
{
#ifdef WIN32
    HANDLE                   thread_handle;
    HANDLE                   messages_semaphore;
    CRITICAL_SECTION         messages_critical_section;
    friend unsigned int __stdcall QueueMessageProc(void *ptr);
#else
    pthread_t                thread_id;
    sem_t                    messages_semaphore;
    pthread_mutex_t          messages_mutex;
    friend void             *QueueMessageProc(void *ptr);
#endif
    std::list< std::pair<std::string, std::string> > messages;
    std::string              activemq_ip;
    std::string              activemq_port;
    bool                     running;
    void                     SendToQueue();
public:
    ActiveMQDynamicSender(std::string activemq_ip,
                          std::string activemq_port);
    ~ActiveMQDynamicSender();
    void Insert(std::string activemq_name, std::string sms);
};
#endif /* ACTIVEMQ_DYNAMIC_SENDER_H_ */

