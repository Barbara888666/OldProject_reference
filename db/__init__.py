import sqlite3,os,hashlib
from flask import g
dbpath=os.path.join(os.path.expanduser('~'),'.market')
dbfilepath=os.path.join(dbpath,'info.db')
imgpath=os.path.join(dbpath,'imgs')

if not os.path.exists(dbpath):
    os.mkdir(dbpath)
if os.path.isfile(dbfilepath):
    file=open(dbfilepath)
    file.close()
db=sqlite3.connect(dbfilepath)
db.cursor()
tb=db.execute("select name from sqlite_master where type='table' order by name").fetchall()
if ('items',) not in tb:
    db.execute('''
    CREATE TABLE items (
    item_id     INTEGER  PRIMARY KEY AUTOINCREMENT
                         UNIQUE
                         NOT NULL,
    item_name   TEXT     NOT NULL,
    seller_id   INT      REFERENCES users (id) 
                         NOT NULL,
    description TEXT     NOT NULL,
    added_date  DATETIME NOT NULL,
    is_urgent   BOOLEAN  DEFAULT (false),
    view_time   INT      DEFAULT (0) 
                         NOT NULL,
    category    STRING   DEFAULT ('other'),
    price       NUMERIC
    );
    ''')
    db.commit()
if ('users',) not in tb:
    db.execute('''
    CREATE TABLE users (
        id           INTEGER   PRIMARY KEY
                           NOT NULL
                           UNIQUE,
        user_name    TEXT      NOT NULL,
        password     TEXT      NOT NULL,
        email        TEXT      NOT NULL,
        phone_number CHAR (11),
        sex          BOOLEAN,
        birth_date   DATE
    );
    ''')
    db.commit()
db.close()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbfilepath)
    return db
def dbop(query,issearch):
    gdb=get_db()
    gdb.cursor()
    if issearch:
        return gdb.execute(query).fetchall()
    else:
        gdb.execute(query)
    gdb.commit()
<<<<<<< HEAD
def hash(text,*salt):
    if len(salt)==0:
        t=hashlib.md5()
    else:
        t=hashlib.md5(bytes(salt[0]))
    t.update(text.encode(encoding='UTF-8'))
    return t.hexdigest()
=======


>>>>>>> 6bb184512095c8b8ee60b29e43498b39f22a0386
