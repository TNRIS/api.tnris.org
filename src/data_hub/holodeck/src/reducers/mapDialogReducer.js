import {
  OPEN_MAP_DIALOG,
  CLOSE_MAP_DIALOG
} from '../constants/mapDialogActionTypes';

const initialState = {
  showMapDialog: false
}

export default function mapDialogReducer(state = initialState, action) {
  switch(action.type) {
    case OPEN_MAP_DIALOG:
      // Set showCollectionDialog in the state to true so that we may open the dialog
      return {
        ...state,
        showMapDialog: true
      };

    case CLOSE_MAP_DIALOG:
      // Set showMapDialog in the state to false so that we may close the dialog
      return {
        ...state,
        showMapDialog: false
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
