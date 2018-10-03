-- Create resource_management view for API to hit. Aggregates unique list
-- of resources per collection with resource_type joins
DROP VIEW IF EXISTS "resource_management";
CREATE VIEW "resource_management" as
SELECT resource.resource_id,
  resource.resource,
  resource.filesize,
  resource.area_type_id,
  resource.collection_id,
  resource_type.resource_type_name,
  resource_type.resource_type_abbreviation,
  area_type.area_type

FROM resource

LEFT JOIN resource_type ON resource_type.resource_type_id=resource.resource_type_id
LEFT JOIN area_type ON area_type.area_type_id=resource.area_type_id

GROUP BY resource.resource_id,
         resource.resource,
         resource.filesize,
         resource.area_type_id,
         resource.collection_id,
         resource_type.resource_type_name,
         resource_type.resource_type_abbreviation,
         area_type.area_type;
