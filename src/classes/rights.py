import sqlite3


class Rights:
    @staticmethod
    def get(name:str) -> tuple[int, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM rights WHERE name = ?', (name,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такого права.')
            return res

    @staticmethod
    def getbyuuid(uuid:int) -> tuple[int, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM rights WHERE uuid = ?', (uuid,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такого права.')
            return res

    @staticmethod
    def all() -> list[tuple[int, str, str]]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            return cur.execute('SELECT * FROM rights').fetchall()

    @staticmethod
    def add(name:str, descr:str) -> str|None:
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('INSERT INTO rights(name, description) VALUES (?, ?)', (name, descr))
        except sqlite3.Error as e:
            return e.__str__()

    @staticmethod
    def change(old_name:str, new_name:str, new_descr:str) -> str|None:
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                if cur.execute('SELECT uuid FROM rights WHERE name = ?', (old_name,)).fetchone() is None: return 'Не найдено такого права.'
                cur.execute('UPDATE rights SET name = ?, description = ? WHERE name = ?', (new_name, new_descr, old_name))
        except sqlite3.Error as e:
            return e.__str__()

    @staticmethod
    def delete(name:str) -> str|None:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if cur.execute('SELECT uuid FROM rights WHERE name = ?', (name,)).fetchone() is None: return 'Не найдено такого права.'
            try: cur.execute('DELETE FROM rights WHERE name = ?', (name,))
            except sqlite3.Error: return 'Сначала удалите это право у всех должностей.'
