# 8번

f = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/Python_Coding_License_Examination_No20(up_to_No16)/question8_abc.txt", 'r')
listt = f.readlines()
f.close()
lis = []
for i in listt:
    i.strip()
    lis.append(i)
f = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/Python_Coding_License_Examination_No20(up_to_No16)/question8_abc.txt", 'w')
for i in range(len(lis)):
    f.write(lis[len(lis) - 1 - i])
    if i == 0:
        f.write('\n')
f.close()