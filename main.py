import pyodbc
import toml
import os
from dotenv import load_dotenv
from utils import execute_procedure

# Env and Config Setup
load_dotenv()
script_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(script_dir, "config.toml")

with open(config_path, "r") as f:
    config = toml.load(f)
    usp_config = config["usp_tester"]
    defaults = usp_config["defaults"]

db_server = os.getenv("DB_SERVER")
db_port = os.getenv("DB_PORT")
db_database = os.getenv("DB_DATABASE")
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_driver = os.getenv("DB_DRIVER")
db_encrypt = os.getenv("DB_ENCRYPT")

conn_str = (
    f"DRIVER={db_driver};"
    f"SERVER={db_server},{db_port};"
    f"DATABASE={db_database};"
    f"UID={db_username};"
    f"PWD={db_password};"
    f"Encrypt={db_encrypt};"
)

conn = pyodbc.connect(conn_str)
schema = usp_config["schema"]

try:
    # Fetch stored procedures in the given schema
    query = f"""
    SELECT SPECIFIC_NAME
    FROM INFORMATION_SCHEMA.ROUTINES
    WHERE ROUTINE_TYPE = 'PROCEDURE'
    AND ROUTINE_SCHEMA = '{schema}'
    """
    cursor = conn.cursor()
    cursor.execute(query)
    stored_procedures = cursor.fetchall()

    # Execute each stored procedure
    for proc in stored_procedures:
        proc_name = proc[0]
        print(f"Executing stored procedure: {proc_name}...")
        execute_procedure(conn, schema, proc_name, defaults)
        print("")

except pyodbc.Error as ex:
    print(f"Database error: {ex}")

finally:
    conn.close()
