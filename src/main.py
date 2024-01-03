from getpass import getpass
import os, logging
from . import settings, utils, menu, client
from .writer import TxtWriter


def start_parser(name: str, mode: int) -> callable:
    def call() -> None:
        print('Укажите путь до текстового файла со списком '
            'ключевых слов/словосочетаний ИЛИ вставьте слово/словосочетание')
        keywords = utils.extract_data(input('>>> '))
        keywords = [el.lower() for el in keywords]
        if 0 <= mode <= 2:
            print('Укажите путь до текстового файла со списком '
                'ссылок на посты ИЛИ вставьте ссылку на один пост')
        else:
            print('Укажите путь до текстового файла со списком '
                'ссылок на аккаунты/имён аккаунтов ИЛИ '
                'вставьте ссылку на один аккаунт/имя одного аккаунта')
        data = utils.extract_data(input('>>> '))
        account = client.Parser(name, keywords, TxtWriter())
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
        return lambda : menu.draw(
            menu.Item('Назад', main_start),
            *[menu.Item(items[i], start_parser(name, i)) for i in range(len(items))],
            prompt='Выберите источник пользователей для проверки',
        )

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
            logging.info(f'Сессия аккаунта {name} успешно удалена (путь {path})')
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


def log_settings() -> callable:
    def next_step(level: str) -> callable:
        def call() -> None:
            settings.update_settings('log_level', level)
            logging.info('Уровень логирования обновлён. '
                'Чтобы изменения вступили в силу, перезапустите программу')
            main_menu()
        return call
    return lambda : menu.draw(
        menu.Item('Назад', settings_menu),
        menu.Item('DEBUG (выводить все сообщения, в том числе сообщения для отладки)', next_step('debug')),
        menu.Item('INFO (выводить информационные сообщения и ошибки)', next_step('info')),
        menu.Item('ERROR (выводить только ошибки)', next_step('error')),
        menu.Item('отключить логирование (не выводить никаких сообщений)', next_step('disabled')),
    )


def dir_settings(property_name: str) -> callable:
    def call() -> None:
        property_name += '_path'
        mean = getattr(settings, property_name.upper())
        value = ''
        print(f'Укажите путь до папки, в которое будут храниться данные (значение сейчас: {mean}) '
            'ИЛИ напишите 0, чтобы вернуться в главное меню')
        while not os.path.isdir(value) or value != '0':
            value = input('>>> ')
        if value != '0':
            settings.update_settings(property_name, value)
            logging.info(f'Значение параметра {property_name} обновлено ({mean} -> {value}) '
                'Чтобы изменения вступили в силу, перезапустите программу')
        main_menu()
    return call


def set_default_settings() -> None:
    settings.write_file(settings.default_values)
    logging.info('Настройки сброшены до значений по умолчанию. '
        'Чтобы изменения вступили в силу, перезапустите программу')
    main_menu()


def settings_menu() -> callable:
    return lambda : menu.draw(
        menu.Item('Назад', main_menu),
        menu.Item('Настроить логи', log_settings),
        menu.Item('Указать место хранение файлов сессий', dir_settings('sessions')),
        menu.Item('Указать место хранение выходных файлов', dir_settings('output')),
        menu.Item('Сбросить настройки', set_default_settings),
    )


def main_menu() -> None:
    menu.draw(
        menu.Item('Запустить парсер', main_start),
        menu.Item('Добавить акканут', add_account),
        menu.Item('Удалить аккаунт', delete_account),
        menu.Item('Настройки программы', settings_menu),
        zero_index=1,
    )


def start() -> None:
    # setup
    utils.logging_setup()
    utils.check_path(settings.SESSIONS_PATH)
    utils.check_path(settings.OUTPUT_PATH)
    # run
    try:
        main_menu()
    except KeyboardInterrupt:
        logging.info('Выход из программы')
        input('Нажмите любую кнопку для закрытия окна')
    except Exception as e:
        logging.error(e)
        logging.debug(e, exc_info=True)
