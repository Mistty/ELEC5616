#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <cstdlib>
#include <thread>
#include <atomic>
#include <sys/time.h>
#include <cstring>
#include <fstream>

#include "sha1.h"
#include "hiredis.h"

using namespace std;
using namespace chrono;

namespace
{
	string baseMessage;
	string goal;
	int numthreads;
	string salt;
	
	void printNonce(unsigned long int nonce, char nonstr[17])
	{
		nonstr[16] = '\0';
		sprintf(nonstr, "%lu", nonce);
		bool startWriting=false;
		for (char* c = nonstr; c != nonstr+16; c++)
		{
			if (*c == '\0')
				startWriting = true;
			if (startWriting)
				*c = '0';
		}
		
		salt.copy(nonstr + 16 - salt.size(), salt.size(), 0);
	}
	
	void outputAnswer(long int result)
	{
		char nonstr[17];
		printNonce(result, nonstr);
			
		cout << "Nonce: " << nonstr << endl;
			
		ofstream output("minedcommit.txt");
		output << baseMessage << nonstr;
		
		cout << "Updated commit message written to minedcommit.txt" << endl;
	}

	void findNonce(unsigned int threadId)
	{
		sha1::Hasher hasher(baseMessage);

		for (unsigned long int nonce = threadId; true; nonce+=numthreads)
		{
			char nonstr[17];
			printNonce(nonce, nonstr);
			
			hasher.hashNonce(nonstr);
			
			stringstream resultstr;

			for (int i = 0; i < 5; i++)
			{
				resultstr << setfill('0') << setw(8) << hex << (int)(hasher.hash[i]);
			}

			if (goal > resultstr.str())
			{
				cout << "Hash: " << resultstr.str() << endl;
				outputAnswer(nonce);
				exit(0);
			}
		}
	}
};

int main(int argc, char** argv)
{ 
	if (argc < 5)
		cout << "Invalid args" << endl << "Usage is <filepath> <target> <#threads> <salt>" << endl;
	else
	{
		//connect to redis
		redisContext *c = redisConnect("cryptologic.org", 6379);
		if (c != NULL && c->err) {
			printf("Error: %s\n", c->errstr);
			// handle error
		}
		cout << "Connected to redis" << endl;
		
		string path = argv[1];
		goal = argv[2];
		numthreads = atoi(argv[3]);
		salt = argv[4];
		std::ifstream in(path, std::ios::in | std::ios::binary);
		if (in)
		{
			in.seekg(0, std::ios::end);
			baseMessage.resize(in.tellg());
			in.seekg(0, std::ios::beg);
			in.read(&baseMessage[0], baseMessage.size());
			in.close();
		}

		//spawn threads
		thread* threads = new thread[numthreads];
		for (int i = 0; i < numthreads; i++)
		{
			threads[i] = thread(findNonce, (unsigned int)i);
			threads[i].detach();
		}
			
		redisReply *reply = (redisReply *)redisCommand(c,"SUBSCRIBE gitcoin");
		freeReplyObject(reply);
		while(redisGetReply(c,(void**)&reply) == REDIS_OK) {
			cout << "Solution found elsewhere" << endl;
			cout << reply->element[2]->str << endl;
			freeReplyObject(reply);
			cout << "Terminating" << endl;
			quick_exit(1);
		}
		
		return 1;
	}
}


