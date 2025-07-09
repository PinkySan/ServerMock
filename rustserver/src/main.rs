use clap::Parser;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use chrono::Utc;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Address to listen on (e.g. 127.0.0.1:2345)
    #[arg(short, long, default_value = "127.0.0.1:2345")]
    listen: String,
}

fn log_message(prefix: &str, addr: &str, msg: &[u8]) {
    let now = Utc::now().to_rfc3339();
    println!("[{}] {} [{}]: {:?}", now, prefix, addr, msg);
}

// Simple length-prefixed message format
fn read_tcp_message(stream: &mut TcpStream) -> std::io::Result<Vec<u8>> {
    let mut len_buf = [0u8; 4];
    stream.read_exact(&mut len_buf)?;
    let len = u32::from_be_bytes(len_buf) as usize;
    let mut buf = vec![0u8; len];
    stream.read_exact(&mut buf)?;
    Ok(buf)
}

fn write_tcp_message(stream: &mut TcpStream, msg: &[u8]) -> std::io::Result<()> {
    let len = (msg.len() as u32).to_be_bytes();
    stream.write_all(&len)?;
    stream.write_all(msg)?;
    Ok(())
}

fn handle_client(mut stream: TcpStream) -> std::io::Result<()> {
    let addr = stream.peer_addr()?.to_string();
    let msg = read_tcp_message(&mut stream)?;
    log_message("Received", &addr, &msg);

    // Example response: echo the message back
    write_tcp_message(&mut stream, &msg)?;
    log_message("Sent", &addr, &msg);

    Ok(())
}

fn main() -> std::io::Result<()> {
    let args = Args::parse();

    let listener = TcpListener::bind(&args.listen)?;
    println!("Server listening on {}", &args.listen);

    // Only support a single client at a time
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let peer = stream.peer_addr().unwrap();
                println!("Client connected: {}", peer);
                if let Err(e) = handle_client(stream) {
                    eprintln!("Error handling client: {}", e);
                }
                println!("Client disconnected: {}", peer);
            }
            Err(e) => {
                eprintln!("Connection failed: {}", e);
            }
        }
    }
    Ok(())
}