import sqlite3,os,hashlib
from flask import g
from os import urandom,path,remove
from shutil import rmtree
from random import sample
import time
dbpath=os.path.join(os.path.expanduser('~'),'.market')
dbfilepath=os.path.join(dbpath,'info.db')
imgpath=os.path.join(dbpath,'imgs')
#数据库位置：当前用户文件夹下.markets/info.db
def init():
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
    price       NUMERIC,
    situation   INT      NOT NULL
                         DEFAULT (0) 
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
                           DEFAULT ('default_avatar.png'),
    salt         TEXT
);
    ''')
        db.commit()
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
    if ('chats',) not in tb:
        db.execute('''
CREATE TABLE chats (
    chat_id     INTEGER  PRIMARY KEY AUTOINCREMENT
                         UNIQUE
                         NOT NULL,
    sender_id   INT      REFERENCES users (id) 
                         NOT NULL,
    receiver_id INT      REFERENCES users (id) 
                         NOT NULL,
    content     TEXT     NOT NULL,
    send_time   DATETIME NOT NULL
);
    ''')
        db.commit()
    if ('item_imgs',) not in tb:
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
    if ('likes_category',) not in tb:
        db.execute('''
    CREATE TABLE likes (
    self_id   INT PRIMARY KEY
                     REFERENCES users (id) ON DELETE CASCADE
                    NOT NULL,
    category STRING REFERENCES items (category) ON DELETE CASCADE
                          NOT NULL
);
    ''')
        db.commit()
    if ('replies',) not in tb:
        db.execute('''
CREATE TABLE replies (
    item_id       INT      REFERENCES items (item_id) ON DELETE CASCADE
                           NOT NULL,
    user_id       INT      REFERENCES users (id) ON DELETE SET DEFAULT
                           NOT NULL
                           DEFAULT ('unexisted user'),
    reply_content TEXT     NOT NULL,
    reply_id      INTEGER  PRIMARY KEY AUTOINCREMENT
                           NOT NULL
                           UNIQUE,
    added_date    DATETIME NOT NULL
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
    if ('admins',) not in tb:
        db.execute('''
        CREATE TABLE banned_user (
    user_id    INT     REFERENCES users (id) 
                       NOT NULL,
    ban_id     INTEGER PRIMARY KEY AUTOINCREMENT
                       NOT NULL,
    unban_date DATE    NOT NULL,
    reason     TEXT    NOT NULL
                       DEFAULT ('No reason') 
);
''')
        db.commit()
    if ('notifications',) not in tb:
        db.execute('''
        CREATE TABLE notifications (
    noti_id     INT  PRIMARY KEY AUTOINCREMENT
                          NOT NULL,
     user_id    INT  REFERENCES users (id)  NOT NULL
     seen       BOOLEAN  DEFAULT(false)          
);
''')
        db.commit()
    if ('banned_user',) not in tb:
        db.execute('''
        CREATE TABLE banned_user (
    user_id    INT     REFERENCES users (id) 
                       NOT NULL,
    ban_id     INTEGER PRIMARY KEY AUTOINCREMENT
                       NOT NULL,
    unban_date DATE    NOT NULL,
    reason     TEXT    NOT NULL
                       DEFAULT ('No reason') 
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
        t=hashlib.md5(bytes(salt[0].encode('UTF-8')))
    t.update(text.encode(encoding='UTF-8'))
    return t.hexdigest()
def uploadimgs(image,des,id):
    if not isinstance(image,list):
        image=[image]
    r=[]
    t=path.join(imgpath,des,id)
    for t in image:
        s=t.content_type.split('.')[-1]
        n=hash(str(urandom(16),encoding="UTF-8"))+'.'+s
        p=path.join(p,n)
        if not path.exists(p):
            with open(p,'w') as a:
                pass
        image.save(p)
        r.append(n)
    return r #返回有被添加文件的名字的表
def delimgs(*imgpath):
    err=[]
    for t in imgpath:
        if path.exists(t):
            remove(t)
            continue
        err.append(t)
    if err!=[]:
        return err
def delimgf(des,id):
    f=path.join(imgpath,des,id)
    if path.exists(f):
        rmtree(f)
def getctime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
def getsalt():
    return ''.join(sample('zyxwvutsrqponmlkjihgfedcba1234567890!@#$%^&*',10))