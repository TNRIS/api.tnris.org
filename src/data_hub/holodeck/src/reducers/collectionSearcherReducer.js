import {
  SET_COLLECTION_SEARCH_QUERY
} from '../constants/collectionSearcherActionTypes';

const initialState = {
  collectionSearchQuery: ''
};

export default function collectionSearcherReducer(state = initialState, action) {
  switch(action.type) {
    case SET_COLLECTION_SEARCH_QUERY:
      // Set the collection search query in the state
      return {
        ...state,
        collectionSearchQuery: action.payload.collectionSearchQuery
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
