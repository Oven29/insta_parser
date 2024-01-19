from __future__ import annotations
from peewee import Model, PrimaryKeyField, ForeignKeyField, IntegerField, \
    CharField, BooleanField, DateTimeField, SqliteDatabase, TextField
from playhouse.hybrid import hybrid_property
import os
from typing import List
from . import settings


connect = SqliteDatabase(settings.DB_PATH)


class ArrayField(TextField):
    SEP = '\n'

    def db_value(self, value: List[str] | None) -> str | None:
        if value:
            return self.SEP.join(value)

    def python_value(self, value: str | None) -> List[str] | None:
        if value:
            return value.split(self.SEP)


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = connect
        order_by = 'id'


class Account(BaseModel):
    login = CharField(max_length=128)
    password = CharField(max_length=128)
    added_date = DateTimeField(null=False)
    is_del = BooleanField(null=False, default=False)


class Proccess(BaseModel):
    data = ArrayField(null=False)
    keywords = ArrayField(null=False)
    mode = ArrayField(null=False)
    account = ForeignKeyField(Account)
    created_date = DateTimeField(null=False)
    status = BooleanField(null=False, default=False)  # ended
    pid = IntegerField(null=True)
    type = CharField(max_length=32, null=False)

    @hybrid_property
    def output_filename(self) -> str:
        return os.path.join(settings.OUTPUT_PATH, f'output-{self.id}.txt')

    @hybrid_property
    def log_filename(self) -> str:
        return os.path.join(settings.LOGS_PATH, f'log-{self.id}.txt')

    @hybrid_property
    def account_info(self) -> str:
        if self.account.is_del:
            return f'Аккаунт удалён ({self.account.login})'
        return f'{self.account.id}. {self.account.login}'


def setup() -> None:
    "Creating tables"
    models = (Account, Proccess,)
    for model in models:
        model.create_table()
