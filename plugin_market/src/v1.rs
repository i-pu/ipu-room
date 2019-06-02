use actix_web::{HttpRequest, web};

pub mod plugin;

pub fn hello(req: HttpRequest) -> &'static str {
    "hello"
}
