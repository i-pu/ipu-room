use std::io::Write;

use serde::Serialize;

#[derive(Debug, Serialize)]
struct JsonLog<T: Serialize> {
    severity: String,
    /// record.target
    target: String,
    /// must json
    content: T,
    module_path: String,
    file: String,
    line: u32,
}

pub fn json_log_formatter(formatter: &mut env_logger::fmt::Formatter, record: &log::Record)
                          -> Result<(), std::io::Error> {
    let jl = JsonLog {
        severity: format!("{}", record.level()),
        target: format!("{}", record.target()),
        content: record.args(),
        module_path: format!("{}", record.module_path().unwrap_or("null")),
        file: format!("{}", record.file().unwrap_or("unknown")),
        line: record.line().unwrap_or(0),
    };
    writeln!(formatter, "{}", serde_json::to_string(&jl)?)
}
