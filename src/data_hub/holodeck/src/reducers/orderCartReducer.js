import {
  OPEN_ORDER_CART_DIALOG,
  CLOSE_ORDER_CART_DIALOG
} from '../constants/orderCartDialogActionTypes';

import {
  ADD_COLLECTION_TO_CART,
  REMOVE_COLLECTION_FROM_CART
} from '../constants/orderCartActionTypes';

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

    case ADD_COLLECTION_TO_CART:
      const formObj = {};
      formObj[action.payload.collectionId] = action.payload.formInfo;
      const newOrders = {...state.orders, ...formObj};
      return {
        ...state,
        orders: newOrders
      };

    case REMOVE_COLLECTION_FROM_CART:
      const { [action.payload.collectionId]:value , ...removedOrders } = state.orders;
      console.log(removedOrders);
      return {
        ...state,
        orders: removedOrders
      };

    default:
      // ALWAYS have a default case in a reducer
      return state;
  }
}
