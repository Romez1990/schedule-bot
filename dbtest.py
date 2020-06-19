from os import getenv as env

from dotenv import load_dotenv
from enum import Enum as PyEnum
from typing import List
from structures import Group
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# load_dotenv()

engine = create_engine('postgres://sbkjclqewptzdy:c22307b458901cf8f46d7ac2d2b7eb782637e436e989ce273aedcfae71d4ba08@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/dcq2rk4s8urnjo')
session = sessionmaker(bind=engine)()

Base = declarative_base()


class Service(PyEnum):
    TG = 1
    VK = 2


class Theme(PyEnum):
    LIGHT = 0
    DARK = 1


class Mode(PyEnum):
    MANUAL = 0
    AUTOMATIC = 1


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    service = Column(Enum(Service))
    mode = Column(Enum(Mode))
    theme = Column(Enum(Theme))
    groups = relationship("UserGroup", primaryjoin="User.id==UserGroup.user_id")

    def __init__(self, user_id: int, service: Service, mode: Mode, theme: Theme):
        self.user_id = user_id
        self.service = service
        self.mode = mode
        self.theme = theme

    def __str__(self):
        return f'{self.id} {self.user_id} {self.service} {self.mode} {self.theme} groups: {str(self.groups)}'


class UserGroup(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(32))

    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f'{self.id} {self.user_id} {self.name}'


class GroupHash(Base):
    __tablename__ = 'hashes'

    id = Column(Integer, primary_key=True)
    group_name = Column(String(32))
    old_hash = Column(Integer)
    cur_hash = Column(Integer)

    def __init__(self, group_name: str, old_hash: int, cur_hash: int):
        self.group_name = group_name
        self.old_hash = old_hash
        self.cur_hash = cur_hash

    def __str__(self):
        return f'{self.id} {self.group_name} {self.old_hash} {self.cur_hash}'


class DBHelper:
    @staticmethod
    def is_user_presented(user_id: int, service: Service = Service.VK) -> bool:
        query = session.query(User).filter_by(user_id=user_id, service=service)
        return query.count() > 0

    @staticmethod
    def add_user(user_id: int, service: Service, mode: Mode, theme: Theme):
        user = User(user_id, service, mode, theme)
        session.add(user)
        session.commit()

    @staticmethod
    def get_user(user_id: int, service: Service = Service.VK) -> User:
        query = session.query(User).filter_by(user_id=user_id, service=service)
        return query.first()
        # query = session.query(User) # query = query.options(undefer('excerpt')) # query.all()

    @staticmethod
    def get_user_by_id(table_id: int, service: Service = Service.VK) -> User:
        query = session.query(User).filter_by(id=table_id, service=service)
        return query.first()

    @staticmethod
    def del_user(user_id: int, service: Service = Service.VK):
        query = session.query(User).filter_by(user_id=user_id, service=service)
        session.delete(query)
        session.commit()

    @staticmethod
    def is_group_presented_on_user(user: User, name: str) -> bool:
        query = session.query(UserGroup).filter_by(user_id=user.id, name=name)
        return query.count() > 0

    @staticmethod
    def add_group_to_user(user: User, name: str):
        group = UserGroup(user.id, name)
        session.add(group)
        session.commit()

    @staticmethod
    def get_groups_from_user(user: User) -> List[Group]:
        return [Group(group.name) for group in user.groups]

    @staticmethod
    def del_group_from_user(user: User, name: str):
        query = session.query(UserGroup).filter_by(user_id=user.id, name=name)
        query.delete()  # session.delete(query)
        session.commit()

    @staticmethod
    def update():
        session.commit()

    @staticmethod
    def add_group_to_hashtable(name: str, old_hash: int, cur_hash: int):
        group = GroupHash(name, old_hash, cur_hash)
        session.add(group)
        session.commit()

    @staticmethod
    def is_group_presented_in_hashtable(name: str) -> bool:
        query = session.query(GroupHash).filter_by(group_name=name)
        return query.count() > 0

    @staticmethod
    def get_group_hashes(name: str) -> GroupHash:
        query = session.query(GroupHash).filter_by(group_name=name)
        return query.first()

    @staticmethod
    def get_users_with_group(name: str) -> List[UserGroup]:
        query = session.query(UserGroup).filter_by(name=name)
        return query.all()


Base.metadata.create_all(engine)

# @staticmethod
# def set_old_hash(group: GroupHash, old_hash: int):
#     group.old_hash = old_hash
#     session.commit()
#
# @staticmethod
# def set_cur_hash(group: GroupHash, cur_hash: int):
#     group.cur_hash = cur_hash
#     session.commit()

# if DBHelper.is_user_presented(12345, Service.TG):
#     test = DBHelper.get_user(12345, Service.TG)
#     print(DBHelper.get_groups_from_user(test))
# if not DBHelper.is_user_presented(12345, Service.TG):
#     DBHelper.add_user(12345, Service.TG, 0, Theme.LIGHT, 1337)
# if DBHelper.is_user_presented(12345, Service.TG):
#     test = DBHelper.get_user(12345, Service.TG)
#     print('user 12345 is presented in db')
#     print(test)
#     if test.theme == Theme.LIGHT:
#         test.theme = Theme.DARK
#         DBHelper.update()
#         print(test)
#
# if not DBHelper.is_user_presented(54321, Service.TG):
#     DBHelper.add_user(54321, Service.TG, 0, Theme.LIGHT, 7331)
#
# if not DBHelper.is_user_presented(222222, Service.VK):
#     DBHelper.add_user(222222, Service.VK, 0, Theme.LIGHT, 1337)
#
# kek = DBHelper.get_user(12345, Service.TG)
# if not DBHelper.is_group_presented_on_user(kek, '4ПрИн-5.16'):
#     DBHelper.add_group_to_user(kek, '4ПрИн-5.16')
#     print('add 5.16 again')
# if not DBHelper.is_group_presented_on_user(kek, '4ПрИн-5а.16'):
#     DBHelper.add_group_to_user(kek, '4ПрИн-5а.16')
#     print('add 5a.16 again')
#
# test_user: User
# for test_user in session.query(User).filter_by(chat_id=12345):
#     print(test_user)
#     keke: Group
#     for keke in DBHelper.get_groups_from_user(test_user):
#         print(keke)


# query = session.query(User)
# query = query.options(undefer('excerpt'))
# query.all()


# Base.metadata.create_all(engine)  # used for relationship between tables
# user = User(55555, Service.VK, 0, 0, 0)
# session.add(user)
# session.commit()
# group = Group(user.id, 'aaa')
# session.add(group)
# session.commit()
# print(", ".join(str(g) for g in user.groups))

# for group in user.groups:
#     print(group.name)
