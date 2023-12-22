-- mysql -u root -p < E:\ThnBih_HK3\MatMaHoc\project\code\Create_schema.sql
CREATE DATABASE IF NOT EXISTS DATA_FALCON;
USE DATA_FALCON;
DROP TABLE IF EXISTS Qualifications;
DROP TABLE IF EXISTS Institution;
DROP TABLE IF EXISTS StudentInfor;

CREATE TABLE Institution (
    institution_id INT AUTO_INCREMENT PRIMARY KEY,
    institution_name VARCHAR(255),
    authority_person VARCHAR(255),
    email_address VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    certificate_file LONGBLOB
);

CREATE TABLE StudentInfor (
    id_sv INT AUTO_INCREMENT PRIMARY KEY,
    school VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE Qualifications (
    degree_code INT AUTO_INCREMENT PRIMARY KEY ,
    id_sv INT,
    issue_date DATE,
    expiration_date DATE,
    institution_id INT,
    pdf_file LONGBLOB,

    FOREIGN KEY (id_sv) REFERENCES StudentInfor (id_sv),
    FOREIGN KEY (institution_id) REFERENCES Institution (institution_id)
);
