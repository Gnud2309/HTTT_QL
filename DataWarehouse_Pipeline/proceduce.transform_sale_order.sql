CREATE PROCEDURE TransformBronzeSaleOrderToSilver
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Cleanup if exists
        IF OBJECT_ID('tempdb..#StagingSaleOrder') IS NOT NULL
            DROP TABLE #StagingSaleOrder;

        -- Step 1: Clean and Deduplicate
        WITH Cleaned AS (
            SELECT
                TRY_CAST(order_id AS BIGINT) AS order_id,
                LTRIM(RTRIM(order_number)) AS order_number,
                TRY_CAST(user_id AS BIGINT) AS user_id,
                LTRIM(RTRIM(full_name)) AS full_name,
                REPLACE(REPLACE(REPLACE(phone, '-', ''), ' ', ''), '.', '') AS phone,
                LOWER(LTRIM(RTRIM(email))) AS email,
                LTRIM(RTRIM(city)) AS city,
                LTRIM(RTRIM(district)) AS district,
                LTRIM(RTRIM(ward)) AS ward,
                LTRIM(RTRIM(road)) AS road,
                NULLIF(LTRIM(RTRIM(order_note)), '') AS order_note,
                TRY_CAST(order_total AS FLOAT) AS order_total,
                TRY_CAST(tax AS FLOAT) AS tax,
                TRY_CAST(total_items AS INT) AS total_items,
                TRY_CAST(payment_id AS BIGINT) AS payment_id,
                LTRIM(RTRIM(payment_method)) AS payment_method,
                LTRIM(RTRIM(status)) AS status,
                LTRIM(RTRIM(order_status)) AS order_status,
                LTRIM(RTRIM(ip_address)) AS ip_address,
                CASE WHEN is_ordered IS NOT NULL THEN CAST(is_ordered AS BIT) ELSE 0 END AS is_ordered,
                CASE WHEN is_viewed IS NOT NULL THEN CAST(is_viewed AS BIT) ELSE 0 END AS is_viewed,
                TRY_CAST(created_at AS DATETIME) AS created_at,
                TRY_CAST(updated_at AS DATETIME) AS updated_at,
                COALESCE(load_time, GETDATE()) AS load_time
            FROM bronze.sale_order
            WHERE order_id IS NOT NULL
        ),
        Deduplicated AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY load_time DESC) AS rn
            FROM Cleaned
        )

        -- Step 2: Stage cleaned, deduplicated rows
        SELECT
            order_id,
            order_number,
            user_id,
            full_name,
            phone,
            email,
            city,
            district,
            ward,
            road,
            order_note,
            order_total,
            tax,
            total_items,
            payment_id,
            payment_method,
            status,
            order_status,
            ip_address,
            is_ordered,
            is_viewed,
            created_at,
            updated_at,
            load_time
        INTO #StagingSaleOrder
        FROM Deduplicated
        WHERE rn = 1;

        -- Step 3: Insert to silver
        INSERT INTO silver.sale_order (
            order_id,
            order_number,
            user_id,
            full_name,
            phone,
            email,
            city,
            district,
            ward,
            road,
            order_note,
            order_total,
            tax,
            total_items,
            payment_id,
            payment_method,
            status,
            order_status,
            ip_address,
            is_ordered,
            is_viewed,
            created_at,
            updated_at,
            load_time
        )
        SELECT * FROM #StagingSaleOrder;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        DECLARE @msg NVARCHAR(MAX) = ERROR_MESSAGE();
        RAISERROR('Sale order transformation failed: %s', 16, 1, @msg);
    END CATCH
END;

Exec TransformBronzeSaleOrderToSilver;