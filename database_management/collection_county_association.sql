-- Create collection_county_association view for API to hit. Applies list of
-- counties associated with each non-historical-aerial collection based on
-- template type and resources. This SQL only needs to be run after initial database
-- creation
DROP VIEW IF EXISTS "collection_county_association";
CREATE VIEW "collection_county_association" as
SELECT collection.collection_id,
  collection.name,
  template_type.template,
  CASE
    WHEN (
      (template_type.template ~ '.*outside-entity.*')
    ) THEN array_to_string(ARRAY(SELECT county.name
          FROM county
          ORDER BY county.name), ',')
    ELSE 'filler'
  END AS counties

FROM collection

LEFT JOIN template_type ON template_type.template_type_id=collection.template_type_id

GROUP BY collection.collection_id,
				 template_type.template;
