from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from datetime import datetime

from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', 'todo', url_prefix="/todo")


def get_todo(id, check_author=True):
    todo = get_db().execute(
        'SELECT t.id, title, task, date, author_id, username'
        ' FROM task t JOIN user u ON t.author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if todo is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and todo['author_id'] != g.user['id']:
        abort(403)

    return todo


@bp.route('/')
@login_required
def index():
    db = get_db()
    todos = db.execute('SELECT t.id,t.title,t.task,t.date,t.done '
                       'FROM task t,user u '
                       'WHERE t.author_id = u.id').fetchall()
    username = g.user['username']
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    string = ""
    return render_template('todo/index.html', todos=todos, username=username, string=string, today=today)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        task = request.form['task']
        date = request.form['date']

        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        error = None

        if not title:
            error = 'Title is required.'
        if not date:
            error = 'Date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, task, date, done, author_id)'
                ' VALUES (?, ?, ?, 0, ?)',
                (title, task, date, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    todo = get_todo(id)

    if request.method == 'POST':
        title = request.form['title']
        task = request.form['task']
        date = request.form['date']

        date = datetime.strptime(date, '%Y-%m-%dT%H:%M')

        error = None

        if not title:
            error = 'Title is required.'
        if not date:
            error = 'Date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET title = ?, task = ?, date = ?'
                ' WHERE id = ?',
                (title, task, date, id)
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/edit.html', todo=todo)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_todo(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id =?', (id,))
    db.commit()
    return redirect(url_for('todo.index'))


@bp.route('/update', methods=('POST',))
@login_required
def update():
    if request.method == 'POST':
        id = int(request.form['id'])
        done = request.form['done']

        db = get_db()
        db.execute('UPDATE task SET done = ?'
                   ' WHERE id = ?',
                   (done, id))
        db.commit()
    return


@bp.route('/week')
@login_required
def weekly():
    db = get_db()
    todos = db.execute('SELECT t.id,t.title,t.task,t.date,t.done '
                       'FROM task t,user u '
                       'WHERE t.author_id = u.id').fetchall()
    username = g.user['username']
    string = "These are the tasks that are due for the next 7 days."
    now = datetime.now().strftime('%Y-%m-%d')
    today = int(now[8:10])
    ref_todo = []

    for todo in todos:
        if todo[3][5:7] == now[5:7]:
            if int(todo[3][8:10]) in range(today,today + 7):
                ref_todo.append(todo)

    return render_template('todo/index.html', todos=ref_todo, username=username, string=string, today=now)



