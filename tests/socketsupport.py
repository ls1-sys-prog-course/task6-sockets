import tempfile
import sys
import random
import subprocess
import os
import time

from testsupport import (
    run_project_executable,
    info,
    warn,
    find_project_executable,
    test_root,
    project_root,
    run,
    ensure_library,
)


def run_client(num_threads: int, port: int, num_messages: int, add: int, sub: int):
    info(
        f"Running client with {num_threads} threads and {num_messages} messages per thread."
    )

    extra_env = {"LD_LIBRARY_PATH": project_root()}

    with tempfile.TemporaryFile(mode="w+") as stdout:
        run_project_executable(
            "client",
            args=[
                str(num_threads),
                "localhost",
                str(port),
                str(num_messages),
                str(add),
                str(sub),
            ],
            extra_env=extra_env,
            stdout=stdout,
        )

        stdout.seek(0)
        lines = stdout.read().splitlines()
        numbers = [int(x) for x in lines]
        if len(numbers) != num_threads:
            warn(f"Expected {num_threads} results from client, got {len(numbers)}")
            sys.exit(1)

        return sorted(numbers)


def test_server(
    num_server_threads: int,
    num_client_threads: int,
    num_client_instances: int,
) -> None:
    try:
        server = find_project_executable("server")
        extra_env = {"LD_LIBRARY_PATH": project_root()}

        sub = random.randint(1, 49)
        add = random.randint(50, 99)
        num_messages = 10000

        info(f"Run server with {num_server_threads} threads...")

        with subprocess.Popen(
            [server, str(num_server_threads), "1025"],
            stdout=subprocess.PIPE,
            text=True,
            env=extra_env,
        ) as proc:
            # Wait for server init
            time.sleep(1.0)

            pid_ = proc.pid
            test_proc = subprocess.Popen(['ps' ,'-o', 'thcount', str(pid_)],
                           stdout=subprocess.PIPE,
                           text=True,)
            shell_out, _ = test_proc.communicate()
            test_proc.terminate()

            output = shell_out.splitlines()
            thread_count = int(output[-1].strip()) - 1
            client_numbers = []

            for _ in range(num_client_instances):
                client_numbers = client_numbers + run_client(
                    num_client_threads, 1025, num_messages, add, sub
                )

            client_numbers.sort()

            proc.terminate()
            stdout, _ = proc.communicate()
            unsorted_server_numbers = [int(x) for x in stdout.splitlines()]
            sorted_server_numbers = sorted(unsorted_server_numbers)

            if thread_count != num_server_threads:
                warn(f"Expected server threads number incorrect, got {thread_count}")
                sys.exit(1)

            if client_numbers != sorted_server_numbers:
                warn(f"Client and server responded differently")
                sys.exit(1)

            expected = (
                num_client_instances
                * num_client_threads
                * (num_messages // 2)
                * (add - sub)
            )
            if unsorted_server_numbers[-1] != expected:
                warn(
                    f"Expected {expected} as last number, got {unsorted_server_numbers[-1]}"
                )
                sys.exit(1)

            info("OK")

    except OSError as e:
        warn(f"Failed to run command: {e}")
        sys.exit(1)


def test_client(num_threads: int) -> None:
    test_server = test_root().joinpath("test_client_testserver")

    if not test_server.exists():
        run(["make", "-C", str(test_root()), "test_client_testserver"])

    lib = ensure_library("libutils.so")
    extra_env = {"LD_LIBRARY_PATH": str(os.path.dirname(lib))}

    try:
        info(f"Run test server {test_server}...")

        sub = random.randint(1, 49)
        add = random.randint(50, 99)
        num_messages = 10000

        with subprocess.Popen(
            [test_server, "1025"], stdout=subprocess.PIPE, env=extra_env, text=True
        ) as proc:
            # Wait for server init
            time.sleep(1.0)

            client_numbers = run_client(num_threads, 1025, num_messages, add, sub)

            proc.terminate()
            stdout, _ = proc.communicate()
            unsorted_server_numbers = [int(x) for x in stdout.splitlines()]
            sorted_server_numbers = sorted(unsorted_server_numbers)

            if client_numbers != sorted_server_numbers:
                warn(f"Client and server responded differently")
                sys.exit(1)

            expected = num_threads * (num_messages // 2) * (add - sub)
            if unsorted_server_numbers[-1] != expected:
                warn(
                    f"Expected {expected} as last number, got {unsorted_server_numbers[-1]}"
                )
                sys.exit(1)

            info("OK")

    except OSError as e:
        warn(f"Failed to run command: {e}")
        sys.exit(1)

def test_server_performance(
    num_server_threads: int,
    num_client_threads: int,
    num_client_instances: int,
    proportion: int) -> None:

    # Sanity check
    assert(all([proportion, num_client_instances, num_client_threads,
                num_server_threads]), f"no argument can be 0 in invocation of {__name__}")

    # Determine duration of single-threaded server
    try:
        start = time.monotonic_ns()
        test_server(1, num_client_threads, num_client_instances)
        duration_single = time.monotonic_ns() - start

        # Determine duration of multi-threaded server
        start = time.monotonic_ns()
        test_server(num_server_threads, num_client_threads, num_client_instances)
        duration_multi = time.monotonic_ns() - start

        min_speedup = 1-proportion
        speedup = duration_multi / duration_single

        info("Your speedup " + str(speedup*100) + " vs minimum speedup " + str(min_speedup*100))
        if speedup < min_speedup:
            warn(f"Minimum speedup of {min_speedup*100:.1f}% not achieved, current speedup: {speedup*100:.1f}%")
            sys.exit(1)

        info("OK")
    except Exception as e:
        warn(f"Failed due to exception: {e}")
        sys.exit(1)

