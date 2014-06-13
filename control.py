# -*- coding: utf-8 -*- #

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from werkzeug.utils import secure_filename
import re
import sqlite3
import StringIO
import markdown
import codecs



def secure_cn_filename(s):
    s = re.sub('[" "\/\--.]+', '-', s)
    s = re.sub(r':-', ':', s)
    s = re.sub(r'^-|-$', '', s)
    return s



def initDB():
    try:
        c = sqlite3.connect('resource.db').cursor()
        c.execute('''
            CREATE TABLE resource(
            uid INTEGER PRIMARY KEY NOT NULL,
            file BLOB NOT NULL,
            filename TEXT NOT NULL,
            filetype TEXT NOT NULL)''')
        c.commit()
    except:
        pass
#初始化数据库
#initDB()

def SaveToDB(files, filename):
    conn = sqlite3.connect('resource.db')
    c = conn.cursor()

    c.execute('SELECT max(uid) FROM resource')
    uid =  c.fetchone()[0] + 1

    filetype = secure_filename(filename).split('.')[-1].lower()

    c.execute('INSERT INTO resource VALUES (?, ?, ?, ?)', (uid, sqlite3.Binary(files.read()), filename, filetype))
    conn.commit()

    return uid


def ReadDB(uid):
    conn = sqlite3.connect('resource.db')
    c = conn.cursor()
    c.execute('SELECT uid, file, filename, filetype FROM resource WHERE uid = %s' % str(uid))
    return c.fetchone()

def md(files):
    files = codecs.open(files, mode="r", encoding="utf-8")
    text = files.read()
    html = markdown.markdown(text)
    return html

if __name__ == '__main__':
    #for test
    #files = open('test.png', 'rb')
    #SaveToDB(files, 'test.png')
    #uid = 10
    #print ReadDB(uid)
    pass