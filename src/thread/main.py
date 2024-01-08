import logging
from .. import utils, db
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
    try:
        for el in proccess.data:
            if 'likers' in proccess.mode:
                logging.info(f'Start checking commentators post {el}')
                parser.parse_likers(parser.get_post(el))
            if 'commentators' in proccess.mode:
                logging.info(f'Start checking likers post {el}')
                parser.parse_commentators(parser.get_post(el))
            if 'followees' in proccess.mode:
                logging.info(f'Start checking followees profile {el}')
                parser.parse_followees(parser.get_profile(el))
            if 'followers' in proccess.mode:
                logging.info(f'Start checking followers profile {el}')
                parser.parse_followers(parser.get_profile(el))
    except Exception as e:
        logging.error(e, exc_info=True)
    finally:
        proccess.status = True
        proccess.save()
