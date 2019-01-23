from flask_wtf import FlaskForm
from wtforms import (StringField,
                     DateField,
                     RadioField,
                     SubmitField,
                     BooleanField,
                     SelectField,
                     validators)


class AddForm(FlaskForm):
    name = StringField('Назва:', validators=[
        validators.DataRequired('Введіть назву'),
        validators.Length(min=5, max=30, message='Допустима кількість символів для назви між 5 та 30')])
    desc = StringField('Опис:', validators=[
        validators.DataRequired('Введіть опис')])
    submit = SubmitField('Додати')


class UpdateForm(FlaskForm):
    def get_form(self, names):
        class DynamicForm(FlaskForm):
            name = SelectField('Опис: ', choices=[(name_field, name_field) for name_field in names])
        setattr(DynamicForm, 'desc', StringField('Опис:', validators=[validators.DataRequired('Введіть опис')]))
        setattr(DynamicForm, 'submit', SubmitField('Оновити'))
        return DynamicForm()


class DeleteForm(FlaskForm):
    def get_form(self, names):
        class DynamicForm(FlaskForm):
            name = SelectField('Назва: ', choices=[(name_field, name_field) for name_field in names])
        setattr(DynamicForm, 'submit', SubmitField('Видалити'))
        return DynamicForm()
