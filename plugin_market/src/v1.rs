use std::collections::HashMap;
use std::hash::Hash;


use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    query_dsl::RunQueryDsl,
    QueryResult,
};
use uuid::Uuid;

use crate::model::{PluginInfo, uuid4_str};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_plugins(req: HttpRequest) -> web::Json<Vec<PluginInfo>> {
    web::Json(vec![])
}

pub fn get_plugin(req: HttpRequest, path: web::Path<String>) -> web::Json<PluginInfo> {
    unimplemented!()
}

/// create plugin
pub fn post_plugin(req: HttpRequest, json: web::Json<PluginInfo>, pool: web::Data<Pool>)
                   -> web::Json<PluginInfo>
{
    /// 返り値をResult にする
    /// todo: pluginのid を同じやつにして，エラーを返してみる
    use crate::schema::plugin_infos::dsl::plugin_infos;
    let p: PluginInfo =
        diesel::insert_into(plugin_infos)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:?}", p);
    web::Json(p)
}

/// update plugin
pub fn put_plugin(req: HttpRequest, plugin_info: web::Json<PluginInfo>, pool: web::Data<Pool>)
                  -> web::Json<PluginInfo>
{
    println!("{:?}", plugin_info);
    let mut hash_map = HashMap::new();
    hash_map.insert("state".to_owned(), true);
    unimplemented!()
}

fn create_plugin(json: web::Json<PluginInfo>, pool: web::Data<Pool>)
                 -> Result<PluginInfo, diesel::result::Error>
{
    let pi: PluginInfo = PluginInfo {
        id: uuid4_str(),
        name: (&json.name).to_owned(),
    };
    let conn: &PgConnection = &pool.get().expect("Can't find pool");
    unimplemented!()
}

pub fn hello(req: HttpRequest) -> &'static str {
    "hello"
}
