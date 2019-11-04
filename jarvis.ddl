create table User
(
	id int auto_increment primary key,
	name varchar(200) not null,
	password varchar(200) not null,
	salt varchar(200) not null,
	role varchar(200) not null
);

create unique index user_id_uindex
	on User (id);

create table Command
(
	id int auto_increment primary key ,
	description varchar(200) null,
	operation varchar(200) null,
	code int null
);

create unique index command_id_uindex
	on Command (id);


