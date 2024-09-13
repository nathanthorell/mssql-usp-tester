# MSSQL Stored Procedure Tester

A simple tester script for all the stored procedures on a SQL Server database.  Uses default values in config file to pass in to each procedures parameters based on data type.  This is mainly intended just to check that reporting type procedures execute without errors.

## Local Env Setup

1. `python -m venv .venv/`
1. `source .venv/bin/activate`
1. `python -m pip install -r ./requirements.txt`

  - Note: on Apple Silicon use `brew install unixodbc` and `pip install --no-binary :all: pyodbc==4.0.39`
  - Also [https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16#microsoft-odbc-18]

## Environment Variable Setup

These are required

```text
DB_DRIVER="ODBC Driver 18 for SQL Server"
DB_ENCRYPT=no
DB_SERVER=
DB_PORT=
DB_DATABASE=
DB_USERNAME=
DB_PASSWORD=
```
