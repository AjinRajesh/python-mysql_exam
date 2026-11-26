create database library_management;
use library_management;

create table books(book_id int auto_increment primary key, title varchar(100) not null,author varchar(50) not null,category varchar(30),total_copies int,available_copies int);