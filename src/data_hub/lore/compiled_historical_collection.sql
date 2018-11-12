-- Create compiled_historical_collection view for API to hit. Aggregates values from all
-- associated lookup tables. This SQL only needs to be run after initial database
-- creation
DROP VIEW IF EXISTS "compiled_historical_collection";
CREATE VIEW "compiled_historical_collection" as
SELECT historical_collection.id as collection_id,
  historical_collection.collection,
  historical_collection.from_date,
  historical_collection.to_date as acquisition_date,
  historical_collection.public,
  historical_collection.index_service_url,
  historical_collection.frames_service_url,
  historical_collection.mosaic_service_url,
  string_agg(distinct county.name, ', ' order by county.name) as counties,
  agency.name as agency_name,
  agency.abbreviation as agency_abbreviation,
  array_to_string(ARRAY(SELECT json_build_object('coverage', product.coverage,
                                 'number_of_frames', product.number_of_frames,
                                 'medium', product.medium,
                                 'print_type', product.print_type,
                                 'scale', scale.scale,
                                 'frame_size', frame_size.frame_size)
        FROM product
        LEFT JOIN scale ON scale.id=product.scale_id
        LEFT JOIN frame_size ON frame_size.id=product.frame_size_id
        WHERE product.collection_id=historical_collection.id), ',') as products,
  CASE
    WHEN (
      (string_agg(distinct county.name, ',' order by county.name)
      ~ '.*(,).*')
      ) THEN CONCAT('Multi-County ', agency.abbreviation, ' Historic Imagery')
    ELSE CONCAT(string_agg(distinct county.name, ',' order by county.name), ' ', agency.abbreviation, ' Historic Imagery')
  END AS name,
  'historical-aerial' as template,
  'Order_Only' as availability,
  'https://s3.amazonaws.com/data.tnris.org/historical_thumbnail.jpg' as thumbnail_image,
  'Historic Imagery' as category,
  'Historical Use,Research' as recommended_use,
  array_to_string(ARRAY(SELECT json_build_object('year', photo_index_scanned_ls4_link.year,
                                 'size', photo_index_scanned_ls4_link.size,
                                 'sheet', photo_index_scanned_ls4_link.sheet,
                                 'link', photo_index_scanned_ls4_link.link)
        FROM photo_index_scanned_ls4_link
        WHERE photo_index_scanned_ls4_link.collection_id=historical_collection.id), ',') as scanned_index_ls4_links

FROM historical_collection

LEFT JOIN county_relate ON county_relate.collection_id=historical_collection.id
LEFT JOIN county ON county.id=county_relate.county_id

LEFT JOIN agency ON agency.id=historical_collection.agency_id

GROUP BY historical_collection.id,
         agency.name,
         agency.abbreviation;
