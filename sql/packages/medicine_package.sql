CREATE OR REPLACE PACKAGE medicine_package IS
    TYPE medicine_row IS RECORD (
        meddesc medicine.med_desc%TYPE
    );
    TYPE tblgetmeddesc IS
        TABLE OF medicine_row;
    PROCEDURE add_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE,
        meddesc   IN        medicine.med_desc%TYPE
    );

    PROCEDURE del_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE
    );

    PROCEDURE update_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE,
        meddesc   IN        medicine.med_desc%TYPE
    );

    FUNCTION get_medicine (
        medname   IN        medicine.med_name%TYPE
    ) RETURN tblgetmeddesc
        PIPELINED;

END medicine_package;
/

CREATE OR REPLACE PACKAGE BODY medicine_package IS

    PROCEDURE add_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE,
        meddesc   IN        medicine.med_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        INSERT INTO medicine (
            med_name,
            med_desc
        ) VALUES (
            medname,
            meddesc
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така назва уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_medicine;

    PROCEDURE del_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        DELETE FROM medicine_view
        WHERE
            medicine_view.med_name = medname;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_medicine;

    PROCEDURE update_medicine (
        status    OUT       VARCHAR2,
        medname   IN        medicine.med_name%TYPE,
        meddesc   IN        medicine.med_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        UPDATE medicine
        SET
            medicine.med_desc = meddesc
        WHERE
            medicine.med_name = medname;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END update_medicine;

    FUNCTION get_medicine (
        medname   IN        medicine.med_name%TYPE
    ) RETURN tblgetmeddesc
        PIPELINED
    IS
    BEGIN
        SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
        FOR curr IN (
            SELECT DISTINCT
                med_desc
            FROM
                medicine
            WHERE
                medicine.med_name = medname
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_medicine;

END medicine_package;