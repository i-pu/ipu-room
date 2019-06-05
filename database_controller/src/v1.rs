use actix_web::{HttpRequest, web};

pub mod plugin;

pub fn hello() -> &'static str {
    "hello"
}
