use std::os::unix::io::RawFd;

mod sockets {
    include!(concat!(env!("OUT_DIR"), "/sockets.rs"));
}

/// Open a `SOCK_STREAM` socket listening on the specified port.
pub fn listening_socket(port: u16) -> nix::Result<RawFd> {
    todo!()
}

/// Accept a connection on the specified sockfd.
pub fn accept_connection(sockfd: RawFd) -> nix::Result<RawFd> {
    todo!()
}

/// Read one message from `sockfd` and fill the parameters.
/// Make sure that the whole message is read.
pub fn recv_msg(sockfd: RawFd) -> Result<sockets::Message, ()> {
    todo!()
}

/// Send one message to `sockfd` given the parameters.
/// Make sure that the whole message is sent.
pub fn send_msg(sockfd: RawFd, message: sockets::Message) -> Result<(), ()> {
    todo!()
}

/// Expose FFI with unmangled symbols to be used as shared C library.
mod ffi {
    use std::{convert::TryInto, os::raw::c_int};

    /// Open a `SOCK_STREAM` socket listening on the specified port.
    ///
    /// Return `sockfd` if successful, `-1` on failure.
    #[no_mangle]
    pub extern "C" fn listening_socket(port: c_int) -> c_int {
        super::listening_socket(port.try_into().unwrap()).unwrap_or(-1)
    }

    /// Accept a connection on the specified sockfd.
    ///
    /// Return `sockfd` of new connection when successful, `-1` on failure.
    #[no_mangle]
    pub extern "C" fn accept_connection(sockfd: c_int) -> c_int {
        super::accept_connection(sockfd).unwrap_or(-1)
    }

    /// Read one message from `sockfd` and fill the parameters.
    /// Make sure that the whole message is read.
    ///
    /// Return `0` on success, `1` on failure.
    #[no_mangle]
    pub extern "C" fn recv_msg(
        sockfd: c_int,
        operation_type: *mut i32,
        argument: *mut i64,
    ) -> c_int {
        if let Ok(message) = super::recv_msg(sockfd) {
            unsafe { *operation_type = message.r#type().into() };
            unsafe { *argument = message.argument() };
            0
        } else {
            1
        }
    }

    /// Send one message to `sockfd` given the parameters.
    /// Make sure that the whole message is sent.
    ///
    /// Return `0` on success, `1` on failure.
    #[no_mangle]
    pub extern "C" fn send_msg(sockfd: c_int, operation_type: i32, argument: i64) -> c_int {
        let mut message = super::sockets::Message::default();
        message.set_type(
            if let Some(message_type) =
                super::sockets::message::OperationType::from_i32(operation_type)
            {
                message_type
            } else {
                return 1;
            },
        );
        message.argument = Some(argument);

        super::send_msg(sockfd, message).map(|_| 0).unwrap_or(1)
    }
}
