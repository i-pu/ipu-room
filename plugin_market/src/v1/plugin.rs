use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{PluginInfo};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_plugins(pool: web::Data<Pool>) -> web::Json<Vec<PluginInfo>> {
    use crate::schema::plugin_infos::dsl::plugin_infos;
    web::Json(plugin_infos.load(&pool.get().unwrap()).unwrap())
}

pub fn get_plugin(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<PluginInfo> {
    use crate::schema::plugin_infos::dsl::plugin_infos;
    web::Json(plugin_infos.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create plugin
pub fn post_plugin(json: web::Json<PluginInfo>, pool: web::Data<Pool>)
                   -> web::Json<PluginInfo>
{
    /// todo: 返り値をResult にする
    use crate::schema::plugin_infos::dsl::plugin_infos;
    let p: PluginInfo =
        diesel::insert_into(plugin_infos)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update plugin
pub fn put_plugin(path: web::Path<String>, json: web::Json<PluginInfo>, pool: web::Data<Pool>)
                  -> web::Json<PluginInfo>
{
    use crate::schema::plugin_infos::{dsl::*};
    let pi: PluginInfo = PluginInfo { id: path.into_inner(), .. json.0};
    let p: PluginInfo =
        diesel::update(plugin_infos.find(pi.id.clone()))
            .set(pi)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
