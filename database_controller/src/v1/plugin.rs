use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{Plugin};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_plugins(pool: web::Data<Pool>) -> web::Json<Vec<Plugin>> {
    use crate::schema::plugins::dsl::plugins;
    web::Json(plugins.load(&pool.get().unwrap()).unwrap())
}

pub fn get_plugin(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<Plugin> {
    use crate::schema::plugins::dsl::plugins;
    web::Json(plugins.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create plugin
pub fn post_plugin(json: web::Json<Plugin>, pool: web::Data<Pool>)
                   -> web::Json<Plugin>
{
    /// todo: 返り値をResult にする
    use crate::schema::plugins::dsl::plugins;
    let p: Plugin =
        diesel::insert_into(plugins)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update plugin
pub fn put_plugin(json: web::Json<Plugin>, pool: web::Data<Pool>)
                  -> web::Json<Plugin>
{
    use crate::schema::plugins::{dsl::*};
    let mut p: Plugin = json.0;
    p = diesel::update(plugins.find(p.id.clone()))
            .set(p)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
