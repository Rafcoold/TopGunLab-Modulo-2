import psycopg

PASSWORD = "My_password"

class UserConnection:
    conn = None

    def __init__(self):
        try:
            self.conn = psycopg.connect(f"dbname=veterinary user=postgres password={PASSWORD} host=localhost port=5432")
        except psycopg.OperationalError as error:
            print(error)
            self.conn.close()

    def read_all(self):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                            SELECT * FROM "user"
                                """)
            return data.fetchall()

    def select_one(self, id):
        with self.conn.cursor() as cur:
            data = cur.execute("""
                            SELECT * FROM "user" WHERE id = %s
                        """, (id,))
            return data.fetchone()

    def write(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO "user"(name, age, species, breed) VALUES (%(name)s, %(age)s, %(species)s, %(breed)s)
                        """, data)
        self.conn.commit()

    def update(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE "user" SET name = %(name)s, age = %(age)s, species = %(species)s, breed = %(breed)s 
                WHERE id = %(id)s    
            """, data)
        self.conn.commit()

    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("""
            DELETE FROM "user" WHERE id = %s
                        """, (id,))
        self.conn.commit()

    def __def__(self):
        self.conn.close()
