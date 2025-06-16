import random
import pymysql
from datetime import datetime, timedelta

# Kết nối cơ sở dữ liệu MySQL
try:
    conn = pymysql.connect(
        host='localhost',
        port=3310,
        user='root',
        password='123',
        db='EcomRecomendation',
        charset='utf8mb4',
        connect_timeout=10,
        read_timeout=30
    )
    cursor = conn.cursor()

    # Lấy tất cả các user_id hợp lệ từ bảng accounts_account
    cursor.execute("SELECT id FROM accounts_account")
    valid_user_ids = [row[0] for row in cursor.fetchall()]

    # Lấy tất cả các product_id hợp lệ từ bảng store_product
    cursor.execute("SELECT id FROM store_product")
    valid_product_ids = [row[0] for row in cursor.fetchall()]

    # Hàm fake dữ liệu
    def generate_fake_event_data():
        event_types = ['view', 'cart', 'pay']  # Các loại sự kiện cần fake
        events_per_type = 200  # Tổng số sự kiện cho mỗi loại
        start_date = datetime.now() - timedelta(days=180)  # 6 tháng trước
        end_date = datetime.now()  # Hiện tại

        for event_type in event_types:
            for _ in range(events_per_type):  # Tạo 2000 bản ghi cho mỗi loại sự kiện
                # Chọn ngẫu nhiên các giá trị
                user_id = random.choice(valid_user_ids)  # Chọn user_id hợp lệ từ danh sách đã lấy
                product_id = random.choice([None, random.choice(valid_product_ids)])  # Chọn ngẫu nhiên sản phẩm hoặc để trống
                frequency = random.randint(1, 70)  # Tạo tần suất ngẫu nhiên từ 1 đến 70
                rating = random.choice([None, random.randint(1, 5)])  # Điểm đánh giá có thể có hoặc không

                # Chọn thời gian ngẫu nhiên trong khoảng 6 tháng
                event_timestamp = start_date + timedelta(days=random.randint(0, 180))  # Ngẫu nhiên trong 180 ngày
                event_hour = random.randint(0, 11)  # Ngẫu nhiên chọn 1 trong 12 khung giờ (0-11)
                event_timestamp = event_timestamp.replace(hour=event_hour * 2, minute=random.randint(0, 59))  # Phân bổ vào khung giờ 2 giờ
                event_timestamp_str = event_timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Chuyển đổi thành chuỗi

                # Chèn dữ liệu vào bảng `accounts_eventuser` nhiều lần nếu tần suất > 1
                for _ in range(frequency):
                    query = """
                    INSERT INTO accounts_eventuser (event_timestamp, event_type, product_id, user_id, frequency, rating)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (event_timestamp_str, event_type, product_id, user_id, frequency, rating))

        # Commit thay đổi vào cơ sở dữ liệu
        conn.commit()
        print("Dữ liệu giả đã được chèn vào cơ sở dữ liệu.")

    # Gọi hàm để tạo dữ liệu giả
    generate_fake_event_data()

except pymysql.MySQLError as e:
    print(f"Lỗi khi kết nối cơ sở dữ liệu: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()
