CREATE VIEW medicine_view AS
    SELECT
        med_name,
        med_desc
    FROM
        medicine
    WHERE
        medicine.deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_medicine INSTEAD OF
    DELETE ON medicine_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE medicine
    SET
        medicine.deleted = systimestamp
    WHERE
        medicine.med_name = :old.med_name;

    COMMIT;
END;