use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{ActivePlugin};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_active_plugins(pool: web::Data<Pool>) -> web::Json<Vec<ActivePlugin>> {
    use crate::schema::active_plugins::dsl::active_plugins;
    web::Json(active_plugins.load(&pool.get().unwrap()).unwrap())
}

pub fn get_active_plugin(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<ActivePlugin> {
    use crate::schema::active_plugins::dsl::active_plugins;
    web::Json(active_plugins.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create active_plugin
pub fn post_active_plugin(json: web::Json<ActivePlugin>, pool: web::Data<Pool>)
                   -> web::Json<ActivePlugin>
{
    /// todo: 返り値をResult にする
    use crate::schema::active_plugins::dsl::active_plugins;
    let p: ActivePlugin =
        diesel::insert_into(active_plugins)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update active_plugin
pub fn put_active_plugin(path: web::Path<String>, json: web::Json<ActivePlugin>, pool: web::Data<Pool>)
                  -> web::Json<ActivePlugin>
{
    use crate::schema::active_plugins::{dsl::*};
    let pi: ActivePlugin = ActivePlugin { id: path.into_inner(), .. json.0};
    let p: ActivePlugin =
        diesel::update(active_plugins.find(pi.id.clone()))
            .set(pi)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
