USE [master];
GO
CREATE DATABASE myapp;
GO
USE [myapp];
GO
CREATE TABLE location (street varchar(20), city varchar(20), state varchar(20));
GO
INSERT INTO location (street, city, state)
VALUES ('main', 'anytown', 'california');
