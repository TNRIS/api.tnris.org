import {
  ADD_COLLECTION_TO_CART,
  REMOVE_COLLECTION_FROM_CART
} from '../constants/orderCartActionTypes';

export const addCollectionToCart = (collectionId, formInfo) => {
  return (dispatch) => {
    dispatch({
      type: ADD_COLLECTION_TO_CART,
      payload: { collectionId, formInfo }
    })
  }
};

export const removeCollectionFromCart = (collectionId) => {
  return (dispatch) => {
    dispatch({
      type: REMOVE_COLLECTION_FROM_CART,
      payload: { collectionId }
    })
  }
};
