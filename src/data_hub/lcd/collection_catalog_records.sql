-- Create collection_catalog_records view for API to hit. Aggregates values from all
-- associated lookup tables. This SQL only needs to be run after initial database
-- creation
DROP VIEW IF EXISTS "collection_catalog_records";
CREATE VIEW "collection_catalog_records" as
SELECT collection.name,
	collection.acquisition_date,
	collection.short_description,
	collection.description,
	collection.source,
	collection.authoritative,
	collection.known_issues,
	collection.wms_link,
	collection.popup_link,
	collection.carto_map_id,
	collection.overview_image,
	collection.thumbnail_image,
	collection.natural_image,
	collection.urban_image,
	collection.tile_index_url,
	collection.supplemental_report_url,
	collection.lidar_breaklines_url,
	collection.coverage_extent,
	collection.tags,
	string_agg(distinct band_type.band_abbreviation, ',' order by band_type.band_abbreviation) as bands,
	string_agg(distinct category_type.category, ',' order by category_type.category) as categories,
	string_agg(distinct data_type.data_type, ',' order by data_type.data_type) as data_type,
	string_agg(distinct epsg_type.epsg_code, ',' order by epsg_type.epsg_code) as spatial_reference,
	string_agg(distinct file_type.file_type, ',' order by file_type.file_type) as file_type,
	string_agg(distinct resolution_type.resolution, '/' order by resolution_type.resolution) as resolution,
	string_agg(distinct use_type.use_type, ',' order by use_type.use_type) as uses
FROM collection
LEFT JOIN band_relate ON band_relate.collection_id=collection.collection_id
LEFT JOIN band_type ON band_type.band_type_id=band_relate.band_type_id

LEFT JOIN category_relate ON category_relate.collection_id=collection.collection_id
LEFT JOIN category_type ON category_type.category_type_id=category_relate.category_type_id

LEFT JOIN data_type_relate ON data_type_relate.collection_id=collection.collection_id
LEFT JOIN data_type ON data_type.data_type_id=data_type_relate.data_type_id

LEFT JOIN epsg_relate ON epsg_relate.collection_id=collection.collection_id
LEFT JOIN epsg_type ON epsg_type.epsg_type_id=epsg_relate.epsg_type_id

LEFT JOIN file_type_relate ON file_type_relate.collection_id=collection.collection_id
LEFT JOIN file_type ON file_type.file_type_id=file_type_relate.file_type_id

LEFT JOIN resolution_relate ON resolution_relate.collection_id=collection.collection_id
LEFT JOIN resolution_type ON resolution_type.resolution_type_id=resolution_relate.resolution_type_id

LEFT JOIN use_relate ON use_relate.collection_id=collection.collection_id
LEFT JOIN use_type ON use_type.use_type_id=use_relate.use_type_id

WHERE collection.public = True
GROUP BY collection.collection_id;