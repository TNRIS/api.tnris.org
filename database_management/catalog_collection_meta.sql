/** SQL for creating the materialized table 'catalog_collection_meta'
this materialized view contains the combined historical and contemporary collection metadata
required for generating the catalog view. it generates a common schema for key metadata fields held
roughly in common between the two types of datasets for a unified querying / search experience on the 
front end with data.tnris.org **/

DROP MATERIALIZED VIEW IF EXISTS catalog_collection_meta;
CREATE MATERIALIZED VIEW catalog_collection_meta AS
 SELECT c.collection_id,
    c.thumbnail_image,
    c.acquisition_date::date AS acquisition_date,
    c.tile_index_url,
    c.description,
    c.public,
    c.counties,
    c.source_name,
    c.source_abbreviation,
    c.license_name,
    c.license_abbreviation,
    c.license_url,
    c.name,
    c.template,
    CASE
        WHEN c.wms_link IS NOT NULL THEN concat(c.availability, ',', 'WMS_Service')
        ELSE c.availability
    END AS availability,
    c.category,
    c.recommended_use,
    c.file_type,
    g.the_geom
   FROM collection_catalog_record c
     LEFT JOIN collection_footprint g ON c.collection_id = g.collection_id_id
UNION
 SELECT h.collection_id,
    h.thumbnail_image,
    h.acquisition_date,
    h.index_service_url AS tile_index_url,
    h.about AS description,
    h.public,
    h.counties,
    h.source_name,
    h.source_abbreviation,
    h.license_name,
    h.license_abbreviation,
    h.license_url,
    h.name,
    h.template,
    h.availability,
    h.category,
    h.recommended_use,
    'TIFF'::text AS file_type,
    ( SELECT st_simplifypreservetopology(st_union(geom.the_geom), 0.05::double precision) AS the_geom
           FROM ( SELECT a_t_g.wkb_geometry AS the_geom
                   FROM county_relate c_r
                     RIGHT JOIN county c ON c_r.county_id = c.id
                     RIGHT JOIN area_type a_t ON c.name::text = a_t.area_type_name
                     RIGHT JOIN area_type_geom a_t_g ON a_t.area_type_id = a_t_g.area_type_id
                  WHERE c_r.collection_id = h.collection_id) geom) AS the_geom
   FROM compiled_historical_collection h;