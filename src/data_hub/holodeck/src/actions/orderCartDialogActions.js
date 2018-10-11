import {
  OPEN_ORDER_CART_DIALOG,
  CLOSE_ORDER_CART_DIALOG
} from '../constants/orderCartDialogActionTypes';

export const openOrderCartDialog = () => {
  return (dispatch) => {
    dispatch({
      type: OPEN_ORDER_CART_DIALOG
    })
  }
};

export const closeOrderCartDialog = () => {
  return (dispatch) => {
    dispatch({
      type: CLOSE_ORDER_CART_DIALOG
    })
  }
};
