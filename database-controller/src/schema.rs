table! {
    active_plugins (id) {
        id -> Varchar,
        plugin_id -> Varchar,
        room_id -> Varchar,
        enabled -> Bool,
    }
}

table! {
    plugins (id) {
        id -> Varchar,
        name -> Varchar,
        description -> Varchar,
        author -> Varchar,
        tags -> Varchar,
        content -> Text,
    }
}

table! {
    rooms (id) {
        id -> Varchar,
        name -> Varchar,
    }
}

table! {
    users (id) {
        id -> Varchar,
        name -> Varchar,
        room_id -> Nullable<Varchar>,
    }
}

allow_tables_to_appear_in_same_query!(
    active_plugins,
    plugins,
    rooms,
    users,
);
