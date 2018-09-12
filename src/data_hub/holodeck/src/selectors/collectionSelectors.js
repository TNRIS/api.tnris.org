import { createSelector } from 'reselect';

const getCollections = (state) => state.collections.items;
const sortOrder = (state) => state.sorter.sortOrder;

export const getVisibleCollections = createSelector(
  [ getCollections ],
  (collections) => {
    const allCollections = collections.entities !== undefined ? collections.entities.collectionsById : {};
    return allCollections;
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
