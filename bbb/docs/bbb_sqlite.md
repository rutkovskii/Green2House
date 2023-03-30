# Sqlite on Debian

## Install

    sudo apt-get install sqlite3

# Not Tested or Needed beyond that point (from what I think)

## Create database

    sqlite3 greenhouse.db

## Create table

    CREATE TABLE greenhouse (id INTEGER PRIMARY KEY, date TEXT, temperature REAL, humidity REAL);

## Insert data

    INSERT INTO greenhouse (date, temperature, humidity) VALUES (datetime('now'), 22.5, 55.5);

## Select data

    SELECT * FROM greenhouse;

## Exit

    .quit

## References

- [SQLite Tutorial](https://www.sqlitetutorial.net/sqlite-python/)

[]: # # Path: bbb/docs/bbb_sqlite.md
[]: # Compare this snippet from docs/fuc.md:
[]: # `ssh
