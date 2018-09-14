import { createSelector } from 'reselect';

const getCollections = (state) => state.collections.items;
const sortOrder = (state) => state.sorter.sortOrder;
const getfilters = (state) => state.collectionFilter.collectionFilter;

export const getAllCollections = createSelector(
  [ getCollections ],
  (collections) => {
    // Check if collections are in the state
    if (collections.result) {
      // return just the collection details object; key'd by collection_id
      return collections.entities.collectionsById;
    }
  }
)

// /////////////////////////////////////////////////////////////
// Below are the selectors that pertain to the collectionFilter
// and the cards that are visible in the catalog at a given time
// /////////////////////////////////////////////////////////////

// Grabs the array of collections to show in the catalog view.
// If a filter is set, returns only those collections that pass
// through the filter.
export const getVisibleCollections = createSelector(
  [ getCollections, getfilters ],
  (collections, filters) => {
    let filteredCollections = [];
    // Check if collections are in the state
    if (collections.result) {
      collections.result.map(collectionId => {
        for (let key in filters) {
          if (filters.hasOwnProperty(key)) {
            let collectionPropertyValues = collections.entities.collectionsById[collectionId][key].split(',');
            collectionPropertyValues.map(propertyValue => {
              if (propertyValue === filters[key]) {
                if(filteredCollections.indexOf(collectionId) < 0) {
                  filteredCollections.push(collectionId);
                }
              }
              return propertyValue;
            })
          }
        }
        return collectionId;
      })
    }
    return !Array.isArray(filteredCollections) || !filteredCollections.length ?
      collections.result : filteredCollections;
  }
)

// Sets up the choices available to the CollectionFilter component fom the
// available properties in the collections object.
export const getCollectionFilterChoices = createSelector(
  [ getCollections ],
  (collections) => {
    // Here we set which properties will be available to the filter.
    // The key must match a property of the collections object and
    // the value is an empty array.
    const collectionFilterChoices = {
      category: [],
      recommended_use: [],
    };
    // If collections are in the state, continue setting the value arrays in the
    // collectionFilterChoices object from above.
    if (collections.result) {
      collections.result.map(collectionId => {
        for (let key in collectionFilterChoices) {
          if (collectionFilterChoices.hasOwnProperty(key)) {
            let collectionPropertyValues = collections.entities.collectionsById[collectionId][key].split(',');
            collectionPropertyValues.map(propertyValue => {
              if (collectionFilterChoices[key].indexOf(propertyValue) < 0) {
                collectionFilterChoices[key].push(propertyValue);
              }
              return propertyValue;
            })
          }
        }
        return collectionId;
      })
    }
    return collectionFilterChoices;
  }
)


// takes the filtered array of collection ids and reorders them based on the
// sort order delcared in the store by the Sort component
export const sortCollections = createSelector(
  [ getAllCollections, sortOrder, getVisibleCollections ],
  (collections, order, visibleCollections) => {
    // if the collections are in the store
    if (collections) {
      let collectionIds = visibleCollections;
      // do the order based on the declared field
      switch(order) {
        // order by title/name alphabetically
        case 'AZ':
          collectionIds.sort((a,b) => {
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
          collectionIds.sort((a,b) => {
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
          collectionIds.sort((a,b) => {
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
          collectionIds.sort((a,b) => {
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
          collectionIds.sort((a,b) => {
            const one = collections[a]
            const two = collections[b]
            if (one.name < two.name)
              return -1;
            if (one.name > two.name)
              return 1;
            return 0;
          });
      }
      return collectionIds;
    }
  }
)
