drop table if exists entries;

create table entries (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null
);

drop table if exists comments;
create table comments (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null,
  entry_id integer not null,
  foreign key(entry_id) references entries(id)
);
