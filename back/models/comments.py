import sqlite3

def get_db():
    return sqlite3.connect("campus_market.db")

# 添加评价（只能添加一次）
def add_comment(order_id, buyer_id, seller_id, rating):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO comments (order_id, buyer_id, seller_id, rating)
            VALUES (?, ?, ?, ?)
        """, (order_id, buyer_id, seller_id, rating))
        conn.commit()
    except sqlite3.IntegrityError:
        print("该订单已评价或无效。")
    finally:
        conn.close()

# 获取某位用户作为卖家的所有评价
def get_comments_for_seller(seller_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM comments WHERE seller_id = ?
    """, (seller_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

# 获取卖家的平均评分
def get_average_rating_for_seller(seller_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(rating) FROM comments WHERE seller_id = ?
    """, (seller_id,))
    avg = cur.fetchone()[0]
    conn.close()
    return round(avg, 2) if avg else None

# 检查某订单是否已经评价
def has_commented(order_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM comments WHERE order_id = ?
    """, (order_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count > 0
