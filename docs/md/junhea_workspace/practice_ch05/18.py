import math

ran = math.gcd(200, 80)

print(f'타일 한 선의 길이 : {ran}')
print(f'필요한 타일의 개수 : {int((200/ran)*(80/ran))}')