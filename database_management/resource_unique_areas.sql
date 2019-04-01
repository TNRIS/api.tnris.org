-- Create resource_unique_areas view for API to hit. Aggregates unique list
-- of collection area_types
DROP VIEW IF EXISTS "resource_unique_areas";
CREATE VIEW "resource_unique_areas" as
SELECT row_number() OVER () AS id, resource.collection_id, area_type.area_type
FROM resource
LEFT JOIN area_type ON area_type.area_type_id=resource.area_type_id
GROUP BY resource.collection_id, area_type.area_type
ORDER BY collection_id;
