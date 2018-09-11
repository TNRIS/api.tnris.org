
import {
  SET_SORT_AZ,
  SET_SORT_ZA,
} from '../constants/sortActionTypes';

export const setSortAZ = () => {
  return (dispatch) => {
    dispatch({
      type: SET_SORT_AZ
    })
  }
};

export const setSortZA = () => {
  return (dispatch) => {
    dispatch({
      type: SET_SORT_ZA
    })
  }
};
