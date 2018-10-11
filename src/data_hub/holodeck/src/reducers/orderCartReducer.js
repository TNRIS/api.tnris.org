import {
  OPEN_ORDER_CART_DIALOG,
  CLOSE_ORDER_CART_DIALOG
} from '../constants/orderCartDialogActionTypes';

// import {
//
// } from '../constants/orderCartActionTypes';

const initialState = {
  showOrderCartDialog: false,
  orders: {}
};

export default function contactReducer(state = initialState, action) {
  switch(action.type) {
    case OPEN_ORDER_CART_DIALOG:
      // Set showOrderCartDialog in the state to true so that we may open the dialog
      return {
        ...state,
        showOrderCartDialog: true
      };

    case CLOSE_ORDER_CART_DIALOG:
      // Set showOrderCartDialog in the state to false so that we may close the dialog
      return {
        ...state,
        showOrderCartDialog: false
      };

      default:
        // ALWAYS have a default case in a reducer
        return state;
  }
}
