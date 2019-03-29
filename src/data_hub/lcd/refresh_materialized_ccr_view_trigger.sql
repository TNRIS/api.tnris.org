-- CCR materialized view refresh
DROP TRIGGER IF EXISTS collection_change ON collection;
DROP TRIGGER IF EXISTS category_relate_change ON category_relate;
DROP TRIGGER IF EXISTS epsg_relate_change ON epsg_relate;
DROP TRIGGER IF EXISTS file_type_relate_change ON file_type_relate;
DROP TRIGGER IF EXISTS resolution_relate_change ON resolution_relate;
DROP TRIGGER IF EXISTS collection_county_relate_change ON collection_county_relate;
DROP TRIGGER IF EXISTS use_relate_change ON use_relate;
DROP TRIGGER IF EXISTS resource_type_relate_change ON resource_type_relate;
DROP TRIGGER IF EXISTS image_change ON image;

-- the function
CREATE OR REPLACE FUNCTION refresh_ccr_view()
  RETURNS trigger AS $$
    BEGIN
      REFRESH MATERIALIZED VIEW collection_catalog_record with DATA;
      RETURN NULL;
    END
  $$
  LANGUAGE plpgsql;

-- the triggers wired to all view related, non-domain tables
CREATE TRIGGER collection_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON collection
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER category_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON category_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER epsg_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON epsg_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER file_type_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON file_type_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER resolution_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON resolution_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER collection_county_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON collection_county_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER use_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON use_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER resource_type_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON resource_type_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();

CREATE TRIGGER image_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON image
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_ccr_view();
