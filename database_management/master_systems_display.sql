-- Create master_systems_display view for API to hit. Aggregates values from all
-- associated lookup tables. This SQL only needs to be run after initial database
-- creation
-- Main collection api endpoint for MSD historical datasets: api/v1/map/collections/
DROP MATERIALIZED VIEW IF EXISTS "master_systems_display";

CREATE MATERIALIZED VIEW "master_systems_display" as
SELECT map_collection.map_collection_id as collection_id,
  map_collection.name,
  map_collection.publish_date,
  map_collection.description,
  map_collection.thumbnail_link,
  map_collection.public,
  -- json list of data collections
  array_to_string(ARRAY(SELECT json_build_object(collection.collection_id, collection.name)
        FROM collection
        LEFT JOIN map_data_relate ON map_data_relate.collection_id=collection.collection_id
        -- LEFT JOIN collection ON collection.collection_id=map_data_relate.collection_id
        WHERE map_data_relate.map_collection_id=map_collection.map_collection_id
        ORDER BY collection.name), ',') as data_collections,
  -- json list of map downloads
  array_to_string(ARRAY(SELECT json_build_object('url', map_download.download_url,
                                'label', map_download.label,
                                'map_size', map_size.label,
                                'width', map_size.width,
                                'length', map_size.length,
                                'ppi', pixels_per_inch.pixels_per_inch)
        FROM map_download
        LEFT JOIN map_size ON map_size.id=map_download.map_size_id
        LEFT JOIN pixels_per_inch ON pixels_per_inch.id=map_download.pixels_per_inch_id
        WHERE map_download.map_collection_id=map_collection.map_collection_id
        ORDER BY map_size.label), ',') as map_downloads
FROM map_collection

GROUP BY map_collection.map_collection_id

WITH DATA;
