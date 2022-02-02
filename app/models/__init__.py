import psycopg2


class DatabaseConector:
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(host="localhost", database="anime_stock", user="vina", password="1234")
        cls.cur = cls.conn.cursor()
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes (
                id              BIGSERIAL    CONSTRAINT pk_series   PRIMARY KEY,
                anime           VARCHAR(100)    NOT NULL        UNIQUE,
                released_date   DATE            NOT NULL,
                seasons         INTEGER         NOT NULL
            );"""
        )

    @classmethod
    def commit_and_close(cls):
        cls.conn.commit()
        cls.cur.close()
        cls.conn.close()