#[macro_use]
extern crate failure;
#[macro_use]
extern crate diesel;

use actix_web::{
    App, HttpServer,
    web,
    middleware,
};
use diesel::{
    r2d2::{self, ConnectionManager, Pool},
    pg::PgConnection,
    result::QueryResult
};
use dotenv;

mod v1;
mod schema;
mod model;


fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();

    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    let pool = Pool::builder()
        .build(manager).expect("Fail to create pool");

    env_logger::init();

    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .wrap(middleware::Logger::new("%a %r"))
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
