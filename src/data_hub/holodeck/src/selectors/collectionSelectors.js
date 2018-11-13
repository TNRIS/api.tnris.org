import { createSelector } from 'reselect';
import elasticlunr from 'elasticlunr';

const getCollections = (state) => state.collections.items;
const getFilters = (state) => state.collectionFilter.collectionFilter;
const getSearchQuery = (state) => state.collectionSearcher.collectionSearchQuery;
const getSortOrder = (state) => state.sorter.sortOrder;
const getFilterMapFilter = (state) => state.collectionFilterMap.collectionFilterMapFilter;
const setTimeslider = (state) => state.collectionTimeslider.collectionTimeslider;

// ///////////////////////////////////////////////////////////////
// Below are the selectors that pertain to filtering, sorting,
// and searching the collections in the catalog.
// This group of selectors are more generic and used my multiple other
// selectors & components, including the ToolDrawer filter chain
// ///////////////////////////////////////////////////////////////

export const getAllCollections = createSelector(
  [ getCollections ],
  (collections) => {
    // Check if collections are ready in the state
    if (collections.result) {
      // return just the collection details object; key'd by collection_id
      return collections.entities.collectionsById;
    }
  }
);

export const getAllCollectionIds = createSelector(
  [ getCollections ],
  (collections) => {
    // Check if collections are ready in the state
    if (collections.result) {
      // return just the collection_id array (collections.result)
      return collections.result;
    }
  }
);

export const getSearchIndex = createSelector(
  [ getCollections ],
  (collections) => {
    // Here we set which fields we want to add to the search index.
    // The fieldnames must match a property of the collections object.
    // These are the fields from the collection that will be searched.
    const searchFields = [
      'name',
      'description',
      'counties',
      'acquisition_date',
      'agency_name',
      'agency_abbreviation'
    ];
    const searchIndex = elasticlunr(function() {
      searchFields.map(field => {
        this.addField(field);
        return field;
      })
      this.setRef('collection_id');
    });

    // Check if collections are ready in the state. If so, map the array of
    // collection ids and set their chosen field values in the search
    // document, then add it to the index.
    if (collections.result) {
      collections.result.map(collectionId => {
        let doc = {'collection_id': collectionId};
        searchFields.map(field => {
          doc[field] = collections.entities.collectionsById[collectionId][field];
          return field;
        })
        searchIndex.addDoc(doc);
        return collectionId;
      })
    }
    return searchIndex;
  }
);

// Sets up the choices available to the CollectionFilter component fom the
// available properties in the collections object.
export const getCollectionFilterChoices = createSelector(
  [ getAllCollections, getAllCollectionIds ],
  (collections, collectionIds) => {
    // Here we set which properties will be available to the filter.
    // The key must match a property of the collections object and
    // the value is an empty array.
    const collectionFilterChoices = {
      template: [],
      category: []
    };
    // If collections are in ready the state, continue setting the value arrays in the
    // collectionFilterChoices object from above.
    if (collections) {
      collectionIds.map(collectionId => {
        for (let key in collectionFilterChoices) {
          if (collectionFilterChoices.hasOwnProperty(key)) {
            // need to check if collection has a
            // value for the key so it can be split
            if (collections[collectionId][key]) {
              let collectionPropertyValues = collections[collectionId][key].split(',');
              collectionPropertyValues.map(propertyValue => {
                if (collectionFilterChoices[key].indexOf(propertyValue) < 0) {
                  collectionFilterChoices[key].push(propertyValue);
                }
                return propertyValue;
              })
            }
          }
          collectionFilterChoices[key].sort();
        }
        return collectionId;
      })
    }
    return collectionFilterChoices;
  }
);

export const getCollectionTimesliderRange = createSelector(
  [ getCollections ],
  (collections) => {
    // Check if collections are ready in the state
    if (collections.result) {
      let range = [0, 0];
      collections.result.map(collectionId => {
        const coll = collections.entities.collectionsById[collectionId];
        const year = coll.acquisition_date ? parseInt(coll.acquisition_date.substring(0, 4), 10) : 0;
        if (year !== 0) {
          if (range[0] === 0 || year < range[0]) {
            range[0] = year;
          }
          if (range[1] === 0 || year > range[1]) {
            range[1] = year;
          }
        }
        return year;
      });
      // return the range array [min year, max year]
      return range;
    }
    else {
      return setTimeslider;
    }
  }
);

// ///////////////////////////////////////////////////////////////
// Below are the chained selectors which use the search, timeslider,
// filter checkboxes, filter map, and sort components in then
// ToolDrawer sidebar to change the visible collections array the
// catalog uses to display CollectionCards
// ///////////////////////////////////////////////////////////////

// Returns an array of collections to show in the catalog view.
// If 1 or more filters are set, returns only those collections that pass
// through the filters. If no filters are set, or on initial page load,
// returns an array of all collection_ids available in the catalog.
export const getFilteredCollections = createSelector(
  [ getAllCollections, getAllCollectionIds, getFilters ],
  (collections, collectionIds, filters) => {
    // Check if collections are ready in the state
    if (collections) {
      let filteredCollectionIds = [];
      let multiFilteredCollectionIds = [];
      collectionIds.map(collectionId => {
        for (let key in filters) {
          if (filters.hasOwnProperty(key)) {
            // need to check if collection has a
            // value for the key so it can be split
            if (collections[collectionId][key]) {
              let collectionPropertyValues = collections[collectionId][key].split(',');
              collectionPropertyValues.map(propertyValue => {
                if (filters[key].indexOf(propertyValue) >= 0) {
                  if (filteredCollectionIds.indexOf(collectionId) < 0) {
                    // set collection_ids that pass the filter conditions
                    // into this array
                    filteredCollectionIds.push(collectionId);
                  } else {
                    // set any duplicate collection_ids from the conditional
                    // above into this array to account for cross filtering
                    multiFilteredCollectionIds.push(collectionId);
                  }
                }
                return propertyValue;
              })
            }
          }
        }
        return collectionId;
      })
      // when no filters are set, return all collection_ids to make all
      // collections available to the view
      if (Object.keys(filters).length < 1) {
        return collectionIds;
      }
      // when 1 or more filters are set, return the collection_ids that
      // pass through those filters. The multiFilteredCollectionIds account
      // for cross filtering scenarios.
      return Object.keys(filters).length > 1 ? multiFilteredCollectionIds : filteredCollectionIds;
    }
  }
);

// Returns an array of collections to show in the catalog view.
// If the user has set a map filter, returns only those collections
// that pass through the map filter.
export const getMapFilteredCollections = createSelector(
  [ getFilteredCollections, getFilterMapFilter ],
  (collectionIds, filterMapFilter) => {
    let mapFilteredCollectionIds = [];
    if (filterMapFilter.length > 0) {
      collectionIds.map(collectionId => {
        if (filterMapFilter.indexOf(collectionId) >= 0) {
          mapFilteredCollectionIds.push(collectionId);
        }
        return collectionId;
      })
      return mapFilteredCollectionIds;
    }
    mapFilteredCollectionIds = collectionIds;
    return mapFilteredCollectionIds;
  }
)

// Returns an array of collections to show in the catalog view.
// If the user has entered a search query, returns only those collections
// that return from the search.
export const getSearchedCollections = createSelector(
  [ getAllCollections, getMapFilteredCollections, getSearchQuery, getSearchIndex ],
  (collections, collectionIds, searchQuery, searchIndex) => {
    // Check if collections are ready in the state
    if (collections) {
      let searchedCollectionIds = [];
      if (searchQuery) {
        let queryResult = searchIndex.search(searchQuery, {expand: true});
        if (!Array.isArray(queryResult) || !queryResult.length) {
          searchedCollectionIds = [];
        } else {
          queryResult.map(result => {
            if (collectionIds.includes(result.ref) && !searchedCollectionIds.includes(result.ref)) {
              searchedCollectionIds.push(result.ref);
            }
            return result;
          })
        }
        return searchedCollectionIds;
      }
      searchedCollectionIds = collectionIds;
      return searchedCollectionIds;
    }
  }
);

// Takes the filtered and searched array of collection ids and reduces them
// to an array of Ids whose collection acquisition_date year is within the
// year range as designated by the CollectionTimeslider component
export const getTimesliderCollections = createSelector(
  [ getAllCollections, getSearchedCollections, setTimeslider ],
  (collections, collectionIds, range) => {
    // Check if collections are ready in the state
    if (collections) {
      let timesliderCollectionIds = [];
      // iterate current searched collection Id list
      collectionIds.map(collectionId => {
        const coll = collections[collectionId];
        const year = coll.acquisition_date ? parseInt(coll.acquisition_date.substring(0, 4), 10) : 0;
        if (year !== 0) {
          if (range[0] <= year && year <= range[1]) {
            timesliderCollectionIds.push(collectionId);
          }
        }
        return year;
      });
      return timesliderCollectionIds;
    }
  }
);

// Takes the filtered array of collection ids and reorders them based on the
// sort order delcared in the store by the Sort component
export const getSortedCollections = createSelector(
  [ getAllCollections, getTimesliderCollections, getSortOrder ],
  (collections, collectionIds, order) => {
    // Check if collections are ready in the state
    if (collections) {
      let sortedCollectionIds = collectionIds;
      // do the order based on the declared field
      switch(order) {
        // order by title/name alphabetically
        case 'AZ':
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.name.toLowerCase() < two.name.toLowerCase())
              return -1;
            if (one.name.toLowerCase() > two.name.toLowerCase())
              return 1;
            return 0;
          });
          break;
        // order by title/name reverse alphabetically
        case 'ZA':
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.name.toLowerCase() > two.name.toLowerCase())
              return -1;
            if (one.name.toLowerCase() < two.name.toLowerCase())
              return 1;
            return 0;
          });
          break;
        // order by the date of the collection newest to oldest
        case 'NEW':
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.acquisition_date > two.acquisition_date)
              return -1;
            if (one.acquisition_date < two.acquisition_date)
              return 1;
            return 0;
          });
          break;
        // order by the date of the collection oldest to newest
        case 'OLD':
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.acquisition_date < two.acquisition_date)
              return -1;
            if (one.acquisition_date > two.acquisition_date)
              return 1;
            return 0;
          });
          break;
        // default order is by title/name alphabetically
        default:
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.name < two.name)
              return -1;
            if (one.name > two.name)
              return 1;
            return 0;
          });
      }
      return sortedCollectionIds;
    }
  }
);
