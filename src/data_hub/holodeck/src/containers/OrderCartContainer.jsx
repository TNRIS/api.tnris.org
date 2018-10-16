import { connect } from 'react-redux';

import OrderCart from '../components/OrderCart';

import { orderCartActions } from '../actions';

const mapStateToProps = state => ({
  orders: state.orderCart.orders,
  submitting: state.orderCart.submitting,
  submitError: state.orderCart.submitError
});

const mapDispatchToProps = dispatch => ({
  removeCollectionFromCart: (collectionId) => {
    dispatch(orderCartActions.removeCollectionFromCart(collectionId));
  },
  submitOrderSuccess: () => {
    dispatch(orderCartActions.submitOrderSuccess());
  }
})

const OrderCartContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(OrderCart);

export default OrderCartContainer;
