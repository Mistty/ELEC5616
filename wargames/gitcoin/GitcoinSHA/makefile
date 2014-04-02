CC=g++
CFLAGS=-Wall -std=c++0x -O3
LDFLAGS=-pthread 
REDISLIB=libhiredis.a
SOURCES=main.cpp sha1.cpp 
64BIT=sha1-fast-64.S
32BIT=sha1-fast-32.S
EXECUTABLE=sha1

all:
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) $(REDISLIB) $(64BIT) -o $(EXECUTABLE)

32bit: 
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) $(REDISLIB) $(32BIT) -o $(EXECUTABLE)
	
