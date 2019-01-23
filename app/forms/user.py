from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     DateField,
                     RadioField,
                     SubmitField,
                     BooleanField,
                     SelectField,
                     validators)


class LoginForm(FlaskForm):
    login = StringField('Логін: ', validators=[
        validators.DataRequired('Введіть Ваш логін')])
    password = PasswordField('Пароль: ', validators=[
        validators.DataRequired('Введіть Ваш пароль')])
    remember_me = BooleanField("Запам'ятай мене")
    submit = SubmitField('Увійти')


class RegistrationForm(FlaskForm):
    login = StringField('Логін:', validators=[
        validators.DataRequired('Введіть Ваш логін'),
        validators.Length(min=5, max=30, message='Допустима кількість символів для лігіна між 5 та 30')])
    password = PasswordField('Пароль:', validators=[
        validators.DataRequired('Введіть Ваш пароль'),
        validators.Length(min=5, max=30, message='Допустима кількість символів пароля між 5 та 30')])
    password_repeat = PasswordField('Повторіть пароль:', validators=[
        validators.DataRequired('Повторіть Ваш пароль')])
    first_name = StringField('Ім\'я:', validators=[
        validators.DataRequired('Введіть Ваше Ім\'я'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в імені між 5 та 30')])
    last_name = StringField('Прізвище:', validators=[
        validators.DataRequired('Введіть Ваше Прізвище'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в прізвищі між 5 та 30')])
    birth_day = DateField('Дата народження (рік-місяць-день):', format='%Y-%m-%d', validators=[
        validators.DataRequired('Введіть Вашу Дату народження у форматі (рік-місяць-день):')
    ])
    sex = RadioField('Стать:', choices=[
        ('1', 'Чоловік'),
        ('0', 'Жінка')
    ], default='1')
    doctor = RadioField('Оберіть вашу роль:', choices=[
        ('0', 'Пацієнт'),
        ('1', 'Доктор')
    ], default='0')
    registration = SubmitField('Зареєструватися')


class UpdateUserForm(FlaskForm):
    first_name = StringField('Ім\'я:', validators=[
        validators.DataRequired('Введіть Ваше Ім\'я'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в імені між 5 та 30')])
    last_name = StringField('Прізвище:', validators=[
        validators.DataRequired('Введіть Ваше Прізвище'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в прізвищі між 5 та 30')])
    birth_day = DateField('Дата народження (рік-місяць-день):', format='%Y-%m-%d', validators=[
        validators.DataRequired('Введіть Вашу Дату народження у форматі (рік-місяць-день):')
    ])
    sex = SelectField('Стать:', choices=[
        ('1', 'Чоловік'),
        ('0', 'Жінка')
    ])
    doctor = SelectField('Оберіть вашу роль:', choices=[
        ('1', 'Доктор'),
        ('0', 'Пацієнт')
    ])
    subscript = SelectField('Оберіть чи ви підписані:', choices=[
        ('1', 'Так'),
        ('0', 'Ні')
    ])
    submit = SubmitField('Оновити')
