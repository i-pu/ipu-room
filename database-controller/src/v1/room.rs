use actix_web::web;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::Room;

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

pub fn get_all_rooms(pool: web::Data<Pool>)
                     -> Result<web::Json<Vec<Room>>, failure::Error> {
    use crate::schema::rooms;
    let rooms = rooms::dsl::rooms.load(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&rooms)?);
    Ok(web::Json(rooms))
}

pub fn get_room(path: web::Path<String>, pool: web::Data<Pool>)
                -> Result<web::Json<Room>, failure::Error> {
    use crate::schema::rooms;
    let id = path.into_inner();
    let room = rooms::dsl::rooms.find(&id).first(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&room)?);
    Ok(web::Json(room))
}

/// create room
pub fn post_room(json: web::Json<Room>, pool: web::Data<Pool>)
                 -> Result<web::Json<Room>, failure::Error>
{
    use crate::schema::rooms::dsl::rooms;
    let room: Room = diesel::insert_into(rooms)
        .values(&json.0)
        .get_result(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&room)?);
    Ok(web::Json(room))
}

/// update room
pub fn put_room(json: web::Json<Room>, pool: web::Data<Pool>)
                -> Result<web::Json<Room>, failure::Error>
{
    use crate::schema::rooms::dsl::{rooms, id};
    let new_room = diesel::update(rooms.find(json.id.clone()))
        .set(json.0)
        .get_result(&pool.get()?)?;

    debug!("{}", serde_json::to_string(&new_room)?);
    Ok(web::Json(new_room))
}
