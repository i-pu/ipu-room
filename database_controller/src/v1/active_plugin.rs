use actix_web::{web};
use serde::Deserialize;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
    ExpressionMethods, // filter eq 用
};

use crate::model::ActivePlugin;

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Debug, Deserialize)]
pub struct ActivePluginQuery {
    room_id: Option<String>,
}

pub fn get_active_plugins(query: web::Query<ActivePluginQuery>, pool: web::Data<Pool>)
                          -> web::Json<Vec<ActivePlugin>>
{
    use crate::schema::active_plugins;
    println!("{:#?}", query);
    let mut active_plugins;
    if let Some(ref room_id) = query.room_id {
        active_plugins = active_plugins::dsl::active_plugins
            .filter(active_plugins::room_id.eq(room_id))
            .load(&pool.get().unwrap())
            .unwrap();
    } else {
        active_plugins = active_plugins::dsl::active_plugins
            .load(&pool.get().unwrap())
            .unwrap();
    }
    println!("{:#?}", active_plugins);
    web::Json(active_plugins)
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
pub fn put_active_plugin(json: web::Json<ActivePlugin>, pool: web::Data<Pool>)
                         -> web::Json<ActivePlugin>
{
    use crate::schema::active_plugins::{dsl::*};
    let mut ap: ActivePlugin = json.0;
    ap = diesel::update(active_plugins.find(ap.id.clone()))
        .set(ap)
        .get_result(&pool.get().unwrap())
        .unwrap();

    println!("{:#?}", ap);
    web::Json(ap)
}
