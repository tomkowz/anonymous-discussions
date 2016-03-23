DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS admin;

CREATE TABLE entries (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  approved INTEGER DEFAULT NULL
);

CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  entry_id INTEGER NOT NULL,
  FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE entry_votes (
  entry_id INTEGER REFERENCES entries(id),
  value INTEGER NOT NULL
);

CREATE TABLE comment_votes (
  comment_id INTEGER REFERENCES comments(id),
  value INTEGER NOT NULL
);

CREATE TABLE admin (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(50) NOT NULL
);

INSERT INTO admin(username, password) VALUES('tomkowz', 'oxe8peGVUrR4Eg');
