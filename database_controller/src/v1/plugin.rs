use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{PluginMeta};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_plugins(pool: web::Data<Pool>) -> web::Json<Vec<PluginMeta>> {
    use crate::schema::plugin_metas::dsl::plugin_metas;
    web::Json(plugin_metas.load(&pool.get().unwrap()).unwrap())
}

pub fn get_plugin(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<PluginMeta> {
    use crate::schema::plugin_metas::dsl::plugin_metas;
    web::Json(plugin_metas.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create plugin
pub fn post_plugin(json: web::Json<PluginMeta>, pool: web::Data<Pool>)
                   -> web::Json<PluginMeta>
{
    /// todo: 返り値をResult にする
    use crate::schema::plugin_metas::dsl::plugin_metas;
    let p: PluginMeta =
        diesel::insert_into(plugin_metas)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update plugin
pub fn put_plugin(path: web::Path<String>, json: web::Json<PluginMeta>, pool: web::Data<Pool>)
                  -> web::Json<PluginMeta>
{
    use crate::schema::plugin_metas::{dsl::*};
    let pi: PluginMeta = PluginMeta { id: path.into_inner(), .. json.0};
    let p: PluginMeta =
        diesel::update(plugin_metas.find(pi.id.clone()))
            .set(pi)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
