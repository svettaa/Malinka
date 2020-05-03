from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, \
    RadioField, HiddenField, FormField, FieldList, DateTimeField
from wtforms.validators import InputRequired, Optional, NumberRange, Regexp
from wtforms.fields.html5 import TelField, EmailField, IntegerField


class BaseForm(FlaskForm):
    pass


class NoCsrfBaseForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(NoCsrfBaseForm, self).__init__(meta={'csrf': False}, *args, **kwargs)


class AdminCategoryForm(BaseForm):
    name = StringField('Назва категорії', validators=[InputRequired('Введіть назву категорії')])


class AdminProcedureForm(BaseForm):
    category_id = SelectField('Назва категорії', validators=[InputRequired('Виберіть категорію')],
                              coerce=int)
    name = StringField('Назва процедури', validators=[InputRequired('Введіть назву процедури')])
    price_min = IntegerField('Мінімальна ціна',
                             default=100,
                             validators=[InputRequired('Введіть мінімальну ціну'),
                                         NumberRange(min=0, message='Ціна не може бути від\'ємною')])
    price_max = IntegerField('Максимальна ціна',
                             validators=[Optional(),
                                         NumberRange(min=0, message='Ціна не може бути від\'ємною')])
    info = TextAreaField('Додаткова інформація', validators=[Optional()])


class AdminPaintForm(BaseForm):
    code = StringField('Номер фарби', validators=[InputRequired('Введіть номер фарби')])
    name = StringField('Назва фарби', validators=[InputRequired('Введіть назву фарби')])
    left_ml = HiddenField('')


class AdminSupplyForm(BaseForm):
    paint_id = SelectField('Фарба', validators=[InputRequired('Виберіть фарбу')],
                           coerce=int)
    amount = IntegerField('Кількість, мл',
                          default=100,
                          validators=[InputRequired('Введіть кількість фарби'),
                                      NumberRange(min=1, message='Кількість має бути більше нуля')])
    supply_date = DateTimeField('Дата', validators=[InputRequired('Введіть дату')],
                                render_kw={'data-target': '#supply_date_datetimepicker'},
                                format='%d.%m.%Y')


class AdminClientForm(BaseForm):
    surname = StringField('Прізвище', validators=[InputRequired('Введіть прізвище')])
    first_name = StringField('Ім\'я', validators=[InputRequired('Введіть ім\'я')])
    second_name = StringField('По-батькові', validators=[Optional()])
    is_male = RadioField('Стать', validators=[InputRequired('Виберіть стать')],
                         choices=[(1, 'Чоловіча'), (0, 'Жіноча')], coerce=int)
    phone = TelField('Телефон, +38', validators=[InputRequired('Введіть телефон'),
                                            Regexp('[0-9]{10}', message='Некоректний телефон')])
    email = EmailField('Email', validators=[Optional()])


class AdminMasterProceduresForm(NoCsrfBaseForm):
    procedure_id = HiddenField('')
    procedure_name = HiddenField('')
    category_name = HiddenField('')
    duration = IntegerField('Тривалість',
                            validators=[Optional(),
                                        NumberRange(min=1, message='Тривалість має бути більше нуля')])


class AdminEditMasterForm(BaseForm):
    even_schedule = RadioField('Графік', validators=[InputRequired('Оберіть графік')],
                               choices=[(1, 'Парний'), (0, 'Непарний')], coerce=int)
    is_hired = RadioField('Статус', validators=[InputRequired('Оберіть статус')],
                          choices=[(1, 'Працює'), (0, 'Звільнено')], coerce=int)
    procedures = FieldList(FormField(AdminMasterProceduresForm))


class AdminNewMasterForm(AdminEditMasterForm):
    id = SelectField('Користувач', validators=[InputRequired('Виберіть користувача')],
                     coerce=int)


class AdminScheduleChangeForm(BaseForm):
    master_id = SelectField('Майстер', validators=[InputRequired('Виберіть майстра')],
                            coerce=int)
    change_start = DateTimeField('Початок', validators=[InputRequired('Введіть початок зміни в графіку')],
                                 render_kw={'data-target': '#change_start_datetimepicker'},
                                 format='%d.%m.%Y %H:%M')
    change_end = DateTimeField('Кінець', validators=[InputRequired('Введіть кінець зміни в графіку')],
                               render_kw={'data-target': '#change_end_datetimepicker'},
                               format='%d.%m.%Y %H:%M')
    is_working = RadioField('Працює', validators=[InputRequired('Оберіть тип зміни')],
                            choices=[(1, 'Так'), (0, 'Ні')], coerce=int)
