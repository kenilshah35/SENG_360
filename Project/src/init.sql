CREATE DATABASE IF NOT EXISTS dev;
CREATE USER 'server' IDENTIFIED WITH mysql_native_password BY 'tomato';
USE dev;
CREATE TABLE IF NOT EXISTS credentials (id INTEGER AUTO_INCREMENT, username TEXT, password TEXT, active BOOLEAN, PRIMARY KEY (id));
INSERT INTO credentials (username, password, active) VALUES ('ella','carrot',1);
INSERT INTO credentials (username, password, active) VALUES ('roy','turnip',1);
GRANT SELECT, UPDATE, INSERT, DELETE ON dev.credentials TO 'server';