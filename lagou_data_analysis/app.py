# _*_ coding : UTF-8 _*_
# 开发人员："夏沫丶"
# 开发时间： 2020/1/16 21:29
# 文件名称： app.py
# 开发工具： PyCharm
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=80)
