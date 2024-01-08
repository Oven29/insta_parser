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


class Proccess(BaseModel):
    data = ArrayField(null=False)
    keywords = ArrayField(null=False)
    mode = CharField(max_length=32, null=False)
    account = ForeignKeyField(Account)
    created_date = DateTimeField(null=False)
    status = BooleanField(null=False, default=False)
    pid = IntegerField(null=True)
    
    @hybrid_property
    def output_filename(self) -> str:
        return os.path.join(settings.OUTPUT_PATH, f'output-{self.id}.txt')

    @hybrid_property
    def log_filename(self) -> str:
        return os.path.join(settings.LOGS_PATH, f'{self.id}.log')


def setup() -> None:
    "Creating tables"
    models = (Account, Proccess,)
    for model in models:
        model.create_table()
