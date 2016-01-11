from sqlitedict import SqliteDict

flixrdb = SqliteDict('./movies.sqlite', autocommit=True)