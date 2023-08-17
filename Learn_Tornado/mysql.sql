create user
    'learn_tornado1' @'localhost' identified by 'learn_tornado1';

grant all privileges on *.* to 'learn_tornado1'@'localhost';

create user
    'learn_tornado2' @'localhost' identified by 'learn_tornado2';

grant all privileges on *.* to 'learn_tornado2'@'localhost';

flush privileges;

create database learn_tornado1;

create database learn_tornado2;

create table
    `learn_tornado1`.`user` (
        `id` bigint not null auto_increment primary key,
        `first_name` varchar(255) not null,
        `middle_name` varchar(255) null,
        `last_name` varchar(255) not null,
        `gender` int not null,
        `salt_value` varchar(255) not null,
        `password` varchar(500) not null
    );

create table
    `learn_tornado1`.`user_email` (
        `id` bigint not null auto_increment primary key,
        `user_id` bigint not null,
        `email` varchar(255) not null,
        `is_primary` boolean not null default false,
        foreign key (user_id) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`user_number` (
        `id` bigint not null auto_increment primary key,
        `user_id` bigint not null,
        `country_code` varchar(5) null,
        `number` varchar(255) not null,
        `is_primary` boolean not null default false,
        foreign key (user_id) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`user_photo` (
        `id` bigint not null auto_increment primary key,
        `user_id` bigint not null,
        `photo_url` varchar(1000) not null,
        `is_primary` boolean not null default false,
        foreign key (user_id) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`client` (
        `id` bigint not null auto_increment primary key,
        `name` varchar(255) not null,
        `display_name` varchar(500) null,
        `registered_id` varchar(20) not null
    );

create table
    `learn_tornado1`.`client_email` (
        `id` bigint not null auto_increment primary key,
        `client_id` bigint not null,
        `email` varchar(255) not null,
        `is_primary` boolean not null default false,
        foreign key (client_id) references `learn_tornado1`.`client` (id)
    );

create table
    `learn_tornado1`.`client_number` (
        `id` bigint not null auto_increment primary key,
        `client_id` bigint not null,
        `country_code` varchar(5) null,
        `number` varchar(255) not null,
        `is_primary` boolean not null default false,
        foreign key (client_id) references `learn_tornado1`.`client` (id)
    );

create table
    `learn_tornado1`.`chat` (
        `id` bigint not null auto_increment primary key,
        `is_group_chat` boolean not null default false,
        `name` varchar(255),
        `created_at` timestamp not null default current_timestamp,
        `created_by` bigint not null,
        foreign key (created_by) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`chat_member` (
        `id` bigint not null auto_increment primary key,
        `chat_id` bigint not null,
        `user1_id` bigint not null,
        `user2_id` bigint not null,
        `user1_joined_at` timestamp,
        `user2_joined_at` timestamp,
        foreign key (chat_id) references `learn_tornado1`.`chat` (id),
        foreign key (user1_id) references `learn_tornado1`.`user` (id),
        foreign key (user2_id) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`group_chat_member` (
        `id` bigint not null auto_increment primary key,
        `chat_id` bigint not null,
        `user_id` bigint not null,
        `is_admin` boolean not null default false,
        `joined_at` timestamp not null default now(),
        `added_by` bigint not null,
        foreign key (chat_id) references `learn_tornado1`.`chat` (id),
        foreign key (user_id) references `learn_tornado1`.`user` (id),
        foreign key (added_by) references `learn_tornado1`.`user` (id)
    );

create table
    `learn_tornado1`.`message` (
        `id` bigint not null auto_increment primary key,
        `chat_id` bigint not null,
        `sender_id` bigint not null,
        `message` text,
        `sent_at` timestamp default current_timestamp,
        `delivered_at` timestamp default current_timestamp,
        foreign key (chat_id) references `learn_tornado1`.`chat` (id),
        foreign key (sender_id) references `learn_tornado1`.`user` (id)
    );