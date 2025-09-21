import sqlite3

class Database:
    DB_FILE = 'data.db1'

    @classmethod
    def initialize(cls):
        db = sqlite3.connect(cls.DB_FILE)
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS logged (
                id INTEGER PRIMARY KEY,
                user_logged INTEGER,
                city_set TEXT,
                country_set TEXT,
                advices INTEGER,
                skin TEXT,
                units TEXT,
                lang TEXT
            )""")
        cur.execute("SELECT * FROM logged WHERE user_logged = 1")
        if not cur.fetchone():
            cur.execute("INSERT INTO logged (user_logged, city_set, country_set, advices, skin, units, lang) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, None, None, 1, None, 'metric', 'en'))
        db.commit()
        db.close()



    @classmethod
    def get_city(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT city_set, country_set FROM logged WHERE user_logged = 1")
        row = cur.fetchone()

        city = None
        country = None

        if row:
            city = row[0]
            country = row[1]


        return f"{city}, {country}" if city and country else None

    @classmethod
    def get_skin(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT skin FROM logged WHERE user_logged = 1")
        skin = cur.fetchone()[0]

        return skin



    @classmethod
    def get_units(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT units FROM logged WHERE user_logged = 1")
        units = cur.fetchone()[0]


        return units


    @classmethod
    def user_advices(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT advices FROM logged WHERE user_logged = 1")
        are_enabled = cur.fetchone()[0]



        return are_enabled

    @classmethod
    def get_lang(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT lang FROM logged WHERE user_logged = 1")
        lang = cur.fetchone()[0]
        return lang