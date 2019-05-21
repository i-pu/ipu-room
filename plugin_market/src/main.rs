use actix_web::{App, Result, http, HttpRequest, HttpResponse, Responder,  FromRequest, web::{self, Json}, HttpServer};
use serde::{Deserialize, Serialize};
use futures::{Future, future};

#[derive(Serialize, Deserialize, Debug)]
struct PluginPath {
    id: String,
}

fn plugin_get(req: HttpRequest, ppjson: Json<PluginPath>) -> Json<Vec<PluginPath>> {
    println!("{:?}", ppjson);
    Json(vec![ppjson.0])
}

fn main() -> std::io::Result<()>{
    HttpServer::new(|| {
        App::new()
        .service(web::resource("/").route(web::post().to(plugin_get)))
    })
        .bind("127.0.0.1:8888")?
        .run()
}
