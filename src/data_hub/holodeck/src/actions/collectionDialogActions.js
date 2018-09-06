import {
  OPEN_COLLECTION_DIALOG,
  CLOSE_COLLECTION_DIALOG
} from '../constants/collectionDialogActionTypes';

export const openCollectionDialog = () => {
  return (dispatch) => {
    dispatch({
      type: OPEN_COLLECTION_DIALOG
    })
  }
};

export const closeCollectionDialog = () => {
  return (dispatch) => {
    dispatch({
      type: CLOSE_COLLECTION_DIALOG
    })
  }
};
