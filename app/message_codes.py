from enum import Enum


class Success(Enum):
    ADDED_PROCEDURE = 1
    ADDED_CATEGORY = 2
    UPDATED_CATEGORY = 3
    UPDATED_PROCEDURE = 4
    DELETED_CATEGORY = 5
    DELETED_PROCEDURE = 6
    ADDED_PAINT = 7
    UPDATED_PAINT = 8
    DELETED_PAINT = 9
    ADDED_SUPPLY = 10
    UPDATED_SUPPLY = 11
    DELETED_SUPPLY = 12
    ADDED_USER = 13
    UPDATED_USER = 14
    DELETED_USER = 15
    ADDED_MASTER = 16
    UPDATED_MASTER = 17
    DELETED_MASTER = 18


class Error(Enum):
    CATEGORY_HAS_PROCEDURES = 1
    CATEGORY_NAME_EXISTS = 2
    PROCEDURE_NAME_EXISTS = 3
    PROCEDURE_ILLEGAL_DATA = 4
    PROCEDURE_HAS_APPOINTMENTS = 5
    PAINT_CODE_EXISTS = 6
    PAINT_ILLEGAL_DATA = 7
    PAINT_HAS_APPOINTMENTS = 8
    SUPPLY_ILLEGAL_DATA = 9
    USER_PHONE_EXISTS = 10
    USER_HAS_APPOINTMENTS = 11
    USER_ILLEGAL_DATA = 12
    MASTER_HAS_APPOINTMENTS = 13
    MASTER_ILLEGAL_DATA = 14


message = {Success.ADDED_CATEGORY: 'Успішно додано категорію',
           Success.ADDED_PROCEDURE: 'Успішно додано процедуру',
           Success.UPDATED_CATEGORY: 'Успішно змінено категорію',
           Success.UPDATED_PROCEDURE: 'Успішно змінено процедуру',
           Success.DELETED_CATEGORY: 'Успішно видалено категорію',
           Success.DELETED_PROCEDURE: 'Успішно видалено процедуру',
           Success.ADDED_PAINT: 'Успішно додано фарбу',
           Success.UPDATED_PAINT: 'Успішно змінено фарбу',
           Success.DELETED_PAINT: 'Успішно видалено фарбу',
           Success.ADDED_SUPPLY: 'Успішно додано поставку',
           Success.UPDATED_SUPPLY: 'Успішно змінено поставку',
           Success.DELETED_SUPPLY: 'Успішно видалено поставку',
           Success.ADDED_USER: 'Успішно додано користувача',
           Success.UPDATED_USER: 'Успішно змінено користувача',
           Success.DELETED_USER: 'Успішно видалено користувача',
           Success.ADDED_MASTER: 'Успішно додано майстра',
           Success.UPDATED_MASTER: 'Успішно змінено майстра',
           Success.DELETED_MASTER: 'Успішно видалено майстра',
           Error.CATEGORY_HAS_PROCEDURES: 'Неможливо видалити категорію, що містить процедури',
           Error.CATEGORY_NAME_EXISTS: 'Неможливо змінити або додати категорію, '
                                       'категорія з такою назваю вже існує',
           Error.PROCEDURE_NAME_EXISTS: 'Неможливо змінити або додати процедуру, '
                                        'процедура з такою назваю вже існує',
           Error.PROCEDURE_ILLEGAL_DATA: 'Неможливо змінити або додати процедуру '
                                         'через неправильно введені дані. Можливі причини: '
                                         'Некоректний числовий формат для ціни '
                                         'Не вказана мінімальна ціна',
           Error.PAINT_ILLEGAL_DATA: 'Неможливо змінити або додати фарбу '
                                     'через неправильно введені дані. Можливі причини: '
                                     'Не вказано залишок',
           Error.PROCEDURE_HAS_APPOINTMENTS: 'Неможливо видалити процедуру, що міститься у записах '
                                             'або улюблених',
           Error.PAINT_HAS_APPOINTMENTS: 'Неможливо видалити фарбу, що міститься у записах '
                                         'або для якої є поставки',
           Error.USER_HAS_APPOINTMENTS: 'Неможливо видалити клієнта, що міститься у записах '
                                        'або є майстром',
           Error.USER_PHONE_EXISTS: 'Неможливо додати або змінити користувача, '
                                    'користувач з таким номером вже існує',
           Error.PAINT_CODE_EXISTS: 'Неможливо змінити або додати фарбу, '
                                    'фарба з таким номером вже існує',
           Error.SUPPLY_ILLEGAL_DATA: 'Неможливо змінити або додати поставку. '
                                      'Можливі причини: '
                                      'Неправильно вказана дата '
                                      'Не вказано кількість',
           Error.USER_ILLEGAL_DATA: 'Неможливо додати або змінити користувача, '
                                    'неправильно введені дані',
           Error.MASTER_ILLEGAL_DATA: 'Неможливо додати або змінити майстра, '
                                      'неправильно введені дані',
           Error.MASTER_HAS_APPOINTMENTS: 'Неможливо видалити майстра, що міститься у записах, '
                                          'улюблених або у змінах графіку',
           }


def get_error_message(code):
    if code is not None:
        try:
            return message[Error(int(code))]
        except ValueError:
            pass


def get_success_message(code):
    if code is not None:
        try:
            return message[Success(int(code))]
        except ValueError:
            pass
