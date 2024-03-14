# 9번

f = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/Python_Coding_License_Examination_No20(up_to_No16)/question9_sample.txt", 'r')
tem = f.readlines()
f.close()
score = []
for i in tem:
    i.strip()
    score.append(i)
all = 0
for i in score:
    all += int(i)

average = all / len(score)

f = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/Python_Coding_License_Examination_No20(up_to_No16)/question9_result.txt", 'w')
f.write(str(average))
f.close