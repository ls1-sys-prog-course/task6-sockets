// DO NOT EDIT

#include <unistd.h>

#include <iostream>
#include <string>

#include "utils.h"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "usage: ./test_client_testserver <port>\n";
        return 1;
    }

    int port = std::atoi(argv[1]);
    int listenfd = listening_socket(port);

    if (listenfd == -1) {
        fprintf(stderr, "Failed creating listening socket.");
        exit(1);
    }

    int64_t counter = 0;
    int32_t operation_type = 0;
    int64_t argument = 0;

    while (true) {
        int connfd = accept_connection(listenfd);

        if (connfd == -1) {
            fprintf(stderr, "Failed accepting new connection.");
            exit(1);
        }

        bool connected = true;

        while (connected) {
            if (recv_msg(connfd, &operation_type, &argument) != 0) {
                fprintf(stderr, "Failed receiving message from client.");
                exit(1);
            }

            switch (operation_type) {
                case OPERATION_ADD: {
                    counter += argument;
                    break;
                }

                case OPERATION_SUB: {
                    counter -= argument;
                    break;
                }

                case OPERATION_TERMINATION: {
                    printf("%ld\n", counter);
                    fflush(stdout);

                    if (send_msg(connfd, OPERATION_COUNTER, counter) != 0) {
                        fprintf(stderr, "Failed sending message to client.");
                        exit(1);
                    }

                    close(connfd);
                    connected = false;
                    break;
                }
            }
        }
    }

    close(listenfd);
}
