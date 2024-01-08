import os, signal, subprocess, sys
from datetime import datetime
from typing import Any
import flask as f
from .. import db, utils, settings


app = f.Flask(__name__)
app.secret_key = '123'


@app.route('/')
def index() -> Any:
    return f.redirect(f.url_for('.pr_list'))


@app.route('/pr_list')
def pr_list() -> Any:
    proccesses = reversed(db.Proccess.select())
    return f.render_template(
        'pr_list.html',
        title='Список процессов',
        proccesses=proccesses,
    )


@app.route('/add_pr', methods=['GET', 'POST'])
def add_pr() -> Any:
    response = lambda : f.render_template(
        'add_pr.html',
        title='Добавление процесса/процессов',
    )
    if f.request.method == 'GET':
        return response()

    form = f.request.form
    available_modes = ('likers', 'commentators', 'followers', 'followees',)
    mode = [m for m in available_modes if not form.get(m) is None]
    if not len(mode):
        f.flash('Процесс не был добавлен, поскольку не указан режим работы')
        return response()
    if not form.get('data') or not form.get('keywords'):
        f.flash('Процесс не был добавлен, не указаны ссылки и/или ключевые слова')
        return response()
    if form.get('account'):
        acc = form.get('account')
        if acc.isdigit():
            acc = db.Account.get_or_none(db.Account.id == int(acc))
        else:
            acc = db.Account.get_or_none(db.Account.login == acc)
        if acc is None:
            f.flash('Аккаунт, который был указан процессу не найден!')
            return response()
        proccess = db.Proccess.create(
            data=utils.extract_data(form['data']),
            keywords=utils.extract_data(form['keywords']),
            mode=mode,
            account=acc,
            created_date=datetime.now(),
        )
        proccess.pid = subprocess.Popen([
            sys.executable,
            os.path.join(settings._dir, 'run.py'),
            str(proccess.id),
        ]).pid
        proccess.save()
        f.flash(f'Процесс успешно добавлен {proccess.id=}')
        return response()
    data = utils.extract_data(form['data'])
    keywords = utils.extract_data(form['keywords'])
    now = datetime.now()
    active_proccesses = db.Proccess.select().where(
        (db.Proccess.status == False) & db.Proccess.account.is_null()
    )
    accounts = db.Account.select()
    busy = set()
    for apr in active_proccesses:
        busy.add(apr.account.id)
    accounts = accounts.where(db.Account.id.not_in(busy))
    if len(accounts) == 0:
        f.flash('Нет свободных аккаунтов! Вам нужно указать номер/логин '
            'аккаунта-исполнителя добавить новые аккаунты')
        return response()
    step = (len(data) // len(accounts)) + (1 if len(data) % len(accounts) else 0)
    count = 0
    for offset in range(0, len(data), step):
        proccess = db.Proccess.create(
            data=data[offset:offset+step],
            keywords=keywords,
            mode=mode,
            account=accounts[count],
            created_date=now,
        )
        proccess.pid = subprocess.Popen([
            sys.executable,
            os.path.join(settings._dir, 'run.py'),
            str(proccess.id),
        ]).pid
        proccess.save()
        count += 1
    f.flash(f'Добавлено {count} процессов')
    return response()


@app.route('/pr_info/<int:id>')
def pr_info(id: int) -> Any:
    proccess = db.Proccess.get(db.Proccess.id == id)
    return f.render_template(
        'pr_info.html',
        title='Информация о процессе',
        proccess=proccess,
    )


@app.route('/kill_pr/<int:id>')
def kill_pr(id: int) -> Any:
    proccess: db.Proccess = db.Proccess.get(db.Proccess.id == id)
    try:
        os.kill(proccess.id, signal.SIGTERM)
        f.flash(f'Процесс, начатый {proccess.created_date}, успешно завершён {proccess.id=}')
        proccess.status = True
        proccess.save()
    except Exception:
        f.flash(f'Процесс, начатый {proccess.created_date}, не был завершён. '
            f'Скорее всего этот процесс уже не работает. {proccess.id=}')
    return f.redirect(f.url_for('.index'))


@app.route('/acc_list')
def acc_list() -> Any:
    accounts = db.Account.select()
    return f.render_template(
        'acc_list.html',
        title='Список аккаунтов',
        accounts=accounts,
    )


@app.route('/add_acc', methods=['GET', 'POST'])
def add_acc() -> Any:
    if f.request.method == 'POST':
        now = datetime.now()
        data = utils.extract_data(f.request.form.get('accounts'))
        for log_pas in data:
            login, password = log_pas.split(':', 1)
            db.Account.create(
                login=login,
                password=password,
                added_date=now,
            )
        f.flash(f'Аккаунты успешно добавлены (количество: {len(data)})')

    return f.render_template(
        'add_acc.html',
        title='Добавление аккаунта',
    )


@app.route('/del_acc/<int:id>')
def del_acc(id: int ) -> Any:
    acc = db.Account.get(db.Account.id == id)
    db.Account.delete().where(db.Account.id == id).execute()
    f.flash(f'Аккаунт {acc.login} удален')
    return f.redirect(f.url_for('.index'))


def start() -> None:
    "Start server"
    # setuping
    db.setup()
    utils.check_path(settings.SESSIONS_PATH)
    utils.check_path(settings.OUTPUT_PATH)
    proccesses = db.Proccess.select().where(db.Proccess.status == False)
    for pr in proccesses:
        pr.status = True
        pr.save()
        try: os.kill(pr.id, signal.SIGTERM)
        except Exception: ...
    # launching
    app.run(debug=True)
