import sqlite3

class User:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                          username TEXT UNIQUE PRIMARY KEY,
                          password TEXT)""")
    
    def insert_into_users(self, user):
        self.cur.execute("""INSERT OR IGNORE INTO users VALUES(?,?)""", user)
        self.conn.commit()
    
    def read_usernames(self):
        self.cur.execute("""SELECT username FROM users""")
        usernames = self.cur.fetchall()
        return usernames
    def check_user(self, username):
        self.cur.execute("""SELECT password FROM users WHERE username = ?""", (username,))
        user = self.cur.fetchone()
        return user
