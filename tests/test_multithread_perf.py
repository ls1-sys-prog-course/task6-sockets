#!/usr/bin/env python3

from testsupport import subtest
from socketsupport import test_server_performance

def main() -> None:
    # with subtest("Testing multithreaded server performance"):
    test_server_performance(num_server_threads=4, num_client_threads=6, num_client_instances=6, proportion=1/2)


if __name__ == "__main__":
    main()

