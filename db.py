import psycopg2

class DB:

    # DONE
    def __init__(self, hostname, port, dbname, username, password):
        self.dburl = "host=" + hostname + " port=" + str(port) + " dbname=" + dbname + \
                     " user=" + username + " password=" + password

    # DONE
    def get_connection(self, dburl):
        return psycopg2.connect(self.dburl)

    # DONE
    def execute(self, sql, data):
        conn = psycopg2.connect(self.dburl)
        cur = conn.cursor()
        if data == None:
            cur.execute(sql)
        else:
            cur.execute(sql, data)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows;

    # DONE
    def update(self, sql, data):
        conn = psycopg2.connect(self.dburl)
        conn.autocommit = False
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        cur.close()
        conn.close()
