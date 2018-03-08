from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length


class UserForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[Required(), Length(1, 128),
                    Email()],
        render_kw={"placeholder": "e-mail address"})

    password = PasswordField(
        'Password',
        validators=[Required(), Length(1, 32)],
        render_kw={"placeholder": "password"})

    remember = BooleanField('keep me logged in')

    submit = SubmitField("Sign In")
