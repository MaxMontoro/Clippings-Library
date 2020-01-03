#!/usr/bin/env python
import os
import sqlite3
from operator import itemgetter
from collections import OrderedDict

from flask import Flask, request, session, g, redirect, url_for, abort, render_template

from clippings_browser import build_library

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'quotes.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema2.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()    


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

quotes, _, _ = build_library()

@app.cli.command('addall')
@app.route('/addall', methods=['POST', 'GET'])
def add_entry():
    db = get_db()
    for source in quotes:
        for item in quotes[source]:
            db.execute('insert into quotes (source, text) '
                       'values (?, ?)',[str(source), str(item)])
    db.commit()
    return redirect(url_for('show_entries'))
    
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select source, count(*) from quotes group by source order by count(*) desc ')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/search/', methods=['POST', 'GET'])
def pre_filter_quotes():
    query = request.form['text']
    return redirect('/search/' + query)

@app.route('/search/<path:query>', methods=['GET', 'POST'])
def filter_quotes(query):
    db = get_db()
    cur = db.execute('select id, source, text '
                     'from quotes where source '
                     'like ? or text like ? order by id', ['%' + query +'%', '%' + query +'%'])
    entries = cur.fetchall()
    entries_list = [entry for entry in entries if len(entry[2].split()) > 2]
    words = [entry[2] for entry in entries if len(entry[2].split()) < 2] # one-word highlights - probably dictionary lookups
    return render_template('show_entries.html', entries=entries_list, words=words)

@app.route('/random')
def random_quote():
    db = get_db()
    cur = db.execute('select source, text from quotes order by random() limit 1')
    random = cur.fetchall()
    return render_template('show_entries.html', entries=random)

app.run(debug=True, host='0.0.0.0', port=8001)
