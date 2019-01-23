create table DESEASE
(
  DIS_NAME VARCHAR2(30) not null
    constraint DESEASE_PK
      primary key
    constraint DIS_NAME_CHECK
      check ( REGEXP_LIKE(dis_name,
                          '^[0-9A-Z_a-z]{1,30}$')),
  DIS_DESC CLOB
    constraint DIS_DESC_CHECK
      check ( REGEXP_LIKE(dis_desc,
                          '^(.{0,2000})?( )?$')),
  DELETED  DATE default NULL
)
/

create table MDS
(
  MDS_DATE          DATE not null
    constraint MDS_PK
      primary key,
  DESEASE_DIS_NAME  VARCHAR2(30),
  SYMPTOM_SYM_NAME  VARCHAR2(30),
  MEDICINE_MED_NAME VARCHAR2(30),
  DELETED           DATE default NULL
)
/

create table MEDICINE
(
  MED_NAME VARCHAR2(30) not null
    constraint MEDICINE_PK
      primary key
    constraint MED_NAME_CHECK
      check ( REGEXP_LIKE(med_name,
                          '^[0-9A-Z_a-z]{1,30}$')),
  MED_DESC CLOB
    constraint MED_DESC_CHECK
      check ( REGEXP_LIKE(med_desc,
                          '^(.{0,2000})?( )?$')),
  DELETED  DATE
)
/

create table SYMPTOM
(
  SYM_NAME VARCHAR2(30) not null
    constraint SYMPTOM_PK
      primary key
    constraint SYM_NAME_CHECK
      check ( REGEXP_LIKE(sym_name,
                          '^[0-9A-Z_a-z]{1,30}$')),
  SYM_DESC CLOB
    constraint SYM_DESC_CHECK
      check ( REGEXP_LIKE(sym_desc,
                          '^(.{0,2000})?( )?$')),
  DELETED  DATE
)
/

create table USER_INFO
(
  LOGIN      VARCHAR2(30) not null
    constraint USER_PK
      primary key
    constraint LOGIN_CHECK
      check ( REGEXP_LIKE(login,
                          '^[0-9A-Z_a-z]{1,30}$')),
  FIRST_NAME VARCHAR2(30)
    constraint FIRST_NAME_CHECK
      check ( REGEXP_LIKE(first_name,
                          '^[0-9A-Z_a-z]{1,30}$')),
  LAST_NAME  VARCHAR2(30)
    constraint LAST_NAME_CHECK
      check ( REGEXP_LIKE(last_name,
                          '^[0-9A-Z_a-z]{1,30}$')),
  BIRTHDAY   DATE,
  SEX        CHAR
    constraint DOCTOR
      check ( REGEXP_LIKE(sex,
                          '^[0-1]{1}$'))
    constraint DOCTOR_CHECK
      check ( REGEXP_LIKE(sex,
                          '^[0-1]{1}$'))
    constraint SEX_CHECK
      check ( REGEXP_LIKE(sex,
                          '^[0-1]{1}$')),
  PASSWORD_  VARCHAR2(30),
  DOCTOR     CHAR,
  SUBMITED   CHAR default 0
    constraint SUBMIT_CHECK
      check ( REGEXP_LIKE(SUBMITED,
                          '^[0-1]{1}$'))
)
/

create table CARD
(
  CARD_NUMBER NUMBER       not null
    constraint CARD_PK
      primary key
    constraint CARD_NUMBER_CHECK
      check ( REGEXP_LIKE(card_number,
                          '^[0-9]{1,8}$')),
  USER_LOGIN  VARCHAR2(30) not null
    constraint CARD_USER_FK
      references USER_INFO
    constraint USER_LOGIN_CHECK
      check ( REGEXP_LIKE(user_login,
                          '^[0-9a-z]{1,30}$'))
)
/

create table USER_MDS
(
  USER_LOGIN   VARCHAR2(30) not null
    constraint USER_MDS_USER_FK
      references USER_INFO
    constraint USER_MDS_LOGIN_CHECK
      check ( REGEXP_LIKE(user_login,
                          '^[0-9A-Z_a-z]{1,30}$')),
  MDS_MDS_DATE DATE         not null
    constraint USER_MDS_MDS_FK
      references MDS,
  constraint USER_MDS_PK
    primary key (USER_LOGIN, MDS_MDS_DATE)
)
/

