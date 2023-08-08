from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def HOME():
    return render_template('home.html')

@app.route('/temp')
def TEMP():
    return render_template('TEMP.html')

@app.route('/spec')
def SPEC():
    return render_template('SPEC.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)