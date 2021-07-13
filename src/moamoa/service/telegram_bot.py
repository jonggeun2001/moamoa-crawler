import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from moamoa.dao import dao
from moamoa.service import ppomppu_crawler


class Bot:
  def __init__(self, User):
    self.id = User.id
    self.token = User.token

  def check_id(self, _id) -> bool:
    return self.id == _id

  def send_message(self, message=str):
    #if not hasattr(self, 'bot'):
    self.bot = telegram.Bot(self.token)
    self.bot.sendMessage(self.id, message)

  def get_message(self, update, context):
    print(str(self.id) + ":" + update.message.text)
    message = update.message.text
    if message.find(":") > 0:
      command = message.split(":")[0].strip()
      keyword = message.split(":")[1].strip()
      if command == '등록':
        dao.insert_keyword(self.id, keyword)
        self.send_message('"' + keyword + '" 등록 완료')
        self.send_keyword_list()
      elif command == '제거':
        dao.delete_keyword(self.id, keyword)
        self.send_message('"' + keyword + '" 제거 완료')
        self.send_keyword_list()
      elif command == '찾기' or command == '검색':
        item_list = ppomppu_crawler.get_ppomppu_link([dao.Keyword(self.id, keyword)])
        if len(item_list) == 0 :
          self.send_message("찾는 물품이 없습니다")
          return
        for item in item_list:
          self.send_message(item['title'] + '\n' + item['url'])
      else:
        pass

      return None

    if message == '초기화':
      dao.delete_all_keyword(self.id)
      self.send_message( '초기화 완료')
      return

    if message == '찾기' or message == '검색':
      keyword_list = dao.select_keyword_list(self.id)

      item_list = ppomppu_crawler.get_ppomppu_link(keyword_list)
      if len(item_list) == 0 :
        self.send_message("찾는 물품이 없습니다")
        return
      for item in item_list:
        self.send_message(item['title'] + '\n' + item['url'])
      return

    if message == '목록' or message == '리스트':
      self.send_keyword_list()
      return None


  # help reply function
  def help_command(self, update, context):
    self.send_message('찾기 = 찾기:아이템')

  def send_keyword_list(self):
    keyword_list = dao.select_keyword_list(self.id)
    resigster_message = "등록 키워드 내역 = "

    for keyword in keyword_list:
      resigster_message += keyword.keyword + ","
    self.send_message(resigster_message[:-1])

    return None

  def run(self):
    updater = Updater(self.token, use_context=True)

    message_handler = MessageHandler(Filters.text & (~Filters.command),
                                     self.get_message)  # 메세지중에서 command 제외
    updater.dispatcher.add_handler(message_handler)

    help_handler = CommandHandler('help', self.help_command)
    updater.dispatcher.add_handler(help_handler)

    updater.start_polling(timeout=3, drop_pending_updates=True)
    updater.idle()


