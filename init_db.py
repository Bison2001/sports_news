import sqlite3

connection = sqlite3.connect('nba_schedule.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO nba_schedule (away, home, match_time, match_date, date_id) VALUES (?, ?, ?, ?, ?)",
            ('GSW', 'LAL', '11:00 PM', 'Wednesday, October 11, 2023 - Preseason', '20231011')
            )

cur.execute("INSERT INTO nba_schedule (away, home, match_time, match_date, date_id) VALUES (?, ?, ?, ?, ?)",
            ('GSW', 'LAC', '08:00 PM', 'Wednesday, October 12, 2023 - Preseason', '20231011')
            )

connection.commit()
connection.close()