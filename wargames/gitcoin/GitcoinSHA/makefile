CC=g++
CFLAGS=-Wall -std=c++0x -O3
LDFLAGS=-pthread 
SOURCES=main.cpp sha1.cpp sha1-fast-64.S
OBJECTS=$(SOURCES:.cpp=.o) sha1-fast-64.o
EXECUTABLE=sha1

all: 
	$(CC) $(CFLAGS) $(LDFLAGS) $(SOURCES) -o $(EXECUTABLE)
	
