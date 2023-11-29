-- mysql -u root -p < E:\ThnBih_HK3\MatMaHoc\project\code\Create_schema.sql

CREATE DATABASE IF NOT EXISTS DATA_FALCON;
USE DATA_FALCON;

CREATE TABLE qrcode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    data LONGBLOB
);  

CREATE TABLE certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    file LONGBLOB,
    qrcode_id INT,
    FOREIGN KEY (qrcode_id) REFERENCES qrcode(id)
);

CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    file LONGBLOB,
    qrcode_id INT,
    FOREIGN KEY (qrcode_id) REFERENCES qrcode(id)
);

CREATE TABLE user_credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    qrcode_id INT,
    FOREIGN KEY (qrcode_id) REFERENCES qrcode(id)
);
