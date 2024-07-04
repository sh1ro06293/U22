import requests
from bs4 import BeautifulSoup
import csv

res = requests.get('https://www.jreast-timetable.jp/2407/timetable-v/630u1.html')
res.encoding = res.apparent_encoding # 日本語の文字化け防止
bsObj = BeautifulSoup(res.text,"html.parser")

csv_path = "station_data\yamanote_uchimawari_heijitu.csv"

# 要素の抽出
items = bsObj.find_all("tr")
item_list = []
for i in items:
    item_list = list(i.text.split("\n"))
    with open(csv_path, 'a', newline='',encoding= "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(item_list)