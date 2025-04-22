from utils.db.sqlte3_connector import SqLite3Connector
from fastapi import status, HTTPException

default_user_settings = """{"autosave":2,"formatting":1,"darkmode":0,"left_widget":0,"right_widget":0,"fullpage_content":0,"markdown_export":0,"flashcards_enabled":1,"default_doc":0,"keep_session":1,"session":[],"lang":"__"}"""

class DbClient():
    def __init__(self, database_name:str, database_type:str="sqlite3", init_tables_at_start:bool=True):
        self.database_type = database_type
        self.client = SqLite3Connector(f"{database_name}.db")
        if init_tables_at_start:
            self.create_tables()

    def _execute(self, query, *args) -> list|dict:
        output = self.client.execute(query, *args)
        #output = self.client.execute(query[self.database_type], *args)
        try:
            if str(output[0][0]).startswith("ERROR:"):
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, output)
            return output
        except IndexError:
            return []

    def create_tables(self):
        r"creates tables and indexes"
        self._execute("""CREATE TABLE IF NOT EXISTS pages (
    page_id TEXT PRIMARY KEY,
    page_json TEXT NOT NULL
);
""")
        return

        # TABLES
        ## auth
        for f in dir(auth):
            if f.startswith("create_table"):
                query = getattr(auth, f)
                self._execute(
                        query
                        )

        # INDEXES
        for f in dir(auth):
            if f.startswith("create_index"):
                query = getattr(auth, f)
                self._execute(
                        query
                        )

        for f in dir(docs):
            if f.startswith("create_table"):
                query = getattr(docs, f)
                self._execute(query)

    def create_or_update_page(self, page_id, data:str):
        query = """INSERT INTO pages (page_id, page_json)
                VALUES (?, ?)
                ON CONFLICT(page_id) DO UPDATE SET page_json = excluded.page_json;
                """
        self._execute(query, page_id, data)

    def get_page(self, page_id):
        query = """SELECT page_json FROM pages WHERE page_id = ?;"""
        out = self._execute(query, page_id)
        return out[0][0][0]

    def delete_page(self, page_id):
        raise NotImplementedError("Not implemented as long as pages don't have passwords")
        query  =""" DELETE FROM pages WHERE page_id = ?;"""
        self._execute(query, page_id)




