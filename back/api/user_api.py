# api/user_api.py
from flask import Blueprint, request, jsonify
from models import users  # 你写的 user.py 文件
import hashlib


#============api/user_api.py============#


# 创建蓝图
user_bp = Blueprint('user', __name__)


# 注册接口
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address', '')

    if not username or not password or (not email and not phone):
        return jsonify({'success': False, 'message': '用户名、密码和邮箱或手机号必须填写'}), 400

    register_method = 'email' if email else 'phone'

    # 直接使用明文密码（已去除哈希）
    result = users.create_user(username, password, email, phone, register_method, address)

    if result:
        return jsonify({'success': True, 'message': '注册成功'})
    else:
        return jsonify({'success': False, 'message': '用户已存在或注册失败'}), 500


# 登录接口
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('email') or data.get('phone')
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'success': False, 'message': '邮箱/手机号和密码必须填写'}), 400

    user = users.verify_user_password(identifier, password)

    if user:
        # 把 Row 对象转换为 dict 返回
        return jsonify({'success': True, 'message': '登录成功', 'user': dict(user)})
    else:
        return jsonify({'success': False, 'message': '登录失败，请检查信息是否正确'}), 401


# 获取用户信息接口
@user_bp.route('/update_contact/<int:user_id>', methods=['PUT'])
def update_contact(user_id):
    data = request.get_json()
    phone = data.get('phone')
    address = data.get('address')

    if not phone and not address:
        return jsonify({'success': False, 'message': '请至少提供电话或地址'}), 400

    from models import users
    updated_rows = users.update_user_contact(user_id, phone, address)

    if updated_rows == 0:
        return jsonify({'success': False, 'message': '更新失败，可能用户不存在或数据未变动'}), 404
    else:
        return jsonify({'success': True, 'message': '联系方式更新成功'})
