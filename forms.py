from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Email

csrf = CSRFProtect()


class CreateTodoList(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(min=3, max=80)])
    cover = StringField('Ссылка на обложку', validators=[DataRequired(), URL()])


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
