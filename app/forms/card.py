from flask_wtf import FlaskForm
from wtforms import (StringField,
                     FieldList,
                     SubmitField,
                     BooleanField,
                     RadioField,
                     SelectField,
                     IntegerField,
                     validators)


class SelectCardForm(FlaskForm):
    def get_dynamic(self, names):
        class DynamicForm(FlaskForm):
            card = SelectField('Карта: ', choices=[(name_field, name_field) for name_field in names])
        setattr(DynamicForm, 'submit', SubmitField('Підписатися'))
        return DynamicForm()


class AddCard(FlaskForm):
    number = StringField('Номер карти: ', validators=[
        validators.Length(message='Максимальна кількість чисел - 8', min=1, max=8)])
    submit = SubmitField('Додати')
