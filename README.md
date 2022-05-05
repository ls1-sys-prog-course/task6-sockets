# Task 6 - Sockets

This week, your task is to implement a client/server application over TCP/IP using sockets API (e.g. STREAM_SOCK). 

First you will implement a client which will send requests to the server. Then you will implement the server to process these requests.

- The requests can be of type: `ADD`, `SUB`, and `TERMINATION`.
  - `ADD`/`SUB` manipulate a global counter the server manages.
  - `TERMINATION` notifies the server about a clients termination.
- The server process stores a global counter and atomically updates it based on the received requests. 
- Along with `ADD`/`SUB` requests, the request also contains a number that will be added/sub from the global counter respectively. 
- The `TERMINATION` request instructs the server to sent back to the client a message that contains the value of the global counter via a `COUNTER` message. 
  - In particular, for each `TERMINATION` request the server prints the value of the global counter **and** sends it over the network via a `COUNTER` message.
  - Similarly, each client thread prints the value the server has sent to it via the `COUNTER` response. 
- As a serialization protocol, you are encouraged to use `google::protobufs`. 
  - Note that the `.proto` files that describe the message layout are already provided for you. 

In short, `ADD`/`SUB`/`TERMINATION` are from client to server, while `COUNTER` is from server to client.

The following things are to be delivered:

## Task 6.0

Design a network protocol to implement the requirements above. Note that we encourage you to use Google protobufs (see `message.proto` for a skeleton). You can add additional members to this message. You can also design your own protocol if you want.

## Task 6.1

A library `libutils.so` implementing the interface given in `utils.h`. Please look at the documentation given there.

### Hints:

For `recv_msg` and `send_msg` you will have to make sure that you receive or send a whole message. However, TCP communication does not distinguish between different messages. `recv` system call might return a stream of bytes that refers to more than one distinct application message. To process the individual messages, applications should implement their own message's formatting or serialization protocol.

A common approach is to encapsulate the payload size as follows: `<--size--><--payload-->`, where payload is a serialized protobuf (byte-stream). The size should be a fixed size integer (i.e. `uint32_t`) The receiving side can then always read one 4 byte integer, decode the size and read the specified bytes afterwards.

Note that it's possible that `send` and `recv` do not send or receive the number of bytes passed as arguments. You may have to call them in a loop to make sure that the whole message has been sent or received.

## Task 6.2

Implement the client. It should be callable via: `./client <num_threads> <hostname> <port> <num_messages> <add> <sub>`.

- The client process spawns a number of threads given as `<num_threads>` each of which independently connects to the server.
- The client process takes as an argument the address (`<hostname>` and `<port>`) of the server. 
  Note that in the tests `<hostname>` = `"localhost"`
- After establishing the connection with the server, **each thread** should send a variable number of messages (taken as `<num_messages>`).
  - **Important**: The client should alternate between `ADD` and `SUB` requests, starting with `ADD` until it has sent `<num_messages>`
  - **Important**: The client should use the passed `<add>` and `<sub>` command line parameters as arguments for these requests
- Once all messages are sent, each client-thread should send a `TERMINATION` message to the server. 
- Right after the delivery of the termination message the thread should receive from the server the value of the global counter and should print the received value to stdout
- Once all the client threads have finished, the client process terminates.

### Hints:

Suppose the client is called like

`./client 1 localhost 1025 4 2 1`

it should send

    ADD 2
    SUB 1
    ADD 2
    SUB 1

and print the counter received from the server to stdout.

Reuse the functionality you have implemented for `libutils.so`!

## Task 6.3

Implement the server. It should be callable via: `./server <num_threads> <port`.

- The server process initially spawns a fixed number of threads (taken as `<num_threads>`, e.g. 2, 4, 8). 
- Then it should accept connections on a port passed as `<port>` and listen on `localhost`
- Each server thread should be able to handle multiple connections at the same time, i.e. it should be **non-blocking** (see Hints).
- The server should be available to accept connections at any time and should not terminate (long running process). 
- Once a connection is accepted, the server process should assign this connection to one of the server threads. You could find the elected thread's id by dividing the number of connections with the number of the server threads (`nb_connections % nb_threads`).
- If a server thread receives a termination message, it should reply back to the client the current global counter value via a `COUNTER` message **and** print the counter to stdout

### Hints

Reuse the functionality you have implemented for `libutils.so`!

You might want to use either `select()`, `poll()` or `epoll()` to implement the server threads.

## Notes

`printf()`-based functions are not thread-safe and in the presence of many clients you might print the correct counter values in the same line. In that case, the tests in the grading system might fail.
We encourage you to wrap the print-functions with a global mutex to ensure that a message is flushed to standard output in a specific order. Also you should flush the stream after writing to stdout using `fflush()`.

You might want to set `SO_REUSEADDR` on your sockets to allow easier testing.

## References

- [Protocol Buffer Basics: C++](https://developers.google.com/protocol-buffers/docs/cpptutorial)
- [select()](https://man7.org/linux/man-pages/man2/select.2.html)
- [epoll()](https://man7.org/linux/man-pages/man7/epoll.7.html)
