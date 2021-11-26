# Set you prefererred CFLAGS/compiler compiler here.
# Our github runner provides gcc-10 by default.
CC ?= cc
CFLAGS ?= -g -Wall -O2
CXX ?= c++
CXXFLAGS ?= -g -Wall -O0
CARGO ?= cargo
RUSTFLAGS ?= -g
LDFLAGS = -lprotobuf -lpthread

.PHONY: all clean

all:
	echo "Set build command here"
	exit 1

clean:
	-rm -f server client libutils.so message.pb.*

# libutils.so: utils.cpp message.pb.cc
# 	$(CXX) $(CXXFLAGS) -shared -fPIC -o $@ utils.cpp message.pb.cc $(LDFLAGS)

# server: server_nb.cpp utils.cpp message.pb.cc
# 	$(CXX) $(CXXFLAGS) -o $@ server_nb.cpp utils.cpp message.pb.cc $(LDFLAGS)

# client: client.cpp utils.cpp message.pb.cc
# 	$(CXX) $(CXXFLAGS) -o $@ client.cpp utils.cpp message.pb.cc $(LDFLAGS)

message.pb.cc: message.proto
	protoc --cpp_out=. $^

# Usually there is no need to modify this
check: all
	$(MAKE) -C tests check