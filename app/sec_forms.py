from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_babel import lazy_gettext
from wtforms import StringField
from wtforms.validators import DataRequired


class WehaUserInfoEdit(DynamicForm):
    emp_number = StringField(
        lazy_gettext("Emp. Number"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
        description=lazy_gettext("Employee Number"),
    )
