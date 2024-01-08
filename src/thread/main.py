import os, logging
from .. import settings, utils, db
from . import client
from .writer import TxtWriter


def start(pr_id: int) -> None:
    "Run parser"
    proccess: db.Proccess = db.Proccess.get(db.Proccess.id == int(pr_id))
    utils.logging_setup(proccess.log_filename)
    parser = client.Parser(
        username=proccess.account.login,
        password=proccess.account.password,
        keywords=proccess.keywords,
        writer=TxtWriter(proccess.output_filename),
    )
    for el in proccess.data:
        if 'likes' in proccess.mode:
            logging.info(f'Start checking commentators post {el}')
            parser.parse_likers(parser.get_post(el))
        if 'comments' in proccess.mode:
            logging.info(f'Start checking likers post {el}')
            parser.parse_commentators(parser.get_post(el))
        if 'folowees' in proccess.mode:
            logging.info(f'Start checking followees profile {el}')
            parser.parse_followees(parser.get_profile(el))
        if 'folowers' in proccess.mode:
            logging.info(f'Start checking followers profile {el}')
            parser.parse_followers(parser.get_profile(el))
    proccess.status = True
    proccess.save()
