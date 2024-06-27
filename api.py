import requests
from os import environ
data = {'key': 'values'}
get_data = {}

request_base = 'https://api.odpt.org'
# request_endpoint = f'/api/v4/odpt:Railway?dc:title=多摩モノレール&acl:consumerKey={environ.get("API_TOKEN")}'
# request_endpoint = f'/api/v4/odpt:Station?owl:sameAs=odpt.Station:JR-East.Yamanote.Gotanda&acl:consumerKey={environ.get("API_TOKEN")}'
# request_endpoint = f'/api/v4/odpt:Station?odpt:station=JR-East.Yamanote.Tokyo&acl:consumerKey={environ.get("API_TOKEN")}'

# これで駅ごとのタイムテーブル取得
# request_endpoint = f'/api/v4/odpt:StationTimetable?owl:sameAs=odpt.StationTimetable:TamaMonorail.TamaMonorail.Manganji.Southbound.SaturdayHoliday&acl:consumerKey={environ.get("API_TOKEN")}'
request_endpoint = f'/api/v4/odpt:StationTimetable?odpt:railway=odpt.Railway:TamaMonorail.TamaMonorail&acl:consumerKey={environ.get("API_TOKEN")}'

# request_endpoint = f'/api/v4/odpt:StationTimetable?acl:consumerKey={environ.get("API_TOKEN")}'

request_url = request_base + request_endpoint

# リクエストを送る
response = requests.get(request_url)
# レスポンスのステータスコードを確認
if response.status_code == 200:
    # レスポンスのjsonデータを取得
    get_data = response.json() 
    print(get_data)
    print("\n")
    print(get_data[0].keys())



# https://biz.jorudan.co.jp/file/norikae_openAPI.pdf

