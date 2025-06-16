CREATE PROCEDURE TransformBronzeSalePaymentToSilver
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        WITH Deduplicated AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY payment_id ORDER BY load_time DESC) AS rn
            FROM bronze.sale_payment
            WHERE payment_id IS NOT NULL
        )
        INSERT INTO silver.sale_payment
        SELECT 
            payment_id,
            LTRIM(RTRIM(payment_code)),
            LTRIM(RTRIM(payment_method)),
            amount_paid,
            LTRIM(RTRIM(status)),
            user_id,
            TRY_CAST(created_at AS DATETIME),
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
