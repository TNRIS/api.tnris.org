import { createSelector } from 'reselect';
import elasticlunr from 'elasticlunr';

const getCollections = (state) => state.collections.items;
const getFilters = (state) => state.collectionFilter.collectionFilter;
const getSearchQuery = (state) => state.collectionSearcher.collectionSearchQuery;
const getSortOrder = (state) => state.sorter.sortOrder;

// ///////////////////////////////////////////////////////////////
// Below are the selectors that pertain to filtering, sorting,
// and searching the collections in the catalog. These are called
// by collectionFilter, CollectionSorter, and CollectionSearcher.
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
      category: [],
      recommended_use: [],
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

// Returns the array of collections to show in the catalog view.
// If a filter is set, returns only those collections that pass
// through the filter.
export const getFilteredCollections = createSelector(
  [ getAllCollections, getAllCollectionIds, getFilters ],
  (collections, collectionIds, filters) => {
    // Check if collections are ready in the state
    if (collections) {
      let filteredCollectionIds = [];
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
                    filteredCollectionIds.push(collectionId);
                  }
                }
                return propertyValue;
              })
            }
          }
        }
        return collectionId;
      })
      return !Array.isArray(filteredCollectionIds) || !filteredCollectionIds.length ?
        collectionIds : filteredCollectionIds;
    }
  }
);

// Returns the array of collections to show in the catalog view.
// If the user has entered a search query, returns only those collections
// that return from the search.
export const getSearchedCollections = createSelector(
  [ getAllCollections, getFilteredCollections, getSearchQuery, getSearchIndex ],
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
      } else {
        searchedCollectionIds = collectionIds;
      }
      return searchedCollectionIds;
    }
  }
);

// Takes the filtered array of collection ids and reorders them based on the
// sort order delcared in the store by the Sort component
export const getSortedCollections = createSelector(
  [ getAllCollections, getSearchedCollections, getSortOrder ],
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
            if (one.name < two.name)
              return -1;
            if (one.name > two.name)
              return 1;
            return 0;
          });
          break;
        // order by title/name reverse alphabetically
        case 'ZA':
          sortedCollectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.name > two.name)
              return -1;
            if (one.name < two.name)
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
