-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS "C21-703-3".stations
(
    name character varying(255) NOT NULL,
    "number tariff zone" integer NOT NULL,
    station_id integer,
    PRIMARY KEY (station_id)
);

CREATE TABLE IF NOT EXISTS "C21-703-3".routes
(
    train_id integer,
    station integer NOT NULL,
    "time stop" time without time zone,
    "number of station" integer DEFAULT 0,
    PRIMARY KEY (train_id, "number of station")
);

CREATE TABLE IF NOT EXISTS "C21-703-3".tickets
(
    price numeric(7, 2) NOT NULL,
    id integer,
    "count zone" integer NOT NULL,
    station_from integer NOT NULL,
    station_to integer NOT NULL,
    PRIMARY KEY (id),
	CONSTRAINT price_positive CHECK(price > 0)
);

CREATE TABLE IF NOT EXISTS "C21-703-3".trains
(
    id integer,
    "start station" integer NOT NULL,
    "final station" integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS "C21-703-3"."day-train"
(
    day integer,
    train_id integer,
    PRIMARY KEY (train_id, day)
);

ALTER TABLE IF EXISTS "C21-703-3".routes
    ADD FOREIGN KEY (train_id)
    REFERENCES "C21-703-3".trains (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3".routes
    ADD FOREIGN KEY (station)
    REFERENCES "C21-703-3".stations (station_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3".tickets
    ADD FOREIGN KEY (station_from)
    REFERENCES "C21-703-3".stations (station_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3".tickets
    ADD FOREIGN KEY (station_to)
    REFERENCES "C21-703-3".stations (station_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3".trains
    ADD FOREIGN KEY ("start station")
    REFERENCES "C21-703-3".stations (station_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3".trains
    ADD FOREIGN KEY ("final station")
    REFERENCES "C21-703-3".stations (station_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS "C21-703-3"."day-train"
    ADD FOREIGN KEY (train_id)
    REFERENCES "C21-703-3".trains (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;