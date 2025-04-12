import mysql.connector

class Database:
    def __init__(self, host="leo", user="pokemat", password="pokemat123", db="pokemat"):

        self.conn = mysql.connector.connect(
            host='leo',       # or your host
            user='pokemat',
            password='pokemat123',
            database='pokemat'
        )
        self.cursor = self.conn.cursor()
    
    def add_friend(self, name, my_name, days_to_go, friend_level): 

        sql = "INSERT INTO friends (name, trainer, days_to_go, friend_level) VALUES (%s, %s, %s, %s)"
        values = (name, my_name, days_to_go, friend_level)
        # values = (name, "Aphex Twin")
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            print("Duplicate entry...ignoring {}".format(values))
