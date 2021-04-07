/** SQL for creating the materialized table 'catalog_collection_meta'
this materialized view contains the combined historical and contemporary collection metadata
required for generating the catalog view. it generates a common schema for key metadata fields held
roughly in common between the two types of datasets for a unified querying / search experience on the 
front end with data.tnris.org **/

DROP MATERIALIZED VIEW IF EXISTS catalog_collection_meta;
CREATE MATERIALIZED VIEW catalog_collection_meta AS
(
	SELECT
	c.collection_id, c.thumbnail_image, c.acquisition_date::DATE, 
	c.tile_index_url, c.description, c.public, c.counties, 
	c.source_name, c.source_abbreviation, c.license_name, 
	c.license_abbreviation, c.license_url, c.name, c.template, 
	c.availability, c.category, c.recommended_use, 
	c.file_type, g.the_geom
	FROM collection_catalog_record c
	RIGHT JOIN collection_coverage_geom g 
	ON c.collection_id = g.collection_id
)
UNION
(
	SELECT
	h.collection_id, h.thumbnail_image, h.acquisition_date::DATE, 
	h.index_service_url as tile_index_url, h.about as description, 
	h.public, h.counties, h.source_name, h.source_abbreviation, 
	h.license_name, h.license_abbreviation, h.license_url, 
	h.name, h.template, h.availability, h.category, 
	h.recommended_use, 'TIFF' as file_type, 
	ST_Polygon('LINESTRING(75 29, 77 29, 77 29, 75 29)'::geometry, 4326) as the_geom
	FROM compiled_historical_collection h
)