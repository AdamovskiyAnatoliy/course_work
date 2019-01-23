CREATE VIEW symptom_view AS
    SELECT
        sym_name,
        sym_desc
    FROM
        symptom
    WHERE
        symptom.deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_symptom INSTEAD OF
    DELETE ON symptom_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE symptom
    SET
        symptom.deleted = systimestamp
    WHERE
        symptom.sym_name = :old.sym_name;

    COMMIT;
END;