import sqlite3


class Translate:
    def __init__(self, language: str, source: str):
        self.lang = language.split(',')[0].lower().replace('-', '_')
        self.connection = sqlite3.connect(source)
        self.columns = [fields[1] for fields in self.connection.execute(f"PRAGMA table_info(translation)").fetchall()]
        pass

    def t(self, s: str) -> str:
        cur = self.connection.cursor()
        if self.lang != 'en_us' and self.lang in self.columns:
            q = f"SELECT {self.lang} FROM translation WHERE en_us = ?"
            r = cur.execute(q, (s,)).fetchone()
            if r is not None and len(r) > 0:
                s = r[0]
        return s
