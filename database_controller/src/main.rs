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
    let env = std::env::var("ENV").unwrap_or(String::new());
    if env != "prd" {
        dotenv::dotenv().ok();
    }

    let port = std::env::var("PORT").expect("PORT must be set");

    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let manager = ConnectionManager::<PgConnection>::new(database_url);
    let pool = Pool::builder()
        .build(manager).expect("Fail to create pool");
    env_logger::init();


    // todo: delete も作る
    HttpServer::new(move || {
        App::new()
            .data(pool.clone())
            .wrap(middleware::Logger::new("%a %r"))

            // .service(web::resource("/api/v1/sample")
            //     .route(web::get().to(v1::sample)))
            .service(web::resource("/api/v1/healthz")
                .route(web::get().to(v1::healthz)))

            .service(web::resource("/api/v1/plugins")
                .route(web::get().to(v1::plugin::get_all_plugins))
                .route(web::post().to(v1::plugin::post_plugin)))
            .service(web::resource("/api/v1/plugins/{id}")
                .route(web::get().to(v1::plugin::get_plugin))
                .route(web::put().to(v1::plugin::put_plugin)))

            .service(web::resource("/api/v1/users")
                .route(web::get().to(v1::user::get_all_users))
                .route(web::post().to(v1::user::post_user)))
            .service(web::resource("/api/v1/users/{id}")
                .route(web::get().to(v1::user::get_user))
                .route(web::put().to(v1::user::put_user)))

            .service(web::resource("/api/v1/rooms")
                .route(web::get().to(v1::room::get_all_rooms))
                .route(web::post().to(v1::room::post_room)))
            .service(web::resource("/api/v1/rooms/{id}")
                .route(web::get().to(v1::room::get_room))
                .route(web::put().to(v1::room::put_room)))

            .service(web::resource("/api/v1/active_plugins")
                .route(web::get().to(v1::active_plugin::get_all_active_plugins))
                .route(web::post().to(v1::active_plugin::post_active_plugin)))
            .service(web::resource("/api/v1/active_plugins/{id}")
                .route(web::get().to(v1::active_plugin::get_active_plugin))
                .route(web::put().to(v1::active_plugin::put_active_plugin)))
    })
        .bind("0.0.0.0:".to_owned()+&port)?
        .run()
}
