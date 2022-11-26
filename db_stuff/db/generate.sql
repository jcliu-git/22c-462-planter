-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;

drop table if exists water_level;
drop table if exists moisture_level;
drop table if exists temperature;
drop table if exists light;
drop table if exists photos;


CREATE TABLE IF NOT EXISTS water_level
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 ),
    "timestamp" timestamp without time zone NOT NULL,
    distance double precision NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS moisture_level
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 ),
    sensor1 double precision NOT NULL,
    sensor2 double precision NOT NULL,
    sensor3 double precision NOT NULL,
    sensor4 double precision NOT NULL,
    sensor5 double precision NOT NULL,
    sensor6 double precision NOT NULL,
    sensor7 double precision NOT NULL,
    sensor8 double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS temperature
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    fahrenheit double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS photos
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    "timestamp" timestamp without time zone NOT NULL,
    filepath text NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    phototype text NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS light
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    luminosity double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    PRIMARY KEY (id)
);
END;