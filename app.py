from flask import Flask, render_template, request, redirect, url_for
import thread_Youtube
app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def hello():
    if request.method == "POST":
        id = request.form["YouTuber"]
        content, time = thread_Youtube.run(id)
        return render_template('result.html',content=content, time=time)
    return render_template('search.html')

# @app.route("/result")
# def show_result(content):
#     return render_template('result.html',content=content)

if __name__ == 'main':
    app.run(host='127.0.0.1', port=5000, debug=False)