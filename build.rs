fn main() -> std::io::Result<()> {
    prost_build::compile_protos(&["message.proto"], &["."])?;
    Ok(())
}
