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
    ADDED_SCHEDULE = 19
    UPDATED_SCHEDULE = 20
    DELETED_SCHEDULE = 21
    ADDED_APPOINTMENT = 22
    UPDATED_APPOINTMENT = 23
    DELETED_APPOINTMENT = 24
    ADDED_APPOINTMENT_PAINT = 25
    UPDATED_APPOINTMENT_PAINT = 26
    DELETED_APPOINTMENT_PAINT = 27
    USER_PROFILE_UPDATED = 28


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
    SCHEDULE_INTEGRITY = 15
    SCHEDULE_DELETE_INTEGRITY = 16
    SUPPLY_INTEGRITY = 17
    APPOINTMENT_INTEGRITY = 18
    APPOINTMENT_PAINT_INTEGRITY = 19
    USER_NOT_EXISTS = 20
    PAST_APPOINTMENT_DELETION = 21


messages = {Success.ADDED_CATEGORY: 'Успішно додано категорію',
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
            Success.ADDED_SCHEDULE: 'Успішно додано зміну в графіку',
            Success.UPDATED_SCHEDULE: 'Успішно змінено зміну в графіку',
            Success.DELETED_SCHEDULE: 'Успішно видалено зміну в графіку',
            Success.ADDED_APPOINTMENT: 'Успішно додано запис',
            Success.UPDATED_APPOINTMENT: 'Успішно змінено запис',
            Success.DELETED_APPOINTMENT: 'Успішно видалено запис',
            Success.ADDED_APPOINTMENT_PAINT: 'Успішно додано фарбу до запису',
            Success.UPDATED_APPOINTMENT_PAINT: 'Успішно змінено фарбу до запису',
            Success.DELETED_APPOINTMENT_PAINT: 'Успішно видалено фарбу до запису',
            Success.USER_PROFILE_UPDATED: 'Успішно змінено дані',
            Error.CATEGORY_HAS_PROCEDURES: 'Неможливо видалити категорію, що містить процедури',
            Error.CATEGORY_NAME_EXISTS: 'Неможливо змінити або додати категорію, '
                                        'категорія з такою назваю вже існує',
            Error.PROCEDURE_NAME_EXISTS: 'Неможливо змінити або додати процедуру, '
                                         'процедура з такою назваю вже існує, '
                                         'або максимальна ціна менша за мінімальну',
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
            Error.SCHEDULE_INTEGRITY: 'Неможливо оновити зміну в графіку, можливі причини: '
                                      'Дати перетинаються з іншими змінами в графіку даного майстра, '
                                      'Існує запис в дані дати',
            Error.SCHEDULE_DELETE_INTEGRITY: 'Неможливо видалити зміну в графіку, можливі причини: '
                                             'Вже існує запис в дані дати для даного майстра',
            Error.SUPPLY_INTEGRITY: 'Неможливо видалити, недостатньо фарби',
            Error.APPOINTMENT_INTEGRITY: 'Порушення цілісності записів',
            Error.APPOINTMENT_PAINT_INTEGRITY: 'Порушення цілісності фарб запису',
            Error.USER_NOT_EXISTS: 'Користувача з таким номером телефону не існує',
            Error.PAST_APPOINTMENT_DELETION: 'Неможливо видалити минулий запис',
            }


def get_error_message(code):
    if code is not None:
        try:
            return messages[Error(int(code))]
        except ValueError:
            pass


def get_success_message(code):
    if code is not None:
        try:
            return messages[Success(int(code))]
        except ValueError:
            pass
