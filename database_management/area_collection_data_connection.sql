-- Create area_collection_data_connection view for API to hit. Aggregates unique list
-- of collections per area
DROP VIEW IF EXISTS "area_collection_data_connection";
CREATE VIEW "area_collection_data_connection" as
SELECT resource.resource,
  collection.name,
  area_type.area_type,
  area_type.area_type_name,
  area_type.area_type_id

FROM resource

LEFT JOIN area_type ON area_type.area_type_id=resource.area_type_id

LEFT JOIN collection on collection.collection_id=resource.collection_id

GROUP BY resource.resource,
         area_type.area_type_id,
         collection.collection_id;
