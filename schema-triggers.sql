create trigger entries_insert
before insert on entries
for each row
set NEW.created_at = CURRENT_TIMESTAMP, NEW.updated_at = CURRENT_TIMESTAMP;

create trigger entries_update
before update on entries
for each row
set NEW.updated_at = CURRENT_TIMESTAMP;

create trigger comments_insert
before insert on comments
for each row
set NEW.created_at = CURRENT_TIMESTAMP, NEW.updated_at = CURRENT_TIMESTAMP;

create trigger comments_update
before update on comments
for each row
set NEW.updated_at = CURRENT_TIMESTAMP;

DELIMITER //
CREATE TRIGGER tokens_insert
AFTER INSERT
  ON tokens FOR EACH ROWS
BEGIN
  INSERT INTO user_settings (token) VALUES (NEW.value);
END; //
DELIMITER ;
