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
                skin TEXT
            )""")
        cur.execute("SELECT * FROM logged WHERE user_logged = 1")
        if not cur.fetchone():
            cur.execute("INSERT INTO logged (user_logged, city_set, skin) VALUES (?, ?, ?)", (1, None, None))
        db.commit()
        db.close()



    @classmethod
    def get_city(cls):
        db = sqlite3.connect(cls.DB_FILE)  # -> opens the connection with the db
        cur = db.cursor()  # -> sets a cursor to move inside the db

        cur.execute("SELECT city_set FROM logged WHERE user_logged = 1")
        city = cur.fetchone()[0]

        return city