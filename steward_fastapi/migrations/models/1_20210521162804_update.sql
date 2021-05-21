-- upgrade --
ALTER TABLE "content" ADD "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
-- downgrade --
ALTER TABLE "content" DROP COLUMN "date";
