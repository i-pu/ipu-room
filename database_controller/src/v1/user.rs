use actix_web::{web};
use serde::Deserialize;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
    ExpressionMethods, // filter eq 用
};

use crate::model::User;

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

pub fn get_user(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<User> {
    use crate::schema::users::dsl::users;
    let id = path.into_inner();
    let user = users.find(&id).first(&pool.get().unwrap())
                    .expect(&format!("not found user: {:?}", id));
    println!("{:#?}", user);
    web::Json(user)
}

/// create user
pub fn post_user(json: web::Json<User>, pool: web::Data<Pool>)
                 -> web::Json<User>
{
    /// todo: 返り値をResult にする
    use crate::schema::users::dsl::users;
    let user: User =
        diesel::insert_into(users)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", user);
    web::Json(user)
}

/// update user
pub fn put_user(json: web::Json<User>, pool: web::Data<Pool>)
                -> web::Json<User>
{
    use crate::schema::users::{dsl::*};
    let mut new_user: User = json.0;
    new_user =
        diesel::update(users.find(new_user.id.clone()))
            .set(new_user)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", new_user);
    web::Json(new_user)
}
