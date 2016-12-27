drop table if exists quotes;
create table quotes (
  id integer primary key autoincrement,
  source text not null,
  'text' text not null
);