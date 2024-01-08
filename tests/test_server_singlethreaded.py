#!/usr/bin/env python3

from testsupport import subtest
from socketsupport import test_server


def main() -> None:
    with subtest("Testing singlethreaded server"):
        test_server(num_server_threads=1, num_client_threads=1, num_client_instances=6)


if __name__ == "__main__":
    main()
