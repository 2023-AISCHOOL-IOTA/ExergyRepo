from flask import Flask, render_template, request, jsonify, redirect, url_for,flash
import mysql.connector


app = Flask(__name__)

app.secret_key = 'd4a6cb15-5e8e-4a69-9cbe-6f4ce1b09d1e'
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


# TEMP 라우트에서 온습도 값 가져오는 함수 호출
@app.route('/TEMP')
def temp():
    temp , hum = get_temp_hum()
    return render_template('TEMP.html', temp=temp, hum=hum)

@app.route('/insert_temp', methods=['GET'])
def insert_temp():
    connection = mysql.connector.connect(**db_config)
    sensor_id = request.args.get('sensor')
    temperature = request.args.get('temp')

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO temp (Sensor_ID, Temp_Value) VALUES (%s, %s)"
            cursor.execute(sql, (sensor_id, float(temperature)))
        connection.commit()
        return 'Success', 200
    except Exception as e:
        return str(e), 500


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
        flash("등록되지 않은 회원입니다.",'error')
        return redirect(url_for('index'))
    

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
    app.run(host='0.0.0.0', port=5000,debug=True)