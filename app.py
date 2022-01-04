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
    contract_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    object_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    worker_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Contract %r>' % self.id


class Act(db.Model):  # создаем класс Акты проверок
    act_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    contract_id = db.Column(db.Integer)
    worker_id = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    contract_number = db.Column(db.String(100), nullable=False)
    object_adress = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Act %r>' % self.id


class Client(db.Model):  # создаем класс Клиент
    client_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    name = db.Column(db.String(100), nullable=False)
    client_person = db.Column(db.String(100), nullable=False)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Client %r>' % self.id


class Worker(db.Model):  # создаем класс Сотрудник
    worker_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Worker %r>' % self.id


class Object(db.Model):  # создаем класс Объект
    object_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    id_contract = db.Column(db.Integer, nullable=False)
    adress = db.Column(db.String(300), nullable=False)
    rooms_amount = db.Column(db.Integer, nullable=False)
    entries_amount = db.Column(db.Integer, nullable=False)
    windows_amount = db.Column(db.Integer, nullable=False)
    people_object = db.Column(db.String(300), nullable=False)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Object %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contracts')
def contracts():

    q = request.args.get('q')

    if q:
        contracts = Contract.query.filter(Contract.title.contains(q) | Contract.text.contains(
            q) | Contract.contract_id.contains(q) | Contract.intro.contains(q)).all()
    else:
        # Выводим все записи из БД сортируя по дате:
        contracts = Contract.query.order_by(Contract.date.desc()).all()
        # в шаблон передаем список контрактов
    return render_template("contracts.html", contracts=contracts)


@app.route('/acts')
def acts():

    q = request.args.get('q')

    if q:
        acts = Act.query.filter(Act.title.contains(q) | Act.text.contains(
            q) | Act.act_id.contains(q) | Act.status.contains(q) | Act.object_adress.contains(q)).all()
    else:
        # Выводим все записи из БД сортируя по дате:
        acts = Act.query.order_by(Act.date.desc()).all()
        # в шаблон передаем список контрактов
    return render_template("acts.html", acts=acts)


@app.route('/contracts/<int:contract_id>')
def contract_detail(contract_id):

    # Выводим все записи из БД сортируя по дате:
    contract = Contract.query.get(contract_id)
    # в шаблон передаем список контрактов
    return render_template("contract_detail.html", contract=contract)


@app.route('/contracts/<int:contract_id>/del')
def contract_delet(contract_id):
    # Ищем нужную запись в БД:
    contract = Contract.query.get_or_404(contract_id)

    try:
        db.session.delete(contract)
        db.session.commit()
        return redirect('/contracts')
    except:  # На случай ошибки
        return "При удалении статьи произошла ошибка"


@app.route('/acts/<int:act_id>/del')
def act_delet(act_id):
    # Ищем нужную запись в БД:
    act = Act.query.get_or_404(act_id)

    try:
        db.session.delete(act)
        db.session.commit()
        return redirect('/acts')
    except:  # На случай ошибки
        return "При удалении статьи произошла ошибка"


@app.route('/acts/<int:act_id>')
def act_detail(act_id):

    # Выводим все записи из БД сортируя по дате:
    act = Act.query.get(act_id)
    # в шаблон передаем список контрактов
    return render_template("act_detail.html", act=act)


@app.route('/create_contract', methods=['POST', 'GET'])
def create_contract():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        intro = request.form['intro']
        text = request.form['text']
        cost = request.form['cost']

        # Создаем объект, заполняем поля, передавая переменные
        contract = Contract(title=title, intro=intro, text=text, cost=cost)
        try:  # Обрабатываем ошибки
            if title and intro and text and cost:  # Проверка на заполненность
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


@app.route('/contracts/<int:contract_id>/update', methods=['POST', 'GET'])
def contracts_update(contract_id):
    contract = Contract.query.get(contract_id)  # Ищем объект
    if request.method == "POST":
        contract.title = request.form['title']  # Заполняем поля из формы
        contract.intro = request.form['intro']
        contract.text = request.form['text']
        contract.cost = request.form['cost']

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
        except:  # На случай ошибки
            return render_template("create_act.html")
        # traceback.format_exc() # Код ошибки

    else:
        return render_template("create_act.html")


@app.route('/acts/<int:act_id>/update', methods=['POST', 'GET'])
def acts_update(act_id):
    act = Act.query.get(act_id)  # Ищем объект
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


# @app.route('/director_report')
# def director_report():

#     return render_template("director_report.html")


if __name__ == "__main__":
    app.run(debug=True)
