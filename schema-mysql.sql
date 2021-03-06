DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS admin;

CREATE TABLE entries (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  votes_up INTEGER DEFAULT 0,
  votes_down INTEGER DEFAULT 0,
  approved INTEGER DEFAULT NULL,
  op_token VARCHAR(80) DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted INT DEFAULT 0,
  deleted_reason VARCHAR(100) DEFAULT NULL
);

CREATE TABLE comments (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  content TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  votes_up INTEGER DEFAULT 0,
  votes_down INTEGER DEFAULT 0,
  entry_id INTEGER NOT NULL,
  op_token VARCHAR(80) DEFAULT NULL,
  updated_at TIMESTAMP DEFAULT NULL,
  deleted INT DEFAULT 0,
  deleted_reason VARCHAR(100) DEFAULT NULL,
  FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE hashtags (
  name VARCHAR(100) NOT NULL UNIQUE,
  count INTEGER DEFAULT 1
);

CREATE TABLE recommended_hashtags (
  hashtag_name VARCHAR(100) NOT NULL UNIQUE,
  position INTEGER DEFAULT 0
);

CREATE TABLE tokens (
  value VARCHAR(80) DEFAULT NULL UNIQUE
);

CREATE TABLE tokens_votes_cache (
  user_token VARCHAR(80) NOT NULL,
  object_id INTEGER NOT NULL,
  object_type VARCHAR(15) NOT NULL,
  value VARCHAR(4) NOT NULL
);

CREATE TABLE user_notifications (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_token VARCHAR(80) NOT NULL,
  content VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  object_id INTEGER NOT NULL,
  object_type VARCHAR(15) NOT NULL,
  active INTEGER DEFAULT 1
);

CREATE TABLE followed_entries (
  user_token VARCHAR(80) NOT NULL,
  entry_id INTEGER NOT NULL,
  FOREIGN KEY(entry_id) REFERENCES entries(id)
);

CREATE TABLE user_settings (
  token VARCHAR(80) NOT NULL,
  mark_my_posts INTEGER DEFAULT 1,
  FOREIGN KEY(token) REFERENCES tokens(value)
);
