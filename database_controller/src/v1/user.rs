use actix_web::{HttpRequest, web};
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
};

use crate::model::{User};

type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

pub fn get_all_users(pool: web::Data<Pool>) -> web::Json<Vec<User>> {
    use crate::schema::users::dsl::users;
    web::Json(users.load(&pool.get().unwrap()).unwrap())
}

pub fn get_user(path: web::Path<String>, pool: web::Data<Pool>) -> web::Json<User> {
    use crate::schema::users::dsl::users;
    web::Json(users.find(path.into_inner()).first(&pool.get().unwrap()).unwrap())
}

/// create user
pub fn post_user(json: web::Json<User>, pool: web::Data<Pool>)
                   -> web::Json<User>
{
    /// todo: 返り値をResult にする
    use crate::schema::users::dsl::users;
    let p: User =
        diesel::insert_into(users)
            .values(&json.0)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}

/// update user
pub fn put_user(path: web::Path<String>, json: web::Json<User>, pool: web::Data<Pool>)
                  -> web::Json<User>
{
    use crate::schema::users::{dsl::*};
    let pi: User = User { id: path.into_inner(), .. json.0};
    let p: User =
        diesel::update(users.find(pi.id.clone()))
            .set(pi)
            .get_result(&pool.get().unwrap())
            .unwrap();

    println!("{:#?}", p);
    web::Json(p)
}
