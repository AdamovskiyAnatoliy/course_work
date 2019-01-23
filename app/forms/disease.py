from flask_wtf import FlaskForm
from wtforms import (StringField,
                     FieldList,
                     SubmitField,
                     BooleanField,
                     RadioField,
                     validators)


class SelectDiseaseForm(FlaskForm):
    def get_dynamic(self, diseases):
        class DynamicForm(FlaskForm):
            disease = RadioField('Хвороба: ',
                                 choices=[(str(inx), dis_name) for inx, dis_name in enumerate(diseases)],
                                 default='0')
        setattr(DynamicForm, 'submit', SubmitField('Індивідуальне лікування'))
        return DynamicForm()
