import sqlite3 as sql
import pymysql

from moamoa.util.config import Config

CONFIG = Config()
host = CONFIG.JDBC.HOST
user = CONFIG.JDBC.USER
password = CONFIG.JDBC.PASSWORD
db = CONFIG.JDBC.DB
charset = CONFIG.JDBC.CHARSET

class User:
  def __init__(self, _id, token):
    self.id = _id
    self.token = token

class Keyword:
  def __init__(self, user_id, keyword):
    self.user_id = user_id
    self.keyword = keyword

class History:
  def __init__(self, user_id, keyword, item, url):
    self.user_id = user_id
    self.keyword = keyword
    self.item = item
    self.url = url
    self.bot_send_yn = 'N'

  def __init__(self, user_id, keyword, item, url, bot_send_yn):
    self.user_id = user_id
    self.keyword = keyword
    self.item = item
    self.url = url
    self.bot_send_yn = bot_send_yn


def init_db(conn):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()

    cur.execute('''CREATE TABLE user
                   (ID INTEGER, TOKEN text)''')

    cur.execute('''CREATE TABLE keyword
                   (ID INTEGER, USER_ID INTEGER, KEYWORD text)''')

    cur.execute('''CREATE TABLE history
                   (ID INTEGER, 
                   USER_ID INTEGER, 
                   KEYWORD text, 
                   ITEM text, 
                   URL text,
                   BOT_SEND_YN text)''')

    cur.close()
    conn.commit()


def insert(sql, conn):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()


def select_user_list():
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    result = []
    cur = conn.cursor()
    cur.execute('SELECT id,token FROM USER')

    for row in cur.fetchall():
      result.append(User(row[0], row[1]))
    cur.close()
    return result


def select_user(user_id) -> User:
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    cur.execute('SELECT id,token FROM USER WHERE id = ' + str(user_id))

    for row in cur.fetchall():
      return User(row[0], row[1])
    cur.close()
    return None


def insert_keyword(user_id, keyword):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    try :
      cur = conn.cursor()
      if type(keyword) == list:
        values = []
        for item in keyword:
          values.append((user_id, item))
        cur.executemany("INSERT INTO keyword(USER_ID,KEYWORD) values('%s','%s')" % values)
      elif type(keyword) == str:
        cur.execute("INSERT INTO keyword(USER_ID,KEYWORD) values('%s','%s')" %
                    (user_id, keyword))
      conn.commit()
      cur.close()
    except sql.IntegrityError:
      pass

def select_keyword_list(user_id):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    result = []
    cur = conn.cursor()
    cur.execute("SELECT user_id,keyword FROM KEYWORD WHERE user_id = '%s'" % user_id)

    for row in cur.fetchall():
      result.append(Keyword(row[0], row[1]))

    cur.close()
    return result

def delete_keyword(user_id, keyword):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    cur.execute("DELETE FROM KEYWORD WHERE user_id = '%s' AND keyword = '%s'" % (user_id , keyword))
    conn.commit()
    cur.close()


def delete_all_keyword(user_id):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    cur.execute("DELETE FROM KEYWORD WHERE user_id = %d" % user_id)
    cur.close()
    conn.commit()

def insert_history(history):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    try :
      if type(history) == list:
        values = []
        for element in history:
          values.append((element.user_id, element.keyword, element.item, element.url, 'N',))
        cur.executemany("INSERT INTO History(USER_ID,KEYWORD, ITEM, URL, BOT_SEND_YN) values('%s','%s','%s','%s','%s')"% values)
      elif type(history) == History:
        values = (history.user_id, history.keyword, history.item, history.url, 'N',)
        cur.execute("INSERT INTO History(USER_ID,KEYWORD, ITEM, URL, BOT_SEND_YN) values('%s','%s','%s','%s','%s')"% values)
      conn.commit()
      cur.close()
    except sql.IntegrityError:
      pass


def select_history(user_id, title=None) -> list:
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    result = None
    cur = conn.cursor()
    if title == None:
      cur.execute("SELECT user_id,keyword, item, url, bot_send_yn FROM HISTORY WHERE user_id = '%s'" % user_id)
    else:
      cur.execute("SELECT user_id,keyword, item, url, bot_send_yn FROM HISTORY WHERE user_id = '%s' AND item = '%s'" % (user_id, title,))

    for row in cur.fetchall():
      result = History(row[0], row[1], row[2], row[3], row[4])

    cur.close()
    return result

def update_history_send_y(history):
  with pymysql.connect(host=host, user=user, password=password, db=db, charset=charset) as conn:
    cur = conn.cursor()
    try :
      if type(history) == list:
        values = []
        for element in history:
          values.append((element.user_id, element.keyword, element.item))
        cur.execute("UPDATE History SET BOT_SEND_YN = 'Y' WHERE user_id = '%s' AND keyword = '%s' AND item = '%s'" % values)
      elif type(history) == History:
        values = (history.user_id, history.keyword, history.item)
        cur.execute("UPDATE History SET BOT_SEND_YN = 'Y' WHERE user_id = '%s' AND keyword = '%s' AND item = '%s'" % values)
      conn.commit()
      cur.close()
    except sql.IntegrityError:
      pass
