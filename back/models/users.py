import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'campus_market.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 1. 用户注册函数
def create_user(username, password, email=None, phone=None, register_method='email', address=None):
    """
    注册新用户，密码加密存储
    参数:
        username: 用户名，唯一
        password: 明文密码，会在函数内加密
        email: 邮箱，可选
        phone: 电话，可选
        register_method: 注册方式，'email'或'phone'
        address: 联系地址，可选
    返回:
        新增用户的id
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password, email, phone, register_method, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, email, phone, register_method, address))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"数据库错误: {e}")
        user_id = None
    finally:
        conn.close()

    return user_id


# 2.查找用户（根据邮箱或手机号）
def get_user_by_identifier(identifier):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? OR phone = ?', (identifier, identifier))
    user = cursor.fetchone()
    conn.close()
    return user

# 3.登录验证：返回用户行对象（如果成功），否则返回 None
def verify_user_password(identifier, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email = ? OR phone = ?
    ''', (identifier, identifier))
    user = cursor.fetchone()
    conn.close()

    if user and user['password'] == password:
        return user  # 返回用户 Row 对象
    else:
        return None


# 4. 修改用户联系信息（手机号和地址）
def update_user_contact(user_id, phone=None, address=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    fields = []
    params = []
    if phone is not None:
        fields.append('phone = ?')
        params.append(phone)
    if address is not None:
        fields.append('address = ?')
        params.append(address)

    if not fields:
        conn.close()
        return 0  # 无更新字段

    params.append(user_id)
    sql = f'UPDATE users SET {", ".join(fields)} WHERE id = ?'
    cursor.execute(sql, params)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

