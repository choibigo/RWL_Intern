d= {'a': 'b'}

print(d)


fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5,
}

def make_lemonade(count):
    n = 1
    print(f'레몬 {count*n} 개로 레모네이드 {count//n} 개를 만듭니다.')
    fresh_fruit['레몬'] -= (count * n)
    print(f'레몬이 {fresh_fruit["레몬"]} 개 남았습니다.')

    
def out_of_stock():
    print(f'제료가 부족합니다. 재료를 보충해 주세요.')

count = fresh_fruit.get('레몬', 0)
print(fresh_fruit)

if count:
    make_lemonade(count)
else:
    out_of_stock()



fresh_fruit['레몬'] = 5  # 테스트를 위해 갯수 리셋

print(fresh_fruit)

print(a := fresh_fruit.get('lemon', 0))


fresh_fruit = {
    '사과': 10,
    '바나나': 8,
    '레몬': 5,
}

if count := fresh_fruit.get('lemon', 0): # if문 입력 중에 바로 무언가를 넣을 수 없다.
    print(count)

print(count)


numbers = [1 , 2]

if count := numbers[1] : # if문 입력 중에 바로 무언가를 넣을 수 없다.
    print(count)
