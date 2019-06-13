create table plugin_metas (
    id varchar(40) primary key,
    name varchar(20) not null,
    description varchar(140) not null,
    author varchar(40) not null,
    tags varchar(100) not null,
    content text not null
);

create table users (
    id varchar(40) primary key,
    name varchar(20) not null,
    room_id varchar(40)
);

create table rooms (
    id varchar(40) primary key,
    name varchar(20) not null
);

create table active_plugins (
    id varchar(40) primary key,
    plugin_name varchar(20) not null,
    room_id varchar(40) not null
);
