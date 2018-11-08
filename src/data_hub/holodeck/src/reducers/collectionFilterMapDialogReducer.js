import {
  OPEN_COLLECTION_FILTER_MAP_DIALOG,
  CLOSE_COLLECTION_FILTER_MAP_DIALOG
} from '../constants/collectionFilterMapDialogActionTypes';

const initialState = {
  showCollectionFilterMapDialog: false
}

export default function collectionFilterMapDialogReducer(state = initialState, action) {
  switch(action.type) {
    case OPEN_COLLECTION_FILTER_MAP_DIALOG:
      // Set showCollectionFilterMapDialog in the state to true so that we may open the dialog
      return {
        ...state,
        showCollectionFilterMapDialog: true
      };

    case CLOSE_COLLECTION_FILTER_MAP_DIALOG:
      // Set showCollectionFilterMapDialog in the state to false so that we may close the dialog
      return {
        ...state,
        showCollectionFilterMapDialog: false
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
