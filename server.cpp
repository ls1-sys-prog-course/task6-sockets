#include <atomic>
#include <iostream>
#include <string>

#include "utils.h"

std::atomic<int64_t> number{0};

int main(int args, char *argv[]) {
    if (args < 3) {
        std::cerr << "usage: ./server <numThreads> <port>\n";
        exit(1);
    }

    int numThreads = std::atoi(argv[1]);
    int port = std::atoi(argv[2]);

    return 0;
}
