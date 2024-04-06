from bs4 import BeautifulSoup
import urllib.request
import requests

hdr = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

data = 'https://finance.naver.com/sise/sise_quant.naver'

response = requests.get(data)

company_name_list = []
company_stock_price = []
company_stock_price_change = []
company_stock_price_change_percent = []
company_stock_trade_amount = []

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

def nametagsort(listA):
    ans = []
    find_num = 13
    name_num = 0
    stack = 1
    while name_num < 30:
        if listA[find_num] in company_name_list[name_num]:
            while find_num < len(listA):
                i = find_num + stack
                if listA[i] in company_name_list[name_num]:
                    stack += 1
                else:
                    ans.append(company_name_list[name_num])
                    name_num += 1
                    break
            find_num += stack
            stack = 1
        for i in range(11):
            try:
                ans.append(listA[find_num + i])
            except:
                pass
        find_num += 11
    return ans

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
    companylist = dividerstr(company.get_text())
    sortedcompany = nametagsort(companylist)
    memo = open("C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/naver_stock.txt", 'w')
    for i in range(len(sortedcompany)):                             # 이름, 현재가격, 전일비, 등락률, 거래량, 거래대금, 매수호가, 매도호가, 시가총액, PER, ROE 순서대로 반복해서 출력
        memo.write('\n' + str(i) + ' : ' + sortedcompany[i])
    for i in range(len(company_name_list)):                        # 이름 정렬 테스트용
        memo.write('\n' + str(i) + ' : ' + company_name_list[i])
    memo.close
else:
    print('response.status_code')