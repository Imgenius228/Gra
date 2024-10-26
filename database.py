import sqlite3 as sq

def init_db():
    with sq.connect('battle_city.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            level INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

def add_score(player_name, score, level):
    with sq.connect('battle_city.db') as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO high_scores (player_name, score, level) 
                      VALUES (?, ?, ?)""", (player_name, score, level))

def get_high_scores(limit=10):
    with sq.connect('battle_city.db') as con:
        cur = con.cursor()
        scores = cur.execute("""
            SELECT player_name, score, level, date 
            FROM high_scores 
            ORDER BY score DESC 
            LIMIT ?""", (limit,)).fetchall()
        return scores

def get_personal_best(player_name):
    with sq.connect('battle_city.db') as con:
        cur = con.cursor()
        best_score = cur.execute("""
            SELECT MAX(score) 
            FROM high_scores 
            WHERE player_name = ?""", (player_name,)).fetchone()
        return best_score[0] if best_score[0] else 0
