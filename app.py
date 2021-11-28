from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy  # Подключение БД
from datetime import date, datetime

from werkzeug.utils import redirect  # Импорт функции реального времени

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ovo.db'  # Создаем БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Запускаем БД
# db.create_all()


class Contract(db.Model):  # создаем класс Договоры
    id = db.Column(db.Integer, primary_key=True)  # создаем поля
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Contract %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contracts')
def contracts():
    # Выводим все записи из БД сортируя по дате:
    contracts = Contract.query.order_by(Contract.date.desc()).all()
    # в шаблон передаем список контрактов
    return render_template("contracts.html", contracts=contracts)


@app.route('/contracts/<int:id>')
def contract_detail(id):
    # Выводим все записи из БД сортируя по дате:
    contract = Contract.query.get(id)
    # в шаблон передаем список контрактов
    return render_template("contract_detail.html", contract=contract)


@app.route('/create_contract', methods=['POST', 'GET'])
def create_contract():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        intro = request.form['intro']
        text = request.form['text']
        # Создаем объект, заполняем поля, передавая переменные
        contract = Contract(title=title, intro=intro, text=text)
        try:  # Обрабатываем ошибки
            # if title and intro and text:  # Проверка на заполненность
            db.session.add(contract)  # Добавляем объект
            db.session.commit()  # Сохраняем объект
        # Если успешно - переводим на главную страницy:
            return redirect('/contracts')
        # return "dONE"
        # else:
        # return redirect('/create_contract')
        except:  # На случай ошибки
            return "Error 1"
        # traceback.format_exc() # Код ошибки

    else:
        return render_template("create_contract.html")


# @app.route('/user/<string:name>/<int:id>')
# def user(name, id):
#     return "User page: " + name + " - " + str(id)


@app.route('/signin')
def signin():
    return render_template("signin.html")


if __name__ == "__main__":
    app.run(debug=True)
