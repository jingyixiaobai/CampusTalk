from flask import Flask,request,jsonify

app = Flask(__name__)
@app.route("/post")
def post():
    return render_template("post.html")