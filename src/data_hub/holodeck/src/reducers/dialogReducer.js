import {
  OPEN_DIALOG,
  CLOSE_DIALOG
} from '../constants/dialogActionTypes';

const initialState = {
  showDialog: false
}

export default function dialogReducer(state = initialState, action) {
  switch(action.type) {
    case OPEN_DIALOG:
      // Set dialog in the state to true so that we may open the dialog
      return {
        ...state,
        showDialog: true
      };

    case CLOSE_DIALOG:
      // Set dialog in the state to false so that we may close the dialog
      return {
        ...state,
        showDialog: false
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
