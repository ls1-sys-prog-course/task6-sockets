// DO NOT EDIT

#include <sys/types.h>
#include <unistd.h>

#include <atomic>
#include <chrono>
#include <cstring>
#include <iostream>
#include <thread>
#include <vector>

namespace chrono = std::chrono;

#include "utils.h"

void client_function(const int port, int numMessages, int delay) {
    auto sockfd = connect_socket("localhost", port);

    for (int i = 0; i < numMessages; i++) {
        send_msg(sockfd, OPERATION_ADD, 5);
        std::this_thread::sleep_for(chrono::milliseconds(delay));
    }
    
    fprintf(stderr, "[%d] Done\n", gettid());

    send_msg(sockfd, OPERATION_TERMINATION, 0);

    int32_t operation_type;
    int64_t argument;
    recv_msg(sockfd, &operation_type, &argument);

    close(sockfd);
}

int main(int args, char *argv[]) {
    if (args < 4) {
        std::cerr << "usage: ./test_server_testclient <port> <threads> "
                     "<numMessages> <delay>\n";
        exit(1);
    }

    int port = std::atoi(argv[1]);
    int numThreads = std::atoi(argv[2]);
    int numMessages = std::atoi(argv[3]);
    int delay = std::atoi(argv[4]);

    std::vector<std::thread> threads;

    for (int i = 0; i < numThreads; i++) {
        threads.emplace_back(
            [=]() { client_function(port, numMessages, delay); });
    }

    for (auto &thread : threads) {
        thread.join();
    }

    fprintf(stderr, "All threads done\n");
}
