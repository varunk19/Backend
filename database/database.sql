CREATE TABLE user (
	id INTEGER NOT NULL, 
	userid VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (userid)
);
CREATE TABLE flight (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	plan VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);