drop table if exists entries;

create table entries (
  id integer primary key autoincrement,
  content text not null,
  timestamp long not null
);
