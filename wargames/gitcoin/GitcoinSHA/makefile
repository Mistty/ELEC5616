CC=g++
CFLAGS=-Wall -std=c++0x -static-libstdc++ -O3
LDFLAGS=-pthread 
SOURCES=main.cpp sha1.cpp 
64BIT=sha1-fast-64.S
32BIT=sha1-fast-32.S
OBJECTS=$(SOURCES:.cpp=.o) sha1-fast-64.o
EXECUTABLE=sha1

all:
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) $(64BIT) -o $(EXECUTABLE)

32bit: 
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) $(32BIT) -o $(EXECUTABLE)
	
