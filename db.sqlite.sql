BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "account" (
"id" 		    INTEGER PRIMARY KEY AUTOINCREMENT,
"first_name"    TEXT    NOT NULL,
"last_name" 	TEXT    NOT NULL,
"email" 		TEXT    NOT NULL UNIQUE,
"password"   	TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
"id" 		      INTEGER PRIMARY KEY AUTOINCREMENT,
"name"            TEXT    NOT NULL UNIQUE,
"parent_id"       TEXT    ,
"account_id"      INTEGER NOT NULL,
FOREIGN KEY("account_id" ) REFERENCES "account"("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "transaction" (
"id"           INTEGER PRIMARY KEY AUTOINCREMENT,
"type"         INTEGER NOT NULL,
"sum"          INTEGER NOT NULL,
"description"  TEXT    ,
"date_time"    INTEGER ,
"category_id"  INTEGER ,
"account_id"   INTEGER NOT NULL,
FOREIGN KEY("category_id")  REFERENCES "category"("id") ON DELETE SET NULL,
FOREIGN KEY("account_id") REFERENCES "account"("id") ON DELETE CASCADE
);
COMMIT;





