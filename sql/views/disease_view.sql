CREATE OR REPLACE VIEW disease_view AS
    SELECT
        dis_name,
        dis_desc
    FROM
        desease
    WHERE
        desease.deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_disease INSTEAD OF
    DELETE ON disease_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE desease
    SET
        desease.deleted = systimestamp
    WHERE
        desease.dis_name = :old.dis_name;

    COMMIT;
END;