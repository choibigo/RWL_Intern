f1 = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch04/test.txt", 'w')
f1.write("Life is too short")
f1.close()  ## 이 줄을 추가하면 오류가 사라진다. 항상 파일 사용 마지막에는 닫아줘야 한다. 이를 자주 잊을 것 같다면 with를 쓰도록 하자.

f2 = open("C:/anaconda3 for study/gitgit/uninstructed_robot-1/docs/md/junhea_workspace/practice_ch04/test.txt", 'r')
print(f2.read())
f2.close()