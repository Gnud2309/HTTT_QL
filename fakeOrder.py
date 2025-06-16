# import pymysql
# import random
# from faker import Faker
# from faker.providers import BaseProvider
# from datetime import datetime, timedelta
#
#
# # Định nghĩa provider tùy chỉnh cho ward_name
# class VietnamAddressProvider(BaseProvider):
#     def ward_name(self):
#         wards = [
#             "Phường 1", "Phường 2", "Xã Tân Lập", "Xã Hòa Bình", "Phường Tân An",
#             "Xã Phú Thọ", "Phường Hòa Khánh", "Xã An Lộc"
#         ]
#         return random.choice(wards)
#
#
# # Khởi tạo Faker với locale vi_VN và thêm provider tùy chỉnh
# fake = Faker('vi_VN')
# fake.add_provider(VietnamAddressProvider)
#
# # Định nghĩa city_ids
# city_ids = {
#     'R1973756': 'VN-SG', 'R1875748': 'An Giang', 'R1873533': 'VN-55',
#     'R1904296': 'Bà Rịa–Vũng Tàu', 'R1902941': 'Bắc Giang', 'R1903471': 'Bắc Kạn',
#     'R1902690': 'Bắc Ninh', 'R1875968': 'Bến Tre', 'R1906037': 'Bình Dương',
#     'R1889794': 'Bình Định', 'R1898841': 'Bình Phước', 'R1904231': 'Bình Thuận',
#     'R1873490': 'Cà Mau', 'R1844412': 'Cao Bằng', 'R1874283': 'VN-CT',
#     'R1891418': 'VN-DN', 'R1884034': 'Đắk Lắk', 'R1884042': 'VN-72',
#     'R1903340': 'Điện Biên', 'R1904421': 'Đồng Nai', 'R1875866': 'Đồng Tháp',
#     'R1884018': 'Gia Lai', 'R1903478': 'Hà Giang', 'R1902686': 'Hải Dương',
#     'R1902682': 'Hải Phòng', 'R1901010': 'Hà Nam', 'R1903516': 'VN-HN',
#     'R1898458': 'Hà Tĩnh', 'R1874249': 'Hậu Giang', 'R1902973': 'Hòa Bình',
#     'R1901032': 'Hưng Yên', 'R1887959': 'Khánh Hòa', 'R1874471': 'Kiên Giang',
#     'R1879515': 'Kon Tum', 'R1903322': 'Lai Châu', 'R5522596': 'Lạng Sơn',
#     'R1903400': 'Lào Cai', 'R1885367': 'Lâm Đồng', 'R1877236': 'Long An',
#     'R1901008': 'Nam Định', 'R1898509': 'Nghệ An', 'R1900963': 'Ninh Bình',
#     'R1886159': 'Ninh Thuận', 'R1902930': 'Phú Thọ', 'R1889204': 'Phú Yên',
#     'R1896050': 'Quảng Bình', 'R1891352': 'Quảng Nam', 'R1890793': 'Quảng Ngãi',
#     'R1902947': 'Quảng Ninh', 'R1895630': 'Quảng Trị', 'R1873632': 'Sóc Trăng',
#     'R1903291': 'Sơn La', 'R1898961': 'Tây Ninh', 'R1901019': 'Thái Bình',
#     'R1902967': 'Thái Nguyên', 'R1898590': 'Thanh Hóa', 'R1891483': 'Thừa Thiên–Huế',
#     'R1876011': 'Tiền Giang', 'R1873642': 'Trà Vinh', 'R1903418': 'Tuyên Quang',
#     'R1875887': 'Vĩnh Long', 'R1902889': 'Vĩnh Phúc', 'R1903199': 'Yên Bái'
# }
#
# # Kết nối database
# try:
#     conn = pymysql.connect(
#         host='localhost',
#         port=3310,
#         user='root',
#         password='123',
#         db='EcomRecomendation',
#         charset='utf8mb4',
#         connect_timeout=10,
#         read_timeout=30
#     )
#     cursor = conn.cursor()
#
#     # Lấy sẵn id user, product, variation và kiểm tra dữ liệu
#     cursor.execute("SELECT id FROM accounts_account")
#     user_ids = [row[0] for row in cursor.fetchall()]
#     if not user_ids:
#         raise ValueError("Bảng accounts_account rỗng!")
#
#     cursor.execute("SELECT id, price FROM store_product")
#     products = cursor.fetchall()
#     if not products:
#         raise ValueError("Bảng store_product rỗng!")
#
#     cursor.execute("SELECT id, Product_id FROM store_variation")
#     variations = cursor.fetchall()
#     if not variations:
#         raise ValueError("Bảng store_variation rỗng!")
#
#     PAYMENT_METHODS = ['VNPAY', 'COD', 'MOMO']
#
#
#     def random_date_within_six_months():
#         now = datetime.now()
#         months = random.randint(0, 6)  # Chọn một ngày ngẫu nhiên trong 6 tháng qua
#         return now - timedelta(days=months * 30 + random.randint(0, 29))
#
#
#
#     ORDER_STATUS_PROBABILITIES = {
#         'Accepted': 0.30,
#         'Ready to ship': 0.15,
#         'On shipping': 0.10,
#         'Delivered': 0.20,
#         'Cancelled': 0.20,
#         'Return': 0.05
#     }
#
#
#     payment_data = []
#     order_data = []
#     orderproduct_data = []
#     orderproduct_variation_data = []
#
#     for i in range(2000):  # Tạo 2000 đơn hàng trong 6 tháng qua
#         user_id = random.choice(user_ids)
#         product_id, product_price = random.choice(products)
#
#         # Chọn trạng thái đơn hàng theo tỷ lệ đã cho
#         order_status = random.choices(
#             list(ORDER_STATUS_PROBABILITIES.keys()),
#             list(ORDER_STATUS_PROBABILITIES.values())
#         )[0]
#
#         payment_method = random.choice(PAYMENT_METHODS)
#         created_at = random_date_within_six_months()  # Thời gian trong 6 tháng qua
#         amount_paid = random.randint(100, 10000)
#
#         # Tạo payment_id duy nhất
#         while True:
#             payment_id = fake.random_number(digits=8)
#             cursor.execute("SELECT COUNT(*) FROM orders_payment WHERE payment_id = %s", (payment_id,))
#             if cursor.fetchone()[0] == 0:
#                 break
#
#         # Chuẩn bị dữ liệu payment
#         payment_data.append((payment_id, payment_method, amount_paid,
#                              'Completed' if order_status != 'Cancelled' else 'Cancelled', created_at, user_id))
#
#         # Chuẩn bị dữ liệu order
#         city_code = random.choice(list(city_ids.keys()))
#         order_data.append((user_id, None, fake.unique.bothify(text='R########'), fake.name(), fake.phone_number(),
#                            fake.email(), payment_method, fake.street_address(), fake.ward_name(), fake.city_suffix(),
#                            city_code, fake.sentence(), amount_paid, round(amount_paid * 0.05, 2), order_status,
#                            '127.0.0.1', 1, created_at, created_at, 1, order_status, 1))
#
#         # Chuẩn bị dữ liệu orderproduct
#         orderproduct_data.append(
#             (None, None, user_id, product_id, random.randint(1, 5), product_price, 1, created_at, created_at, 0))
#
#         # Chuẩn bị dữ liệu orderproduct_variation
#         product_variation_ids = [v[0] for v in variations if v[1] == product_id]
#         variation_id = random.choice(product_variation_ids) if product_variation_ids else random.choice(variations)[0]
#         orderproduct_variation_data.append((None, variation_id))
#
#         if (i + 1) % 100 == 0 or i == 1999:
#             # Chèn payment và lấy payment_ids
#             cursor.executemany("""
#                 INSERT INTO orders_payment (payment_id, payment_method, amount_paid, status, created_at, user_id)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#             """, payment_data)
#             conn.commit()
#             cursor.execute("SELECT id FROM orders_payment ORDER BY id DESC LIMIT %s", (len(payment_data),))
#             payment_ids = [row[0] for row in cursor.fetchall()][::-1]
#
#             # Chèn order và lấy order_ids
#             cursor.executemany("""
#                 INSERT INTO orders_order (
#                     user_id, payment_id, order_number, full_name, phone, email, payment_method,
#                     road, ward, district, city, order_note, order_total, tax, status, ip,
#                     is_ordered, created_at, updated_at, total_items, order_status, is_view
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, order_data)
#             conn.commit()
#             cursor.execute("SELECT id FROM orders_order ORDER BY id DESC LIMIT %s", (len(order_data),))
#             order_ids = [row[0] for row in cursor.fetchall()][::-1]
#
#             # Cập nhật orderproduct với order_id và payment_id
#             for j in range(len(orderproduct_data)):
#                 orderproduct_data[j] = (order_ids[j], payment_ids[j],) + orderproduct_data[j][2:]
#             cursor.executemany("""
#                 INSERT INTO orders_orderproduct (
#                     order_id, payment_id, user_id, product_id, quantity, product_price, ordered, created_at, updated_at, discount_amount
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#             """, orderproduct_data)
#             conn.commit()
#             orderproduct_ids = [cursor.lastrowid - len(orderproduct_data) + 1 + j for j in
#                                 range(len(orderproduct_data))]
#
#             # Cập nhật orderproduct_variation với orderproduct_id
#             for j in range(len(orderproduct_variation_data)):
#                 orderproduct_variation_data[j] = (orderproduct_ids[j],) + orderproduct_variation_data[j][1:]
#             cursor.executemany("""
#                 INSERT INTO orders_orderproduct_variation (orderproduct_id, variation_id)
#                 VALUES (%s, %s)
#             """, orderproduct_variation_data)
#             conn.commit()
#
#             # Reset danh sách
#             payment_data = []
#             order_data = []
#             orderproduct_data = []
#             orderproduct_variation_data = []
#
#             print(f"Đã fake {i + 1} đơn hàng")
#
#     print("Hoàn thành fake 2000 đơn hàng trong 6 tháng!")
#
# except Exception as e:
#     print(f"Lỗi: {e}")
# finally:
#     cursor.close()
#     conn.close()


import pymysql
import random
from faker import Faker
from faker.providers import BaseProvider
from datetime import datetime, timedelta


# Định nghĩa provider tùy chỉnh cho ward_name
class VietnamAddressProvider(BaseProvider):
    def ward_name(self):
        wards = [
            "Phường 1", "Phường 2", "Xã Tân Lập", "Xã Hòa Bình", "Phường Tân An",
            "Xã Phú Thọ", "Phường Hòa Khánh", "Xã An Lộc"
        ]
        return random.choice(wards)


# Khởi tạo Faker với locale vi_VN và thêm provider tùy chỉnh
fake = Faker('vi_VN')
fake.add_provider(VietnamAddressProvider)

# Định nghĩa city_ids
city_ids = {
    'R1973756': 'VN-SG', 'R1875748': 'An Giang', 'R1873533': 'VN-55',
    'R1904296': 'Bà Rịa–Vũng Tàu', 'R1902941': 'Bắc Giang', 'R1903471': 'Bắc Kạn',
    'R1902690': 'Bắc Ninh', 'R1875968': 'Bến Tre', 'R1906037': 'Bình Dương',
    'R1889794': 'Bình Định', 'R1898841': 'Bình Phước', 'R1904231': 'Bình Thuận',
    'R1873490': 'Cà Mau', 'R1844412': 'Cao Bằng', 'R1874283': 'VN-CT',
    'R1891418': 'VN-DN', 'R1884034': 'Đắk Lắk', 'R1884042': 'VN-72',
    'R1903340': 'Điện Biên', 'R1904421': 'Đồng Nai', 'R1875866': 'Đồng Tháp',
    'R1884018': 'Gia Lai', 'R1903478': 'Hà Giang', 'R1902686': 'Hải Dương',
    'R1902682': 'Hải Phòng', 'R1901010': 'Hà Nam', 'R1903516': 'VN-HN',
    'R1898458': 'Hà Tĩnh', 'R1874249': 'Hậu Giang', 'R1902973': 'Hòa Bình',
    'R1901032': 'Hưng Yên', 'R1887959': 'Khánh Hòa', 'R1874471': 'Kiên Giang',
    'R1879515': 'Kon Tum', 'R1903322': 'Lai Châu', 'R5522596': 'Lạng Sơn',
    'R1903400': 'Lào Cai', 'R1885367': 'Lâm Đồng', 'R1877236': 'Long An',
    'R1901008': 'Nam Định', 'R1898509': 'Nghệ An', 'R1900963': 'Ninh Bình',
    'R1886159': 'Ninh Thuận', 'R1902930': 'Phú Thọ', 'R1889204': 'Phú Yên',
    'R1896050': 'Quảng Bình', 'R1891352': 'Quảng Nam', 'R1890793': 'Quảng Ngãi',
    'R1902947': 'Quảng Ninh', 'R1895630': 'Quảng Trị', 'R1873632': 'Sóc Trăng',
    'R1903291': 'Sơn La', 'R1898961': 'Tây Ninh', 'R1901019': 'Thái Bình',
    'R1902967': 'Thái Nguyên', 'R1898590': 'Thanh Hóa', 'R1891483': 'Thừa Thiên–Huế',
    'R1876011': 'Tiền Giang', 'R1873642': 'Trà Vinh', 'R1903418': 'Tuyên Quang',
    'R1875887': 'Vĩnh Long', 'R1902889': 'Vĩnh Phúc', 'R1903199': 'Yên Bái'
}

# Kết nối database
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

    # Lấy sẵn id user, product, variation và kiểm tra dữ liệu
    cursor.execute("SELECT id FROM accounts_account")
    user_ids = [row[0] for row in cursor.fetchall()]
    if not user_ids:
        raise ValueError("Bảng accounts_account rỗng!")

    cursor.execute("SELECT id, price FROM store_product")
    products = cursor.fetchall()
    if not products:
        raise ValueError("Bảng store_product rỗng!")

    cursor.execute("SELECT id, Product_id FROM store_variation")
    variations = cursor.fetchall()
    if not variations:
        raise ValueError("Bảng store_variation rỗng!")

    PAYMENT_METHODS = ['VNPAY', 'COD', 'MOMO']


    def random_date_within_day():
        now = datetime.now()
        hours = random.randint(0, 23)  # Chọn ngẫu nhiên giờ trong ngày
        minutes = random.randint(0, 59)
        return now.replace(hour=hours, minute=minutes, second=0, microsecond=0)


    # Tỷ lệ phân chia trạng thái đơn hàng
    ORDER_STATUS_PROBABILITIES = {
        'Accepted': 0.30,  # 30%
        'Ready to ship': 0.15,  # 15%
        'On shipping': 0.10,  # 10%
        'Delivered': 0.20,  # 20%
        'Cancelled': 0.20,  # 20%
        'Return': 0.05  # 5%
    }

    # Danh sách để lưu các bản ghi trước khi chèn
    payment_data = []
    order_data = []
    orderproduct_data = []
    orderproduct_variation_data = []

    orders_per_hour = 2000 // 24  # Số đơn hàng cho mỗi giờ (chia đều)

    for i in range(2000):  # Tạo 2000 đơn hàng
        # Chọn giờ để phân bổ đều trong ngày
        hour_of_day = i // orders_per_hour
        created_at = random_date_within_day().replace(hour=hour_of_day)  # Giới hạn giờ cho mỗi đơn hàng

        user_id = random.choice(user_ids)
        product_id, product_price = random.choice(products)

        # Chọn trạng thái đơn hàng theo tỷ lệ đã cho
        order_status = random.choices(
            list(ORDER_STATUS_PROBABILITIES.keys()),
            list(ORDER_STATUS_PROBABILITIES.values())
        )[0]

        payment_method = random.choice(PAYMENT_METHODS)
        amount_paid = random.randint(100, 10000)

        # Tạo payment_id duy nhất
        while True:
            payment_id = fake.random_number(digits=8)
            cursor.execute("SELECT COUNT(*) FROM orders_payment WHERE payment_id = %s", (payment_id,))
            if cursor.fetchone()[0] == 0:
                break

        # Chuẩn bị dữ liệu payment
        payment_data.append((payment_id, payment_method, amount_paid,
                             'Completed' if order_status != 'Cancelled' else 'Cancelled', created_at, user_id))

        # Chuẩn bị dữ liệu order
        city_code = random.choice(list(city_ids.keys()))
        order_data.append((user_id, None, fake.unique.bothify(text='R########'), fake.name(), fake.phone_number(),
                           fake.email(), payment_method, fake.street_address(), fake.ward_name(), fake.city_suffix(),
                           city_code, fake.sentence(), amount_paid, round(amount_paid * 0.05, 2), order_status,
                           '127.0.0.1', 1, created_at, created_at, 1, order_status, 1))

        # Chuẩn bị dữ liệu orderproduct
        orderproduct_data.append(
            (None, None, user_id, product_id, random.randint(1, 5), product_price, 1, created_at, created_at, 0))

        # Chuẩn bị dữ liệu orderproduct_variation
        product_variation_ids = [v[0] for v in variations if v[1] == product_id]
        variation_id = random.choice(product_variation_ids) if product_variation_ids else random.choice(variations)[0]
        orderproduct_variation_data.append((None, variation_id))

        if (i + 1) % 100 == 0 or i == 1999:
            # Chèn payment và lấy payment_ids
            cursor.executemany("""
                INSERT INTO orders_payment (payment_id, payment_method, amount_paid, status, created_at, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, payment_data)
            conn.commit()
            cursor.execute("SELECT id FROM orders_payment ORDER BY id DESC LIMIT %s", (len(payment_data),))
            payment_ids = [row[0] for row in cursor.fetchall()][::-1]

            # Chèn order và lấy order_ids
            cursor.executemany("""
                INSERT INTO orders_order (
                    user_id, payment_id, order_number, full_name, phone, email, payment_method,
                    road, ward, district, city, order_note, order_total, tax, status, ip,
                    is_ordered, created_at, updated_at, total_items, order_status, is_view
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, order_data)
            conn.commit()
            cursor.execute("SELECT id FROM orders_order ORDER BY id DESC LIMIT %s", (len(order_data),))
            order_ids = [row[0] for row in cursor.fetchall()][::-1]

            # Cập nhật orderproduct với order_id và payment_id
            for j in range(len(orderproduct_data)):
                orderproduct_data[j] = (order_ids[j], payment_ids[j],) + orderproduct_data[j][2:]
            cursor.executemany("""
                INSERT INTO orders_orderproduct (
                    order_id, payment_id, user_id, product_id, quantity, product_price, ordered, created_at, updated_at, discount_amount
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, orderproduct_data)
            conn.commit()
            orderproduct_ids = [cursor.lastrowid - len(orderproduct_data) + 1 + j for j in
                                range(len(orderproduct_data))]

            # Cập nhật orderproduct_variation với orderproduct_id
            for j in range(len(orderproduct_variation_data)):
                orderproduct_variation_data[j] = (orderproduct_ids[j],) + orderproduct_variation_data[j][1:]
            cursor.executemany("""
                INSERT INTO orders_orderproduct_variation (orderproduct_id, variation_id)
                VALUES (%s, %s)
            """, orderproduct_variation_data)
            conn.commit()

            # Reset danh sách
            payment_data = []
            order_data = []
            orderproduct_data = []
            orderproduct_variation_data = []

            print(f"Đã fake {i + 1} đơn hàng")

    print("Hoàn thành fake 2000 đơn hàng phân bố đều trong 24 giờ!")

except Exception as e:
    print(f"Lỗi: {e}")
finally:
    cursor.close()
    conn.close()
