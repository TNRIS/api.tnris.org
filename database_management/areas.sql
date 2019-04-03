-- Create areas view for API to hit. Aggregates collection_id values from resources.
-- This SQL only needs to be run after initial database creation
-- Main collection api endpoint for all collections (historical and non) area associations: api/v1/areas
-- Used in areas_view CSV generator lambda function which ultimately syncs with Carto for geofilter
DROP VIEW IF EXISTS "areas";

CREATE MATERIALIZED VIEW "areas" as

WITH historical_county_join as (
  -- use county lookup table to attribute county names to area_types
  WITH county_area_join as (
    SELECT
    county.id as county_id,
    county.fips as county_fips,
    county.name as county_name,
    area_type.area_type_id,
    area_type.area_type,
    area_type.area_code
    FROM county
    INNER JOIN area_type on county.fips::text = area_type.area_code
  )
  -- use the county/area join to create collection_id list on those county area_types
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
),

outside_entity_state_join as (
  -- -- use county lookup table to attribute county names to area_types
  WITH outside_area_join as (
    SELECT
    collection.collection_id,
    template_type.template,
    template_type.template_type_id,
    (SELECT area_type.area_type FROM area_type WHERE area_type.area_type = 'state') as area_type,
    (SELECT area_type.area_type_id FROM area_type WHERE area_type.area_type = 'state') as area_type_id
    FROM collection
    INNER JOIN template_type ON collection.template_type_id=template_type.template_type_id
    WHERE template_type.template = 'outside-entity' AND collection.public = true
    ORDER BY collection.collection_id
  )
  -- use the outside/area join to create collection_id list on the state area_type
  SELECT
  area_type.area_type_id,
  area_type.area_type,
  string_agg(CAST(outside_area_join.collection_id as varchar), ',') as collections
  FROM area_type
  INNER JOIN outside_area_join ON outside_area_join.area_type_id = area_type.area_type_id
  GROUP BY area_type.area_type_id
),

order_county_join as (
  -- use collection and template_type tables to create list of order only collection_ids
  WITH order_collections as (
    SELECT
    collection.collection_id
    FROM collection
    INNER JOIN template_type ON collection.template_type_id=template_type.template_type_id
    WHERE template_type.template = 'tnris-order' AND collection.public = true
  )
  -- use the collection/template_type join to create collection_id list for
  -- all associated county area_types
  SELECT
  collection_county_relate.area_type_id,
  string_agg(CAST(collection_county_relate.collection_id as varchar), ',') as collections
  FROM
  collection_county_relate
  INNER JOIN order_collections ON order_collections.collection_id = collection_county_relate.collection_id
  GROUP BY collection_county_relate.area_type_id
)

SELECT
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type,
  -- individual collection_id lists by template_type
  string_agg(CAST(resource.collection_id as varchar), ',') as download,
  historical_county_join.collections as historical,
  outside_entity_state_join.collections as outside_entity,
  order_county_join.collections as order,
  -- aggregated collection_id list of all template_types (this is the
  -- field used by the geography filter)
  concat_ws(',',
            string_agg(CAST(resource.collection_id as varchar), ','),
            historical_county_join.collections,
            outside_entity_state_join.collections,
            order_county_join.collections) as collections
FROM
  resource

INNER JOIN area_type
ON resource.area_type_id = area_type.area_type_id

LEFT JOIN historical_county_join
ON resource.area_type_id = historical_county_join.area_type_id

LEFT JOIN outside_entity_state_join
ON resource.area_type_id = outside_entity_state_join.area_type_id

LEFT JOIN order_county_join
ON resource.area_type_id = order_county_join.area_type_id

GROUP BY
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type,
  historical_county_join.collections,
  outside_entity_state_join.collections,
  order_county_join.collections

WITH DATA;
