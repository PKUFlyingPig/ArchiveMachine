import sqlite3
con = sqlite3.connect("index.db")
cur = con.cursor()
# Insert a row of data
cur.execute("""SELECT * FROM ID2PATH WHERE SnapshotID=?""", ('3ea250922ae405bb9f475c148df41b411b51f7366ca5a1a4d73aae462ab6fe4e',))
_, path, url, timestamp = cur.fetchone()
print(path, url, timestamp)
con.close()