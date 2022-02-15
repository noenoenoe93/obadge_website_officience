CREATE DATABASE obadge_officience_database;
CREATE TABLE inscription (
    id_inscription INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(60) NOT NULL,
    password_user VARCHAR(100) NOT NULL,
    email_user VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_inscription)
);

CREATE TABLE login (
    id_login INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(60) NOT NULL,
    password_user VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_login)
);