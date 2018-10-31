-- temp etl view. shouldn't be needed after initial etl
DROP VIEW IF EXISTS "etl_scanned_index";
CREATE VIEW "etl_scanned_index" as
SELECT historical_collection.id as collection_id,
  string_agg(distinct county.name, ',' order by county.name) as county,
  agency.abbreviation as agency,
  EXTRACT(year FROM historical_collection.from_date) as from_date,
  EXTRACT(year FROM historical_collection.to_date) as to_date

FROM historical_collection

LEFT JOIN county_relate ON county_relate.collection_id=historical_collection.id
LEFT JOIN county ON county.id=county_relate.county_id

LEFT JOIN agency ON agency.id=historical_collection.agency_id

GROUP BY historical_collection.id,
         agency.name,
         agency.abbreviation;
