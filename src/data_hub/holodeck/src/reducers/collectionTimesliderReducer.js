import {
  SET_COLLECTION_TIMESLIDER,
  // SET_COLLECTION_TIMESLIDER_RANGE
} from '../constants/collectionTimesliderActionTypes';

const initialState = {
  collectionTimeslider: [1800, 2100],
  // collectionTimesliderRange: [1800, 2100]
};

export default function collectionTimesliderReducer(state = initialState, action) {
  switch(action.type) {
    case SET_COLLECTION_TIMESLIDER:
      // Set the collection user chosen timeslider values in the state
      return {
        ...state,
        collectionTimeslider: action.payload.collectionTimeslider
      };

    // case SET_COLLECTION_TIMESLIDER_RANGE:
    //   // Set the collection timeslider range in the state
    //   return {
    //     ...state,
    //     collectionTimesliderRange: action.payload.collectionTimesliderRange
    //   };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
