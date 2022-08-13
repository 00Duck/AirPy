import mariadb
import pandas as pd
import datetime

class DB:
    def __init__(self):
        self.error = False
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = mariadb.connect(
            user="airpy",
            password="airpy",
            host="localhost",
            database="airpy")
            self.cur = self.conn.cursor()
        except Exception as e:
            print("Failed to connect to database: ", str(e))

        try:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS sensor (
            id int auto_increment primary key,
            pm_two_five float,
            pm_ten float,
            measured_at DATETIME
            ) engine=InnoDB default charset utf8;
            """)
        except Exception as e:
            print("Failed to create existing table: ", str(e))

    def collect(self, data: tuple[str, str, str]):
        try:
            self.cur.execute("INSERT INTO sensor (pm_two_five,pm_ten,measured_at) VALUES (?, ?, ?)", data)
            self.conn.commit()
        except mariadb.Error as e:
            print("Database insert error: ", str(e))
    
    def retrieve_data(self) -> pd.DataFrame:
        try:
            df = pd.read_sql(sql="SELECT id, pm_two_five, pm_ten, measured_at FROM sensor ORDER BY measured_at DESC;", con=self.conn, parse_dates=["measured_at"])
            # Seems hackish. I found this solution to convert the times to ET from UTC. This allows me to modify the data with tz_convert
            # Instead of modifying the index (which is how tz_convert normally works)
            df['measured_at'] = pd.to_datetime(df['measured_at']).dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
            return df
        except mariadb.Error as e:
            print("Database getData error: ", str(e))
            return []