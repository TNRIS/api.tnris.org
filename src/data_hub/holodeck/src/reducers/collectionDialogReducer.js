import {
  OPEN_COLLECTION_DIALOG,
  CLOSE_COLLECTION_DIALOG
} from '../constants/collectionDialogActionTypes';

const initialState = {
  showCollectionDialog: false
}

export default function collectionDialogReducer(state = initialState, action) {
  switch(action.type) {
    case OPEN_COLLECTION_DIALOG:
      // Set showCollectionDialog in the state to true so that we may open the dialog
      return {
        ...state,
        showCollectionDialog: true
      };

    case CLOSE_COLLECTION_DIALOG:
      // Set showCollectionDialog in the state to false so that we may close the dialog
      return {
        ...state,
        showCollectionDialog: false
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
