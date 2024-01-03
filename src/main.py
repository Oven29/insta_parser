from getpass import getpass
import os, logging
from . import settings, utils, menu, client


def start_parser(name: str, mode: int) -> callable:
    def call() -> None:
        if 0 <= mode <= 2:
            print('Укажите путь до текстового файла со списком '
                'ссылок на посты ИЛИ вставьте ссылку на один пост')
        else:
            print('Укажите путь до текстового файла со списком '
                'ссылок на аккаунты/имён аккаунтов ИЛИ '
                'вставьте ссылку на один аккаунт/имя одного аккаунта')
        value = input('>>> ')
        if '.' in value:  # path to file with data
            with open(value, 'r', encoding='utf-8') as f:
                data = f.read().split('\n')
                data = [el for el in data if el.data != ' ']
        else:
            data = [value]
        account = client.Parser(name)
        for el in data:
            if 0 <= mode <= 2:
                logging.info(f'Начало проверки поста {el}')
                post = account.get_post(el)
                if mode in (0, 1):
                    account.parse_likers(post)
                if mode in (0, 2):
                    account.parse_commentators(post)
            else:
                logging.info(f'Начало проверки профиля {el}')
                profile = account.get_profile(el)
                if mode == 3:
                    account.parse_followees(profile)
                elif mode == 4:
                    account.parse_followers(profile)
    return call


def main_start() -> None:
    def next_step(name: str) -> callable:
        items = (
            'Лайкнувшие и прокомментировавшие пост/посты',  # 0
            'Лайкнувшие пост/посты',                        # 1
            'Прокомментировавшие пост/посты',               # 2
            'Подписки пользователя/пользователей',          # 3
            'Подписчики пользователя/пользователей',        # 4
        )
        def call() -> None:
            menu.draw(
                menu.Item('Назад', main_start),
                *[menu.Item(items[i], start_parser(name, i)) for i in range(len(items))],
                prompt='Выберите источник пользователей для проверки',
            )
        return call

    accounts = utils.get_sessions()
    if len(accounts):
        menu.draw(
            menu.Item('Назад', main_menu),
            *[menu.Item(name, next_step(name)) for name in accounts.keys()],
            prompt='Выберите аккаунт, который будет использоваться в парсинге',
        )
    else:
        logging.error('Прежде чем запускать парсер необходимо добавить хотя бы один аккаунт')
        main_menu()


def add_account() -> None:
    username = input('Введите логин: ')
    password = getpass('Введите пароль: ')
    for n in range(1, 4):
        logging.info(f'Попытка добавление аккаунта {username} №{n}')
        try:
            client.login_and_save_session(username, password)
        except Exception as e:
            logging.error(e)
            logging.info('Ошибка может возникать из-за "плохого" ip адреса')
        else:
            logging.info(f'Аккаунт {username} добавлен')
            break
    main_menu()


def delete_account() -> None:
    def _delete_func(name: str, path: str) -> callable:
        def call() -> None:
            os.remove(path)
            logging.info(f'Удаление сессии аккаунта {name} (путь {path})')
            main_menu()
        return call

    accounts = utils.get_sessions()
    if len(accounts):
        menu.draw(
            menu.Item('Назад', main_menu),
            *[menu.Item(name, _delete_func(name, path)) for name, path in accounts.items()],
            prompt='Выберите аккаунт, который хотите удалить',
        )
    else:
        logging.error('У Вас нет добавленных аккаунтов')
        main_menu()


def main_menu() -> None:
    menu.draw(
        menu.Item('Запустить парсер', main_start),
        menu.Item('Добавить акканут', add_account),
        menu.Item('Удалить аккаунт', delete_account),
    )


def start() -> None:
    # setup
    utils.logging_setup()
    utils.check_path(settings.SESSIONS_PATH)
    # run
    try:
        main_menu()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)
        logging.debug(e, exc_info=True)
