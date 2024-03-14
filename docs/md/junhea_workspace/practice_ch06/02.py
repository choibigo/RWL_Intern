# ch06-3 게시판 페이징하기

# 게시물의 총 개수와 페이지당 보여 줄 게시물 수를 받아 총 페이지 수를 계산해 주는 함수를 만든다.

def calpage(a, b):
    page, remain = divmod(a, b)
    if remain == 0:
        return page
    else:
        return page+1