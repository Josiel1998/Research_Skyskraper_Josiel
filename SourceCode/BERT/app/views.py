from app import app

from flask import render_template
from flask import request

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/about")
def about():
    return """
    <h1 style='color: red;'>I'm a red H1 heading!</h1>
    <p>This is a lovely little paragraph</p>
    <code>Flask is <em>awesome</em></code>
    """

@app.route("/bert", methods=['GET','POST'])
def server():
    if request.method == 'POST':
        text = request.form['text']
        return text
    else:
        return "THIS IS A GET"