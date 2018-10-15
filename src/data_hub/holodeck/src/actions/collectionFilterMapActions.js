import {
  SET_COLLECTION_FILTER_MAP_FILTER,
} from '../constants/collectionFilterMapActionTypes';

export const setCollectionFilterMapFilter = (collectionFilterMapFilter) => {
  return (dispatch) => {
    dispatch({
      type: SET_COLLECTION_FILTER_MAP_FILTER,
      payload: { collectionFilterMapFilter }
    })
  }
};
