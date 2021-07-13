import time

from apscheduler.schedulers.background import BackgroundScheduler

from moamoa.service import ppomppu_crawler
from moamoa.service.telegram_bot import Bot
import concurrent.futures
from moamoa.dao import dao

if __name__ == '__main__':
  print(__file__)
  sched = BackgroundScheduler()

  user_list = dao.select_user_list()

  bot_list = {}
  for user in user_list:
    bot_list[user.id] = Bot(user)


  @sched.scheduled_job('interval', seconds=60, id='hello')
  def job1():
    for user in user_list:
      keyword_list = dao.select_keyword_list(user.id)
      search_item_list = ppomppu_crawler.get_ppomppu_link(keyword_list, first_page=True)
      for item in search_item_list:
        exist_history = dao.select_history(user.id, item['title'])
        if exist_history == None:
          print(item)
          new_history = dao.History(user.id, item['keyword'], item['title'],
                                    item['url'], "N")
          dao.insert_history(new_history)
          bot_list[user.id].send_message(item['title'] + '\n' + item['url'])
          new_history.bot_send_yn = 'Y'
          dao.update_history_send_y(new_history)
        elif exist_history.bot_send_yn == 'N':
          bot_list[user.id].send_message(item['title'] + '\n' + item['url'])
          exist_history.bot_send_yn = 'Y'
          dao.update_history_send_y(exist_history)

        # a.send_message(message=str(item) + "\n" + search_item_list[item])

    print(f'job1 : {time.strftime("%H:%M:%S")}')


  sched.start()

  with concurrent.futures.ProcessPoolExecutor() as executor:
    for user in user_list:
      print(user)
      executor.submit(bot_list[user.id].run)
    print("done")
