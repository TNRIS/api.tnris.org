--
-- NOT USED IN PRODUCTION. SAVED ONLY FOR REFERENCE
-- THIS WAS TEST SQL FOR TRIGGERS TO REFRESH THE MATERIALIZED VIEW
-- PERFORMANCE BUSTED IN ADMIN CONSOLE AS THIS CODE TOOK TOO LONG TO EXECUTE
-- THIS FUNCTIONALITY WAS MIGRATED TO 'lambda-refresh_materialized_views'
--

-- CHC materialized view refresh
DROP TRIGGER IF EXISTS historical_collection_change ON historical_collection;
DROP TRIGGER IF EXISTS county_relate_change ON county_relate;
DROP TRIGGER IF EXISTS photo_index_scanned_ls4_link_change ON photo_index_scanned_ls4_link;
DROP TRIGGER IF EXISTS product_change ON product;
DROP TRIGGER IF EXISTS agency_change ON agency;

DROP FUNCTION IF EXISTS refresh_chc_view();

-- the function
CREATE OR REPLACE FUNCTION refresh_chc_view()
  RETURNS trigger AS $$
    BEGIN
      REFRESH MATERIALIZED VIEW compiled_historical_collection with DATA;
      RETURN NULL;
    END
  $$
  LANGUAGE plpgsql;

-- the triggers wired to all view related, non-domain tables
CREATE TRIGGER historical_collection_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON historical_collection
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_chc_view();

CREATE TRIGGER county_relate_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON county_relate
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_chc_view();

CREATE TRIGGER photo_index_scanned_ls4_link_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON photo_index_scanned_ls4_link
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_chc_view();

CREATE TRIGGER product_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON product
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_chc_view();

CREATE TRIGGER agency_change
  AFTER INSERT or UPDATE or DELETE or TRUNCATE
  ON agency
  FOR EACH STATEMENT
  EXECUTE PROCEDURE refresh_chc_view();
