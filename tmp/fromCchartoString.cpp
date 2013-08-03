#include<iostream>
#include<cstdio>
#include<cstring>

int main()
{
	char ip[22] ,tmp[22] ;
	const char* ipstring = "some Text :: 12.23.45.4";
	if ( sscanf(ipstring,"%*{%c%} :: %s", &ip) != 1 ) {
		perror("Could not extract XXX from message object") ;
	}
	strcpy(tmp, ipstring) ;
	strtok(tmp, "::") ;
	std::cout << "Not The ip should be: " << tmp << std::endl; 
	std::cout << "The ip should be: " << strtok(NULL, "::")  <<  std::endl ;

	int i = 10 ;
	/*while ( tmp != NULL && --i ){
		std::cout << strtok(NULL, "::");
	}
	std::cout << " we extracted this ip : " << ip  << std::endl ;
	*/
	return 0; 
}
