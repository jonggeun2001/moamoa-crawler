from bs4 import BeautifulSoup
import requests

ppomppu_base_url = 'https://www.ppomppu.co.kr/zboard/'


# 바로 뽐뿌 컴퓨터 게시판으로 접속한다

def find_keywords(target, keyword_list):
  for keyword in keyword_list:
    if keyword.keyword == '*':
      return keyword.keyword
    if (target.find(keyword.keyword) > 0):
      return keyword.keyword
  return None


def get_ppomppu_link(keyword_list, first_page=None):
  result = []
  pages = range(1, 10)
  if(first_page == True):
    pages = range(1,1)

  for page in range(1, 10):
    r = requests.get(
      ppomppu_base_url + 'zboard.php?id=ppomppu&page=' + str(page))
    if r.status_code == 200:
      # html을 들고와서
      bs = BeautifulSoup(r.text, 'html.parser')

      titles = bs.find_all('font', class_='list_title')
      for title in titles[1:]:
        keyword = find_keywords(title.string, keyword_list)
        if (keyword != None):
          # print(title.string)
          # print(ppomppu_base_url + title.parent['href'])
          item = {}
          item['keyword'] = keyword
          item['title'] = title.string
          item['url'] = ppomppu_base_url + title.parent['href']
          result.append(item)

  return result
