CXX = g++
CXXFLAGS = -O2 -std=c++17 -Wall -g
LDFLAGS = -lprotobuf -lpthread

.PHONY: all

all: test_client_testserver

test_client_testserver: test_client_testserver.cpp
	$(CXX) $(CXXFLAGS) -I.. -o $@ $< -L.. -lutils $(LDFLAGS) 

clean:
	-rm -f test_client_testserver

check: all
	python3 ./test_client_singlethreaded.py
	python3 ./test_client_multithreaded.py
	python3 ./test_server_singlethreaded.py
	python3 ./test_server_multithreaded.py
