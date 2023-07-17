from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('campusTalk.db')
    cur = conn.cursor()
    return conn, cur

def execute_sql_file():
    conn, cur = get_db()
    with open('schema.sql', 'r') as f:
        sql_script = f.read()
    cur.executescript(sql_script)
    conn.commit()
    conn.close()

execute_sql_file()


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    pwd = request.form.get('pwd')

    if not username or not pwd:
        return jsonify({'message': '注册失败', 'errorMessage': '用户名或密码不能为空'})

    db = get_db()
    cursor = db.cursor()

    # 检查用户名是否已经存在
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'message': '注册失败', 'errorMessage': '用户名已经被占用'})

    cursor.execute('INSERT INTO users (username, pwd) VALUES (?, ?)', (username, pwd))
    db.commit()
    return jsonify({'message': '注册成功', 'errorMessage': None})


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    pwd = request.form.get('pwd')

    if not username or not pwd:
        return jsonify({'message': '登录失败', 'errorMessage': '用户名或密码不能为空'})

    db = get_db()
    cursor = db.cursor()

    # 查询用户是否存在，并验证密码是否正确
    cursor.execute('SELECT * FROM users WHERE username = ? AND pwd = ?', (username, pwd))
    user = cursor.fetchone()
    if user:
        return jsonify({'message': '登录成功', 'errorMessage': None})
    else:
        return jsonify({'message': '登录失败', 'errorMessage': '用户名或密码错误'})


if __name__ == '__main__':
    app.run(port=80, debug=True)