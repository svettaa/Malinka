from enum import Enum


class Success(Enum):
    ADDED_PROCEDURE = 1
    ADDED_CATEGORY = 2
    UPDATED_CATEGORY = 3
    UPDATED_PROCEDURE = 4
    DELETED_CATEGORY = 5
    DELETED_PROCEDURE = 6


class Error(Enum):
    CATEGORY_HAS_PROCEDURES = 1
    CATEGORY_NAME_EXISTS = 2
    PROCEDURE_NAME_EXISTS = 3
    PROCEDURE_ILLEGAL_DATA = 4
    PROCEDURE_HAS_APPOINTMENTS = 5


message = {Success.ADDED_CATEGORY: 'Успішно додано категорію',
           Success.ADDED_PROCEDURE: 'Успішно додано процедуру',
           Success.UPDATED_CATEGORY: 'Успішно змінено категорію',
           Success.UPDATED_PROCEDURE: 'Успішно змінено процедуру',
           Success.DELETED_CATEGORY: 'Успішно видалено категорію',
           Success.DELETED_PROCEDURE: 'Успішно видалено процедуру',
           Error.CATEGORY_HAS_PROCEDURES: 'Неможливо видалити категорію, що містить процедури',
           Error.CATEGORY_NAME_EXISTS: 'Неможливо змінити або додати категорію, '
                                       'категорія з такою назваю вже існує',
           Error.PROCEDURE_NAME_EXISTS: 'Неможливо змінити або додати процедуру, '
                                        'процедура з такою назваю вже існує',
           Error.PROCEDURE_ILLEGAL_DATA: 'Неможливо змінити або додати процедуру '
                                         'через неправильно введені дані. Можливі причини: '
                                         'Некоректний числовий формат для ціни '
                                         'Не вказана мінімальна ціна',
           Error.PROCEDURE_HAS_APPOINTMENTS: 'Неможливо видалити процедуру, що міститься у записах'
           }


def get_error_message(code):
    if code is not None:
        return message[Error(int(code))]


def get_success_message(code):
    if code is not None:
        return message[Success(int(code))]
