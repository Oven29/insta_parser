import logging
from .. import db
from . import client
from .writer import TxtWriter


def start(pr_id: int) -> None:
    "Run parser"
    proccess: db.Proccess = db.Proccess.get(db.Proccess.id == int(pr_id))
    logging.basicConfig(
        filename=proccess.log_filename,
        filemode='w',
        encoding='utf-8',
        format='[%(asctime)s | %(levelname)s]: %(message)s',
        datefmt='%m.%d.%Y %H:%M:%S',
        level=logging.INFO,
    )
    try:
        parser = client.Parser(
            username=proccess.account.login,
            password=proccess.account.password,
            keywords=proccess.keywords,
            writer=TxtWriter(proccess.output_filename),
        )
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
        logging.debug(e, exc_info=False)
    finally:
        proccess.status = True
        proccess.save()
