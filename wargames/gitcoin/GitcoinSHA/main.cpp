#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <cstdlib>
#include <thread>
#include <atomic>
#include <sys/time.h>
#include <cstring>

#include "sha1.h"

using namespace std;
using namespace chrono;

namespace
{
	atomic<unsigned long int> result;
	bool resultFound(false);
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
};

void findNonce(unsigned int threadId)
{
	sha1::Hasher hasher(baseMessage);

	for (unsigned long int nonce = threadId; !resultFound; nonce+=numthreads)
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
			resultFound = true;
			result = nonce;
		}
	}
}

int main(int argc, char** argv)
{
	if (argc < 5)
		cout << "Invalid args" << endl << "Usage is <message> <target> <#threads> <salt>" << endl;
	else
	{
		baseMessage = argv[1];
		goal = argv[2];
		numthreads = atoi(argv[3]);
		salt = argv[4];

		//spawn threads
		thread* threads = new thread[numthreads];
		for (int i = 0; i < numthreads-1; i++)
			threads[i] = thread(findNonce, (unsigned int)i);
			
		//the main thread may as well do some work too
		findNonce(numthreads-1);
		
		//join threads and return answer
		for (int i = 0; i < numthreads -1 ; i++)
			threads[i].join();
			
		char nonstr[17];
		printNonce(result.load(), nonstr);
			
		cout << nonstr << endl;
		
		delete[] threads;
	}
}


