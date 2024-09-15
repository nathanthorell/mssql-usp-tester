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
    schema = usp_config["schema"]
    logging_level = usp_config["logging_level"]

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

print(f"Executing script on server: [{db_server}] in database: [{db_database}]")
print(f"Using logging_level: {logging_level}\n")

try:
    # Fetch stored procedures in the given schema
    query = f"""
    SELECT SPECIFIC_NAME
    FROM INFORMATION_SCHEMA.ROUTINES
    WHERE ROUTINE_TYPE = 'PROCEDURE'
    AND ROUTINE_SCHEMA = '{schema}'
    ORDER BY SPECIFIC_NAME;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    stored_procedures = cursor.fetchall()

    results = []
    for proc in stored_procedures:
        proc_name = proc[0]
        if logging_level == "verbose":
            print(f"Executing stored procedure: {proc_name}...")

        result = execute_procedure(conn, schema, proc_name, defaults, logging_level)
        results.append(result)

        if logging_level == "verbose":
            print("")  # For spacing between logs

    if logging_level == "summary":
        print("Execution Summary:")
        print(f"{'Procedure Name':<50} {'Status':<10} {'Execution Time':<15}")
        print("-" * 76)
        for result in results:
            proc_name = result["proc_name"]
            status = result["status"]
            elapsed_time = (
                f"{result['elapsed_time']:.2f}" if result["elapsed_time"] else "N/A"
            )
            print(f"{proc_name:<50} {status:<10} {elapsed_time:<15}")

except pyodbc.Error as ex:
    print(f"Database error: {ex}")

finally:
    conn.close()
