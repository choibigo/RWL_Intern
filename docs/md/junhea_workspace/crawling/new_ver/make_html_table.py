#html 에서 table 내용 채워주는 프로그램

f = open("C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/new_ver/naver_stock.txt", 'r')
listt = f.readlines()
f.close()

a = []
for j in listt:
    j = j.strip()
    a.append(j)

for i in range(len(a)):
    if str(a[i])[2] == ':' or str(a[i])[2] == ' ':
        if str(a[i])[1] == ':' or str(a[i])[1] == ' ':
            a[i] = str(a[i])[4:]
        else:
            a[i] = str(a[i])[5:]
    else:
        a[i] = str(a[i])[6:]

f = open("C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/crawling/new_ver/for_html.txt", 'w')
for i in range(30):
    f.write('<tr>\n')
    f.write('   <td>%2s</td>\n'%(i+1))
    f.write('   <td>%s</td>\n'%a[12*i])
    f.write('   <td>%6s</td>\n'%a[12*i+1])
    f.write('   <td>%5s</td>\n'%a[12*i+2])
    f.write('   <td>{0}{1:>6}</td>\n'.format(str(a[12*i+3])[0], str(a[12*i+3])[1:]))
    f.write('   <td>%11s</td>\n'%a[12*i+4])
    f.write('   <td>%9s</td>\n'%a[12*i+5])
    f.write('   <td>%6s</td>\n'%a[12*i+6])
    f.write('   <td>%6s</td>\n'%a[12*i+7])
    f.write('   <td>%9s</td>\n'%a[12*i+8])
    f.write('   <td>%6s</td>\n'%a[12*i+9])
    f.write('   <td>%6s</td>\n'%a[12*i+10])
    f.write('</tr>\n')

f.close()