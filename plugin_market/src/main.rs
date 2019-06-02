#[macro_use]
extern crate failure;
#[macro_use]
extern crate diesel;

mod v1;
mod schema;
mod model;

use actix_web::{
    App, Result, http, HttpRequest, HttpResponse, Responder, FromRequest,
    web::{self, Json}, HttpServer, ResponseError,
};
use diesel::{r2d2::{self, ConnectionManager, Pool}, pg::PgConnection, result::QueryResult};
use futures::{Future, future};
use dotenv;
use uuid::Uuid;
use diesel::query_dsl::RunQueryDsl;
use crate::model::PluginInfo;


fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();
    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    let pool = Pool::builder()
        .build(manager).expect("Fail to create pool");


    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .service(web::resource("/api/v1/plugins")
                .route(web::get().to(v1::plugin::get_all_plugins))
                .route(web::post().to(v1::plugin::post_plugin)))

            .service(web::resource("/api/v1/plugins/{id}")
                .route(web::get().to(v1::plugin::get_plugin))
                .route(web::put().to(v1::plugin::put_plugin)))

            .service(web::resource("/api/v1/hello")
                .route(web::get().to(v1::hello)))
    })
        .bind("localhost:8888")?
        .run()
}
