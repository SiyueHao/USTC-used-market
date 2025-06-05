import sqlite3

def get_db():
    return sqlite3.connect("campus_market.db")

# 创建订单
def create_order(product_id, buyer_id, seller_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (product_id, buyer_id, seller_id)
        VALUES (?, ?, ?)
    """, (product_id, buyer_id, seller_id))

    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id

# 获取订单信息
def get_order_by_id(order_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cur.fetchone()
    conn.close()
    return order

# 模拟付款（订单状态变为 completed）
def complete_order(order_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE orders SET status = 'completed'
        WHERE id = ?
    """, (order_id,))

    conn.commit()
    conn.close()

# 删除订单（仅允许删除未支付的）
def delete_order(order_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM orders
        WHERE id = ? AND status = 'pending'
    """, (order_id,))
    
    conn.commit()
    conn.close()

# 买家查看自己的订单记录
def get_orders_by_buyer(buyer_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM orders WHERE buyer_id = ?
    """, (buyer_id,))
    
    orders = cur.fetchall()
    conn.close()
    return orders

# 卖家查看自己的订单记录
def get_orders_by_seller(seller_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM orders WHERE seller_id = ?
    """, (seller_id,))
    
    orders = cur.fetchall()
    conn.close()
    return orders
