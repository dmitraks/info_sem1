import re
import sqlite3
from classes.workers import Workers
from classes.positions import Positions
from classes.rights import Rights


class Actions:
    @staticmethod
    def rights_list() -> None:
        data = Rights.all()
        maxlen = max(map(lambda right: len(right[1]), data), default=0) + (len(data)//10) + 2 + 4
        rights_list = '\n'.join([f'{i+1}. {f"\"{right[1]}\"":<{maxlen-len(str(i+1))}}- {right[2]}' for i, right in enumerate(data)])
        print('Права не заданы.' if rights_list == '' else f'Список всех прав:\n{rights_list}')

    @staticmethod
    def rights_create(name:str, descr:str) -> None:
        err = Rights.add(name, descr)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно создано право "{name}".')

    @staticmethod
    def rights_change(old_name:str, new_name:str, new_desc:str) -> None:
        err = Rights.change(old_name, new_name, new_desc)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно изменено право "{old_name}" на "{new_name}" ({new_desc}).')

    @staticmethod
    def rights_delete(right_name:str) -> None:
        err = Rights.delete(right_name)
        if err: print(f'Произошла ошбика: {err}')
        else: print(f'Успешно удалено право "{right_name}".')


    @staticmethod
    def positions_list() -> None:
        data = Positions.all()
        maxlen = max(map(lambda pos: len(pos[1]), data), default=0) + (len(data)//10) + 2 + 4
        poss_list = '\n'.join([f'{i+1}. {f"\"{pos[1]}\"":<{maxlen-len(str(i+1))}}- {pos[2]}' for i, pos in enumerate(data)])
        print('Должности не заданы.' if poss_list == '' else f'Список всех должностей:\n{poss_list}')

    @staticmethod
    def positions_create(name:str, descr:str, raw_rights:str) -> None:
        rightslist = [] if raw_rights == '' else re.split(',[ ]*', raw_rights)
        errs = Positions.add(name, descr, rightslist)
        if isinstance(errs, str): print(f'Произошла ошибка: {errs}')
        elif errs is None: print(f'Успешно создана должность "{name}" ({descr}) с {len(rightslist)} правами.')
        else: print(f'Создана должность {name} ({descr}), но есть ошибки с правами: {"; ".join(errs)}; успешно установлено прав - {len(rightslist)-len(errs)}.')

    @staticmethod
    def positions_change(old_name:str, new_name:str, new_desc:str) -> None:
        err = Positions.change(old_name, new_name, new_desc)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно изменена должность "{old_name}" на "{new_name}" ({new_desc}).')

    @staticmethod
    def positions_delete(pos_name:str) -> None:
        err = Positions.remove(pos_name)
        if err: print(f'Произошла ошбика: {err}')
        else: print(f'Успешно удалена должность "{pos_name}".')


    @staticmethod
    def positions_rights_list(name:str) -> None:
        try: data = Positions.get_rights(name)
        except sqlite3.Error as e: return print(f'Произошла ошибка: {e}')
        maxlen = max(map(lambda pos: len(pos[1]), data), default=0) + (len(data)//10) + 2 + 4
        rights_list = '\n'.join([f'{i+1}. {f"\"{right[1]}\"":<{maxlen-len(str(i+1))}}- {right[2]}' for i, right in enumerate(data)])
        print(f'У "{name}" нет прав.' if rights_list == '' else f'Список всех прав у "{name}":\n{rights_list}')

    @staticmethod
    def positions_rights_add(name:str, right:str) -> None:
        err = Positions.add_right(name, right)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно добавлено право "{right}" к должности "{name}".')

    @staticmethod
    def positions_rights_del(name:str, right:str) -> None:
        err = Positions.del_right(name, right)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно удалено право "{right}" у должности "{name}".')


    @staticmethod
    def workers_list() -> None:
        data = Workers.all()
        maxlen = max(map(lambda wor: len(wor[4]), data), default=0) + (len(data)//10) + 2 + 4
        wors_list = '\n'.join([f'{i+1}. {f"\"{wor[4]}\"":<{maxlen-len(str(i+1))}}- {'Ж' if wor[3] else 'М'} {wor[6]}; {wor[5]}; {wor[1]}' for i, wor in enumerate(data)])
        print('Работники не заданы.' if wors_list == '' else f'Список всех работников:\n{wors_list}')

    @staticmethod
    def workers_create(name:str, token:str, p_name:str, raw_sex:str, birthday:str) -> None:
        match raw_sex:
            case 'м': sex = False
            case 'ж': sex = True
            case _: return print(f'Произошла ошибка: введите в пол именно "м" или "ж", а не "{raw_sex}".')
        err = Workers.add(name, p_name, sex, name, birthday)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Создан работник {name} ({p_name}).')

    @staticmethod
    def workers_change(old_name:str, new_name:str, token:str, p_name:str, raw_sex:str, birthday:str) -> None:
        match raw_sex:
            case 'м': sex = False
            case 'ж': sex = True
            case _: return print(f'Произошла ошибка: введите в пол именно "м" или "ж", а не "{raw_sex}".')
        err = Workers.change(old_name, new_name, token, p_name, sex, birthday)
        if err: print(f'Произошла ошибка: {err}')
        else: print(f'Успешно изменен работник "{old_name}".')

    @staticmethod
    def workers_delete(name:str) -> None:
        err = Workers.remove(name)
        if err: print(f'Произошла ошбика: {err}')
        else: print(f'Успешно удалена должность "{name}".')
