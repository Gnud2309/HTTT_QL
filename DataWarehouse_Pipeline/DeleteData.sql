USE DataWarehouse;
GO

-- Disable foreign key constraints temporarily (if any exist)
-- Optional step depending on whether you have foreign key constraints

-- Delete in proper order to avoid foreign key constraint violations
--DELETE FROM bronze.sale_order_product;
--DELETE FROM bronze.sale_order;
--DELETE FROM bronze.sale_payment;
--DELETE FROM bronze.crm_cust_event;
--DELETE FROM bronze.crm_cust_info;
--DELETE FROM bronze.product_info;


DELETE FROM silver.sale_order_product;
DELETE FROM silver.sale_order;
DELETE FROM silver.sale_payment;
DELETE FROM silver.crm_cust_event;
DELETE FROM silver.crm_cust_info;
DELETE FROM silver.product_info;
