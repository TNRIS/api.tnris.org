import {
  SET_COLLECTION_FILTER_MAP_FILTER
} from '../constants/collectionFilterMapActionTypes';

const initialState = {
  collectionFilterMapFilter: {}
};

export default function collectionFilterMapReducer(state = initialState, action) {
  switch(action.type) {
    case SET_COLLECTION_FILTER_MAP_FILTER:
      // Set the collection filter map filter in the state
      return {
        ...state,
        collectionFilterMapFilter: action.payload.collectionFilterMapFilter
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
