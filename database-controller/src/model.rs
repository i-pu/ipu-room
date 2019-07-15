use serde::{Serialize, Deserialize};
use uuid::Uuid;

use crate::schema::plugins;
use crate::schema::users;
use crate::schema::rooms;
use crate::schema::active_plugins;

fn uuid_str() -> String {
    Uuid::new_v4().to_string()
}


#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "plugins"]
#[serde(rename_all = "camelCase")]
pub struct Plugin {
    #[serde(skip_deserializing, default="uuid_str")]
    pub id: String,
    pub name: String,
    pub description: String,
    pub author: String,
    pub tags: String,
    pub content: String,
}

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "users"]
#[serde(rename_all = "camelCase")]
#[changeset_options(treat_none_as_null="true")]
pub struct User {
    // todo: skip
    pub id: String,
    pub name: String,
    pub room_id: Option<String>,
}

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "rooms"]
#[serde(rename_all = "camelCase")]
pub struct Room {
    // todo: skip
    pub id: String,
    pub name: String,
}

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "active_plugins"]
#[serde(rename_all = "camelCase")]
pub struct ActivePlugin {
    // todo: skip
    pub id: String,
    pub plugin_id: String,
    pub room_id: String,
    pub enabled: bool,
}

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
)]
pub struct State {
    pub state: String,
}
