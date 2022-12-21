import requests
import sqlite3
import re
from bs4 import BeautifulSoup

conn = sqlite3.connect('C:/Users/cfmor/PycharmProjects/Machine Learning Tutorial by Tech with Tim/CSGO rating predicter/db.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Raw')
cur.execute('''
            CREATE TABLE "Raw" (
                "id"	    INTEGER,
                "user"	    TEXT,
                "maps"	    INTEGER,
                "rounds"	INTEGER,
                "kd_diff"	INTEGER,
                "kd_rel"	REAL,
                "rating"	REAL,
                PRIMARY KEY("id" AUTOINCREMENT)
            )
            ''')


URL = "https://www.hltv.org/stats/players?startDate=all"
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
players = soup('tr')

count = -1
for player in players:
    count += 1
    if count <= 0:
        continue

    to_insert = list()
    int_count = 0
    tags = player('td')
    for tag in tags:
        text = tag.get_text().strip()
        if int_count != 1:
            to_insert.append(text)
        int_count += 1
    cur.execute('''
                INSERT INTO Raw(user, maps, rounds, kd_diff, kd_rel, rating)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (to_insert[0], to_insert[1], to_insert[2], to_insert[3], to_insert[4], to_insert[5]))
    conn.commit()

for row in cur.execute('SELECT * FROM Raw'):
    print(row)
cur.close()


