-- Dimension: dim_user
CREATE VIEW gold.dim_user AS
SELECT
    ROW_NUMBER() OVER (ORDER BY cst_id) AS user_key,
    ci.cst_id                       AS user_id,
    ci.cst_username                AS username,
    ci.cst_fullname                AS full_name,
    ci.cst_email                   AS email,
    ci.cst_phone_number            AS phone,
    ci.sex                         AS gender,
    ci.date_of_birth               AS birthdate,
    ci.cst_date_joined             AS date_joined,
    ci.cst_last_login              AS last_login,
    ci.city                        AS city,
    ci.district                    AS district,
    ci.ward                        AS ward,
    ci.road                        AS road
FROM silver.crm_cust_info ci;
GO

-- Dimension: dim_product
CREATE VIEW gold.dim_product AS
SELECT
    ROW_NUMBER() OVER (ORDER BY product_id) AS product_key,
    pi.product_id,
    pi.product_name,
    pi.brand_name,
    pi.season,
    pi.year,
    pi.gender,
    pi.category_main_id,
    pi.sub_category_id,
    pi.price,
    pi.mrp_price,
    pi.is_available,
    pi.rating
FROM silver.product_info pi;
GO

-- Dimension: dim_payment
CREATE VIEW gold.dim_payment AS
SELECT
    ROW_NUMBER() OVER (ORDER BY payment_id) AS payment_key,
    sp.payment_id,
    sp.payment_code,
    sp.payment_method,
    sp.status
FROM silver.sale_payment sp;
GO

-- Dimension: dim_order_status
CREATE VIEW gold.dim_order_status AS
SELECT DISTINCT
    ROW_NUMBER() OVER (ORDER BY order_status) AS status_key,
    so.status,
    so.order_status
FROM silver.sale_order so;
GO

-- Dimension: dim_date
CREATE VIEW gold.dim_date AS
SELECT DISTINCT
    CAST(FORMAT(created_at, 'yyyyMMdd') AS INT) AS date_key,
    CAST(created_at AS DATE) AS full_date,
    YEAR(created_at) AS year,
    DATEPART(QUARTER, created_at) AS quarter,
    MONTH(created_at) AS month,
    DAY(created_at) AS day,
    DATEPART(WEEKDAY, created_at) AS day_of_week,
    DATENAME(WEEKDAY, created_at) AS day_name
FROM silver.sale_order
WHERE created_at IS NOT NULL;
GO
-- Fact: fact_sale
CREATE VIEW gold.fact_sale AS
SELECT
    so.order_id,
    sop.product_id,
    so.user_id,
    so.payment_id,
    CAST(FORMAT(so.created_at, 'yyyyMMdd') AS INT) AS order_date_key,
    sop.quantity,
    sop.product_price,
    sop.discount_amount,
    (sop.product_price * sop.quantity - sop.discount_amount) AS revenue,
    so.tax,
    so.order_total,
    ci.city,
    ci.district,
    ci.ward,
    ci.road,
    ROW_NUMBER() OVER (ORDER BY so.order_id) AS sale_key
FROM silver.sale_order so
LEFT JOIN silver.sale_order_product sop ON so.order_id = sop.order_id
LEFT JOIN silver.crm_cust_info ci ON so.user_id = ci.cst_id;
GO

-- Fact: fact_user_event
CREATE VIEW gold.fact_user_event AS
SELECT
    ce.event_id,
    ce.user_id,
    ce.product_id,
    CAST(FORMAT(ce.event_time, 'yyyyMMdd') AS INT) AS event_date_key,
    ce.event_type,
    ce.frequency,
    ce.rating,
    ci.city,
    ci.district,
    ci.ward,
    ci.road,
    ROW_NUMBER() OVER (ORDER BY ce.event_id) AS user_event_key
FROM silver.crm_cust_event ce
LEFT JOIN silver.crm_cust_info ci ON ce.user_id = ci.cst_id;
GO