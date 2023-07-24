from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect
from extension import db
from models import User, Reply, Article
from datetime import datetime
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusTalk.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.cli.command()
def create():
    db.drop_all()
    db.create_all()


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get('user_id'):
            # 用户未登录，重定向到登录页面
            return redirect('/login')

        # 用户已登录，执行原始视图函数
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        pwd = request.form.get('pwd')

        if not username or not pwd:
            return jsonify({'message': '登录失败', 'errorMessage': '用户名或密码不能为空'})

        # 查询用户是否存在，并验证密码是否正确
        user = User.query.filter_by(username=username, pwd=pwd).first()
        if user:
            session['user_id'] = user.id
            return jsonify({'message': '登录成功', 'errorMessage': None, "back": session.get("back")})
        else:
            return jsonify({'message': '登录失败', 'errorMessage': '用户名或密码错误'})
    return render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        pwd = request.form.get('pwd')

        if not username or not pwd:
            return jsonify({'message': '注册失败', 'errorMessage': '用户名或密码不能为空'})

        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'message': '注册失败', 'errorMessage': '用户名已经被占用'})

        user = User(username=username, pwd=pwd)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': '注册成功', 'errorMessage': None})

    return render_template('register.html')


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect('/')


@app.route("/")
def index():
    articles = Article.query.order_by(Article.create_time.desc()).all()
    return render_template("main.html", articles=articles)


@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        if not session.get("user_id"):
            session["back"] = "/post"
            return jsonify({'message': '跳转登录', 'errorMessage': "未登录"})

        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return jsonify({'message': '发布失败', 'errorMessage': '标题或内容不能为空'})
        if len(title) > 30:
            return jsonify({'message': '发布失败', 'errorMessage': '标题不能超过30个字'})
        article = Article(title=title, content=content, author_id=session["user_id"])
        db.session.add(article)
        db.session.commit()
        return jsonify({'message': '发布成功', 'errorMessage': None})
    return render_template('post.html')


@app.route('/setting', methods=["GET", "POST"])
def setting():
    return render_template('setting.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
