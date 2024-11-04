---------------------------------------------------------------------------------------------------------------------------

-- remove_duplicates.sql
-- Script to manually remove duplicate records from the dbo.Unificado table

WITH CTE_Duplicates AS (
    SELECT 
        CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, MUESTRA, VALOR, ORIGEN, FECHA_COPIA,
        ROW_NUMBER() OVER (
            PARTITION BY CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, MUESTRA, VALOR, ORIGEN, FECHA_COPIA
            ORDER BY FECHA_COPIA DESC
        ) AS rn
    FROM dbo.Unificado
)

    -- Delete duplicates, keeping only the latest record for each set of duplicated values
DELETE FROM CTE_Duplicates 
WHERE rn > 1;

---------------------------------------------------------------------------------------------------------------------------

-- Optional: To verify which records will be deleted, you can first run this query:
-- SELECT * FROM CTE_Duplicates WHERE rn > 1;

---------------------------------------------------------------------------------------------------------------------------

-- Script to create de ExecutionLogs table:

CREATE TABLE dbo.ExecutionLogs (
    ExecutionDate DATETIME,
    AffectedRows INT,
    Instance NVARCHAR(100),
    Message NVARCHAR(255)
);

---------------------------------------------------------------------------------------------------------------------------

-- Script used to eliminate duplicates and store logs:

BEGIN TRY
    -- Variables to store log information
    DECLARE @AffectedRows INT;
    DECLARE @Instance NVARCHAR(100) = @@SERVERNAME;
    
    -- Remove duplicates
    WITH CTE_Duplicates AS (
        SELECT 
            CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO, FORMAT, MUESTRA, VALOR, ORIGEN, FECHA_COPIA,
            ROW_NUMBER() OVER (PARTITION BY ID, MUESTRA, RESULTADO ORDER BY FECHA_COPIA DESC) AS rn
        FROM dbo.Unificado
    )
    DELETE FROM CTE_Duplicates WHERE rn > 1;

    -- Save the number of affected rows
    SET @AffectedRows = @@ROWCOUNT;

    -- Insert into the logs table
    INSERT INTO dbo.ExecutionLogs (ExecutionDate, AffectedRows, Instance, Message)
    VALUES (GETDATE(), @AffectedRows, @Instance, 'Duplicate removal process executed');

END TRY
BEGIN CATCH
    -- In case of error, a log of the error can be saved
    INSERT INTO dbo.ExecutionLogs (ExecutionDate, AffectedRows, Instance, Message)
    VALUES (GETDATE(), 0, @@SERVERNAME, ERROR_MESSAGE());
END CATCH;

---------------------------------------------------------------------------------------------------------------------------
