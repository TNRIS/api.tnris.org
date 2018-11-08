import {
  SET_URL
} from '../constants/urlTrackerActionTypes';

const initialState = {
  previousUrl: window.location.pathname
}

export default function urlTrackerReducer(state = initialState, action) {
  switch(action.type) {
    case SET_URL:
      // Set previous url in the state
      return {
        ...state,
        previousUrl: action.payload.previousUrl
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
