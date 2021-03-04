-- Create resource_management view for API to hit. Aggregates unique list
-- of resources per collection with resource_type joins
-- Main collection api endpoint for LCD non-historical dataset resources/downloads (download map): api/v1/resources
DROP MATERIALIZED VIEW IF EXISTS "resource_management";

CREATE MATERIALIZED VIEW "resource_management" as
SELECT resource.resource_id,
  resource.resource,
  resource.filesize,
  resource.area_type_id,
  resource.collection_id,
  resource_type.resource_type_name,
  resource_type.resource_type_abbreviation,
  area_type.area_type,
  area_type.area_type_name

FROM resource

LEFT JOIN resource_type ON resource_type.resource_type_id=resource.resource_type_id
LEFT JOIN area_type ON area_type.area_type_id=resource.area_type_id

GROUP BY area_type.area_type_name,
        resource.area_type_id, --group by area_type_id first? any objections?
		    resource_type.resource_type_name, --group by area_type_name, idea is like-with-like by default
        resource.resource_id, --
        resource.resource,
        resource.filesize,
        resource.collection_id,
        resource_type.resource_type_abbreviation,
        area_type.area_type

 WITH DATA;
