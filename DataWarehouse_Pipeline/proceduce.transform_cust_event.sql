CREATE PROCEDURE TransformBronzeCustEventToSilver
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Drop temp if exists
        IF OBJECT_ID('tempdb..#CleanedEvent') IS NOT NULL
            DROP TABLE #CleanedEvent;

        -- Step 1: Clean & Deduplicate
        WITH Cleaned AS (
            SELECT
                TRY_CAST(event_id AS BIGINT) AS event_id,
                LTRIM(RTRIM(LOWER(event_type))) AS event_type,
                TRY_CAST(event_time AS DATETIME) AS event_time,
                TRY_CAST(product_id AS BIGINT) AS product_id,
                TRY_CAST(user_id AS BIGINT) AS user_id,
                TRY_CAST(frequency AS INT) AS frequency,
                TRY_CAST(rating AS INT) AS rating,
                COALESCE(load_time, GETDATE()) AS load_time
            FROM bronze.crm_cust_event
            WHERE event_id IS NOT NULL AND user_id IS NOT NULL
        ),
        Deduplicated AS (
            SELECT *, 
                ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY load_time DESC) AS rn
            FROM Cleaned
        )

        -- Step 2: Insert deduplicated rows into temp
        SELECT 
            event_id,
            event_type,
            event_time,
            product_id,
            user_id,
            frequency,
            rating,
            load_time
        INTO #CleanedEvent
        FROM Deduplicated
        WHERE rn = 1;

        -- Step 3: Insert into Silver
        INSERT INTO silver.crm_cust_event (
            event_id,
            event_type,
            event_time,
            product_id,
            user_id,
            frequency,
            rating,
            load_time
        )
        SELECT 
            event_id,
            event_type,
            event_time,
            product_id,
            user_id,
            frequency,
            rating,
            load_time
        FROM #CleanedEvent;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        DECLARE @ErrMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        RAISERROR('Failed to transform crm_cust_event: %s', 16, 1, @ErrMsg);
    END CATCH
END;
