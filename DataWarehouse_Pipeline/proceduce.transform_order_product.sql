CREATE PROCEDURE TransformBronzeSaleOrderProductToSilver
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        WITH Deduplicated AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY order_product_id ORDER BY load_time DESC) AS rn
            FROM bronze.sale_order_product
            WHERE order_product_id IS NOT NULL
        )
        INSERT INTO silver.sale_order_product
        SELECT 
            order_product_id,
            order_id,
            user_id,
            product_id,
            quantity,
            product_price,
            discount_amount,
            CAST(ordered AS BIT),
            payment_id,
            TRY_CAST(created_at AS DATETIME),
            TRY_CAST(updated_at AS DATETIME),
            COALESCE(load_time, GETDATE())
        FROM Deduplicated
        WHERE rn = 1;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
