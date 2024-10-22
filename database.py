import sqlite3 as sq

with sq.connect('database.db') as con:
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS records (
                    value INTEGER DEFAULT 0
                    )""")
    
    
    

def add_result(result):
    with sq.connect('database.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO records (value) VALUES ({result})""")
        
def get_record():
     with sq.connect('database.db') as con:
        cur = con.cursor()
        records = cur.execute("""SELECT value FROM records""").fetchall()

        hight_record = 0 
        for record in records:
            if record[0] > hight_record:
                hight_record = record[0]
                
        return hight_record