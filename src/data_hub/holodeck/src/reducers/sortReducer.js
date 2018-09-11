import {
  SET_SORT_AZ,
  SET_SORT_ZA,
} from '../constants/sortActionTypes';

const initialState = {
  sortOrder: 'AZ'
};

export default function sortReducer(state = initialState, action) {
  switch(action.type) {
    case SET_SORT_AZ:
      // sort collections by title A to Z
      return {
        sortOrder: 'AZ'
      };

    case SET_SORT_ZA:
      // sort collections by title Z to A
      return {
        sortOrder: 'ZA'
      };

    default:
      // ALWAYS have a default case in a reducer
      return state;
  }
}
