from flask import Flask, render_template
from forms.Register import RegisterForm

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


def main():
    app.run()


if __name__ == '__main__':
    main()