from datetime import datetime, timedelta
import json

import pandas as pd
import plotly
import plotly.graph_objs as go
from flask import render_template, request, session, redirect, url_for, make_response
import cx_Oracle

from app.forms.user import LoginForm, RegistrationForm, UpdateUserForm
from app.forms.symptom import SelectSymptomForm
from app.forms.card import SelectCardForm, AddCard
from app.forms.action import AddForm, UpdateForm, DeleteForm
from app.forms.mds import AddMdsForm
from app.db import UserPackage, SymptomPackage, MdsPackage, CardPackage, DiseasePackage, MedicinePackage
from app import app


user_name = 'my_name'
password = 'my_name'
server = 'xe'

table_map = {
    'disease_view': 'Хвороби',
    'medicine_view': 'Ліки',
    'symptom_view': 'Симптоми',
    'mds_view': 'ЛікиХворобиСимптоми'
}

package_map = {
    'disease_view': DiseasePackage(),
    'medicine_view': MedicinePackage(),
    'symptom_view': SymptomPackage(),
    'mds_view': MdsPackage()
}


@app.route('/')
def index():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    if user_login:
        return render_template('index.html', user_login=user_login,  user=user)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        user_login = session.get('login') or request.cookies.get('login')
        if user_login:
            return redirect('/')
        return render_template('login.html', form=form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            user = UserPackage()
            login_res = user.login_user(request.form['login'], request.form['password']).values[0, 0]
            if login_res == 1:
                response = make_response(redirect('/'))
                session['login'] = request.form['login']
                if request.form.get('remember_me'):
                    expires = datetime.now() + timedelta(days=60)
                    response.set_cookie('login', request.form['login'], expires=expires)
                session['login'] = request.form['login']
                return response
            elif login_res == 0:
                return render_template('login.html', form=form, problem='Невірний пароль або логін')
            else:
                return render_template('login.html', form=form, problem='А вто тут прям помилка')


@app.route('/logout')
def logout():
    if request.method == 'GET':
        response = make_response(redirect('/login'))
        response.set_cookie('login', '', expires=0)
        session['login'] = None
        return response


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('registration.html', form=form)
        else:
            user = UserPackage()
            if request.form['password'] == request.form['password_repeat']:
                user_login, status = user.add_user(
                    request.form['login'],
                    request.form['first_name'],
                    request.form['last_name'],
                    datetime.strptime(request.form['birth_day'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                    request.form['sex'],
                    request.form['password'],
                    request.form['doctor']
                )
                if status == 'ok':
                    session['login'] = user_login
                    return redirect('/')
                else:
                    problem = 'Користувач з таким іменем уже існує'
                    problem = problem if status == problem else 'Поля можуть містити лиш букви, числа та симовол "_"'
                    return render_template('registration.html', form=form, problem=problem)
            else:
                return render_template('registration.html', form=form, problem='Повторний пароль невірний')
    return render_template('registration.html', form=form)


@app.route('/my_page', methods=['GET', 'POST'])
def my_page():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    table = user.get_user_info(user_login)
    form = UpdateUserForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('my_page.html', table=table, form=form, user_login=user_login,  user=user)
        status = user.update_user_info(
            user_login,
            request.form['first_name'],
            request.form['last_name'],
            datetime.strptime(request.form['birth_day'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
            request.form['sex'],
            request.form['doctor'],
            request.form['subscript']
        )
        if status == 'ok':
            table = user.get_user_info(user_login)
        else:
            return render_template('my_page.html', table=table, form=form,
                                   problem='Поля можуть містити лиш букви, числа та симовол "_"',
                                   user_login=user_login, user=user)
    return render_template('my_page.html', table=table, form=form,  user_login=user_login,  user=user)


@app.route('/<next_page>/my_symptoms', methods=['GET', 'POST'])
def my_symptoms(next_page):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    symptom = SymptomPackage()
    table = symptom.get_number_symptoms()
    form = SelectSymptomForm().get_dynamic(table.SYMANME)
    return render_template('my_symptoms.html',  form=form, next_page=next_page, user_login=user_login,  user=user)


@app.route('/medication_advice', methods=['GET', 'POST'])
def medication_advice():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    symptoms = list(filter(lambda x: x not in ('csrf_token', 'submit'), request.form))
    mds = MdsPackage()
    medication = []
    symptom_map = []
    for symptom in symptoms:
        med_from_sym = list(mds.get_medication_list(symptom).TYPE_MDS_MED_NAME)
        medication += med_from_sym
        symptom_map += [symptom for i in range(len(med_from_sym))]
    med_res = pd.DataFrame({'symptom': symptom_map, 'medication': medication})
    return render_template('medication_advice.html', med_res=med_res,  user_login=user_login,  user=user)


@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    card = CardPackage()
    card_numbers = list(card.get_all_user_card(user_login).CARDNUMBER)
    form = SelectCardForm().get_dynamic(card_numbers) if card_numbers else None
    if request.method == 'POST':
        status = user.update_user_submit(user_login, '1' if request.form['card'] else '0')
        if status == 'ok':
            return redirect('/possible_illnesses/my_symptoms')
    return render_template('subscription.html', user_login=user_login, user=user, form=form)


@app.route('/possible_illnesses', methods=['GET', 'POST'])
def possible_illnesses():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    symptoms = list(filter(lambda x: x not in ('csrf_token', 'submit'), request.form))

    mds = MdsPackage()
    disease = []
    symptom_map = []
    for symptom in symptoms:
        dis_from_sym = list(mds.get_disease_list(symptom).TYPE_MDS_DIS_NAME)
        disease += dis_from_sym
        symptom_map += [symptom for i in range(len(dis_from_sym))]
    dis_res = pd.DataFrame({'symptom': symptom_map, 'disease': disease})

    return render_template('possible_illnesses.html', user_login=user_login, user=user, dis_res=dis_res)


@app.route('/individual/<dis_name>', methods=['GET', 'POST'])
def individual(dis_name):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    mds = MdsPackage()

    medication = mds.get_medication_list_by_dis(dis_name).TYPE_MDS_MED_NAME
    return render_template('individual.html', user_login=user_login, user=user, medication=medication)


@app.route('/table/<table_name>')
def table_action(table_name):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    connect = cx_Oracle.connect(user_name, password, server)
    sql = "SELECT * from {}".format(table_name)
    table = pd.read_sql_query(sql, connect)
    return render_template('table_action.html',
                           user_login=user_login,
                           user=user,
                           table_name=table_name,
                           table_nameuk=table_map[table_name],
                           table=table.to_html(classes='table table-striped'))


@app.route('/table/add/<table_name>', methods=['GET', 'POST'])
def add(table_name):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    form = AddForm()
    problem = None
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            package = package_map[table_name]
            status = package.add(request.form['name'], request.form['desc'])
            print(status)
            if status == 'ok':
                return redirect(url_for('table_action', table_name=table_name))
            else:
                problem = 'Така назва уже існує'
                problem = problem if status == problem else 'Поля можуть містити лиш букви, числа та симовол "_"'
    return render_template('add_to_table.html',
                           user_login=user_login,
                           user=user,
                           table_name=table_name,
                           table_nameuk=table_map[table_name],
                           form=form,
                           problem=problem)


@app.route('/table/update/<table_name>', methods=['GET', 'POST'])
def update(table_name):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    package = package_map[table_name]
    names = package.get_all_names().iloc[:, 0].values
    form = UpdateForm().get_form(names)
    problem = None
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            print(request.form['name'], request.form['desc'])
            status = package.update(request.form['name'], request.form['desc'])
            print(status)
            if status == 'ok':
                return redirect(url_for('table_action', table_name=table_name))
            else:
                problem = 'Поля можуть містити лиш букви, числа та симовол "_"'
    return render_template('update_table.html',
                           user_login=user_login,
                           user=user,
                           table_name=table_name,
                           table_nameuk=table_map[table_name],
                           form=form,
                           problem=problem)


@app.route('/table/delete/<table_name>', methods=['GET', 'POST'])
def delete(table_name):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    package = package_map[table_name]
    names = package.get_all_names().iloc[:, 0].values
    form = DeleteForm().get_form(names)
    problem = None
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            print(request.form['name'])
            status = package.delete(request.form['name'])
            print(status)
            if status == 'ok':
                return redirect(url_for('table_action', table_name=table_name))
            else:
                problem = 'Оберіть назву з випадаючого списка'
    return render_template('delete_table.html',
                           user_login=user_login,
                           user=user,
                           table_name=table_name,
                           table_nameuk=table_map[table_name],
                           form=form,
                           problem=problem)


@app.route('/mds_view')
def mds_view_table():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    sql = 'SELECT * FROM MDS_VIEW'
    connect = cx_Oracle.connect(user_name, password, server)
    table = pd.read_sql_query(sql, connect).to_html(classes='table table-striped')
    return render_template('mds_view.html',
                           user_login=user_login,
                           user=user,
                           table=table)


@app.route('/mds_view/add/<conection_type>', methods=['GET', 'POST'])
def add_mds(conection_type):
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    table_name1, table_name2 = conection_type.split('_')
    package = MdsPackage()
    names1, names2 = package.get_names(table_name1, table_name2)
    print(names1, names2)
    problem = None
    form = AddMdsForm().get_form(names1, names2)
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            status = package.add(request.form['name1'],
                                 request.form['name2'], table_name1, table_name2)
            print(status)
            if status == 'ok':
                return redirect('mds_view')
            else:
                problem = 'З випадаючих списків необхідно обрати відповідні атрибути'
    return render_template('add_mds.html',
                           user_login=user_login,
                           user=user,
                           form=form,
                           problem=problem,
                           conection_type=conection_type)


@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()
    package = CardPackage()
    form = AddCard()
    problem = None
    if request.method == 'POST':
        if not form.validate():
            pass
        else:
            status = package.add(request.form['number'],
                                 user_login)
            print(status)
            if status == 'ok':
                return redirect('subscription')
            else:
                problem = 'Така назва уже існує'
                problem = problem if status == problem else 'Поле може містити числа '
    return render_template('add_card.html',
                           user_login=user_login,
                           user=user,
                           form=form,
                           problem=problem)


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    user_login = session.get('login') or request.cookies.get('login')
    user = UserPackage()

    connect = cx_Oracle.connect(user_name, password, server)
    sql = "SELECT * from {}".format('DISEASE_VIEW')
    disease = pd.read_sql_query(sql, connect)

    sql = "SELECT * from {}".format('MEDICINE_VIEW')
    medicine = pd.read_sql_query(sql, connect)

    sql = "SELECT * from {}".format('SYMPTOM_VIEW')
    symptom = pd.read_sql_query(sql, connect)

    hist_1 = go.Histogram(
        x=disease.DIS_NAME.apply(len)
    )
    hist_2 = go.Histogram(
        x=medicine.MED_NAME.apply(len)
    )
    hist_3 = go.Histogram(
        x=symptom.SYM_NAME.apply(len)
    )

    data = [hist_1, hist_2, hist_3]
    ids = [1, 2, 3]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('statistics.html', user_login=user_login, user=user, graphJSON=graphJSON, ids=ids)
