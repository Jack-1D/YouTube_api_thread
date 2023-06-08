from flask import Flask, render_template, request, redirect, url_for
import thread_Youtube
import json
app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def hello():
    if request.method == "POST":
        dict = json.loads(request.form["YouTuber"])
        content, time = thread_Youtube.run(dict['id'])
        return render_template('result.html',content=content, time=time, name=dict['name'])
    return render_template('search.html')

if __name__ == 'main':
    app.run(host='127.0.0.1', port=5000, debug=False)