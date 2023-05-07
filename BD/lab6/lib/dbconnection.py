# Установка соединения с базой данных
# (параметры передаются через класс конфиг).
import logging
from datetime import date
from os import sep
import psycopg2
from psycopg2.extras import LoggingConnection
LOG_FILE ="log" + sep + str(date.today()) + ".log"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
FH = logging.FileHandler(LOG_FILE)
basic_formater = logging.Formatter('%(asctime)s : [%(levelname)s] : %(message)s')
FH.setFormatter(basic_formater)
logger.addHandler(FH)

class DbConnection:

    def __init__(self, config):
        self.dbname = config.dbname
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.prefix = config.dbtableprefix
        self.port = config.port
        self.conn = psycopg2.connect(dbname = self.dbname,
                                    user = self.user, 
                                    password = self.password,
                                    host = self.host,
                                    port=self.port,
                                    connection_factory=LoggingConnection)
        self.conn.initialize(logger)
        self.logger = logger

    def __del__(self):
        if self.conn:
            self.conn.close()

    def test(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS test CASCADE")
        cur.execute("CREATE TABLE test(test integer)")
        cur.execute("INSERT INTO test(test) VALUES(1)")
        self.conn.commit()
        cur.execute("SELECT * FROM test")
        result = cur.fetchall()
        cur.execute("DROP TABLE test")
        self.conn.commit()
        return (result[0][0] == 1)
        
