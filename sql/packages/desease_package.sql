CREATE OR REPLACE PACKAGE desease_package IS
    TYPE desease_row IS RECORD (
        disdesc desease.dis_desc%TYPE
    );
    TYPE tblgetdisdesc IS
        TABLE OF desease_row;
    PROCEDURE add_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE,
        disdesc   IN        desease.dis_desc%TYPE
    );

    PROCEDURE del_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE
    );

    PROCEDURE update_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE,
        disdesc   IN        desease.dis_desc%TYPE
    );

    FUNCTION get_desease (
        disname   IN        desease.dis_name%TYPE
    ) RETURN tblgetdisdesc
        PIPELINED;

END desease_package;
/

CREATE OR REPLACE PACKAGE BODY desease_package IS

    PROCEDURE add_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE,
        disdesc   IN        desease.dis_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        INSERT INTO desease (
            dis_name,
            dis_desc
        ) VALUES (
            disname,
            disdesc
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така назва уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_desease;

    PROCEDURE del_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        DELETE FROM disease_view
        WHERE
            disease_view.dis_name = disname;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_desease;

    PROCEDURE update_desease (
        status    OUT       VARCHAR2,
        disname   IN        desease.dis_name%TYPE,
        disdesc   IN        desease.dis_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        UPDATE desease
        SET
            desease.dis_desc = disdesc
        WHERE
            desease.dis_name = disname;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END update_desease;

    FUNCTION get_desease (
        disname   IN        desease.dis_name%TYPE
    ) RETURN tblgetdisdesc
        PIPELINED
    IS
    BEGIN
        SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
        FOR curr IN (
            SELECT DISTINCT
                dis_desc
            FROM
                desease
            WHERE
                desease.dis_name = disname
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_desease;

END desease_package;