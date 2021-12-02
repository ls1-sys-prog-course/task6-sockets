mod utils;

use clap::{App, Arg};
use utils::{accept_connection, listening_socket, recv_msg, send_msg};

fn main() {
    let matches = App::new("server")
        .arg(
            Arg::with_name("num_threads")
                .value_name("num_threads")
                .help("The number of threads used to process requests.")
                .takes_value(true)
                .required(true),
        )
        .arg(
            Arg::with_name("port")
                .value_name("port")
                .help("The port the server listens to.")
                .required(true)
                .takes_value(true),
        )
        .get_matches();

    let num_threads = matches
        .value_of("num_threads")
        .unwrap()
        .parse::<u32>()
        .unwrap();
    let port = matches.value_of("port").unwrap().parse::<u32>().unwrap();
}
