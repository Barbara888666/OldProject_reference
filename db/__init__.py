import sqlite3,os,hashlib
from flask import g
dbpath=os.path.join(os.path.expanduser('~'),'.market')
dbfilepath=os.path.join(dbpath,'info.db')
imgpath=os.path.join(dbpath,'imgs')
#数据库位置：当前用户文件夹下.markets/info.db
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
    is_sell     BOOLEAN  DEFAULT (false) 
                         NOT NULL,
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
    birth_date   DATE,
    description  TEXT,
    avatar_name  TEXT      NOT NULL
                           DEFAULT ('default_avatar.png') 
);
    ''')
if ('albums',) not in tb:
    db.execute('''
    CREATE TABLE albums (
    owner_id INT  PRIMARY KEY
                  REFERENCES users (id) ON DELETE CASCADE
                  NOT NULL,
    img_name TEXT NOT NULL,
    seq      INT  NOT NULL
                  DEFAULT (0) 
);
    ''')
    db.commit()
if ('chat_imgs',) not in tb:
    db.execute('''
    CREATE TABLE chat_imgs (
    chat_id  INT  REFERENCES chats (chat_id) ON DELETE CASCADE
                  NOT NULL
                  PRIMARY KEY,
    img_name TEXT NOT NULL,
    seq      INT  DEFAULT (0) 
                  NOT NULL
);
    ''')
    db.commit()
if ('chats',) not in tb:
    db.execute('''
    CREATE TABLE chats (
    chat_id     INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE
                        NOT NULL,
    sender_id   INT     REFERENCES users (id) 
                        NOT NULL,
    receiver_id INT     REFERENCES users (user_name) 
                        NOT NULL,
    content     TEXT    NOT NULL
);
    ''')
    db.commit()
if ('item_imgs') not in tb:
    db.execute('''
    CREATE TABLE item_imgs (
    item_id  INT  PRIMARY KEY
                  REFERENCES items (item_id) ON DELETE CASCADE
                  NOT NULL,
    img_name TEXT NOT NULL,
    seq      INT  NOT NULL
                  DEFAULT (0) 
);
    ''')
    db.commit()
if ('item_reports',) not in tb:
    db.execute('''
    CREATE TABLE item_reports (
    item_id       TEXT    REFERENCES items (item_id) 
                          NOT NULL,
    report_reason TEXT    NOT NULL,
    report_id     INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE
);
    ''')
    db.commit()
if ('likes',) not in tb:
    db.execute('''
    CREATE TABLE likes (
    self_id   INT PRIMARY KEY
                  REFERENCES users (id) ON DELETE CASCADE
                  NOT NULL,
    target_id INT REFERENCES users (id) ON DELETE CASCADE
                  NOT NULL
);
    ''')
    db.commit()
if ('replies',) not in tb:
    db.execute('''
    CREATE TABLE replies (
    item_id       INT     REFERENCES items (item_id) ON DELETE CASCADE
                          NOT NULL,
    user_id       INT     REFERENCES users (id) ON DELETE SET DEFAULT
                          NOT NULL
                          DEFAULT ('unexisted user'),
    reply_content TEXT    NOT NULL,
    reply_id      INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE
);

    ''')
    db.commit()
if ('reply_imgs',) not in tb:
    db.execute('''
CREATE TABLE reply_imgs (
    reply_id INT  PRIMARY KEY
                  REFERENCES replies (reply_id) ON DELETE CASCADE
                  NOT NULL,
    img_name TEXT NOT NULL,
    seq      INT  NOT NULL
                  DEFAULT (0) 
);    
    ''')
    db.commit()
if ('reply_reports',) not in tb:
    db.execute('''
    CREATE TABLE reply_reports (
    report_id     INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL
                          UNIQUE,
    target_reply  INT     REFERENCES replies (reply_content) 
                          NOT NULL,
    report_reason TEXT    NOT NULL
);
  
    ''')
    db.commit()
if ('user_reports',) not in tb:
    db.execute('''
    CREATE TABLE user_reports (
    report_id     INTEGER PRIMARY KEY AUTOINCREMENT
                          NOT NULL,
    report_reason TEXT    NOT NULL,
    target_id     INT     NOT NULL
                          REFERENCES users (id) 
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
def hash(text,*salt):
    if len(salt)==0:
        t=hashlib.md5()
    else:
        t=hashlib.md5(bytes(salt[0]))
    t.update(text.encode(encoding='UTF-8'))
    return t.hexdigest()
