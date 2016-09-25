from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms import validators
from models import User

class LoginForm(Form):
    email = StringField("Email",
                        validators=[validators.DataRequired()])
    password = PasswordField("Password",
                             validators=[validators.DataRequired()])
    remember_me = BooleanField("Remember me?", default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False

        return True