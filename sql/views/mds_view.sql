CREATE OR REPLACE VIEW mds_view AS
    SELECT
        mds_date,
        DESEASE_DIS_NAME,
        SYMPTOM_SYM_NAME,
        MEDICINE_MED_NAME
    FROM
        MDS
    WHERE
        MDS.deleted IS NULL;