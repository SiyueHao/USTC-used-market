import sqlite3

def init_db():
    conn = sqlite3.connect('campus_market.db')
    cursor = conn.cursor()


    # 创建用户表
    cursor.execute('''
        CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT UNIQUE,
        register_method TEXT CHECK(register_method IN ('email', 'phone')),
        address TEXT
    );
        ''')

    # 创建商品表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        tags TEXT,
        status TEXT NOT NULL CHECK(status IN ('在售', '已下架')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (seller_id) REFERENCES users(id)
    );
    ''')

    # 创建商品图片表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    ''')

    # 创建订单表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL CHECK(status IN ('待付款', '已完成')),
        FOREIGN KEY (buyer_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    );
    ''')

    # 创建订单评论表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment TEXT,
        comment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # 创建交易记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL UNIQUE,
        buyer_id INTEGER NOT NULL,
        seller_id INTEGER NOT NULL,
        rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
        review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (buyer_id) REFERENCES users(id),
        FOREIGN KEY (seller_id) REFERENCES users(id)
    );
    ''')

    # 创建销售数据统计
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_stats (
        tag TEXT PRIMARY KEY,
        sales_count INTEGER DEFAULT 0 
    );
    ''')

    conn.commit()
    conn.close()
    print("数据库初始化完成！")

if __name__ == '__main__':
    init_db()


