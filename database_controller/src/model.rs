use serde::{Serialize, Deserialize};

use crate::schema::plugins;
use crate::schema::users;
use crate::schema::rooms;
use crate::schema::active_plugins;

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "plugins"]
#[serde(rename_all = "camelCase")]
pub struct Plugin {
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
pub struct User {
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
