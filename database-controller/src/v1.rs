use std::io::Write;

pub mod plugin;
pub mod user;
pub mod room;
pub mod active_plugin;


pub fn json_log_formatter(formatter: &mut env_logger::fmt::Formatter, record: &log::Record)
                          -> Result<(), std::io::Error> {
    writeln!(formatter,
             "{{severity: {}, target: {}, content: {}, module_path: {}, file: {}, line: {}}}",
             record.level(),
             record.target(),
             record.args(),
             record.module_path().unwrap_or("null"),
             record.file().unwrap_or("unknown"),
             record.line().unwrap_or(0))
}

pub fn healthz() -> &'static str {
    "healthz"
}

pub fn sample() -> &'static str {
    info!("{{\"fn\": \"{}\"", "sample");
    info!("fack");
    "sample"
}

// #[derive()]
// struct MyError {
//
// }
//
// pub fn sample() -> impl error::ResponseError {
// }
