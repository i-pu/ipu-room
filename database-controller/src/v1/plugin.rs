use actix_web::web;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::Plugin;

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;


pub fn get_all_plugins(pool: web::Data<Pool>)
                       -> Result<web::Json<Vec<Plugin>>, failure::Error> {
    use crate::schema::plugins;
    let plugins = plugins::dsl::plugins.load(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&plugins)?);
    Ok(web::Json(plugins))
}

pub fn get_plugin(path: web::Path<String>, pool: web::Data<Pool>)
                  -> Result<web::Json<Plugin>, failure::Error> {
    use crate::schema::plugins::dsl::plugins;
    let plugin = plugins.find(path.into_inner()).first(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&plugin)?);
    Ok(web::Json(plugin))
}

/// create plugin
pub fn post_plugin(json: web::Json<Plugin>, pool: web::Data<Pool>)
                   -> Result<web::Json<Plugin>, failure::Error>
{
    use crate::schema::plugins::dsl::plugins;
    let plugin: Plugin = diesel::insert_into(plugins)
        .values(&json.0)
        .get_result(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&plugin)?);
    Ok(web::Json(plugin))
}

/// update plugin
pub fn put_plugin(json: web::Json<Plugin>, pool: web::Data<Pool>)
                  -> Result<web::Json<Plugin>, failure::Error>
{
    use crate::schema::plugins::dsl::{plugins, id};
    let plugin = diesel::update(plugins.find(json.id.clone()))
        .set(json.0)
        .get_result(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&plugin)?);
    Ok(web::Json(plugin))
}
