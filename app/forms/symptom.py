from flask_wtf import FlaskForm
from wtforms import (StringField,
                     FieldList,
                     SubmitField,
                     BooleanField,
                     validators)


class SelectSymptomForm(FlaskForm):
    def get_dynamic(self, symptoms):
        class DynamicForm(FlaskForm):
            pass
        symptoms = list(filter(lambda x: x not in ('csrf_token', 'submit'), symptoms))
        for val in symptoms:
            setattr(DynamicForm, val, BooleanField(val))
        setattr(DynamicForm, 'submit', SubmitField('Лікуватися'))
        # setattr(DynamicForm, 'shadow_field', StringField(default='/my_symptom'))
        return DynamicForm()