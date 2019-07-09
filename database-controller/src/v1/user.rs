use actix_web::web;
use serde::{Serialize, Deserialize};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
    ExpressionMethods, // filter eq 用
    // OptionalExtension, // get_result に対してoptionalを呼ぶため
};

use crate::model::{User, State};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct UserQuery {
    room_id: Option<String>,
}

pub fn get_users(query: web::Query<UserQuery>, pool: web::Data<Pool>)
                 -> Result<web::Json<Vec<User>>, failure::Error> {
    use crate::schema::users;
    let user_query = query.into_inner();
    info!("{{user_query: {}}}", serde_json::to_string(&user_query)?);
    let users =
        if let Some(ref room_id) = user_query.room_id {
            users::dsl::users
                .filter(users::room_id.eq(room_id))
                .load(&pool.get()?)?
        } else {
            users::dsl::users.load(&pool.get()?)?
        };

    info!("{{users: {}}}", serde_json::to_string(&users)?);
    Ok(web::Json(users))
}

pub fn get_user(path: web::Path<String>, pool: web::Data<Pool>)
                -> Result<web::Json<User>, failure::Error> {
    use crate::schema::users::dsl::users;
    let id = path.into_inner();
    let user = users.find(&id).first(&pool.get()?)?;

    info!("{{user: {}}}", serde_json::to_string(&user)?);
    Ok(web::Json(user))
}

pub fn post_user(json: web::Json<User>, pool: web::Data<Pool>)
                 -> Result<web::Json<User>, failure::Error> {
    use crate::schema::users;
    let user: User =
        diesel::insert_into(users::dsl::users)
            .values(&json.0)
            .get_result(&pool.get()?)?;

    info!("{{user: {}}}", serde_json::to_string(&user)?);
    Ok(web::Json(user))
}

pub fn put_user(json: web::Json<User>, pool: web::Data<Pool>)
                -> Result<web::Json<User>, failure::Error> {
    use crate::schema::users;
    let new_user = diesel::update(users::dsl::users.find(&json.id))
        .set(&json.0)
        .get_result(&pool.get()?)?;

    info!("{{user: {}}}", serde_json::to_string(&new_user)?);
    Ok(web::Json(new_user))
}

pub fn delete_user(path: web::Path<String>, pool: web::Data<Pool>)
                   -> Result<web::Json<State>, failure::Error> {
    use crate::schema::users;
    let id = path.into_inner();
    diesel::delete(users::dsl::users.filter(users::dsl::id.eq(&id)))
        .execute(&pool.get()?)?;

    Ok(web::Json(State { state: "true".to_owned() }))
}
