from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    paragraphs = [
        "Section 1", "Section 2", "Section 3"
    ]
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # 修改代码后不用重新启动app.py，网页就会自动刷新; host='0.0.0.0'才能让其他机器访问; 默认端口5000