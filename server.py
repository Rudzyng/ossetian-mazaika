from flask import Flask, render_template
from forms.RegisterForm import RegisterForm
from forms.LoginForm import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Авторизация', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()