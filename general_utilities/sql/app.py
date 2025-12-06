import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

conn = pyodbc.connect(
    f"DRIVER={config['sql']['DRIVER']};"
    f"SERVER={config['sql']['SERVER']};"
    f"DATABASE={config['sql']['DATABASE']};"
    f"Trusted_Connection={config['sql']['Trusted_Connection']};"
)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.databases")
for row in cursor.fetchall():
    print(row)
conn.close()
