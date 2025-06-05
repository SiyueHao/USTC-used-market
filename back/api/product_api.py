# api/product_api.py

from flask import Blueprint, request, jsonify
from models import products

product_bp = Blueprint('product', __name__)

# 发布商品
@product_bp.route('/create', methods=['POST'])
def create():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    description = data.get('description', '')
    price = data.get('price')
    tag = data.get('tag', '')
    images = data.get('images', [])  # 应该是列表

    if not all([user_id, name, price]):
        return jsonify({'success': False, 'message': 'user_id, name, price 必填'}), 400

    product_id = products.create_product(user_id, name, description, price, tag, images)
    return jsonify({'success': True, 'product_id': product_id})


# 修改商品信息
@product_bp.route('/update/<int:product_id>', methods=['PUT'])
def update(product_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    tag = data.get('tag')
    images = data.get('images')

    result = products.update_product(product_id, name, description, price, tag, images)
    if result:
        return jsonify({'success': True, 'message': '商品更新成功'})
    else:
        return jsonify({'success': False, 'message': '未提供有效更新字段'}), 400


# 上/下架商品
@product_bp.route('/set_status/<int:product_id>', methods=['PUT'])
def set_status(product_id):
    data = request.json
    status = data.get('status')
    result = products.set_product_status(product_id, status)
    if result:
        return jsonify({'success': True, 'message': f'商品状态更新为{status}'})
    else:
        return jsonify({'success': False, 'message': '无效的状态'}), 400


# 搜索商品
@product_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    tag = request.args.get('tag')
    result = products.search_products(keyword, tag)
    return jsonify([dict(row) for row in result])

# 根据标签筛选商品
@product_bp.route('/tag/<string:tag>', methods=['GET'])
def get_by_tag(tag):

    print(f"收到标签查询请求: {tag}")
    result = products.get_products_by_tag(tag)
    print(f"查询结果: {result}")
    return jsonify([dict(row) for row in result])

    result = products.get_products_by_tag(tag)
    return jsonify([dict(row) for row in result])

# 查看某用户发布的商品
@product_bp.route('/user/<int:user_id>', methods=['GET'])
def get_by_user(user_id):
    result = products.get_products_by_user(user_id)
    return jsonify([dict(row) for row in result])

