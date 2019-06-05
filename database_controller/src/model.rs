use serde::{Serialize, Deserialize};
use uuid::Uuid;

use crate::schema::plugin_infos;

#[derive(Debug, Clone, Eq, PartialEq, Hash,
Serialize, Deserialize,
Insertable, Queryable, AsChangeset)]
#[table_name = "plugin_infos"]
pub struct PluginInfo {
    #[serde(default = "uuid4_str", skip_deserializing)]
    pub id: String,
    pub name: String,
    pub description: String,
    pub thumbnail_url: String,
    pub author: String,
    pub tags: String,
    pub content: String,
}

pub fn uuid4_str() -> String {
    Uuid::new_v4().to_string()
}

