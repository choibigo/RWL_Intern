# A 씨는 게시판 프로그램을 작성하고 있다. 그런데 게시물의 총 개수와 한 페이지에 보여 줄 게시물 수를 입력받아 총 페이지 수를 출력하는 프로그램이 필요하다고 한다.
# m: 게시물의 총 개수
# n: 한 페이지에 보여 줄 게시물 수
def get_total_page(m,n):
    total = 0
    total =int(m/n + 1)

    return total


a = get_total_page(23,4)
print(a)