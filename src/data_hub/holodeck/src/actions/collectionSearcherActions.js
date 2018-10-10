import {
  SET_COLLECTION_SEARCH_QUERY,
} from '../constants/collectionSearcherActionTypes';

export const setCollectionSearchQuery = (collectionSearchQuery) => {
  return (dispatch) => {
    dispatch({
      type: SET_COLLECTION_SEARCH_QUERY,
      payload: { collectionSearchQuery }
    })
  }
};
