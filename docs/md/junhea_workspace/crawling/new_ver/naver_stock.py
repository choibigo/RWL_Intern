import json
from openpyxl import load_workbook
import urllib.request

wb = load_workbook('C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/new_ver/company_code.xlsx')

data = wb.active

all_data = {}
for i in range(954):
    item_code = data['A'+str(i+2)].value
    url = "https://m.stock.naver.com/api/stock/%s/integration"%(item_code)
    raw_data = urllib.request.urlopen(url).read()
    json_data = json.loads(raw_data)
    all_data[i] = json_data

with open('C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/new_ver/company_name.json', 'a') as f:
    json.dump(all_data, f, indent=4)