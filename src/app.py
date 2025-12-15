import os
import sqlite3
from time import sleep
from classes.workers import Workers
from classes.actions import Actions
from classes.outputs import Outputs


def main():
    os.makedirs('out', exist_ok=True)
    actions = Actions()
    while True:
        rightslist = make_login()
        if not rightslist is None: break
        sleep(1)
    while True:
        match input('С чем работать? Опции: "права", "должности", "права должности", "сотрудники", "отчёт". Ввод: '):
            case 'права': work_rights(rightslist, actions)
            case 'должности': work_positions(rightslist, actions)
            case 'права должности': work_rights_positions(rightslist, actions)
            case 'сотрудники': work_workers(rightslist, actions)
            case 'отчёт': Outputs().all_sers()
            case _: print('Ошибка, вы ввели некорректное значение.')
        sleep(1)


def make_login() -> None|list[str]:
    try:
        w_name, p_name, rights = Workers.check_token(input('Введите свой код входа: '))
    except sqlite3.Error as e:
        print(f'Произошла ошибка: {e}')
        return None
    print(f'Вы авторизованы как {w_name} ({p_name})!')
    return rights


def work_rights(rights:list[str], actions:Actions):
    match input('Что делать с правами? Опции: "список", "создать", "изменить", "удалить". Ввод: '):
        case 'список':
            if 'rights_list' in rights: actions.rights_list()
            else: print('Ошибка, вам недоступно это действие.')
        case 'создать':
            if 'rights_create' in rights: actions.rights_create(input('Ввод названия права: '), input('Ввод описания права: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'изменить':
            if 'rights_change' in rights: actions.rights_change(input('Ввод старого названия права: '), input('Ввод нового названия права: '), input('Ввод нового описания права: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'удалить':
            if 'rights_delete' in rights: actions.rights_delete(input('Ввод названия права: '))
            else: print('Ошибка, вам недоступно это действие.')
        case _: print('Ошибка, вы ввели некорректное значение.')

def work_positions(rights:list[str], actions:Actions):
    match input('Что делать с должностями? Опции: "список", "создать", "изменить", "удалить". Ввод: '):
        case 'список':
            if 'positions_list' in rights: actions.positions_list()
            else: print('Ошибка, вам недоступно это действие.')
        case 'создать':
            if 'positions_create' in rights: actions.positions_create(input('Ввод названия должности: '), input('Ввод описания должности: '), input('Ввод прав должности через запятую: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'изменить':
            if 'positions_change' in rights: actions.positions_change(input('Ввод старого названия должности: '), input('Ввод нового названия должности: '), input('Ввод нового описания должности: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'удалить':
            if 'positions_delete' in rights: actions.positions_delete(input('Ввод названия должности: '))
            else: print('Ошибка, вам недоступно это действие.')
        case _: print('Ошибка, вы ввели некорректное значение.')

def work_rights_positions(rights:list[str], actions:Actions):
    match input('Что делать с правами у этой должности? Опции: "список", "добавить", "удалить". Ввод: '):
        case 'список':
            if 'positions_rights' in rights: actions.positions_rights_list(input('Ввод названия должности: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'добавить':
            if 'positions_rights' in rights: actions.positions_rights_add(input('Ввод названия должности: '), input('Ввод права для добавления: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'удалить':
            if 'positions_rights' in rights: actions.positions_rights_del(input('Ввод названия должности: '), input('Ввод права для удаления: '))
            else: print('Ошибка, вам недоступно это действие.')
        case _: print('Ошибка, вы ввели некорректное значение.')

def work_workers(rights:list[str], actions:Actions):
    match input('Что делать с работниками? Опции: "список", "создать", "изменить", "удалить". Ввод: '):
        case 'список':
            if 'workers_list' in rights: actions.workers_list()
            else: print('Ошибка, вам недоступно это действие.')
        case 'создать':
            if 'workers_create' in rights: actions.workers_create(input('Ввод имени работника: '), input('Ввод кода входа для работника: '), input('Ввод должности работника: '), input('Ввод пола работника (м/ж): '), input('Ввод дня рождения работника: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'изменить':
            if 'workers_change' in rights: actions.workers_change(input('Ввод старого имени работника: '), input('Ввод нового имени работника: '), input('Ввод нового кода входа для работника: '), input('Ввод новой должности работника: '), input('Ввод нового пола работника (м/ж): '), input('Ввод нового дня рождения работника: '))
            else: print('Ошибка, вам недоступно это действие.')
        case 'удалить':
            if 'workers_delete' in rights: actions.workers_delete(input('Ввод названия должности: '))
            else: print('Ошибка, вам недоступно это действие.')
        case _: print('Ошибка, вы ввели некорректное значение.')


if __name__ == '__main__': main()
else: raise ImportError('You can\'t use it as a library')
