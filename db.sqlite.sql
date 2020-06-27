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
"name"            TEXT    NOT NULL,
"parent_id"       INTEGER,
"account_id"      INTEGER NOT NULL,
"path"            TEXT DEFAULT '',
FOREIGN KEY("account_id") REFERENCES "account"("id") ON DELETE CASCADE,
FOREIGN KEY("parent_id") REFERENCES "category"("id") ON DELETE CASCADE,
CONSTRAINT UC_Category UNIQUE (account_id, name)
);

CREATE INDEX cp_idx ON category (`path`);

CREATE TRIGGER category__ai_path_set AFTER INSERT ON category
BEGIN
    -- Вычисление материализованного пути.
    UPDATE category
        SET path =
            CASE
                WHEN parent_id IS NULL THEN '.' || NEW.id || '.'
                ELSE (
                        SELECT path || NEW.id || '.'
                        FROM category
                        WHERE id = NEW.parent_id
                    )
            END
        WHERE id = NEW.id;
END;

CREATE TRIGGER category__bd_category_remove BEFORE DELETE ON category
BEGIN
    -- Удалить всех потомков.
    DELETE FROM category
    WHERE path LIKE OLD.path || '_%';
END;

CREATE TRIGGER category__bu_integrity_check BEFORE UPDATE OF id, path ON category
BEGIN
    SELECT
        CASE
            WHEN OLD.id != NEW.id -- Смена id?
                OR NEW.parent_id IS OLD.id -- Ссылка на самого себя как на предка?
                OR NEW.path !=
                    CASE
                        WHEN NEW.parent_id IS NULL THEN '.' || OLD.id || '.'
                        ELSE (
                                SELECT path || OLD.id || '.'
                                FROM category
                                WHERE id = NEW.parent_id
                            )
                    END -- Материализованный путь не соответствует рассчетному?
                OR NEW.path LIKE '%.' || OLD.id || '._%' -- Закольцовка пути?
                    THEN RAISE(ABORT, 'An attempt to damage the integrity of the category.')
        END;
END;

CREATE TRIGGER category__au_path_update AFTER UPDATE OF parent_id ON category
BEGIN
    SELECT
        CASE
            WHEN NEW.parent_id IS OLD.id -- Ссылка на самого себя?
                    THEN RAISE(ABORT, 'An attempt to damage the integrity of the category.')
        END;
    -- Массовое обновление материализованного пути у текущей строки и у всех потомков.
    UPDATE category
        SET path = REPLACE(
                path,
                OLD.path,
                CASE
                    WHEN NEW.parent_id IS NULL THEN '.' || OLD.id || '.'
                    ELSE (
                            SELECT path || OLD.id || '.'
                            FROM category
                            WHERE id = NEW.parent_id
                        )
                END
            )
        WHERE path LIKE OLD.path || '%';
END;

CREATE TABLE IF NOT EXISTS "transaction" (
"id"           INTEGER PRIMARY KEY AUTOINCREMENT,
"type"         INTEGER NOT NULL,
"sum"          INTEGER NOT NULL,
"description"  TEXT    ,
"date_time"    INTEGER NOT NULL,
"category_id"  INTEGER ,
"account_id"   INTEGER NOT NULL,
FOREIGN KEY("category_id") REFERENCES "category"("id") ON DELETE SET NULL,
FOREIGN KEY("account_id") REFERENCES "account"("id") ON DELETE CASCADE
);
COMMIT;





