use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{Room};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

pub fn get_all_rooms(pool: web::Data<Pool>) -> web::Json<Vec<Room>> {
    use crate::schema::rooms::dsl::rooms;
    web::Json(rooms.load(&pool.get().unwrap()).unwrap())
}

pub fn get_room(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<Room> {
    use crate::schema::rooms::dsl::rooms;
    web::Json(rooms.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create room
pub fn post_room(json: web::Json<Room>, pool: web::Data<Pool>)
                   -> web::Json<Room>
{
    /// todo: 返り値をResult にする
    use crate::schema::rooms::dsl::rooms;
    let p: Room =
        diesel::insert_into(rooms)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update room
pub fn put_room(path: web::Path<String>, json: web::Json<Room>, pool: web::Data<Pool>)
                  -> web::Json<Room>
{
    use crate::schema::rooms::{dsl::*};
    let pi: Room = Room { id: path.into_inner(), .. json.0};
    let p: Room =
        diesel::update(rooms.find(pi.id.clone()))
            .set(pi)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
