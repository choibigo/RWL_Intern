import json
import urllib.request

item_code = "373220"
url = "https://m.stock.naver.com/api/stock/%s/integration"%(item_code)

raw_data = urllib.request.urlopen(url).read()
json_data = json.loads(raw_data)

print(json_data)