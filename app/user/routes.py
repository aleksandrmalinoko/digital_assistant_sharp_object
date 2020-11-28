from app.user import blueprint
from flask import render_template, request
from flask_login import login_required

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker


class Resume(object):
    def __init__(self, firstName, lastName, middleName, phone, email, tags, profile):
        self.firstName = firstName
        self.lastName = lastName
        self.middleName = middleName
        self.phone = phone
        self.email = email
        self.tags = tags
        self.profile = profile

    def __repr__(self):
        return "<Resume('%s';'%s';'%s';'%s';'%s';'%s';'%s')>" % (self.firstName, self.lastName, self.middleName,
                                                                 self.phone, self.email, self.tags, self.profile)


class Vacancy(object):
    def __init__(self, position, type, short_description, profile):
        self.position = position
        self.type = type
        self.short_description = short_description
        self.profile = profile

    def __repr__(self):
        return "<Vacancy('%s';'%s';'%s';'%s')>" % (self.position, self.type, self.short_description, self.profile)


class Database(object):
    def __init__(self, idResume, idVacancy, percent):
        self.idResume = idResume
        self.idVacancy = idVacancy
        self.percent = percent

    def __repr__(self):
        return "<Database('%s';'%s';'%d')>" % (self.idResume, self.idVacancy, self.percent)


def create_table():
    engine = create_engine('sqlite:///resume.db', echo=True)
    metadata = MetaData()

    resume_table = Table('resume', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('firstName', String),
                         Column('lastName', String),
                         Column('middleName', String),
                         Column('phone', String),
                         Column('email', String),
                         Column('tags', String),
                         Column('profile', String)
                         )

    vacancy_table = Table('vacancy', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('position', String),
                          Column('type', String),
                          Column('short_description', String),
                          Column('profile', String)
                          )

    database_table = Table('database', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('id_resume', String),
                           Column('id_vacancy', String),
                           Column('percent', Integer)
                           )

    metadata.create_all(engine)

    mapper(Resume, resume_table)
    mapper(Vacancy, vacancy_table)
    mapper(Database, database_table)

    # args = request.args
    # user = User(args['vacancy'], args['first-name'], args['last-name'], args['middle-name'], args['phone'],
    #             args['tags'], args['profile'])
    #
    # Session = sessionmaker(bind=engine)
    # Session.configure(bind=engine)
    #
    # session = Session()
    # session.add(user)
    # session.commit()


def add_vacancy():
    engine = create_engine('sqlite:///resume.db')
    metadata = MetaData()

    vacancy_table = Table('vacancy', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('position', String),
                          Column('type', String),
                          Column('short_description', String),
                          Column('profile', String)
                          )

    mapper(Vacancy, vacancy_table)
    vacancy = Vacancy(position='DevOps', type='Тестирование',
                      short_description='Необходим инженер со знанием Jenkins, Docker, Python',
                      profile='Требуемый опыт работы: 3–6 лет')

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    session = Session()
    session.add(vacancy)
    session.commit()

    session.close()
    Session.close_all()


def add_resume(data):
    id = 0
    engine = create_engine('sqlite:///resume.db')
    with engine.connect() as connect:
        connect.execute(
            "INSERT INTO resume (firstname, lastname, middlename, phone, email, tags, profile) VALUES " +
            "('{firstName}', '{lastName}', '{middleName}', '{phone}', '{email}', '{tags}', '{profile}')".format(
                firstName=data['first-name'], lastName=data['last-name'], middleName=data['middle-name'],
                phone=data['phone'], email=data['email'], tags=data['tags'], profile=data['profile']))
    id = engine.execute(
            "SELECT id FROM resume WHERE " +
            "resume.firstName='{firstName}' AND resume.lastName='{lastName}' AND resume.middleName='{middleName}' AND resume.phone='{phone}'".format(
                firstName=data['first-name'], lastName=data['last-name'], middleName=data['middle-name'], phone=data['phone']))
            # "AND " +
            # "resume.phone='{phone}' AND resume.email='{email}' AND resume.tags='{tags}' AND resume.profile='{profile}'".format(
            #     , email=data['email'], tags=data['tags'], profile=data['profile']))
    for i in id:
        print(i)
    add_database(data['vacancy'], id)


def add_database(vacancy, id_res):
    engine = create_engine('sqlite:///resume.db')
    id_vac = 0
    with engine.connect() as connect:
        pos = vacancy[:vacancy.find("(") - 1]
        vac = vacancy[vacancy.find("(") + 1:-1]
        id_vac = connect.execute("SELECT id FROM vacancy WHERE position='{pos}' AND type='{vac}'".format(
            pos=pos, vac=vac))
    from random import randint
    with engine.connect() as connect:
        connect.execute(
            "INSERT INTO database (id_resume, id_vacancy, percent) VALUES " +
            "('{id_res}', '{id_vac}', '{percent}')".format(id_res=id_res, id_vac=id_vac, percent=randint(0, 100)))


def get_vacancy():
    #Test
    engine = create_engine('sqlite:///resume.db')
    data = engine.execute("select position, type from vacancy")
    result = list()
    for i in data:
        result.append(i[0] + " (" + i[1] + ")")
    return result


@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    data = dict()
    data['vacancy'] = get_vacancy()
    if 'save' in request.form:
        add_resume(request.form)
        pass
        # from sqlalchemy import create_engine
        # from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
        # engine = create_engine('sqlite:///resume.db', echo=True)
        # metadata = MetaData()
        # users_table = Table('users', metadata,
        #                     Column('id', Integer, primary_key=True),
        #                     Column('vacancy', String),
        #                     Column('firstName', String),
        #                     Column('lastName', String),
        #                     Column('middleName', String),
        #                     Column('phone', String),
        #                     Column('tags', String),
        #                     Column('profile', String)
        #                     )
        # metadata.create_all(engine)
        #
        # class User(object):
        #     def __init__(self, vacancy, firstName, lastName, middleName, phone, tags, profile):
        #         self.vacancy = vacancy
        #         self.firstName = firstName
        #         self.lastName = lastName
        #         self.middleName = middleName
        #         self.phone = phone
        #         self.tags = tags
        #         self.profile = profile
        #
        #     def __repr__(self):
        #         return "<User('%s';'%s';'%s';'%s';'%s';'%s';'%s')>" % (self.vacancy, self.firstName, self.lastName,
        #                                                                self.middleName, self.phone, self.tags,
        #                                                                self.profile)
        #
        # from sqlalchemy.orm import mapper
        # mapper(User, users_table)
        #
        # args = request.args
        # user = User(args['vacancy'], args['first-name'], args['last-name'], args['middle-name'], args['phone'],
        #             args['tags'], args['profile'])
        #
        # from sqlalchemy.orm import sessionmaker
        # Session = sessionmaker(bind=engine)
        # Session.configure(bind=engine)
        #
        # session = Session()
        # session.add(user)
        # session.commit()

    return render_template(template + '.html', data=data)
