create database accountHolder;
use accountHolder;
create table accounts(
	id int auto_increment primary key,
    phone varchar(20),
    name varchar(50),
    password varchar(6),
    balance int default 0
);
use accountHolder;
describe accounts;
