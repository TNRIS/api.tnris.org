## Notes
 * `area_type` table geometry held in the duplicate area_type table dataset in Carto.
 * A copy of the initial dataset upload zipfile/FGDB is located at `./etl/source_data/area_type_carto/area_type.zip`.
 * Records in the area_type table are static to include all state, county, quad, and quarter-quad bounds. Any edits to the `area_type` table must occur in the Carto dataset of the same name (plus geometry) since it is a duplicate but not programmatically linked to the LCD table.
 * 19 record discrepancies existed upon initial creation of the Carto dataset. These records were part of the quad and qquad polygon datasets but were not part of the database `area_type` table (sourced from the historic data-download 'area' table). They were added and updated to the dataset with their "orig_data_download_id" populated with the value `666666`.
* all new area_type polygons which did not previously exist in the original data download have had "orig_data_download_id" populated with `666666`
