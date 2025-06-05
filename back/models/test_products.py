import comments

def test_add_comment():
    print("测试：添加评论")
    order_id = 1
    buyer_id = 2
    seller_id = 1
    rating = 5
    comments.add_comment(order_id, buyer_id, seller_id, rating)
    print("评价已添加（或已存在）\n")

def test_get_comments_for_seller():
    print("测试：获取卖家所有评论")
    seller_id = 1
    all_comments = comments.get_comments_for_seller(seller_id)
    for c in all_comments:
        print(dict(c))
    print()

def test_get_average_rating():
    print("测试：获取卖家的平均评分")
    seller_id = 1
    avg = comments.get_average_rating_for_seller(seller_id)
    if avg:
        print(f"卖家平均评分为：{avg} 星")
    else:
        print("暂无评分")
    print()

def test_has_commented():
    print("测试：检查订单是否已评价")
    order_id = 1
    result = comments.has_commented(order_id)
    print(f"订单 {order_id} 是否已评价：{result}")
    print()

def run_all():
    test_add_comment()
    test_has_commented()
    test_get_comments_for_seller()
    test_get_average_rating()

if __name__ == "__main__":
    run_all()
