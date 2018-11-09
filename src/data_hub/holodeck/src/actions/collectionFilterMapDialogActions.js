import {
  OPEN_COLLECTION_FILTER_MAP_DIALOG,
  CLOSE_COLLECTION_FILTER_MAP_DIALOG
} from '../constants/collectionFilterMapDialogActionTypes';

export const openCollectionFilterMapDialog = () => {
  return (dispatch) => {
    dispatch({
      type: OPEN_COLLECTION_FILTER_MAP_DIALOG
    })
  }
};

export const closeCollectionFilterMapDialog = () => {
  return (dispatch) => {
    dispatch({
      type: CLOSE_COLLECTION_FILTER_MAP_DIALOG
    })
  }
};
