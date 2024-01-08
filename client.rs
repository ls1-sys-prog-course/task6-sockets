mod utils;

use clap::{App, Arg};
use utils::{recv_msg, send_msg};

fn main() {
    let matches = App::new("client")
        .arg(
            Arg::with_name("num_threads")
                .value_name("num_threads")
                .help("A number of threads each of which the client independently connects to the server.")
                .takes_value(true)
                .required(true),
        )
        .arg(
            Arg::with_name("hostname")
                .value_name("hostname")
                .help("The hostname of the server to connect to.")
                .required(true)
                .takes_value(true),
        )
        .arg(
            Arg::with_name("port")
                .value_name("port")
                .help("The port of the server to connect to.")
                .required(true)
                .takes_value(true),
        )
        .arg(
            Arg::with_name("num_messages")
                .value_name("num_messages")
                .help("The number of messages to be sent by the client.")
                .required(true)
                .takes_value(true),
        )
        .arg(
            Arg::with_name("add")
                .value_name("add")
                .help("The argument passed to ADD requests.")
                .required(true)
                .takes_value(true),
        )
        .arg(
            Arg::with_name("sub")
                .value_name("sub")
                .help("The argument passed to SUB requests.")
                .required(true)
                .takes_value(true),
        )
        .get_matches();

    let num_threads = matches
        .value_of("num_threads")
        .unwrap()
        .parse::<u32>()
        .unwrap();
    let hostname = matches
        .value_of("hostname")
        .unwrap()
        .parse::<String>()
        .unwrap();
    let port = matches.value_of("port").unwrap().parse::<u32>().unwrap();
    let num_messages = matches
        .value_of("num_messages")
        .unwrap()
        .parse::<u32>()
        .unwrap();
    let add = matches.value_of("add").unwrap().parse::<u32>().unwrap();
    let sub = matches.value_of("sub").unwrap().parse::<u32>().unwrap();
}
