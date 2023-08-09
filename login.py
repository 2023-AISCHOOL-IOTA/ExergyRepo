from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db_config = {
    'host': 'project-db-stu3.smhrd.com',
    'user': 'Insa4_IOTA_hacksim_5',
    'password': 'aishcool5',
    'database': 'Insa4_IOTA_hacksim_5',
    'port': 3307
}
db = mysql.connector.connect(
    host='project-db-stu3.smhrd.com',
    user='Insa4_IOTA_hacksim_5',
    passwd='aishcool5',
    db='Insa4_IOTA_hacksim_5',
    port=3307
)

def is_duplicate_id(admin_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM admin WHERE ADMIN_ID = %s"
    cursor.execute(sql, (admin_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

@app.route('/')
def index():
    return render_template('login1.html')  # HTML 파일 이름


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM admin WHERE ADMIN_ID = %s AND ADMIN_PW = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return jsonify({"message": "로그인 성공."}) , 200
    else:
        return jsonify({"message": "아이디 or 비밀번호가 올바르지 않습니다."}) , 401
    

@app.route('/signup')
def signup_page():
    return render_template('register.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        admin_id = request.form['ADMIN_ID']
        admin_pw = request.form['ADMIN_PW']
        company = request.form['COMPANY']
        ph = request.form['PH']

        if is_duplicate_id(admin_id):
            return "이미 사용 중인 아이디입니다."

        cursor = db.cursor()
        sql = "INSERT INTO admin (ADMIN_ID, ADMIN_PW, COMPANY, PH) VALUES (%s, %s, %s, %s)"
        values = (admin_id, admin_pw, company, int(ph))

        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        return redirect(url_for('signup_success'))  # 회원가입 성공 페이지로 리다이렉트
    
@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html')  # 회원가입 성공 페이지 렌더링

    

@app.route('/check_id_duplicate/<admin_id>')
def check_id_duplicate(admin_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM admin WHERE ADMIN_ID = %s"
    cursor.execute(sql, (admin_id,))
    count = cursor.fetchone()[0]
    cursor.close()

    if count > 0:
        return "duplicate"
    else:
        return "not_duplicate"



@app.route('/connect')
def connect():
    return render_template('connect.html')


if __name__ == '__main__':
    app.run(debug=True)
