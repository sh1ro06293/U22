import requests
from bs4 import BeautifulSoup
import csv

res = requests.get('https://www.jreast-timetable.jp/2407/timetable-v/630u1.html') # 山の手内回り平日
res = requests.get('https://www.jreast-timetable.jp/2407/timetable-v/630u2.html') # 山の手内回り休日
res = requests.get('https://www.jreast-timetable.jp/2407/timetable-v/630d1.html') # 山の手外回り平日
res = requests.get('https://www.jreast-timetable.jp/2407/timetable-v/630d2.html') # 山の手外回り休日

res.encoding = res.apparent_encoding # 日本語の文字化け防止
bsObj = BeautifulSoup(res.text,"html.parser")

csv_path = "station_data\yamanote_sotomawari_kyuujitu.csv"

# 要素の抽出
items = bsObj.find_all("tr")
item_list = []
cnt = 0
for i in items:
    if cnt <= 2:
        cnt += 1
        continue

    item_list = list(i.text.split("\n"))
    item_list = item_list[1:]
    del item_list[1:4]
        
    with open(csv_path, 'a', newline='',encoding= "utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(item_list)
