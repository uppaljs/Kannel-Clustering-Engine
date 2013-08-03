g++ -fPIC -c Try_to_be_final_from_Samieh_version.cpp /home/ec2-user/Devel/common/*.cpp   -I/home/ec2-user/Devel/common/  -I/usr/include/python2.6/ -I/usr/src/activemq-cpp-library-3.4.4/src/main/ -I/usr/include/apr-1/ 


g++ -shared -Wl,soname,ShabanaAMQ.so -o Try_to_be_final_from_Samieh_version.so -I/home/ec2-user/Devel/common/  -I/usr/include/python2.6/ -I/usr/src/activemq-cpp-library-3.4.4/src/main/ -I/usr/include/apr-1/ -lpthread -lrt -lactivemq-cpp -lpython2.6 -lboost_python
