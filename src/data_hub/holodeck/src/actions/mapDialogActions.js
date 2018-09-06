import {
  OPEN_MAP_DIALOG,
  CLOSE_MAP_DIALOG
} from '../constants/mapDialogActionTypes';

export const openMapDialog = () => {
  return (dispatch) => {
    dispatch({
      type: OPEN_MAP_DIALOG
    })
  }
};

export const closeMapDialog = () => {
  return (dispatch) => {
    dispatch({
      type: CLOSE_MAP_DIALOG
    })
  }
};
