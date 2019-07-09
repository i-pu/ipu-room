pub mod plugin;
pub mod user;
pub mod room;
pub mod active_plugin;



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
