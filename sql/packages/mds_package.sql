CREATE OR REPLACE PACKAGE mds_package AS
    TYPE mds_row IS RECORD (
        mdsdate mds.mds_date%TYPE
    );
    TYPE tblgetmds IS
        TABLE OF mds_row;
    TYPE mds_med_row IS RECORD (
        type_mds_med_name mds.medicine_med_name%TYPE
    );
    TYPE table_mds_med IS
        TABLE OF mds_med_row;
    TYPE mds_des_row IS RECORD (
        type_mds_dis_name mds.desease_dis_name%TYPE
    );
    TYPE table_mds_des IS
        TABLE OF mds_des_row;
    PROCEDURE add_mds (
        status        OUT           VARCHAR2,
        mdsdesease    IN            mds.desease_dis_name%TYPE,
        mdssymptom    IN            mds.symptom_sym_name%TYPE,
        mdsmedicine   IN            mds.medicine_med_name%TYPE
    );

    PROCEDURE del_mds (
        mdsdate   IN        mds.mds_date%TYPE
    );

    PROCEDURE update_mdsdesease (
        mdsdate      IN           mds.mds_date%TYPE,
        mdsdesease   IN           mds.desease_dis_name%TYPE
    );

    PROCEDURE update_mdssymptom (
        status       OUT          VARCHAR2,
        mdsdate      IN           mds.mds_date%TYPE,
        mdssymptom   IN           mds.symptom_sym_name%TYPE
    );

    PROCEDURE update_mdsmedicine (
        mdsdate       IN            mds.mds_date%TYPE,
        mdsmedicine   IN            mds.medicine_med_name%TYPE
    );

    FUNCTION get_mds (
        mdsdate   IN        mds.mds_date%TYPE
    ) RETURN tblgetmds
        PIPELINED;

    FUNCTION get_medication_list (
        symptomname   IN            mds.symptom_sym_name%TYPE
    ) RETURN table_mds_med
        PIPELINED;

    FUNCTION get_medication_list_by_dis (
        disname   IN        mds.desease_dis_name%TYPE
    ) RETURN table_mds_med
        PIPELINED;

    FUNCTION get_disease_list (
        symptomname   IN            mds.symptom_sym_name%TYPE
    ) RETURN table_mds_des
        PIPELINED;

END mds_package;
/

CREATE OR REPLACE PACKAGE BODY mds_package IS

    PROCEDURE add_mds (
        status        OUT           VARCHAR2,
        mdsdesease    IN            mds.desease_dis_name%TYPE,
        mdssymptom    IN            mds.symptom_sym_name%TYPE,
        mdsmedicine   IN            mds.medicine_med_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        INSERT INTO mds (
            mds_date,
            desease_dis_name,
            symptom_sym_name,
            medicine_med_name
        ) VALUES (
            systimestamp,
            mdsdesease,
            mdssymptom,
            mdsmedicine
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така назва уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_mds;

    PROCEDURE del_mds (
        mdsdate   IN        mds.mds_date%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        DELETE FROM mds
        WHERE
            mds.mds_date = mdsdate;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE value_error;
    END del_mds;

    PROCEDURE update_mdsdesease (
        mdsdate      IN           mds.mds_date%TYPE,
        mdsdesease   IN           mds.desease_dis_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        UPDATE mds
        SET
            mds.desease_dis_name = mdsdesease
        WHERE
            mds.mds_date = mdsdate;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE value_error;
    END update_mdsdesease;

    PROCEDURE update_mdssymptom (
        status       OUT          VARCHAR2,
        mdsdate      IN           mds.mds_date%TYPE,
        mdssymptom   IN           mds.symptom_sym_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        UPDATE mds
        SET
            mds.symptom_sym_name = mdssymptom
        WHERE
            mds.mds_date = mdsdate;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END update_mdssymptom;

    PROCEDURE update_mdsmedicine (
        mdsdate       IN            mds.mds_date%TYPE,
        mdsmedicine   IN            mds.medicine_med_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        UPDATE mds
        SET
            mds.medicine_med_name = mdsmedicine
        WHERE
            mds.mds_date = mdsdate;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE value_error;
    END update_mdsmedicine;

    FUNCTION get_mds (
        mdsdate   IN        mds.mds_date%TYPE
    ) RETURN tblgetmds
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                mds_date
            FROM
                mds
            WHERE
                mds.mds_date = mdsdate
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_mds;

    FUNCTION get_medication_list (
        symptomname   IN            mds.symptom_sym_name%TYPE
    ) RETURN table_mds_med
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                mds.medicine_med_name
            FROM
                mds
            WHERE
                mds.symptom_sym_name = symptomname
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_medication_list;

    FUNCTION get_disease_list (
        symptomname   IN            mds.symptom_sym_name%TYPE
    ) RETURN table_mds_des
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                mds.desease_dis_name
            FROM
                mds
            WHERE
                mds.symptom_sym_name = symptomname
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_disease_list;

    FUNCTION get_medication_list_by_dis (
        disname   IN        mds.desease_dis_name%TYPE
    ) RETURN table_mds_med
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                mds.medicine_med_name
            FROM
                mds
            WHERE
                mds.desease_dis_name = disname
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_medication_list_by_dis;

END mds_package;
/