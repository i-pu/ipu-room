-- Your SQL goes here

create table plugin_infos (
    id varchar(40) primary key,
    name varchar(20) not null,
    description varchar(140) not null,
    thumbnail_url varchar(4096) not null,
    author varchar(40) not null,
    tags varchar(100) not null,
    content text not null
);
