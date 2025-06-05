import sqlite3

def delete_tables():

    conn = sqlite3.connect('campus_market.db')
    cursor = conn.cursor()

 

    # 删除
 

    cursor.execute('''
            SELECT * FROM products;
        ''')

    conn.commit()
    conn.close()
    print("操作完成！")

if __name__ == '__main__':
    delete_tables()

    
