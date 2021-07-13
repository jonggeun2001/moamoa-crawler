from bs4 import BeautifulSoup
import requests

daangn_base_url = 'https://www.daangn.com'

def find_keywords(target, keyword_list):
  for keyword in keyword_list:
    if keyword == '*':
      return keyword
    if (target.find(keyword) > 0):
      return keyword
  return None


def get_daangn_url(search_location, search_keyword, first_page=None):
  result = []
  for page in range(1,10):
    r = requests.get(daangn_base_url + '/search/' + search_location + ' ' + search_keyword + '/more/flea_market?page=' + str(page))
    if r.status_code == 200:
      # html을 들고와서
      bs = BeautifulSoup(r.text, 'html.parser')

      info_list = bs.find_all('div', class_='article-info')
      for info in info_list[1:]:
        title = info.contents[1].contents[1].text
        content = str(info.contents[1].contents[3].text).strip()
        location = str(info.contents[3].text).strip()
        price = str(info.contents[5].text).strip()
        url = daangn_base_url + info.parent.parent.contents[3]['href']
        print(title + '\n' + content + '\n' + location + '\n' + price + '\n' + url)
        print('\n')
        #  result.append(item)

  return result

get_daangn_item('언남동', '맥북')
