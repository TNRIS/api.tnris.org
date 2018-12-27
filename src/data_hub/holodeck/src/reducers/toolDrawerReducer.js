import {
  CLOSE_TOOL_DRAWER,
  OPEN_TOOL_DRAWER
} from '../constants/toolDrawerActionTypes';

const initialState = {
  toolDrawerStatus: 'open'
}

export default function collectionDialogReducer(state = initialState, action) {
  switch(action.type) {
    case CLOSE_TOOL_DRAWER:
      // Set toolDrawerStatus in the state to closed so that we may close the drawer
      return {
        ...state,
        toolDrawerStatus: 'closed'
      };

    case OPEN_TOOL_DRAWER:
      // Set toolDrawerStaus in the state to open so that we may open the drawer
      return {
        ...state,
        toolDrawerStatus: 'open'
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
