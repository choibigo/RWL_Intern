# Markdown guide

## **md파일 생성**
```bash
touch name.md
```
를 통해 마크다운 파일 생성 가능. **(Ctrl + Shift + v, Ctrl + k + v 로 미리보기 가능)**

## **제목**
```md
# 제목 1
## 제목 2
### 제목 3
#### 제목 4
##### 제목 5
###### 제목 6
```
- # 제목 1
- ## 제목 2
-  ### 제목 3
-  #### 제목 4
-  ##### 제목 5
-  ###### 제목 6

## 강조 (Emphasis)

*text*           >>>> 기울여 쓰기 (italic) : * 또는 _로 감싸는 텍스트 (`*text*`)  <br>
**text**         >>>> 두껍게 쓰기 (Bold) : ** 또는 __로 감싸는 텍스트 (`**text**`)  <br>
~~text~~         >>>> 취소선 : ~~로 감싼 텍스트 (`~~text~~`)  <br>


## 수평선(Horizontal Rules), 줄바꿈(Line Breaks), 인용(Blockquotes)
### 수평선

**\- 또는 \* 또는 \_ 을 3개 이상 작성.**

****
______
```
------
****
______
```

### 줄바꿈
> `<br>`은 줄바꿈만 수행, `enter`로 칸을 띄우면 다음행으로 한줄 띄우고 넘어감.

### 인용 <br>
`>`으로 시작하는 텍스트 (3개까지 가능)
> a
>> b
>>> c 

그 외에도 인용구 안에는 제목이나 리스트, 텍스트박스 넣을 수 있음
```
> # this is h1!
> * list
> `textbox`
```
> # this is h1!
> * list
> `textbox`

## Lists(목록)
*, +, - 를 이용해서 순서가 없는 목록 생성가능
```
* 머리
  * 코
    * 입  
     
+ 머리
    + 코
    + 입
      * 입

- 머리
- 코
- 입
```
* 머리
  * 코
    * 입
+ 머리
    + 코
    + 입
      * 입
- 머리
- 코
- 입

숫자를 기입하면 순서가 있는 목록 생성 (숫자는 큰 의미가 없고 순서대로 알아서 숫자 매겨짐)
```md
1. 머리
2. 다리
3. 뚝배기
5. 팔             -> 5번을 썻는데도 4번으로 표시된다.
```
1. 머리
2. 다리
3. 뚝배기
5. 팔 <!-- 5번을 썻는데도 4번으로 표시된다. -->

## Backslash Escapes
특수문자를 표현할 때, 표시될 문자 앞에 \를 넣고 특수문자를 사용
* 특수문자 출력안됨
- 특수문자 출력안됨

\* 특수문자 출력

\- 특수문자 출력


## 이미지, 링크

### 링크 넣기
```md
[Google](http://www.google.com "구글")  
[abcdef](http://www.google.com "구글")   -> 링크 이름 변경
```
[Google](http://www.google.com "구글")
[abcdef](http://www.google.com "구글")

### 내부(해시) 링크
```md
[줄바꿈](#줄바꿈)
```
[줄바꿈](#줄바꿈)


### 이미지 넣기
```md
링크와 비슷하지만 앞에 !가 붙음.
인라인 이미지 ![alt text](/test.png)
링크 이미지 ![alt text](image_URL)
이미지의 사이즈를 변경하기 위해서는 <img width="OOOpx" height="OOOpx"></img>와 같이 표현.
```

### 이미지를 링크로 사용.
```md
[ ![text](이미지URL) ]( 링크URL )
```
[![text](https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg)](https://google.com)

### 이미지 크기 조정
```md
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="400px" alt="sample image">
```
<a href="#">
	<img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="400px" alt="sample image">
</a>


## 코드블럭
\`\`\`\` 뒤에 `bash`, `cpp`, `python`, `md`와 같이 언어를 지정하여 syntax color적용 가능
```javascript
function test() {
 console.log("look ma’, no spaces");
}
```

## 체크 리스트
```
- [x] this is a complete item
- [ ] this is an incomplete item
```
- [x] this is a complete item
- [ ] this is an incomplete item

## Table
```
헤더1|헤더2|헤더3|헤더4
---|---|---|---
셀1|셀2|셀3|셀4
셀5|셀6|셀7|셀8
셀9|셀10|셀11|셀12
```
헤더1|헤더2|헤더3|헤더4
---|---|---|---
셀1|셀2|셀3|셀4
셀5|셀6|셀7|셀8
셀9|셀10|셀11|셀12

### 가운데 정렬
```
헤더1|헤더2|헤더3
:---|:---:|---:
Left|Center|Right
1|2|3
4|5|6
7|8|9
```

헤더1|헤더2|헤더3
:---|:---:|---:
Left|Center|Right
1|2|3
4|5|6
7|8|9

