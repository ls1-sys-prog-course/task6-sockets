#!/usr/bin/env python3

from testsupport import subtest
from socketsupport import test_client


def main() -> None:
    with subtest("Testing multithreaded client"):
        test_client(num_threads=6)


if __name__ == "__main__":
    main()
