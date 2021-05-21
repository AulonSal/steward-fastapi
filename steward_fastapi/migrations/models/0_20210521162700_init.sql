-- upgrade --
CREATE TABLE IF NOT EXISTS "agent" (
    "username" VARCHAR(50) NOT NULL  PRIMARY KEY,
    "disabled" BOOL NOT NULL  DEFAULT False,
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
    "id" SERIAL NOT NULL PRIMARY KEY,
    "source_id" VARCHAR(50) NOT NULL REFERENCES "contentsource" ("name") ON DELETE CASCADE,
    "type_id" VARCHAR(50) NOT NULL REFERENCES "contenttype" ("name") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
