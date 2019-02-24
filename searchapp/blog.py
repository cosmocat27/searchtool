# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 14:00:52 2019

@author: Cosmo Zen

Functions for handling document insert and delete
"""

from flask import (
        current_app, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from datetime import datetime

from searchapp.auth import login_required
from searchapp.db import get_db

from searchapp.word_to_elastic import word_to_elastic, delete_from_index

import os
import sys

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    entries = db.execute(
            	'select id, title, body'
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
            docID = db.execute('select max(id) from entries where title=?', [filename]).fetchone()['max(id)']
            db.commit()

            #print(docID, file=sys.stderr)
            word_to_elastic(fullpath, docID)
            os.remove(fullpath)

            flash('New entry was successfully posted')
        
        else:
            flash('Could not post file, only .docx allowed')
        
        return redirect(url_for('blog.index'))
    
    return render_template('blog/create.html')

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM entries WHERE id = ?', (id,))
    db.commit()

    delete_from_index(id)

    flash('Entry was successfully deleted')

    return redirect(url_for('blog.index'))
