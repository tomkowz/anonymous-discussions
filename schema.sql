drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null,
  approved int default(null)
);

drop table if exists comments;
create table comments (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null,
  entry_id integer not null,
  foreign key(entry_id) references entries(id)
);

drop table if exists admin;
create table admin (
  id integer primary key autoincrement,
  username text not null unique,
  password text not null
);

insert into admin (username, password) values ('tomkowz', 'oxe8peGVUrR4Eg');
