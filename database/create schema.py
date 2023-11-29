-- mysql -u root -p < E:\ThnBih_HK3\MatMaHoc\project\code\Create_schema.sql

CREATE DATABASE IF NOT EXISTS DATA_FALCON;
USE DATA_FALCON;

CREATE TABLE StudentInfor (
    id_sv INT PRIMARY KEY,
    school VARCHAR(255),
    degree_code VARCHAR(255)
);

CREATE TABLE Qualifications (
    degree_code VARCHAR(255),
    id_sv INT,
    issue_date DATE,
    expiration_date DATE,
    issuing_authority VARCHAR(255),
    pdf_file LONGBLOB,
    PRIMARY KEY (degree_code, id_sv),
    FOREIGN KEY (id_sv) REFERENCES StudentInfor (id_sv)
);

CREATE TABLE Institution (
    institution_id INT PRIMARY KEY,
    id_sv INT,
    institution_name VARCHAR(255),
    authority_person VARCHAR(255),
    certificate_file LONGBLOB,
    public_key LONGBLOB,
    FOREIGN KEY (id_sv) REFERENCES Qualifications (id_sv)
);
