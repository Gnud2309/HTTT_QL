CREATE PROCEDURE TransformBronzeProductInfoToSilver
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        WITH Deduplicated AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY load_time DESC) AS rn
            FROM bronze.product_info
            WHERE product_id IS NOT NULL
        )
        INSERT INTO silver.product_info
        SELECT 
            product_id,
            LTRIM(RTRIM(product_name)),
            LOWER(LTRIM(RTRIM(slug))),
            LTRIM(RTRIM(short_description)),
            description,
            price,
            mrp_price,
            stock,
            CAST(is_available AS BIT),
            rating,
            LTRIM(RTRIM(brand_name)),
            LTRIM(RTRIM(season)),
            year,
            LOWER(LTRIM(RTRIM(gender))),
            category_main_id,
            sub_category_id,
            TRY_CAST(created_date AS DATETIME),
            TRY_CAST(modified_date AS DATETIME),
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
