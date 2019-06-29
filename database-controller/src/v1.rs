pub mod plugin;
pub mod user;
pub mod room;
pub mod active_plugin;


pub fn healthz() -> &'static str {
    "healthz"
}

// #[derive()]
// struct MyError {
//
// }
//
// pub fn sample() -> impl error::ResponseError {
// }
