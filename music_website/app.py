from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chatbot import chatbot_response, cypher_json

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for the entire application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def process_chatbot_request():
    data = request.get_json()
    input_string = data.get('inputString')
    response = chatbot_response(input_string)
    return jsonify({'outputString': response})

@app.route('/cypher', methods=['POST'])
def process_cypher_request():
    data = request.get_json()
    input_string = data.get('inputString')
    response = cypher_json(input_string)
    return jsonify({'cypherString': response})




if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000) # 修改代码后不用重新启动app.py，网页就会自动刷新; host='0.0.0.0'才能让其他机器访问; 默认端口5000