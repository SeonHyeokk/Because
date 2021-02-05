import os
import sys
import urllib.request
import json
from bs4 import BeautifulSoup
import requests

### input ###
# query: 검색할 단어(str)
# display: 검색 결과 출력 건수(int, 최대 100)
# start: 검색 시작 위치(int, 최대 1000)
# sort: 정렬 기준 ("sim" : 유사도순, "date": 날짜순)

# output: 뉴스 데이터가 저장된 딕셔너리


def get_news_data(query, display=10, start=1, sort="sim"):
    client_id = "8r5zeQfBuknAG9Lp9zLJ"
    client_secret = "DXCG3x9bIf"
    encText = urllib.parse.quote(query)
    # json 결과
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}&start={start}&sort={sort}"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))['items']
    else:
        return "Error Code:" + rescode


# input: 뉴스 링크
# output: 뉴스에 포함된 이미지 링크 중 하나, 이미지가 없을 시 None
def get_photo(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    if "https://news.naver.com/" in link:
        try:
            return soup.find("div", {'id': 'articleBodyContents'}).find("img")['src']
        except:
            return None
    else:
        return None

    # 네이버 기사가 아닌 다른 기사 이미지 찾기
    # try:
    #     return soup.find_all("img")[0]['src']
    # except:
    #     return None
