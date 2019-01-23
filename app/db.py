import cx_Oracle
import pandas as pd


user_name = 'my_name'
password = 'my_name'
server = 'xe'


class UserPackage:
    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add_user(self, login, first_name, last_name, birthday, sex, password, doctor):
        user_login = self.__cursor.var(cx_Oracle.STRING)
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('user_package.add_user', [user_login, status, login, first_name,
                                                         last_name, birthday, sex, password, doctor])
        return user_login.getvalue(), status.getvalue()

    def update_user_first_name(self, status, login, first_name):
        self.__cursor.callproc('user_package.update_user_first_name', [status, login, first_name])

    def update_user_last_name(self, status, login, last_name):
        self.__cursor.callproc('user_package.update_user_last_name', [status, login, last_name])

    def update_user_birthday(self, status, login, birthday):
        self.__cursor.callproc('user_package.update_user_birthday', [status, login, birthday])

    def update_user_sex(self, status, login, sex):
        self.__cursor.callproc('user_package.update_user_sex', [status, login, sex])

    def update_user_doctor(self, status, login, doctor):
        self.__cursor.callproc('user_package.update_user_doctor', [status, login, doctor])

    def update_user_info_detail(self, login, first_name, last_name, birthday, sex, doctor):
        status_first_name = self.__cursor.var(cx_Oracle.STRING)
        status_last_name = self.__cursor.var(cx_Oracle.STRING)
        status_birthday = self.__cursor.var(cx_Oracle.STRING)
        status_sex = self.__cursor.var(cx_Oracle.STRING)
        status_doctor = self.__cursor.var(cx_Oracle.STRING)
        self.update_user_first_name(status_first_name, login, first_name)
        self.update_user_last_name(status_last_name, login, last_name)
        self.update_user_birthday(status_birthday, login, birthday)
        self.update_user_sex(status_sex, login, sex)
        self.update_user_doctor(status_doctor, login, doctor)
        return (status_first_name.getvalue(),
                status_last_name.getvalue(),
                status_birthday.getvalue(),
                status_sex.getvalue(),
                status_doctor.getvalue())

    def update_user_info(self, login, first_name, last_name, birthday, sex, doctor, submit):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('user_package.update_user_info', [status,
                                                                 login,
                                                                 first_name,
                                                                 last_name,
                                                                 birthday,
                                                                 sex,
                                                                 doctor,
                                                                 submit])
        return status.getvalue()

    def update_user_submit(self, login, submit):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('user_package.update_user_submit', [status, login, submit])
        return status.getvalue()

    def del_user(self, login):
        self.__cursor.callproc('user_package.del_user', [login])

    def login_user(self, login, password):
        sql = "SELECT user_package.LOGIN_USER('{}', '{}') FROM dual".format(login, password)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def its_doctor(self, login):
        sql = "SELECT doctor from user_info where login = '{}'".format(login)
        res = pd.read_sql_query(sql, self.__db)
        return res['DOCTOR'][0]

    def its_submited(self, login):
        sql = "SELECT submited from user_info where login = '{}'".format(login)
        res = pd.read_sql_query(sql, self.__db)
        return res['SUBMITED'][0]

    def get_user_info(self, login):
        sql = "SELECT * FROM TABLE(user_package.get_user_info('{}'))".format(login)
        res = pd.read_sql_query(sql, self.__db)
        return res


class SymptomPackage:
    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add(self, sym_name, sym_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('symptom_package.add_symptom', [status, sym_name, sym_desc])
        return status.getvalue()

    def update(self, sym_name, sym_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('symptom_package.update_symptom', [status, sym_name, sym_desc])
        return status.getvalue()

    def delete(self, sym_name):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('symptom_package.del_symptom', [status, sym_name])
        return status.getvalue()

    def get_symptom(self, sym_name):
        sql = "SELECT * FROM TABLE(symptom_package.get_symptom('{}'))".format(sym_name)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def get_number_symptoms(self, limit=25):
        sql =  "SELECT * FROM TABLE(symptom_package.get_symptoms({}))".format(limit)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def get_all_names(self):
        sql = "SELECT SYM_NAME FROM SYMPTOM_VIEW"
        res = pd.read_sql_query(sql, self.__db)
        return res


class MdsPackage:
    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add(self, name1, name2, table_name1, table_name2):
        mds_dis = None
        mds_sym = None
        mds_med = None
        if table_name1 == 'medicine':
            mds_med = name1
        else:
            mds_sym = name1
        if table_name2 == 'disease':
            mds_dis = name2
        else:
            mds_sym = name2
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('mds_package.add_mds', [status, mds_dis, mds_sym, mds_med])
        return status.getvalue()

    def update_mds_dis(self, mds_date, mds_dis):
        self.__cursor.callproc('mds_package.update_mdsdesease', [mds_date, mds_dis])

    def update_mds_med(self, mds_date, mds_med):
        self.__cursor.callproc('mds_package.update_mdsmedicine', [mds_date, mds_med])

    def update_mds_sym(self, mds_date, mds_sym):
        self.__cursor.callproc('mds_package.update_mdssymptom', [mds_date, mds_sym])

    def del_mds(self, mds_date):
        self.__cursor.callproc('mds_package.del_mds', [mds_date])

    def get_all_user_mds(self, mds_date):
        sql = "SELECT * FROM TABLE(mds_package.get_mds('{}'))".format(mds_date)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def get_medication_list(self, symptom):
        sql = "SELECT * FROM TABLE(mds_package.get_medication_list('{}'))".format(symptom)
        medication = pd.read_sql_query(sql, self.__db)
        return medication

    def get_medication_list_by_dis(self, dis):
        sql = "SELECT * FROM TABLE(mds_package.get_medication_list_by_dis('{}'))".format(dis)
        print(sql)
        medication = pd.read_sql_query(sql, self.__db)
        print(medication)
        return medication

    def get_disease_list(self, symptom):
        sql = "SELECT * FROM TABLE(mds_package.get_disease_list('{}'))".format(symptom)
        disease = pd.read_sql_query(sql, self.__db)
        return disease

    def get_names(self, table_name1, table_name2):
        sql1 = 'SELECT * FROM {}'.format(table_name1 + '_view')
        sql2 = 'SELECT * FROM {}'.format(table_name2 + '_view')
        table1 = pd.read_sql_query(sql1, self.__db)
        table2 = pd.read_sql_query(sql2, self.__db)

        names1 = table1.iloc[:, 0]
        names2 = table2.iloc[:, 0]
        return names1, names2


class DiseasePackage:
    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add(self, dis_name, dis_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('DESEASE_PACKAGE.add_desease', [status, dis_name, dis_desc])
        return status.getvalue()

    def update(self, dis_name, dis_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('desease_package.update_desease', [status, dis_name, dis_desc])
        return status.getvalue()

    def delete(self, dis_name):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('desease_package.del_desease', [status, dis_name])
        return status.getvalue()

    def get_disease(self, dis_name):
        sql = "SELECT * FROM TABLE(desease_package.get_desease('{}'))".format(dis_name)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def get_all_names(self):
        sql = "SELECT DIS_NAME FROM DISEASE_VIEW"
        res = pd.read_sql_query(sql, self.__db)
        return res


class MedicinePackage:
    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add(self, med_name, med_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('medicine_package.add_medicine', [status, med_name, med_desc])
        return status.getvalue()

    def update(self, med_name, med_desc):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('medicine_package.update_medicine', [status, med_name, med_desc])
        return status.getvalue()

    def delete(self, med_name):
        status = self.__cursor.var(cx_Oracle.STRING)
        self.__cursor.callproc('medicine_package.del_medicine', [status, med_name])
        return status.getvalue()

    def get_medicine(self, med_name):
        sql = "SELECT * FROM TABLE(medicine_package.get_medicine('{}'))".format(med_name)
        res = pd.read_sql_query(sql, self.__db)
        return res

    def get_all_names(self):
        sql = "SELECT MED_NAME FROM MEDICINE_VIEW"
        res = pd.read_sql_query(sql, self.__db)
        return res


class CardPackage:

    def __init__(self):
        self.__db = cx_Oracle.connect(user_name, password, server)
        self.__cursor = self.__db.cursor()

    def add(self, card_number, user_login):
        status = self.__cursor.var(cx_Oracle.STRING)
        try:
            card_number = int(card_number)
        except ValueError:
            card_number = -1
        self.__cursor.callproc('card_package.card_add_card', [status, card_number, user_login])
        return status.getvalue()

    def update_user(self, card_number, user_login):
        self.__cursor.callproc('card_package.card_update_user_login', [card_number, user_login])

    def delete_card(self, card_number):
        self.__cursor.callproc('card_package.card_delete', [card_number])

    def get_all_user_card(self, user_login):
        sql = "SELECT * FROM TABLE(card_package.get_all_user_card('{}'))".format(user_login)
        res = pd.read_sql_query(sql, self.__db)
        return res
