from flask import Flask, render_template, request, jsonify, redirect, url_for,flash
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

scheduler = BackgroundScheduler()

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'project-db-stu3.smhrd.com',
    'user': 'Insa4_IOTA_hacksim_1',
    'password': 'aishcool1',
    'database': 'Insa4_IOTA_hacksim_1',
    'port': 3307
}
db = mysql.connector.connect(
    host='project-db-stu3.smhrd.com',
    user='Insa4_IOTA_hacksim_1',
    passwd='aishcool1',
    db='Insa4_IOTA_hacksim_1',
    port=3307
)

def is_duplicate_id(admin_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM admin WHERE admin_id= %s"
    cursor.execute(sql, (admin_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# DB에서 온습도 데이터 가져오기
def get_temp_hum(): 
    connection = mysql.connector.connect(**db_config)   # DB에 연결하기                    
    cursor = connection.cursor()

    query = "SELECT Temp_Value FROM temp ORDER BY DateTime DESC LIMIT 1" # 가장 최근 데이터 하나 가져오기
    cursor.execute(query)
    temp = cursor.fetchone()[0] # 첫번째 컬럼값 하나 가져오기

    query = "SELECT REHum_Value FROM rehum ORDER BY DateTime DESC LIMIT 1"
    cursor.execute(query)
    hum = cursor.fetchone()[0]

    cursor.close()       # DB 커서 닫기
    connection.close()   # DB 연결 닫기

    return temp, hum



@app.route('/')
def index():
    return render_template('login1.html')  # HTML 파일 이름

@scheduler.scheduled_job('interval', minutes=30)
def update_data():
    temp, hum = get_temp_hum()
    app.config['TEMP'] = temp
    app.config['HUM'] = hum

scheduler.start()

app.config['TEMP'] = None
app.config['HUM'] = None


# TEMP 라우트에서 온습도 값 가져오는 함수 호출
@app.route('/TEMP')
def temp():
    temp = app.config['TEMP']
    hum = app.config['HUM']
    return render_template('TEMP.html', temp=temp, hum=hum)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT admin_id, admin_pw FROM admin WHERE admin_id = %s AND admin_pw = %s"
    # query2 = "SELECT * FROM admin"
    cursor.execute(query, (username, password))
    # cursor.execute(query2)
    result = cursor.fetchone()
    print(result)

    cursor.close()
    connection.close()

    if result:
        return render_template('HOME.html') , 200
    else:
        return "<h2>로그인 실패</h2>", 400
    

# @app.route('/signup')
# def signup_page():
#     return render_template('register.html')


# @app.route('/signup', methods=['POST'])
# def signup():
#     if request.method == 'POST':
#         admin_id = request.form['ADMIN_ID']
#         admin_pw = request.form['ADMIN_PW']
#         company = request.form['COMPANY']
#         ph = request.form['PH']

#         if is_duplicate_id(admin_id):
#             return "이미 사용 중인 아이디입니다."

#         cursor = db.cursor()
#         sql = "INSERT INTO admin (ADMIN_ID, ADMIN_PW, COMPANY, PH) VALUES (%s, %s, %s, %s)"
#         values = (admin_id, admin_pw, company, int(ph))

#         cursor.execute(sql, values)
#         db.commit()
#         cursor.close()

#         return redirect(url_for('signup_success'))  # 회원가입 성공 페이지로 리다이렉트
    
# @app.route('/signup_success')
# def signup_success():
#     return render_template('signup_success.html')  # 회원가입 성공 페이지 렌더링

    

# @app.route('/check_id_duplicate/<admin_id>')
# def check_id_duplicate(admin_id):
#     cursor = db.cursor()
#     sql = "SELECT COUNT(*) FROM admin WHERE ADMIN_ID = %s"
#     cursor.execute(sql, (admin_id,))
#     count = cursor.fetchone()[0]
#     cursor.close()

#     if count > 0:
#         return "duplicate"
#     else:
#         return "not_duplicate"



# @app.route('/connect')
# def connect():
#     return render_template('connect.html')


if __name__ == '__main__':
    app.run(debug=True)
