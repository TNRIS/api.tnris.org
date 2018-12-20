import {
  SET_SORT_AZ,
  SET_SORT_ZA,
  SET_SORT_NEW,
  SET_SORT_OLD,
} from '../constants/sortActionTypes';

const initialState = {
  sortOrder: 'NEW'
};

export default function sortReducer(state = initialState, action) {
  switch(action.type) {
    case SET_SORT_NEW:
      // sort collections by newest acquisition_date
      return {
        sortOrder: 'NEW'
      };

    case SET_SORT_OLD:
      // sort collections by oldest acquisition_date
      return {
        sortOrder: 'OLD'
      };

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
