USE DataWarehouse;

CREATE TABLE bronze.crm_cust_info (
    cst_id            BIGINT PRIMARY KEY,          
    cst_username      NVARCHAR(50),
    cst_email         NVARCHAR(255),
    cst_fullname      NVARCHAR(50),
    cst_phone_number  NVARCHAR(20),
    cst_date_joined   DATETIME,
    cst_last_login    DATETIME,
    profile_picture   NVARCHAR(500),
    bio               NVARCHAR(MAX),
    date_of_birth     DATE,
    sex               NVARCHAR(100),
    city              NVARCHAR(100),
    district          NVARCHAR(100),
    ward              NVARCHAR(100),
    road              NVARCHAR(150),
    load_time         DATETIME DEFAULT GETDATE()  
);

CREATE TABLE bronze.crm_cust_event (
    event_id        BIGINT PRIMARY KEY,       
    event_type      NVARCHAR(10),             
    event_time      DATETIME,                 
    product_id      BIGINT NULL,             
    user_id         BIGINT NOT NULL,          
    frequency       INT NULL,              
    rating          INT NULL,                 
    load_time       DATETIME DEFAULT GETDATE()
);

CREATE TABLE bronze.sale_order (
    order_id         BIGINT PRIMARY KEY,       
    order_number     NVARCHAR(20),
    user_id          BIGINT,
    full_name        NVARCHAR(100),
    phone            NVARCHAR(20),
    email            NVARCHAR(50),
    city             NVARCHAR(100),
    district         NVARCHAR(100),
    ward             NVARCHAR(100),
    road             NVARCHAR(150),
    order_note       NVARCHAR(MAX),
    order_total      FLOAT,
    tax              FLOAT,
    total_items      INT,
    payment_id       BIGINT,
    payment_method   NVARCHAR(50),
    status           NVARCHAR(50),
    order_status     NVARCHAR(50),
    ip_address       NVARCHAR(20),
    is_ordered       BIT,
    is_viewed        BIT,
    created_at       DATETIME,
    updated_at       DATETIME,
    load_time        DATETIME DEFAULT GETDATE()
);

CREATE TABLE bronze.sale_order_product (
    order_product_id     BIGINT PRIMARY KEY,   
    order_id             BIGINT,
    user_id              BIGINT,
    product_id           BIGINT,
    quantity             INT,
    product_price        FLOAT,
    discount_amount      DECIMAL(10,2),
    ordered              BIT,
    payment_id           BIGINT,
    created_at           DATETIME,
    updated_at           DATETIME,
    load_time            DATETIME DEFAULT GETDATE()
);

CREATE TABLE bronze.sale_payment (
    payment_id       BIGINT PRIMARY KEY,       
    payment_code     NVARCHAR(100),            
    payment_method   NVARCHAR(100),
    amount_paid      FLOAT,
    status           NVARCHAR(100),
    user_id          BIGINT,
    created_at       DATETIME,
    load_time        DATETIME DEFAULT GETDATE()
);



CREATE TABLE bronze.product_info (
    product_id        BIGINT PRIMARY KEY,       
    product_name      NVARCHAR(255),
    slug              NVARCHAR(100),
    short_description NVARCHAR(150),
    description       NVARCHAR(MAX),
    price             DECIMAL(10, 2),
    mrp_price         DECIMAL(10, 2),
    stock             INT,
    is_available      BIT,
    rating            INT,
    brand_name        NVARCHAR(255),
    season            NVARCHAR(50),
    year              INT,
    gender            NVARCHAR(30),
    category_main_id  BIGINT,
    sub_category_id   BIGINT,
    created_date      DATETIME,
    modified_date     DATETIME,
    load_time         DATETIME DEFAULT GETDATE()
);
