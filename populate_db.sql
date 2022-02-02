-- DROP TABLE IF EXISTS anime_stock;
CREATE TABLE IF NOT EXISTS anime_stock;

CREATE TABLE IF NOT EXISTS animes (
                id              BIGSERIAL    CONSTRAINT pk_series   PRIMARY KEY,
                anime           VARCHAR(100)    NOT NULL        UNIQUE,
                released_date   DATE            NOT NULL,
                seasons         INTEGER         NOT NULL,
            );