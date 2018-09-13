import { createSelector } from 'reselect';

const getCollections = (state) => state.collections.items;
const sortOrder = (state) => state.sorter.sortOrder;
const getfilters = (state) => state.collectionFilter.collectionFilter;

export const getAllCollections = createSelector(
  [ getCollections ],
  (collections) => {
    // Check if collections are in the state
    if (collections.result) {
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
    console.log(collections);
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

export const sortCollections = createSelector(
  [ getVisibleCollections, sortOrder ],
  (collections, order) => {
    let collectionIds = collections !== {} ? Object.keys(collections) : [];
    if (collectionIds !== []) {
      switch(order) {
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
    }

    return collectionIds;
  }
)
