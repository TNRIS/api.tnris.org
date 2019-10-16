-- Create collection_catalog_records view for API to hit. Aggregates values from all
-- associated lookup tables. This SQL only needs to be run after initial database
-- creation
-- Main collection api endpoint for LCD non-historical datasets: api/v1/collections
DROP MATERIALIZED VIEW IF EXISTS "collection_catalog_record";

CREATE MATERIALIZED VIEW "collection_catalog_record" as
SELECT collection.collection_id,
  collection.name,
  collection.acquisition_date,
	collection.short_description,
	collection.description,
  collection.partners,
	collection.authoritative,
	collection.public,
	collection.known_issues,
	collection.wms_link,
	collection.popup_link,
	collection.carto_map_id,
	collection.thumbnail_image,
	collection.tile_index_url,
	collection.supplemental_report_url,
	collection.lidar_breaklines_url,
    collection.lidar_buildings_url,
	collection.coverage_extent,
	collection.tags,
	string_agg(distinct category_type.filter_name, ',' order by category_type.filter_name) as category,
	string_agg(distinct epsg_type.epsg_code::char(10), ',' order by epsg_type.epsg_code::char(10)) as spatial_reference,
	string_agg(distinct file_type.file_type, ',' order by file_type.file_type) as file_type,
	string_agg(distinct resolution_type.resolution, '/' order by resolution_type.resolution) as resolution,
	string_agg(distinct use_type.use_type, ',' order by use_type.use_type) as recommended_use,
  string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation) as resource_types,
  string_agg(distinct image.image_url, ',') as images,
  string_agg(distinct outside_entity_services.service_name, ', ' order by outside_entity_services.service_name) as oe_service_names,
  string_agg(distinct outside_entity_services.service_url, ', ' order by outside_entity_services.service_url) as oe_service_urls,


  CASE
    -- if an outside-entity template, override database counties and attribute
    -- all counties, otherwise use the collection_county_relate table
    WHEN (template_type.template = 'outside-entity')
    THEN (
      SELECT
      string_agg(distinct area_type_name, ', ') as counties
      FROM area_type
      WHERE area_type = 'county'
    )
    ELSE (string_agg(distinct area_type.area_type_name, ', ' order by area_type.area_type_name))
  END AS counties,
  CASE
    -- use resource_types from relate table to determine data_types (only for tnris-download)
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*(HYPSO|LPC|VECTOR).*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*(BW|NC|CIR|NC-CIR|DEM|MAP|LC).*')
      ) THEN 'Raster,Vector'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*(BW|NC|CIR|NC-CIR|DEM|MAP|LC).*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*(HYPSO|LPC|VECTOR).*')
      ) THEN 'Raster'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*(HYPSO|LPC|VECTOR).*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*(BW|NC|CIR|NC-CIR|DEM|MAP|LC).*')
      ) THEN 'Vector'
    ELSE NULL
  END AS data_types,
  CASE
    -- use resource_types from relate table to determine band_types (only for tnris-download)
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*CIR.*')
    ) THEN 'BW,NC,CIR'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*CIR.*')
    ) THEN 'BW,NC'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*CIR.*')
    ) THEN 'BW,CIR'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*CIR.*')
    ) THEN 'NC,CIR'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*CIR.*')
    ) THEN 'BW'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*CIR.*')
    ) THEN 'NC'
    WHEN (
      (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*BW.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      !~ '.*NC.*')
      AND (string_agg(distinct resource_type.resource_type_abbreviation, ',' order by resource_type.resource_type_abbreviation)
      ~ '.*CIR.*')
    ) THEN 'CIR'
    ELSE NULL
  END AS band_types,
  source_type.source_name,
	source_type.source_abbreviation,
	source_type.source_website,
  source_type.source_data_website,
	source_type.source_contact,
	license_type.license_name,
	license_type.license_abbreviation,
	license_type.license_url,
	template_type.template,
  template_type.filter_name as availability
FROM collection

LEFT JOIN category_relate ON category_relate.collection_id=collection.collection_id
LEFT JOIN category_type ON category_type.category_type_id=category_relate.category_type_id

LEFT JOIN epsg_relate ON epsg_relate.collection_id=collection.collection_id
LEFT JOIN epsg_type ON epsg_type.epsg_type_id=epsg_relate.epsg_type_id

LEFT JOIN file_type_relate ON file_type_relate.collection_id=collection.collection_id
LEFT JOIN file_type ON file_type.file_type_id=file_type_relate.file_type_id

LEFT JOIN resolution_relate ON resolution_relate.collection_id=collection.collection_id
LEFT JOIN resolution_type ON resolution_type.resolution_type_id=resolution_relate.resolution_type_id

LEFT JOIN use_relate ON use_relate.collection_id=collection.collection_id
LEFT JOIN use_type ON use_type.use_type_id=use_relate.use_type_id

LEFT JOIN resource_type_relate ON resource_type_relate.collection_id=collection.collection_id
LEFT JOIN resource_type ON resource_type.resource_type_id=resource_type_relate.resource_type_id

LEFT JOIN source_type ON source_type.source_type_id=collection.source_type_id

LEFT JOIN license_type ON license_type.license_type_id=collection.license_type_id

LEFT JOIN template_type ON template_type.template_type_id=collection.template_type_id

LEFT JOIN image ON image.collection_id = collection.collection_id

LEFT JOIN collection_county_relate ON collection_county_relate.collection_id=collection.collection_id
LEFT JOIN area_type ON area_type.area_type_id=collection_county_relate.area_type_id

LEFT JOIN outside_entity_services ON outside_entity_services.collection_id = collection.collection_id

GROUP BY collection.collection_id,
        source_type.source_name,
				source_type.source_abbreviation,
				source_type.source_website,
        source_type.source_data_website,
				source_type.source_contact,
				license_type.license_name,
				license_type.license_abbreviation,
				license_type.license_url,
				template_type.template,
        template_type.filter_name

WITH DATA;
