use serde::{Serialize, Deserialize};
use uuid::Uuid;

use crate::schema::plugin_metas;
use crate::schema::users;
use crate::schema::rooms;
use crate::schema::active_plugins;

pub fn uuid4_str() -> String {
    Uuid::new_v4().to_string()
}

#[derive(
    Debug, Clone, Eq, PartialEq, Hash,
    Serialize, Deserialize,
    Insertable, Queryable, AsChangeset
)]
#[table_name = "plugin_metas"]
pub struct PluginMeta {
    #[serde(default = "uuid4_str", skip_deserializing)]
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
pub struct User {
    #[serde(default = "uuid4_str", skip_deserializing)]
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
pub struct Room {
    #[serde(default = "uuid4_str", skip_deserializing)]
    pub id: String,
    pub name: String,
}

#[derive(
Debug, Clone, Eq, PartialEq, Hash,
Serialize, Deserialize,
Insertable, Queryable, AsChangeset
)]
#[table_name = "active_plugins"]
pub struct ActivePlugin {
    #[serde(default = "uuid4_str", skip_deserializing)]
    pub id: String,
    pub plugin_name: String,
    pub room_id: String,
}
