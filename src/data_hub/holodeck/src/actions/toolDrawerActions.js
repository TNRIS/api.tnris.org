
import {
  CLOSE_TOOL_DRAWER,
  OPEN_TOOL_DRAWER
} from '../constants/toolDrawerActionTypes';

export const closeToolDrawer = () => {
  return (dispatch) => {
    dispatch({
      type: CLOSE_TOOL_DRAWER
    })
  }
};

export const openToolDrawer = () => {
  return (dispatch) => {
    dispatch({
      type: OPEN_TOOL_DRAWER
    })
  }
};
