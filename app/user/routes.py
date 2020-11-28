from app.user import blueprint
from flask import render_template, request
from flask_login import login_required


@blueprint.route('/<template>', methods=['GET', 'POST'])
@login_required
def route_template(template):
    if 'save' in request.args:
        from sqlalchemy import create_engine
        from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
        engine = create_engine('sqlite:///resume.db', echo=True)
        metadata = MetaData()
        users_table = Table('users', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('vacancy', String),
                            Column('firstName', String),
                            Column('lastName', String),
                            Column('middleName', String),
                            Column('phone', String),
                            Column('tags', String),
                            Column('profile', String)
                            )
        metadata.create_all(engine)

        class User(object):
            def __init__(self, vacancy, firstName, lastName, middleName, phone, tags, profile):
                self.vacancy = vacancy
                self.firstName = firstName
                self.lastName = lastName
                self.middleName = middleName
                self.phone = phone
                self.tags = tags
                self.profile = profile

            def __repr__(self):
                return "<User('%s';'%s';'%s';'%s';'%s';'%s';'%s')>" % (self.vacancy, self.firstName, self.lastName,
                                                                       self.middleName, self.phone, self.tags,
                                                                       self.profile)

        from sqlalchemy.orm import mapper
        mapper(User, users_table)

        args = request.args
        user = User(args['vacancy'], args['first-name'], args['last-name'], args['middle-name'], args['phone'],
                    args['tags'], args['profile'])

        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)

        session = Session()
        session.add(user)
        session.commit()

    return render_template(template + '.html')
