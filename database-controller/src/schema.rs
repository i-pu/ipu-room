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
    users (id) {
        id -> Varchar,
        name -> Varchar,
        room_id -> Nullable<Varchar>,
    }
}

table! {
    rooms (id) {
        id -> Varchar,
        name -> Varchar,
    }
}

table! {
    active_plugins (id) {
        id -> Varchar,
        plugin_id -> Varchar,
        room_id -> Varchar,
        enabled -> Bool,
    }
}