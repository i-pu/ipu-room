use actix_web::{web};
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
    let id = path.into_inner();
    let room = rooms.find(&id).first(&pool.get().unwrap())
        .expect(&format!("not found room: {:?}", id));
    println!("{:#?}", room);
    web::Json(room)
}

/// create room
pub fn post_room(json: web::Json<Room>, pool: web::Data<Pool>)
                   -> web::Json<Room>
{
    /// todo: 返り値をResult にする
    use crate::schema::rooms::dsl::rooms;
    let room: Room =
        diesel::insert_into(rooms)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", room);
    web::Json(room)
}

/// update room
pub fn put_room(json: web::Json<Room>, pool: web::Data<Pool>)
                  -> web::Json<Room>
{
    use crate::schema::rooms::{dsl::*};
    let mut new_room: Room = json.0;
    new_room =
        diesel::update(rooms.find(new_room.id.clone()))
            .set(new_room)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", new_room);
    web::Json(new_room)
}
