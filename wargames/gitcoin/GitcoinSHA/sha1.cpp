
#include "sha1.h"
#include <cstring>
#include <iostream>
#include <iomanip>
using namespace std;
namespace sha1
{    
    /* Full message hasher */
	Hasher::Hasher(string prefix)
	{
		messageLen = prefix.size() + 16;
		message = new char[messageLen];
		prefix.copy(message, prefix.size(), 0);
		message[10] = 0;
		sha1_hashPrefix((uint8_t*)message, messageLen - 16);
	}
	
	Hasher::~Hasher()
	{
		delete[] message;
	}
	
	void Hasher::sha1_hashPrefix(uint8_t *message, uint32_t len) {
		prefixHash[0] = uint32_t(0x67452301);
		prefixHash[1] = uint32_t(0xEFCDAB89);
		prefixHash[2] = uint32_t(0x98BADCFE);
		prefixHash[3] = uint32_t(0x10325476);
		prefixHash[4] = uint32_t(0xC3D2E1F0);
		
		int i;
		for (i = 0; i + 64 <= len; i += 64)
			sha1_compress(prefixHash, message + i);
			
		nonceStart = i;
	}
	
	void Hasher::hashNonce(char nonce[16])
	{
		for (int i = 0; i < 16; i++)
			message[messageLen - 16 + i] = (uint8_t)nonce[i];
			
		sha1_appendNonce((uint8_t*)message, messageLen, nonceStart);
	}
	
	void Hasher::sha1_appendNonce(uint8_t *message, uint32_t len, int i) {		
		hash[0] = prefixHash[0];
		hash[1] = prefixHash[1];
		hash[2] = prefixHash[2];
		hash[3] = prefixHash[3];
		hash[4] = prefixHash[4];
		
		for ( ; i + 64 <= len; i += 64)
			sha1_compress(hash, message + i);
		
		uint8_t block[64];
		int rem = len - i;
		memcpy(block, message + i, rem);
		
		block[rem] = 0x80;
		rem++;
		if (64 - rem >= 8)
			memset(block + rem, 0, 56 - rem);
		else {
			memset(block + rem, 0, 64 - rem);
			sha1_compress(hash, block);
			memset(block, 0, 56);
		}
		
		uint64_t longLen = ((uint64_t)len) << 3;
		for (i = 0; i < 8; i++)
			block[64 - 1 - i] = (uint8_t)(longLen >> (i * 8));
		sha1_compress(hash, block);
	}
} // namespace sha1
