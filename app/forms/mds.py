from flask_wtf import FlaskForm
from wtforms import (StringField,
                     DateField,
                     RadioField,
                     SubmitField,
                     BooleanField,
                     SelectField,
                     validators)


class AddMdsForm(FlaskForm):
    def get_form(self, names1, names2):
        class DynamicForm(FlaskForm):
            name1 = SelectField('Назва першого об\'єкта: ', choices=[(name_field, name_field) for name_field in names1])
            name2 = SelectField('Назва другого об\'єкта: ', choices=[(name_field, name_field) for name_field in names2])
        setattr(DynamicForm, 'submit', SubmitField('Додати'))
        return DynamicForm()