import { createSelector } from 'reselect';

const getCollections = (state) => state.collections.items;

export const getVisibleCollections = createSelector(
  [ getCollections ],
  (collections) => {
    return collections;
  }
)
