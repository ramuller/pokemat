import mysql.connector
from time import sleep
from contextlib import contextmanager
from random import randrange

class Database:
    def __init__(self, host="leo", user="pokemat", password="pokemat123", db="pokemat"):

        self.conn = mysql.connector.connect(
            host='leo',       # or your host
            user='pokemat',
            password='pokemat123',
            database='pokemat',
            autocommit=True
        )
        self.cursor = self.conn.cursor()
    
    @contextmanager
    def add_friend(self, name, my_name, days_to_go, friend_level): 

        sql = "INSERT INTO friends (name, trainer, days_to_go, friend_level) VALUES (%s, %s, %s, %s)"
        values = (name, my_name, days_to_go, friend_level)
        # values = (name, "Aphex Twin")
        for retry in range(0,7):
            try:
                self.conn.start_transaction()
                self.cursor.execute(sql, values)
                self.conn.commit()
                return True
            except mysql.connector.Error as e:
                self.conn.rollback()
                if e.errno == 1213:  # Deadlock
                    print("Deadlock detected, retrying...")
                    sleep(randrange(1,10)/100.0)
                elif e.errno == 1062:
                    print("Duplicate entry...ignoring {}".format(values))
                    return True
                else:
                    print("Unknow error {} - {}".format(e.errno, e.msg))
                    print("Unknow error {} - {}".format(e.errno, e.msg))
                    raise
                
    @contextmanager
    def update_friend(self, name, trainer, days_to_go, friend_level, opened=False, sent=False):
        sql = "UPDATE friends SET last_check = CURDATE(), days_to_go = %s, friend_level = %s WHERE name = %s and trainer = %s;"
        values = (days_to_go, friend_level, name, trainer)
        # values = (name, "Aphex Twin")
        for retry in range(0,7):
            try:
                self.conn.start_transaction()
                self.cursor.execute(sql, values)
                self.conn.commit()
                return True
            except mysql.connector.Error as e:
                self.conn.rollback()
                if e.errno == 1213:  # Deadlock
                    print("Deadlock detected, retrying...")
                    sleep(randrange(1,10)/100.0)
                elif e.errno == 1062:
                    print("Duplicate entry in update...ignoring {}".format(values))
                    return True
                else:
                    print("Unknow error {} - {}".format(e.errno, e.msg))
                    print("Unknow error {} - {}".format(e.errno, e.msg))
                    raise


    # @contextmanager
    def get_trainer(self, name):
        sql = "SELECT * FROM trainers WHERE name like '" + name + "%';"
        print(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    # @contextmanager
    def get_trainer_in_team(self, team):
        sql = "SELECT name FROM trainers WHERE team = '" + team + "';"
        print(sql)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return [item for tup in rows for item in tup]
      
    
