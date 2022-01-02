from flask import Flask, render_template, url_for, request, redirect, flash
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


class Act(db.Model):  # создаем класс Акты проверок
    id = db.Column(db.Integer, primary_key=True)  # создаем поля
    title = db.Column(db.String(100), nullable=False)
    contract_number = db.Column(db.String(100), nullable=False)
    object_adress = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Act %r>' % self.id


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


@app.route('/acts')
def acts():
    # Выводим все записи из БД сортируя по дате:
    acts = Act.query.order_by(Act.date.desc()).all()
    # в шаблон передаем список контрактов
    return render_template("acts.html", acts=acts)


@app.route('/contracts/<int:id>')
def contract_detail(id):
    # Выводим все записи из БД сортируя по дате:
    contract = Contract.query.get(id)
    # в шаблон передаем список контрактов
    return render_template("contract_detail.html", contract=contract)


@app.route('/contracts/<int:id>/del')
def contract_delet(id):
    # Ищем нужную запись в БД:
    contract = Contract.query.get_or_404(id)

    try:
        db.session.delete(contract)
        db.session.commit()
        return redirect('/contracts')
    except:  # На случай ошибки
        return "При удалении статьи произошла ошибка"


@app.route('/acts/<int:id>/del')
def act_delet(id):
    # Ищем нужную запись в БД:
    act = Act.query.get_or_404(id)

    try:
        db.session.delete(act)
        db.session.commit()
        return redirect('/acts')
    except:  # На случай ошибки
        return "При удалении статьи произошла ошибка"


@app.route('/acts/<int:id>')
def act_detail(id):
    # Выводим все записи из БД сортируя по дате:
    act = Act.query.get(id)
    # в шаблон передаем список контрактов
    return render_template("act_detail.html", act=act)


@app.route('/create_contract', methods=['POST', 'GET'])
def create_contract():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        intro = request.form['intro']
        text = request.form['text']

        # Создаем объект, заполняем поля, передавая переменные
        contract = Contract(title=title, intro=intro, text=text)
        try:  # Обрабатываем ошибки
            if title and intro and text:  # Проверка на заполненность
                db.session.add(contract)  # Добавляем объект
                db.session.commit()  # Сохраняем объект
                # Если успешно - переводим на главную страницy:
                return redirect('/contracts')
            else:
                return "Заполните все поля"

        except:  # На случай ошибки
            return render_template("create_contract.html")
        # traceback.format_exc() # Код ошибки

    else:
        return render_template("create_contract.html")


@app.route('/contracts/<int:id>/update', methods=['POST', 'GET'])
def contracts_update(id):
    contract = Contract.query.get(id)  # Ищем объект
    if request.method == "POST":
        contract.title = request.form['title']  # Заполняем поля из формы
        contract.intro = request.form['intro']
        contract.text = request.form['text']

        try:  # Обрабатываем ошибки
            db.session.commit()  # Сохраняем объект
            return redirect('/contracts')
        except:  # На случай ошибки
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("contract_update.html", contract=contract)


@app.route('/create_act', methods=['POST', 'GET'])
def create_act():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        contract_number = request.form['contract_number']
        object_adress = request.form['object_adress']
        status = request.form['status']
        text = request.form['text']
        # Создаем объект, заполняем поля, передавая переменные
        act = Act(title=title, contract_number=contract_number,
                  object_adress=object_adress, status=status, text=text)
        try:  # Обрабатываем ошибки
            if title and contract_number and object_adress and status and text:  # Проверка на заполненность
                # if title and intro and text:  # Проверка на заполненность
                db.session.add(act)  # Добавляем объект
                db.session.commit()  # Сохраняем объект
                # Если успешно - переводим на главную страницy:
                return redirect('/acts')
            else:
                return "Заполните все поля"
        # return "dONE"
        # else:
        # return redirect('/create_contract')
        except:  # На случай ошибки
            return render_template("create_act.html")
        # traceback.format_exc() # Код ошибки

    else:
        return render_template("create_act.html")


@app.route('/acts/<int:id>/update', methods=['POST', 'GET'])
def acts_update(id):
    act = Act.query.get(id)  # Ищем объект
    if request.method == "POST":
        act.title = request.form['title']  # Заполняем поля из формы
        act.contract_number = request.form['contract_number']
        act.object_adress = request.form['object_adress']
        act.status = request.form['status']
        act.text = request.form['text']
        try:  # Обрабатываем ошибки
            db.session.commit()  # Сохраняем объект
            return redirect('/acts')
        except:  # На случай ошибки
            return "При редактировании актп проверки произошла ошибка"
    else:
        return render_template("act_update.html", act=act)


@app.route('/signin')
def signin():
    return render_template("signin.html")


if __name__ == "__main__":
    app.run(debug=True)
