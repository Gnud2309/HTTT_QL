USE DataWarehouse;

INSERT INTO bronze.crm_cust_info (cst_id, cst_username, cst_email, cst_fullname, cst_phone_number, cst_date_joined, cst_last_login, profile_picture, bio, date_of_birth, sex, city, district, ward, road) VALUES
(1, 'john.doe', 'john.doe@example.com', 'John Doe', '0912345678', '2023-01-15 10:30:00', '2025-06-10 08:00:00', 'http://example.com/pic1.jpg', 'Loves hiking and photography.', '1990-05-20', 'Male', 'Ho Chi Minh City', 'District 1', 'Ben Nghe', 'Nguyen Hue Street'),
(2, 'jane.smith', 'jane.smith@example.com', 'Jane Smith', '0987654321', '2023-02-20 11:00:00', '2025-06-11 09:15:00', 'http://example.com/pic2.jpg', 'Food blogger and avid reader.', '1992-08-12', 'Female', 'Hanoi', 'Hoan Kiem', 'Trang Tien', 'Dinh Tien Hoang Street'),
(3, 'alice.j', 'alice.j@example.com', 'Alice Johnson', '0911223344', '2023-03-10 14:00:00', '2025-06-12 11:30:00', 'http://example.com/pic3.jpg', 'Software developer.', '1988-11-30', 'Female', 'Da Nang', 'Hai Chau', 'Thach Thang', 'Bach Dang Street'),
(4, 'bob.w', 'bob.williams@example.com', 'Bob Williams', '0933445566', '2023-04-05 16:45:00', '2025-06-09 14:00:00', 'http://example.com/pic4.jpg', 'Musician and part-time barista.', '1995-02-18', 'Male', 'Ho Chi Minh City', 'District 3', 'Ward 6', 'Vo Van Tan Street'),
(5, 'charlie.b', 'charlie.brown@example.com', 'Charlie Brown', '0944556677', '2023-05-22 09:00:00', '2025-06-13 10:05:00', 'http://example.com/pic5.jpg', 'Graphic designer.', '1993-07-25', 'Male', 'Hanoi', 'Ba Dinh', 'Dien Bien', 'Hoang Dieu Street'),
(6, 'diana.p', 'diana.prince@example.com', 'Diana Prince', '0955667788', '2023-06-18 18:00:00', '2025-06-14 12:00:00', 'http://example.com/pic6.jpg', 'Art curator.', '1985-03-01', 'Female', 'Ho Chi Minh City', 'District 7', 'Tan Phong', 'Nguyen Van Linh Street'),
(7, 'peter.p', 'peter.parker@example.com', 'Peter Parker', '0966778899', '2023-07-01 12:10:00', '2025-06-11 18:45:00', 'http://example.com/pic7.jpg', 'Freelance photographer.', '2001-08-10', 'Male', 'Can Tho', 'Ninh Kieu', 'An Phu', 'Hoa Binh Avenue'),
(8, 'mary.jane', 'mj.watson@example.com', 'Mary Jane Watson', '0977889900', '2023-08-14 13:20:00', '2025-06-12 20:00:00', 'http://example.com/pic8.jpg', 'Actress and model.', '2000-10-22', 'Female', 'Ho Chi Minh City', 'Binh Thanh', 'Ward 22', 'Nguyen Huu Canh Street'),
(9, 'bruce.w', 'bruce.wayne@example.com', 'Bruce Wayne', '0988990011', '2023-09-09 09:30:00', '2025-06-14 07:30:00', 'http://example.com/pic9.jpg', 'Philanthropist.', '1982-04-17', 'Male', 'Hanoi', 'Tay Ho', 'Quang An', 'To Ngoc Van Street'),
(10, 'selina.k', 'selina.kyle@example.com', 'Selina Kyle', '0999001122', '2023-10-31 23:00:00', '2025-06-13 22:10:00', 'http://example.com/pic10.jpg', 'Animal lover.', '1989-09-05', 'Female', 'Da Nang', 'Son Tra', 'An Hai Bac', 'Vo Nguyen Giap Street');


USE DataWarehouse;

INSERT INTO bronze.product_info (product_id, product_name, slug, short_description, description, price, mrp_price, stock, is_available, rating, brand_name, season, year, gender, category_main_id, sub_category_id, created_date, modified_date) VALUES
(101, 'Classic Leather Jacket', 'classic-leather-jacket', 'A timeless black leather jacket.', 'Made from 100% genuine leather, perfect for all seasons. Features multiple pockets and a comfortable lining.', 2500000.00, 2999000.00, 50, 1, 5, 'UrbanStyle', 'All-Season', 2023, 'Unisex', 1, 10, '2023-01-10 09:00:00', '2024-05-15 14:00:00'),
(102, 'Summer Floral Dress', 'summer-floral-dress', 'A light and airy floral dress.', 'Perfect for a sunny day out. Made from breathable cotton fabric with a vibrant floral print.', 750000.00, 899000.00, 120, 1, 4, 'DaisyChain', 'Summer', 2024, 'Female', 2, 20, '2024-02-20 10:00:00', '2024-05-20 11:00:00'),
(103, 'Men''s Slim-Fit Jeans', 'mens-slim-fit-jeans', 'Modern slim-fit jeans in dark wash.', 'Crafted from stretch denim for maximum comfort and style. A versatile addition to any wardrobe.', 1200000.00, 1500000.00, 80, 1, 5, 'DenimWorks', 'All-Season', 2023, 'Male', 1, 11, '2023-03-15 11:30:00', '2024-04-25 16:00:00'),
(104, 'Running Sports Shoes', 'running-sports-shoes', 'Lightweight shoes for running.', 'Engineered mesh upper for breathability and support. Cushioned midsole for a comfortable run.', 1800000.00, 2200000.00, 200, 1, 4, 'FitStride', 'All-Season', 2024, 'Unisex', 3, 30, '2024-01-05 08:45:00', '2024-05-18 10:20:00'),
(105, 'Silk Evening Gown', 'silk-evening-gown', 'An elegant red silk evening gown.', 'Floor-length gown made from pure silk, featuring a flattering A-line silhouette. Ideal for formal events.', 4500000.00, 5500000.00, 30, 1, 5, 'Elegance', 'Winter', 2023, 'Female', 2, 21, '2023-09-01 15:00:00', '2024-03-10 12:00:00'),
(106, 'Men''s Plaid Flannel Shirt', 'mens-plaid-flannel-shirt', 'Comfortable cotton flannel shirt.', 'Classic plaid pattern, perfect for a casual look. Soft and warm for cooler days.', 650000.00, 799000.00, 150, 1, 4, 'Lumberjack', 'Autumn', 2023, 'Male', 1, 12, '2023-08-10 14:20:00', '2024-02-15 18:00:00'),
(107, 'Leather Ankle Boots', 'leather-ankle-boots', 'Stylish and durable ankle boots.', 'Made from high-quality brown leather with a sturdy rubber sole. A versatile choice for any outfit.', 2100000.00, 2500000.00, 60, 1, 5, 'UrbanStyle', 'Autumn', 2023, 'Female', 3, 31, '2023-07-25 10:00:00', '2024-01-30 09:30:00'),
(108, 'Kids'' Graphic T-Shirt', 'kids-graphic-t-shirt', 'Fun and colorful graphic t-shirt.', 'Made from 100% soft cotton, featuring a playful dinosaur print that kids will love.', 250000.00, 299000.00, 300, 1, 4, 'TinyTots', 'Summer', 2024, 'Unisex', 4, 40, '2024-03-01 11:00:00', '2024-05-22 13:00:00'),
(109, 'Formal Business Suit', 'formal-business-suit', 'A sharp, professional business suit.', 'Two-piece suit in charcoal grey. Tailored for a modern fit. Fabric is a wool blend for comfort and durability.', 5500000.00, 6500000.00, 40, 1, 5, 'ExecWear', 'All-Season', 2023, 'Male', 1, 13, '2023-05-11 16:00:00', '2024-04-11 17:00:00'),
(110, 'Yoga Pants', 'yoga-pants', 'High-waisted, flexible yoga pants.', 'Four-way stretch fabric that is sweat-wicking and breathable. Perfect for yoga, gym, or casual wear.', 800000.00, 950000.00, 180, 1, 5, 'ZenFlex', 'All-Season', 2024, 'Female', 2, 22, '2024-02-14 13:00:00', '2024-05-14 14:00:00');



USE DataWarehouse;

INSERT INTO bronze.crm_cust_event (event_id, event_type, event_time, product_id, user_id, frequency, rating) VALUES
(1001, 'view', '2025-06-01 10:00:00', 102, 2, 3, NULL),
(1002, 'click', '2025-06-01 10:05:00', 102, 2, 1, NULL),
(1003, 'purchase', '2025-06-02 11:20:00', 102, 2, 1, 5),
(1004, 'view', '2025-06-03 14:30:00', 101, 1, 5, NULL),
(1005, 'purchase', '2025-06-04 09:45:00', 101, 1, 1, 5),
(1006, 'view', '2025-06-05 16:00:00', 104, 7, 2, NULL),
(1007, 'click', '2025-06-05 16:02:00', 104, 7, 2, NULL),
(1008, 'view', '2025-06-06 18:10:00', 109, 9, 4, NULL),
(1009, 'purchase', '2025-06-07 10:00:00', 109, 9, 1, 4),
(1010, 'rating', '2025-06-08 12:00:00', 101, 1, 1, 5);

USE DataWarehouse;

INSERT INTO bronze.sale_payment (payment_id, payment_code, payment_method, amount_paid, status, user_id, created_at) VALUES
(201, 'PAY-20250602-001', 'Credit Card', 750000.00, 'Completed', 2, '2025-06-02 11:20:10'),
(202, 'PAY-20250604-002', 'VNPay', 2500000.00, 'Completed', 1, '2025-06-04 09:45:15'),
(203, 'PAY-20250607-003', 'Bank Transfer', 5500000.00, 'Completed', 9, '2025-06-07 10:00:25'),
(204, 'PAY-20250608-004', 'Cash on Delivery', 3000000.00, 'Pending', 4, '2025-06-08 13:00:00'),
(205, 'PAY-20250609-005', 'Momo', 4500000.00, 'Completed', 6, '2025-06-09 15:30:50'),
(206, 'PAY-20250610-006', 'Credit Card', 2050000.00, 'Completed', 3, '2025-06-10 11:05:00'),
(207, 'PAY-20250611-007', 'ZaloPay', 1800000.00, 'Completed', 7, '2025-06-11 19:00:00'),
(208, 'PAY-20250612-008', 'Cash on Delivery', 250000.00, 'Completed', 8, '2025-06-12 20:30:10'),
(209, 'PAY-20250613-009', 'Credit Card', 2900000.00, 'Failed', 10, '2025-06-13 22:15:00'),
(210, 'PAY-20250614-010', 'VNPay', 800000.00, 'Completed', 5, '2025-06-14 09:00:00');

USE DataWarehouse;

INSERT INTO bronze.sale_order (order_id, order_number, user_id, full_name, phone, email, city, district, ward, road, order_note, order_total, tax, total_items, payment_id, payment_method, status, order_status, ip_address, is_ordered, is_viewed, created_at, updated_at) VALUES
(301, 'ORD-20250602-001', 2, 'Jane Smith', '0987654321', 'jane.smith@example.com', 'Hanoi', 'Hoan Kiem', 'Trang Tien', 'Dinh Tien Hoang Street', 'Deliver in the evening.', 750000.00, 56250.00, 1, 201, 'Credit Card', 'Completed', 'Delivered', '113.160.1.1', 1, 1, '2025-06-02 11:20:00', '2025-06-05 17:00:00'),
(302, 'ORD-20250604-002', 1, 'John Doe', '0912345678', 'john.doe@example.com', 'Ho Chi Minh City', 'District 1', 'Ben Nghe', 'Nguyen Hue Street', NULL, 2500000.00, 187500.00, 1, 202, 'VNPay', 'Completed', 'Delivered', '125.212.1.2', 1, 1, '2025-06-04 09:45:00', '2025-06-06 18:00:00'),
(303, 'ORD-20250607-003', 9, 'Bruce Wayne', '0988990011', 'bruce.wayne@example.com', 'Hanoi', 'Tay Ho', 'Quang An', 'To Ngoc Van Street', 'Handle with care.', 5500000.00, 412500.00, 1, 203, 'Bank Transfer', 'Completed', 'Delivered', '27.66.1.3', 1, 1, '2025-06-07 10:00:00', '2025-06-10 14:30:00'),
(304, 'ORD-20250608-004', 4, 'Bob Williams', '0933445566', 'bob.williams@example.com', 'Ho Chi Minh City', 'District 3', 'Ward 6', 'Vo Van Tan Street', 'Call before delivery.', 3000000.00, 225000.00, 2, 204, 'Cash on Delivery', 'Processing', 'Shipped', '14.161.1.4', 1, 1, '2025-06-08 12:59:00', '2025-06-09 11:00:00'),
(305, 'ORD-20250609-005', 6, 'Diana Prince', '0955667788', 'diana.prince@example.com', 'Ho Chi Minh City', 'District 7', 'Tan Phong', 'Nguyen Van Linh Street', NULL, 4500000.00, 337500.00, 1, 205, 'Momo', 'Completed', 'Delivered', '118.69.1.5', 1, 1, '2025-06-09 15:30:00', '2025-06-12 16:00:00'),
(306, 'ORD-20250610-006', 3, 'Alice Johnson', '0911223344', 'alice.j@example.com', 'Da Nang', 'Hai Chau', 'Thach Thang', 'Bach Dang Street', NULL, 2050000.00, 153750.00, 2, 206, 'Credit Card', 'Completed', 'Delivered', '171.252.1.6', 1, 1, '2025-06-10 11:04:00', '2025-06-13 10:00:00'),
(307, 'ORD-20250611-007', 7, 'Peter Parker', '0966778899', 'peter.parker@example.com', 'Can Tho', 'Ninh Kieu', 'An Phu', 'Hoa Binh Avenue', 'Leave at the front door.', 1800000.00, 135000.00, 1, 207, 'ZaloPay', 'Completed', 'Delivered', '42.113.1.7', 1, 1, '2025-06-11 18:59:00', '2025-06-14 11:00:00'),
(308, 'ORD-20250612-008', 8, 'Mary Jane Watson', '0977889900', 'mj.watson@example.com', 'Ho Chi Minh City', 'Binh Thanh', 'Ward 22', 'Nguyen Huu Canh Street', NULL, 250000.00, 18750.00, 1, 208, 'Cash on Delivery', 'Completed', 'Delivered', '123.21.1.8', 1, 1, '2025-06-12 20:30:00', '2025-06-15 10:00:00'),
(309, 'ORD-20250613-009', 10, 'Selina Kyle', '0999001122', 'selina.kyle@example.com', 'Da Nang', 'Son Tra', 'An Hai Bac', 'Vo Nguyen Giap Street', NULL, 2900000.00, 217500.00, 2, 209, 'Credit Card', 'Cancelled', 'Payment Failed', '117.1.1.9', 1, 0, '2025-06-13 22:14:00', '2025-06-13 22:15:00'),
(310, 'ORD-20250614-010', 5, 'Charlie Brown', '0944556677', 'charlie.brown@example.com', 'Hanoi', 'Ba Dinh', 'Dien Bien', 'Hoang Dieu Street', 'Gift wrap please.', 800000.00, 60000.00, 1, 210, 'VNPay', 'Processing', 'Confirmed', '222.252.1.10', 1, 1, '2025-06-14 08:59:00', '2025-06-14 09:30:00');


USE DataWarehouse;

INSERT INTO bronze.sale_order_product (order_product_id, order_id, user_id, product_id, quantity, product_price, discount_amount, ordered, payment_id, created_at, updated_at) VALUES
(401, 301, 2, 102, 1, 750000.00, 149000.00, 1, 201, '2025-06-02 11:20:00', '2025-06-02 11:20:00'),
(402, 302, 1, 101, 1, 2500000.00, 499000.00, 1, 202, '2025-06-04 09:45:00', '2025-06-04 09:45:00'),
(403, 303, 9, 109, 1, 5500000.00, 1000000.00, 1, 203, '2025-06-07 10:00:00', '2025-06-07 10:00:00'),
(404, 304, 4, 103, 1, 1200000.00, 300000.00, 1, 204, '2025-06-08 12:59:00', '2025-06-08 12:59:00'),
(405, 304, 4, 106, 1, 650000.00, 149000.00, 1, 204, '2025-06-08 12:59:00', '2025-06-08 12:59:00'),
(406, 305, 6, 105, 1, 4500000.00, 1000000.00, 1, 205, '2025-06-09 15:30:00', '2025-06-09 15:30:00'),
(407, 306, 3, 106, 1, 650000.00, 149000.00, 1, 206, '2025-06-10 11:04:00', '2025-06-10 11:04:00'),
(408, 307, 7, 104, 1, 1800000.00, 400000.00, 1, 207, '2025-06-11 18:59:00', '2025-06-11 18:59:00'),
(409, 308, 8, 108, 1, 250000.00, 49000.00, 1, 208, '2025-06-12 20:30:00', '2025-06-12 20:30:00'),
(410, 310, 5, 110, 1, 800000.00, 150000.00, 1, 210, '2025-06-14 08:59:00', '2025-06-14 08:59:00');