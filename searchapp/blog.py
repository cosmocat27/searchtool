# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 14:00:52 2019

@author: sem319
"""

from flask import (
        current_app, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from datetime import datetime

from searchapp.auth import login_required
from searchapp.db import get_db

import os

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    entries = db.execute(
            	'select title, body'
            	' FROM entries order by id'
    ).fetchall()
    return render_template('blog/index.html', entries=entries)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        f = request.files['file']
        
        if f and f.filename.rsplit('.', 1)[1] == 'docx':
            filename = secure_filename(f.filename)
            fullpath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            f.save(fullpath)
            
            db = get_db()
            db.execute('insert into entries(title, body, author_id) values(?, ?, ?)',
						[filename, filename, g.user['id']])
            db.commit()
            flash('New entry was successfully posted')
        
        else:
            flask('Could not post file, only .docx allowed')
        
        return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
