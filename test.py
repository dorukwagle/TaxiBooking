from psycopg2 import OperationalError
# database connection test
from utils import DatabaseConnector as dbc
try:
    db = dbc.DatabaseConnector()
    cur = db.cursor
    cur.execute("insert into admin(full_name, username, gender) values ('chdsmart', 'chdyo', 'male')")
    cur.execute("select * from admin")
    # print(cur.fetchone())
    print(cur.fetchall())
except OperationalError as e:
    print(e)
finally:
    db.close()


