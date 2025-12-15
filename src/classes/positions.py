import sqlite3
from classes.rights import Rights


class Positions:
    @staticmethod
    def get(name:str) -> tuple[int, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM positions WHERE name = ?', (name,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такой должности.')
            return res

    @staticmethod
    def getbyuuid(uuid:int) -> tuple[int, str, str]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            res = cur.execute('SELECT * FROM positions WHERE uuid = ?', (uuid,)).fetchone()
            if res is None: raise sqlite3.Error('Не найдено такой должности.')
            return res

    @staticmethod
    def all() -> list[tuple[int, str, str]]:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            return cur.execute('SELECT * FROM positions').fetchall()

    @staticmethod
    def add(name:str, descr:str, rights:list[str]) -> str|list[str]|None:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try: cur.execute('INSERT INTO positions(name, description) VALUES(?, ?)', (name, descr))
            except sqlite3.Error: return 'Такое имя уже используется.'
        pos_id = Positions.get(name)[0]
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            errs:list[str] = []
            for r_name in rights:
                r_uuid = cur.execute('SELECT uuid FROM rights WHERE name = ?', (r_name,)).fetchone()
                if r_uuid is None: errs.append(f'{r_name} (не найдено)')
                else:
                    try: cur.execute('INSERT INTO positionstorights(position, right) VALUES(?, ?)', (pos_id, r_uuid[0]))
                    except sqlite3.Error: errs.append(f'{r_name} (введено дважды)')
            return None if len(errs) == 0 else errs

    @staticmethod
    def change(old_name:str, new_name:str, new_descr:str) -> str|None:
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                if cur.execute('SELECT uuid FROM positions WHERE name = ?', (old_name,)).fetchone() is None: return 'Не найдено такой должности.'
                cur.execute('UPDATE positions SET name = ?, description = ? WHERE name = ?', (new_name, new_descr, old_name))
        except sqlite3.Error as e:
            return e.__str__()

    @staticmethod
    def remove(name:str) -> str|None:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            if cur.execute('SELECT uuid FROM positions WHERE name = ?', (name,)).fetchone() is None: return 'Не найдено такой должности.'
            try: cur.execute('DELETE FROM positions WHERE name = ?', (name,))
            except sqlite3.Error: return 'Сначала удалите все права и уберите всех людей с этой должности.'

    @staticmethod
    def get_rights(name:str) -> list[str]:
        try: uuid = Positions.get(name)[0]
        except sqlite3.Error as e: raise sqlite3.Error(e)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            rights = cur.execute('SELECT rights.uuid, rights.name, rights.description FROM rights JOIN positionstorights ON positionstorights.position = ? AND rights.uuid = positionstorights.right', (uuid,)).fetchall()
            return rights

    @staticmethod
    def add_right(p_name:str, r_name:str) -> str|None:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try:
                p_uuid = Positions.get(p_name)[0]
                r_uuid = Rights.get(r_name)[0]
            except sqlite3.Error as e: return e.__str__()
            try: cur.execute('INSERT INTO positionstorights(position, right) VALUES(?, ?)', (p_uuid, r_uuid))
            except sqlite3.Error: return 'Это право уже есть у этой должности.'

    @staticmethod
    def del_right(p_name:str, r_name:str) -> str|None:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try:
                p_uuid = Positions.get(p_name)[0]
                r_uuid = Rights.get(r_name)[0]
            except sqlite3.Error as e:
                return e.__str__()
            uuid = cur.execute('SELECT uuid FROM positionstorights WHERE position = ? AND right = ?', (p_uuid, r_uuid)).fetchone()
            if uuid is None: return 'Не найдено такой должности.'
            cur.execute('DELETE FROM positionstorights WHERE uuid = ?', (uuid[0],))
