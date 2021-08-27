from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from vaccine.auth import login_required
from vaccine.db import get_db

bp = Blueprint('vaccine', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, hospital, location, created, student_id, username'
        ' FROM post p JOIN user u ON p.student_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('vaccine/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        hospital = request.form['hospital']
        location = request.form['location']
        error = None

        if not hospital:
            error = 'Hospital is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (hospital, location, student_id)'
                ' VALUES (?, ?, ?)',
                (hospital, location, g.user['id'])
            )
            db.commit()
            return redirect(url_for('vaccine.index'))

    return render_template('vaccine/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, hospital, location, created, student_id, username'
        ' FROM post p JOIN user u ON p.student_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['student_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        hospital = request.form['hospital']
        location = request.form['location']
        error = None

        if not hospital:
            error = 'Hospital is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET hospital = ?, body = ?'
                ' WHERE id = ?',
                (hospital, location, id)
            )
            db.commit()
            return redirect(url_for('vaccine.index'))


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('vaccine.index'))     