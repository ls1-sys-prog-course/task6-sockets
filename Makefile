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

all: libutils.so server client

clean:
	-rm -f server client libutils.so message.pb.*

# --- C++ build steps ---

# message.pb.cc: message.proto
# 	protoc --cpp_out=. $^

# libutils.so: utils.cpp message.pb.cc
# 	$(CXX) $(CXXFLAGS) -shared -fPIC -o $@ utils.cpp message.pb.cc $(LDFLAGS)

# server: server.cpp libutils.so message.pb.cc
# 	$(CXX) $(CXXFLAGS) -o $@ server.cpp message.pb.cc -L. -Wl,-rpath=. -lutils $(LDFLAGS)

# client: client.cpp libutils.so message.pb.cc
# 	$(CXX) $(CXXFLAGS) -o $@ client.cpp message.pb.cc -L. -Wl,-rpath=. -lutils $(LDFLAGS)

# --- Rust build steps ---

# libutils.so:
# 	cargo build --lib && cp target/debug/libutils.so .

# server:
# 	cargo build --bin server && cp target/debug/server .

# client:
# 	cargo build --bin client && cp target/debug/client .

# Usually there is no need to modify this
check: all
	$(MAKE) -C tests check
