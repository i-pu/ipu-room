use actix_web::{
    web,
    Result,
};
use serde::Deserialize;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
    ExpressionMethods, // filter eq 用
    // OptionalExtension, // get_result に対してoptionalを呼ぶため
};

use crate::model::{User, State};
use std::panic::resume_unwind;

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct UserQuery {
    room_id: Option<String>,
}

pub fn get_users(query: web::Query<UserQuery>, pool: web::Data<Pool>) -> web::Json<Vec<User>> {
    use crate::schema::users;
    println!("{:#?}", query);
    let mut users;
    if let Some(ref room_id) = query.room_id {
        users = users::dsl::users
            .filter(users::room_id.eq(room_id))
            .load(&pool.get().unwrap())
            .unwrap();
    } else {
        users = users::dsl::users.load(&pool.get().unwrap()).unwrap();
    }
    println!("{:#?}", users);
    web::Json(users)
}

pub fn get_user(path: web::Path<String>, pool: web::Data<Pool>)
                -> Result<web::Json<User>>{
    use crate::schema::users::dsl::users;
    let id = path.into_inner();
    let result_u = users.find(&id).first(&pool.get().unwrap());
    match result_u {
        Ok(user) => {
            println!("{:#?}", user);
            Ok(web::Json(user))
        },
        Err(diesel::NotFound) => {
            Err(actix_web::error::ErrorNotFound("user not found"))
        },
        Err(_) => {
            Err(actix_web::error::ErrorInternalServerError("internal server error"))
        }
    }
}

pub fn post_user(json: web::Json<User>, pool: web::Data<Pool>) -> web::Json<User> {
    /// todo: 返り値をResult にする
    use crate::schema::users;
    let user: User =
        diesel::insert_into(users::dsl::users)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", user);
    web::Json(user)
}

pub fn put_user(json: web::Json<User>, pool: web::Data<Pool>) -> web::Json<User> {
    use crate::schema::users;
    let mut new_user: User = json.0;
    new_user =
        diesel::update(users::dsl::users.find(&new_user.id))
            .set(&new_user)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("user: {:#?}", new_user);
    web::Json(new_user)
}

pub fn delete_user(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<State> {
    use crate::schema::users;
    let id = path.into_inner();
    diesel::delete(users::dsl::users.filter(users::dsl::id.eq(&id)))
        .execute(&pool.get().unwrap())
        .unwrap();
    web::Json(State { state: "true".to_owned() })
}
