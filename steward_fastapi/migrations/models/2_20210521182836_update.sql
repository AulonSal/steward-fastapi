-- upgrade --
CREATE TABLE IF NOT EXISTS "flexibledata" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL,
    "category_1" VARCHAR(50) NOT NULL,
    "category_2" VARCHAR(50) NOT NULL,
    "data" JSONB NOT NULL
);
COMMENT ON COLUMN "flexibledata"."data" IS 'Freeform json data to suit any use case before the implementation is finalised';
-- downgrade --
DROP TABLE IF EXISTS "flexibledata";
