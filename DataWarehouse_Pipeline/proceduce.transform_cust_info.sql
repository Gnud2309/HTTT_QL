


CREATE PROCEDURE TransformCustInfoBronzeToSilver
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- Optional: Clear a staging table if re-running
        IF OBJECT_ID('tempdb..#StagingCustInfo') IS NOT NULL
            DROP TABLE #StagingCustInfo;

        -- Step 1: Prepare cleaned data from bronze
        WITH Cleaned AS (
            SELECT
                TRY_CAST(cst_id AS BIGINT) AS cst_id,
                LTRIM(RTRIM(LOWER(cst_username))) AS cst_username,
                LTRIM(RTRIM(LOWER(cst_email))) AS cst_email,
                LTRIM(RTRIM(cst_fullname)) AS cst_fullname,
                -- Normalize phone number to digits only
                REPLACE(REPLACE(REPLACE(cst_phone_number, '-', ''), ' ', ''), '.', '') AS cst_phone_number,
                TRY_CAST(cst_date_joined AS DATETIME) AS cst_date_joined,
                TRY_CAST(cst_last_login AS DATETIME) AS cst_last_login,
                NULLIF(LTRIM(RTRIM(profile_picture)), '') AS profile_picture,
                NULLIF(LTRIM(RTRIM(bio)), '') AS bio,
                TRY_CAST(date_of_birth AS DATE) AS date_of_birth,
                CASE 
                    WHEN LOWER(sex) IN ('male', 'm', 'Nam') THEN 'Male'
                    WHEN LOWER(sex) IN ('female', 'f', 'Nữ') THEN 'Female'
                    ELSE 'Other'
                END AS sex,
                LTRIM(RTRIM(city)) AS city,
                LTRIM(RTRIM(district)) AS district,
                LTRIM(RTRIM(ward)) AS ward,
                LTRIM(RTRIM(road)) AS road,
                GETDATE() AS load_time
            FROM bronze.crm_cust_info
            WHERE cst_id IS NOT NULL
        ),

        Deduplicated AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY cst_id ORDER BY load_time DESC) AS rn
            FROM Cleaned
        )

        -- Step 2: Write cleaned & deduplicated result to a staging table
        SELECT
            cst_id,
            cst_username,
            cst_email,
            cst_fullname,
            cst_phone_number,
            cst_date_joined,
            cst_last_login,
            profile_picture,
            bio,
            date_of_birth,
            sex,
            city,
            district,
            ward,
            road,
            load_time
        INTO #StagingCustInfo
        FROM Deduplicated
        WHERE rn = 1;

        -- Step 3: Final insert into silver (you could MERGE if needed)
        INSERT INTO silver.crm_cust_info (
            cst_id,
            cst_username,
            cst_email,
            cst_fullname,
            cst_phone_number,
            cst_date_joined,
            cst_last_login,
            profile_picture,
            bio,
            date_of_birth,
            sex,
            city,
            district,
            ward,
            road,
            load_time
        )
        SELECT
            cst_id,
            cst_username,
            cst_email,
            cst_fullname,
            cst_phone_number,
            cst_date_joined,
            cst_last_login,
            profile_picture,
            bio,
            date_of_birth,
            sex,
            city,
            district,
            ward,
            road,
            load_time
        FROM #StagingCustInfo;

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;

        -- Optional: log errors
        DECLARE @msg NVARCHAR(MAX) = ERROR_MESSAGE();
        RAISERROR('Transform failed: %s', 16, 1, @msg);
    END CATCH
END;

Exec TransformCustInfoBronzeToSilver;