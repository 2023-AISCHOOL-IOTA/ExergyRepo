# html을 다른 사람이랑 공유
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')          # 기본 경로
def HOME():
    return render_template('home.html')

@app.route('/temp')      # 추가된 경로
def TEMP():
    return render_template('TEMP.html')

@app.route('/spec')      # 추가된 경로
def SPEC():
    return render_template('SPEC.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)    # 다른 사람들도 볼 수 있도록 open

# mysql에서 web으로 정보 보내는 방법
from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Flask 앱 코드 작성
# 1. MySQL 연결 설정
db = mysql.connector.connect(
    host='project-db-stu3.smhrd.com',     # local host
    user='Insa4_IOTA_hacksim_1',          # 사용자 이름
    passwd='aishcool1',                   # 패스워드
    db='Insa4_IOTA_hacksim_1',            # 데이터베이스 이름
    port=3307                             # 포트번호
)

# 2. 라우트 설정 - 
@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT id, name, email FROM users")  # 적절한 쿼리 사용

    users = cursor.fetchall()

    cursor.close()
    
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)











