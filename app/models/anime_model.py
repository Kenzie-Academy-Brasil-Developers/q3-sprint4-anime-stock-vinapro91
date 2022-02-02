from app.models import DatabaseConector
from psycopg2 import sql


class Animes(DatabaseConector):
    anime_key = ["id", "anime", "released_date", "seasons"]


    def __init__(self,  anime:str, released_date, seasons) -> None:
        self.anime = anime.title(),
        self.released_date = released_date,
        self.seasons = seasons

    
    def create_anime(self):
        self.get_conn_cur()
        
        
        query = sql.SQL(""" INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                ({anime},{released_date},{seasons})
            RETURNING *""").format(anime=sql.Literal(self.__dict__["anime"]), released_date=sql.Literal(self.__dict__["released_date"]), seasons=sql.Literal(self.__dict__["seasons"]))
        

        self.cur.execute(query)


        inserted_anime = self.cur.fetchone()

        self.commit_and_close()
        return inserted_anime
    @staticmethod
    def serialize_animes(data, keys=anime_key):
        if type(data) is tuple:
            return dict(zip(keys, data))
        if type(data)is list:
            return [dict(zip(keys, anime))for anime in data]

    @classmethod
    def read_anime(cls):
        cls.get_conn_cur()        
        query = "SELECT * FROM animes;"
        cls.cur.execute(query)
        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def read_anime_by_id(cls, anime_id):
        cls.get_conn_cur()

        query = sql.SQL("""SELECT * FROM animes WHERE id={id};""").format(id=sql.Literal(anime_id))
        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes
        
    @classmethod
    def delete_anime(cls, id):
        cls.get_conn_cur()

        query = sql.SQL("""DELETE FROM 
                                animes WHERE id={id} 
                                RETURNING
                                        *;
                    """).format(id=sql.Literal(id))
        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def update_anime(cls, id, payload):
        cls.get_conn_cur()


        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]



        query = sql.SQL(
            """
                UPDATE animes

                SET
                    ({columns}) = ROW({values})
                WHERE
                    id={id}
                RETURNING
                    *
             """
        ).format(
            id=sql.Literal(id),
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )


        cls.cur.execute(query)

        updated_user = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_user

