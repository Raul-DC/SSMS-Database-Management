-- remove_duplicates.sql
-- Script to remove duplicate records from the dbo.Unificado table

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

-- Optional: To verify which records will be deleted, you can first run this query:
-- SELECT * FROM CTE_Duplicates WHERE rn > 1;
