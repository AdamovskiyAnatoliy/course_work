CREATE OR REPLACE PACKAGE card_package IS
    TYPE user_card_row IS RECORD (
        cardnumber card.card_number%TYPE
    );
    TYPE tblgetuserallcards IS
        TABLE OF user_card_row;
    PROCEDURE card_add_card (
        status       OUT          VARCHAR2,
        cardnumber   IN           card.card_number%TYPE,
        userlogin    IN           card.user_login%TYPE
    );

    PROCEDURE card_update_user_login (
        cardnumber      IN              card.card_number%TYPE,
        new_userlogin   IN              card.user_login%TYPE
    );

    PROCEDURE card_delete (
        cardnumber   IN           card.card_number%TYPE
    );

    FUNCTION get_all_user_card (
        userlogin   IN          card.user_login%TYPE
    ) RETURN tblgetuserallcards
        PIPELINED;

END card_package;
/

CREATE OR REPLACE PACKAGE BODY card_package IS

    PROCEDURE card_add_card (
        status       OUT          VARCHAR2,
        cardnumber   IN           card.card_number%TYPE,
        userlogin    IN           card.user_login%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        INSERT INTO card (
            card_number,
            user_login
        ) VALUES (
            cardnumber,
            userlogin
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така назва уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END card_add_card;

    PROCEDURE card_update_user_login (
        cardnumber      IN              card.card_number%TYPE,
        new_userlogin   IN              card.user_login%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        UPDATE card
        SET
            card.user_login = new_userlogin
        WHERE
            card.card_number = cardnumber;

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE value_error;
    END card_update_user_login;

    PROCEDURE card_delete (
        cardnumber   IN           card.card_number%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
        DELETE FROM card
        WHERE
            card.card_number = cardnumber;

        COMMIT;
    END card_delete;

    FUNCTION get_all_user_card (
        userlogin   IN          card.user_login%TYPE
    ) RETURN tblgetuserallcards
        PIPELINED
    IS
    BEGIN
        SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
        FOR curr IN (
            SELECT DISTINCT
                card_number
            FROM
                card
            WHERE
                card.user_login = userlogin
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;

    END get_all_user_card;

END card_package;