import sqlite3
from classes.positions import Positions


class Workers:
    @staticmethod
    def check_token(token:str) -> tuple[str, str, list[str]]:
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                w_name, p_name, p_uuid = cur.execute('SELECT workers.name, positions.name, workers.position FROM workers JOIN positions ON workers.token = ? AND positions.uuid = workers.position', (token,)).fetchone()
                if p_uuid is None: raise sqlite3.Error('Не найдено такого кода входа.')
                rights = [right[0] for right in cur.execute('SELECT rights.name FROM rights JOIN positionstorights ON positionstorights.position = ? AND positionstorights.right = rights.uuid', (p_uuid,)).fetchall()]
                return (w_name, p_name, rights)
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

    @staticmethod
    def get(name:str) -> tuple[int, str, int, bool, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM workers WHERE name = ?', (name,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такого работника.')
            return res

    @staticmethod
    def getbyuuid(uuid:int) -> tuple[int, str, int, bool, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM workers WHERE uuid = ?', (uuid,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такого работника.')
            return res

    @staticmethod
    def all() -> list[tuple[int, str, int, bool, str, str, str]]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            return cur.execute('SELECT workers.uuid, workers.token, workers.position, workers.sex, workers.name, workers.birthday, positions.name FROM workers JOIN positions ON positions.uuid = workers.position').fetchall()

    @staticmethod
    def add(token:str, p_name:str, sex:bool, name:str, birthday:str) -> str|None:
        try: p_uuid = Positions.get(p_name)[0]
        except sqlite3.Error: return 'Не найдено такой должности.'
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try: cur.execute('INSERT INTO workers(token, position, sex, name, birthday) VALUES(?, ?, ?, ?, ?)', (token, p_uuid, sex, name, birthday))
            except sqlite3.Error: return 'Уже есть работник с таким именем или кодом входа.'

    @staticmethod
    def change(old_name:str, new_name:str, token:str, p_name:str, sex:bool, birthday:str) -> str|None:
        try: w_uuid = Workers.get(old_name)[0]
        except sqlite3.Error: return 'Не найдено такого работника.'
        try: p_uuid = Positions.get(p_name)[0]
        except sqlite3.Error: return 'Не найдено такой должности.'
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('UPDATE workers SET token = ?, position = ?, sex = ?, name = ?, birthday = ? WHERE uuid = ?', (token, p_uuid, sex, new_name, birthday, w_uuid))
        except sqlite3.Error as e:
            return e.__str__()

    @staticmethod
    def remove(name:str) -> str|None:
        try: w_uuid = Workers.get(name)[0]
        except sqlite3.Error: return 'Не найдено такого работника.'
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('DELETE FROM workers WHERE uuid = ?', (w_uuid,))
