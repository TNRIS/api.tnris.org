-- Create areas view for API to hit. Aggregates collection_id values from resources.
-- This SQL only needs to be run after initial database creation
DROP VIEW IF EXISTS "areas";
CREATE VIEW "areas" as

WITH historical_county_join as (
  WITH county_area_join as (
  SELECT
  county.id as county_id,
  county.fips as county_fips,
  county.name as county_name,
  area_type.area_type_id,
  area_type.area_type,
  area_type.area_code
  FROM county
  INNER JOIN area_type on county.fips = area_type.area_code::int8)
  SELECT
  county_area_join.county_id,
  county_area_join.county_fips,
  county_area_join.county_name,
  county_area_join.area_type_id,
  county_area_join.area_type,
  county_area_join.area_code,
  string_agg(CAST(county_relate.collection_id as varchar), ',') as collections
  FROM county_area_join
  LEFT JOIN county_relate ON county_area_join.county_id = county_relate.county_id
  GROUP BY county_area_join.county_id,
  county_area_join.county_fips,
  county_area_join.county_name,
  county_area_join.area_type_id,
  county_area_join.area_type,
  county_area_join.area_code
)

SELECT
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type,
  string_agg(CAST(resource.collection_id as varchar), ',') as download,
  historical_county_join.collections as historical,
  CASE
    WHEN historical_county_join.collections IS NULL
    THEN string_agg(CAST(resource.collection_id as varchar), ',')
    ELSE concat_ws(',',
                  string_agg(CAST(resource.collection_id as varchar), ','),
                  historical_county_join.collections)
  END AS collections
FROM
  resource

INNER JOIN area_type
ON resource.area_type_id = area_type.area_type_id

LEFT JOIN historical_county_join
ON resource.area_type_id = historical_county_join.area_type_id

GROUP BY
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type,
  historical_county_join.collections;
