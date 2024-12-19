from bs4 import BeautifulSoup
import urllib.request
import requests

hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

data = 'https://finance.naver.com/sise/sise_quant.naver'

response = requests.get(data)

def dividerstr(listA):
    ans = []
    stack = []
    for i in range(len(listA)):
        if listA[i] != ' ' and listA[i] != '\n' and listA[i] != '\t':
            stack.append(listA[i])
            if i+1 != len(listA) and (listA[i+1] == ' ' or listA[i+1] == '\n' or listA[i+1] == '\t'):
                ans.append(''.join(stack))
                stack = []
            elif i+1 == len(listA):
                ans.append(''.join(stack))
    return ans

company_name_list = []
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    company = soup.select_one('table.type_2')
    company_name_find = str(company).split('\n')
    for i in range(len(company_name_find)):
        if '<td>' in company_name_find[i]:
            temp = list(company_name_find[i])
            del temp[3]
            namelocation = temp.index('>')
            company_name_list.append(''.join(temp[namelocation+1:len(temp)-9]))
    memo = open("C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/naver_stock_name.txt", 'w')
    memo.write(company_name_list)
    memo.close
    print(company_name_list)
else:
    print('response.status_code')