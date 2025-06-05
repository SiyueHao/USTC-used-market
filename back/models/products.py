# models/products.py
import sqlite3

DB_PATH = 'campus_market.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 1. 发布商品
def create_product(user_id, name, description, price, tag, image_paths):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (user_id, name, description, price, tag, image1, image2, image3)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, name, description, price, tag,
        image_paths[0] if len(image_paths) > 0 else None,
        image_paths[1] if len(image_paths) > 1 else None,
        image_paths[2] if len(image_paths) > 2 else None
    ))
    conn.commit()
    product_id = cursor.lastrowid
    conn.close()
    return product_id


# 2. 修改商品（仅限发布者）
def update_product(product_id, name=None, description=None, price=None, tag=None, image_paths=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    fields = []
    params = []

    if name:
        fields.append("name = ?")
        params.append(name)
    if description:
        fields.append("description = ?")
        params.append(description)
    if price is not None:
        fields.append("price = ?")
        params.append(price)
    if tag:
        fields.append("tag = ?")
        params.append(tag)
    if image_paths:
        if len(image_paths) > 0:
            fields.append("image1 = ?")
            params.append(image_paths[0])
        if len(image_paths) > 1:
            fields.append("image2 = ?")
            params.append(image_paths[1])
        if len(image_paths) > 2:
            fields.append("image3 = ?")
            params.append(image_paths[2])

    if not fields:
        conn.close()
        return False

    params.append(product_id)
    sql = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    return True


# 3. 商品上下架
def set_product_status(product_id, status):
    if status not in ['on_sale', 'off_shelf']:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE products SET status = ? WHERE id = ?', (status, product_id))
    conn.commit()
    conn.close()
    return True


# 4. 搜索商品（改进版，增加灵活匹配）
def search_products(keyword=None, tag=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE status = 'on_sale'"
    params = []

    if keyword:
        # 转为小写并加通配符
        like_kw = f"%{keyword.lower()}%"
        query += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        params.extend([like_kw, like_kw])

    if tag:
        query += " AND tag = ?"
        params.append(tag)

    cursor.execute(query, params)
    products = cursor.fetchall()
    conn.close()
    return products



# 5. 获取商品详情（可选）
def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

# 6.根据标签筛选在售商品
def get_products_by_tag(tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE tag = ? AND status = 'on_sale'"
    cursor.execute(query, (tag,))
    products = cursor.fetchall()
    conn.close()
    return products

# 7. 获取用户发布的商品（无论是否下架）
def get_products_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE user_id = ? ORDER BY created_at DESC"
    cursor.execute(query, (user_id,))
    products = cursor.fetchall()
    conn.close()
    return products
