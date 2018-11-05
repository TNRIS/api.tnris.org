-- Create areas view for API to hit. Aggregates collection_id values from resources.
-- This SQL only needs to be run after initial database creation
DROP VIEW IF EXISTS "areas";
CREATE VIEW "areas" as
SELECT
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type,
  string_agg(CAST(resource.collection_id as varchar), ',') as collections
FROM
  resource
INNER JOIN area_type
ON resource.area_type_id = area_type.area_type_id
GROUP BY
  resource.area_type_id,
  area_type.area_type_name,
  area_type.area_type;
