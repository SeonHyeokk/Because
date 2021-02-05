import os
import sys
import urllib.request
import requests
import json
from flask import Flask, render_template, request
import news
import re

app = Flask("BE:CAUSE")


@app.route("/")
def home():
    categories = ["정치", "경제", "사회", "생활/문화", "세계", "IT/과학"]
    headline = news.get_headline()
    headline_list = []
    for article in headline:
        data = {}
        data["title"] = article[0]
        data["link"] = article[1]
        data["image"] = news.get_photo(data["link"])
        headline_list.append(data)
    return render_template("index.html", headline=headline_list, categories=categories, enumerate=enumerate)


@app.route("/result")
def result():
    keyword = request.args.get('keyword')
    news_data = news.get_news_data(keyword)
    for article in news_data:
        article["image"] = news.get_photo(article["link"])
        article["title"] = article["title"].replace(
            "<b>", "").replace("</b>", "")
        article["title"] = re.sub(
            pattern='\&.+;', repl='', string=article["title"])
        article["description"] = article["description"].replace(
            "<b>", "").replace("</b>", "")
        article["description"] = re.sub(
            pattern='\&.+;', repl='', string=article["description"])
    return render_template("result.html", keyword=keyword, search_result=news_data)


app.run()
