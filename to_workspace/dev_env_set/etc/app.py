# app.py
import os
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# ENV 실습: 환경변수에서 'USER_NAME'을 가져오고, 없으면 'Guest'를 씁니다.
user_name = os.getenv('USER_NAME', 'Guest')

# VOLUME 실습: 로그를 저장할 경로
log_path = '/data/access.log'

@app.route('/')
def hello():
    # 접속할 때마다 파일에 기록 (데이터 영속성 확인용)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{now}] Access from {user_name}\n")
    
    return f"Hello, {user_name}! Your visit has been recorded."

if __name__ == '__main__':
    # EXPOSE 실습: 5000번 포트로 실행
    app.run(host='0.0.0.0', port=5000)