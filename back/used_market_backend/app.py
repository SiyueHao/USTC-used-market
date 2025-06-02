from flask import Flask, request, jsonify
from models import init_db, add_user, verify_user, add_item, list_items

app = Flask(__name__)
init_db()  # 程序启动时自动创建数据库和表

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    success = add_user(data['username'], data['password'])
    if success:
        return jsonify({"message": "注册成功"})
    else:
        return jsonify({"message": "用户名已存在"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if verify_user(data['username'], data['password']):
        return jsonify({"message": "登录成功"})
    else:
        return jsonify({"message": "用户名或密码错误"}), 401

@app.route('/add_item', methods=['POST'])
def add():
    data = request.json
    add_item(data['title'], data['description'], data['seller'])
    return jsonify({"message": "商品添加成功"})

@app.route('/items', methods=['GET'])
def items():
    result = list_items()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
