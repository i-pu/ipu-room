use actix_web::{web};
use serde::Deserialize;
use diesel::{
    r2d2::{self, ConnectionManager},
    pg::PgConnection,
    QueryDsl,
    RunQueryDsl,
    ExpressionMethods, // filter eq 用
};

use crate::model::{User, State};


type Pool = r2d2::Pool<ConnectionManager<PgConnection>>;

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct UserQuery {
    #[serde(default)]
    room_id: Option<String>,
}

pub fn visit(query: web::Query<UserQuery>, pool: web::Data<Pool>) -> web::Json<Vec<User>> {
    unimplemented!()
}
