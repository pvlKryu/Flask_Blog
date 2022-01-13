from flask import Flask, render_template, url_for, request, redirect
#from config import Configuration
from flask_sqlalchemy import SQLAlchemy  # Подключение БД
from flask_migrate import Migrate
from datetime import date, datetime

from werkzeug.utils import redirect  # Импорт функции реального времени
from sqlalchemy import func, text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ovo.db'  # Создаем БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Запускаем БД
# db.create_all()

# Миграция для обновления БД (система контроля версий БД)
migrate = Migrate(app, db)


class Contract(db.Model):  # создаем класс Договоры
    contract_id = db.Column(db.Integer, primary_key=True)  # создаем поля

    #object_id = db.Column(db.Integer)
    #client_id = db.Column(db.Integer)
    #worker_id = db.Column(db.Integer)

    title = db.Column(db.String(100), nullable=False)
    # ответственное лицо клиента
    client_person = db.Column(db.String(100), nullable=False)
    object_adres = db.Column(db.String(100), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)  # имя клиента
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    type_service = db.Column(db.Integer, nullable=False)  # тип услуги
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):  # По запросу будет выдаваться объект + ID
        return '<Contract %r>' % self.id


class Act(db.Model):  # создаем класс Акты проверок
    act_id = db.Column(db.Integer, primary_key=True)  # создаем поля
    #contract_id = db.Column(db.Integer)
    #worker_id = db.Column(db.Integer)
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
    person = db.Column(db.String(100), nullable=False)

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
            q) | Contract.contract_id.contains(q) | Contract.client_name.contains(q) | Contract.type_service.contains(q) | Contract.object_adres.contains(q) | Contract.intro.contains(q)).all()
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
            q) | Act.act_id.contains(q) | Contract.contract_id.contains(q) | Act.status.contains(q) | Act.object_adress.contains(q)).all()
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
    return render_template("contract_detail_new.html", contract=contract)


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
    return render_template("act_detail_new.html", act=act)


@app.route('/create_contract', methods=['POST', 'GET'])
def create_contract():
    if request.method == "POST":
        title = request.form['title']  # Заполняем поля из формы
        intro = request.form['intro']
        text = request.form['text']
        cost = request.form['cost']
        client_name = request.form['client_name']
        type_service = request.form['type_service']
        client_person = request.form['client_person']
        object_adres = request.form['object_adres']

        # Создаем объект, заполняем поля, передавая переменные
        contract = Contract(title=title, intro=intro, text=text, cost=cost, client_name=client_name,
                            type_service=type_service, client_person=client_person, object_adres=object_adres)
        try:  # Обрабатываем ошибки
            if title and intro and text and cost and client_name and type_service and client_person and object_adres:  # Проверка на заполненность
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
        contract.client_name = request.form['client_name']
        contract.type_service = request.form['type_service']
        contract.client_person = request.form['client_person']
        contract.object_adres = request.form['object_adres']

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


@app.route('/law')
def law():
    return render_template("law.html")


@app.route('/rules')
def rules():
    return render_template("rules.html")


@app.route('/price')
def price():
    return render_template("price.html")


@app.route('/director_report')
def director_report():
    contract_amount = Contract.query.count()  # число новых договоров
    contract_sum = Contract.query.with_entities(
        func.sum(Contract.cost).label('total')).first().total  # доход по договорам
    act_amount = Act.query.count()  # число проверок
    #fake_act_amount = Act.query.filter_by(status='ложный').all().count

    fake_act_amount = db.session.query(Act.status).filter(
        Act.status == 'Ложный').count()  # число ложных вызовов
    real_act_amount = act_amount - fake_act_amount  # число реальных вызовов
    now = datetime.now().date()  # текущая дата
    return render_template("director_report.html", contract_amount=contract_amount, contract_sum=contract_sum, act_amount=act_amount, fake_act_amount=fake_act_amount, real_act_amount=real_act_amount, now=now)


@app.route('/client_report')
def client_report():
    q = request.args.get('q')

    if q:
        act_amount = Act.query.filter(Act.contract_number.contains(q)).count()
        fake_act_amount = Act.query.filter(Act.contract_number.contains(q)).filter(
            Act.status == 'Ложный').count()
        real_act_amount = act_amount - fake_act_amount  # число реальных вызовов
        contract_sum = Act.query.filter(Contract.contract_id.contains(q)).with_entities(
            func.sum(Contract.cost).label('total')).first().total
        now = datetime.now().date()  # текущая дата
        return render_template("client_report.html", now=now, act_amount=act_amount, fake_act_amount=fake_act_amount, real_act_amount=real_act_amount, contract_sum=contract_sum)
    else:
        return render_template("client_report.html")
    #     # Выводим все записи из БД сортируя по дате:
    #     acts = Act.query.order_by(Act.date.desc()).all()
    #     # в шаблон передаем список контрактов


# def inject_now():
#     return {'now': datetime.utcnow()}
# @app.route('/user/<username>')
# def show_user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('show_user.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)
