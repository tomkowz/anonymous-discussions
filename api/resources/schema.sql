drop table if exists entries;

create table entries (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null
);

drop table if exists hashtags;
create table hashtags (
  entry_id integer not null,
  value text not null,
  foreign key(entry_id) references entries(id)
);

drop table if exists comments;
create table comments (
  entry_id integer not null,
  content text not null,
  timestamp long not null,
  foreign key(entry_id) references entries(id)
);
