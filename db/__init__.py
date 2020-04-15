import sqlite3,os,db.upload,db.search
dbpath=os.path.join(os.path.expanduser('~'),'.market')
filepath=os.path.join(dbpath,'info.db')
if not os.path.exists(dbpath):
    os.mkdir(dbpath)
if os.path.isfile(filepath):
    file=open(filepath)
    file.close()
db=sqlite3.connect(filepath)
db.cursor()
t=db.execute("select name from sqlite_master where type='table' order by name")
if 'items' not in t:
    db.execute('''
    CREATE TABLE items (
    item_id     INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE
                        NOT NULL,
    name        TEXT    NOT NULL,
    seller_id   INT     REFERENCES users (id) ON DELETE SET NULL
                        NOT NULL,
    description TEXT,
    image_link  TEXT
    );
    ''')
    db.commit()
if 'users' not in t:
    db.execute('''
    CREATE TABLE users (
        id           INTEGER   PRIMARY KEY
                               NOT NULL
                               UNIQUE,
        name         TEXT      NOT NULL,
        password     TEXT      NOT NULL,
        email        TEXT      NOT NULL,
        avatar       TEXT      DEFAULT ('default_avatar.png'),
        phone_number CHAR (11),
        sex          BOOLEAN,
        birth_date   DATE
    );
    ''')
    db.commit()
db.close()