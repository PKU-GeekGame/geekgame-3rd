import sqlite3
import sys
import json
import time

def get_db():
    return sqlite3.connect('db/db.sqlite')

def init_db():
    db = get_db()
    db.executescript('''
        create table if not exists submits (
            uid int,
            submit_ts int,
            answers_json text
        );
    ''')

def query_history(uid):
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        select submit_ts, answers_json from submits
        where uid=?
        order by submit_ts asc
    ''', [uid])
    return [(x[0], json.loads(x[1])) for x in cur.fetchall()]

def push_history(uid, submission):
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        insert into submits (uid, submit_ts, answers_json)
        values (?, ?, ?)
    ''', [uid, int(time.time()), json.dumps(submission)])
    db.commit()

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--create-tables':
        print('initializing db')
        init_db()