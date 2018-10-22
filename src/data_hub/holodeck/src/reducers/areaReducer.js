import {
  FETCH_AREAS_BEGIN,
  FETCH_AREAS_SUCCESS,
  FETCH_AREAS_FAILURE,
} from '../constants/areaActionTypes';

const initialState = {
  items: [],
  loading: false,
  error: null,
};

export default function areaReducer(state = initialState, action) {
  switch(action.type) {
    case FETCH_AREAS_BEGIN:
      // Mark the state as "loading" so we can show a spinner or something
      // Also, reset any errors. We're starting fresh.
      return {
        ...state,
        loading: true,
        error: null
      };

    case FETCH_AREAS_SUCCESS:
      // All done: set loading "false".
      // Also, replace the items with the ones from the server
      return {
        ...state,
        loading: false,
        items: action.payload.areas
      };

    case FETCH_AREAS_FAILURE:
      // The request failed, but it did stop, so set loading to "false".
      // Save the error, and we can display it somewhere
      // Since it failed, we don't have items to display anymore, so set it empty.
      return {
        ...state,
        loading: false,
        error: action.payload.error,
        items: []
      };

    default:
      // ALWAYS have a default case in a reducer
      return state;
  }
}
