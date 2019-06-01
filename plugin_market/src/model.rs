use diesel::r2d2::{self, ConnectionManager};
use diesel::prelude::*;
use serde::*;
use uuid::Uuid;

use crate::schema::plugin_infos;

#[derive(Debug, Clone, Eq, PartialEq, Hash, Insertable, Serialize, Deserialize, Queryable)]
#[table_name = "plugin_infos"]
pub struct PluginInfo {
    #[serde(default = "uuid4_str", skip_deserializing)]
    pub id: String,
    pub name: String,
}

pub fn uuid4_str() -> String {
    Uuid::new_v4().to_string()
}

