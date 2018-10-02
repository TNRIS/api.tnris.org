import { createSelector } from 'reselect';

const getResources = (state) => state.collections.selectedCollectionResources;

// selector for building object of downloadable resources subnested within
// object of area_type_ids
export const getResourceAreas = createSelector(
  [ getResources ],
  (resources) => {
    // Check if resources are in the state
    if (resources.result) {
      // build object of resources key'd by resource_type (subnested)
      const byId = resources.entities.resourcesById;
      // start with empty object
      const map = {};
      // iterate all resources
      Object.keys(byId).forEach((id) => {
        const rsc = byId[id];
        const cur = map[rsc.area_type_id];
        const lyr = rsc.resource_type_abbreviation;
        // if area_type_id isn't present in parent object, create it.
        // otherwise, update current value
        if (!cur) {
          var n = {};
          n[lyr] = {
            'link': rsc.resource,
            'name': rsc.resource_type_name,
            'filesize': rsc.filesize
          };
          map[rsc.area_type_id] = n;
        }
        else {
          cur[lyr] = {
            'link': rsc.resource,
            'name': rsc.resource_type_name,
            'filesize': rsc.filesize
          };
          map[rsc.area_type_id] = cur;
        }
      });
      return map;
    }
  }
)

// selector for building object of area_type key'd list of area_type_ids
export const getResourceAreaTypes = createSelector(
  [ getResources ],
  (resources) => {
    // Check if resources are in the state
    if (resources.result) {
      // build object of resources key'd by resource_type (subnested)
      const byId = resources.entities.resourcesById;
      // start with empty object
      const map = {};
      // iterate all resources
      Object.keys(byId).forEach((id) => {
        const rsc = byId[id];
        const cur = map[rsc.area_type];
        // if area_type isn't present in parent object, create it.
        // otherwise, update current value
        if (!cur) {
          var n = [];
          n.push(rsc.area_type_id);
          map[rsc.area_type] = n;
        }
        else {
          var n = cur;
          n.push(rsc.area_type_id);
          map[rsc.area_type] = n;
        }
      });
      return map;
    }
  }
)
