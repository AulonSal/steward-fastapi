-- upgrade --
CREATE TABLE IF NOT EXISTS "agent" (
    "username" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "disabled" INT NOT NULL  DEFAULT 0,
    "hashed_password" VARCHAR(200) NOT NULL
);
CREATE TABLE IF NOT EXISTS "contentsource" (
    "name" VARCHAR(50) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "contenttype" (
    "name" VARCHAR(50) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "content" (
    "meta" TEXT,
    "url" VARCHAR(300) NOT NULL UNIQUE,
    "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "type_id" VARCHAR(50) NOT NULL REFERENCES "contenttype" ("name") ON DELETE CASCADE,
    "source_id" VARCHAR(50) NOT NULL REFERENCES "contentsource" ("name") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "flexibledata" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "category_1" VARCHAR(50) NOT NULL,
    "category_2" VARCHAR(50) NOT NULL,
    "data" TEXT NOT NULL  /* Freeform json data to suit any use case before the implementation is finalised */
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
